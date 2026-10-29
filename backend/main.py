
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import services.satellite as sat
import services.weather as wx
import services.ipfs as ipfs
import services.risk_engine as risk
import services.yield_model as ym
import services.ssurgo as soil
import services.crop_profiles as crops
import services.reinsurance as reins
import services.marketplace as market
import services.report as report_mod
import services.sms as sms_mod
import services.voice as voice_mod

app = FastAPI(title="CropShield API - FULL v3", version="3.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(voice_mod.router)

class FieldPolygon(BaseModel):
    farm_id: str
    polygon: List[List[float]]
    crop_type: str = "alfalfa"
    phone: str = ""
    email: str = ""

@app.get("/health")
def health(): return {"status":"ok","version":"3.0 FULL","modules":["satellite_prod","ssurgo","reinsurance","marketplace","sms","voice","disputeDAO","pwa"]}

@app.post("/field/analyze")
def analyze_field(field: FieldPolygon):
    img_data = sat.fetch_sentinel2(field.polygon)
    indices = sat.compute_indices(img_data)
    soil_data = soil.get_soil_for_point(field.polygon[0][1], field.polygon[0][0])
    cid = ipfs.pin_json({"farm_id": field.farm_id, "indices": indices, "soil": soil_data})
    weather = wx.get_triggers(field.polygon)
    payout = risk.evaluate_triggers(weather, indices)
    # Crop-specific override
    crop_payout = crops.get_trigger_for_crop(field.crop_type, weather, indices["ndvi_mean"])
    final_payout = max(payout["payout_pct"], crop_payout)
    yield_est = ym.predict_yield(indices, weather, field.crop_type)
    yield_est = soil.adjust_yield_for_soil(yield_est, soil_data)
    # Check regional reinsurance
    regional = reins.reinsurance.check_regional_trigger([{"farm_id": field.farm_id}] if final_payout>0 else [])
    return {
        "farm_id": field.farm_id, "ndvi": indices["ndvi_mean"], "soil": soil_data,
        "weather": weather, "payout_trigger": {"payout_pct": final_payout, "triggered": final_payout>0, "reasons": payout["reasons"]},
        "yield_estimate_bu_ac": yield_est, "ipfs_cid": cid, "regional_cover": regional
    }

@app.post("/field/report/{farm_id}")
def make_report(farm_id: str):
    data = {"ndvi":0.68,"ndmi":0.22,"stress_pct":18,"weather":{"spi_proxy":-0.8,"heat_days_7d":1},"payout_trigger":{"payout_pct":0,"reasons":[]},"yield_estimate_bu_ac":6.2,"ipfs_cid":"QmMock123"}
    path = f"/tmp/{farm_id}_weekly.pdf"
    report_mod.generate_weekly_pdf(farm_id, data, path)
    return {"pdf": path}

@app.get("/marketplace")
def get_market(): return market.marketplace.get_orderbook()

@app.post("/marketplace/list")
def list_risk(coop_id: str, risk_type: str, amount: float, premium: float):
    return market.marketplace.list_risk(coop_id, risk_type, amount, premium)
