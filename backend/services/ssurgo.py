
"""
USDA SSURGO soil integration via Soil Data Access (SDA) API
Free, no key
"""
import requests

def get_soil_for_point(lat: float, lon: float):
    # SDA WMS query - get mapunit
    # Simplified: query SDA REST
    url = "https://sdmdataaccess.sc.egov.usda.gov/Tabular/post.rest"
    query = f"""
    SELECT mu.mukey, mu.muname, comp.compname, comp.hydgrp, comp.drainagecl,
           horz.hzname, horz.awc_r, horz.ksat_r
    FROM mapunit AS mu
    JOIN component AS comp ON mu.mukey = comp.mukey
    JOIN chorizon AS horz ON comp.cokey = horz.cokey
    WHERE mu.mukey IN (
        SELECT * FROM SDA_Get_Mukey_from_intersection_with_WktWgs84('point({lon} {lat})')
    )
    """
    try:
        r = requests.post(url, json={"format":"JSON", "query": query}, timeout=10)
        data = r.json()
        # Parse first row
        if data and len(data.get("Table",[]))>1:
            row = data["Table"][1]
            return {"mukey": row[0], "soil_name": row[1], "hydrologic_group": row[3], "awc": row[6], "ksat": row[7], "water_holding_capacity": float(row[6] or 0.15)}
    except Exception as e:
        print(f"[SSURGO] Fallback for {lat},{lon}: {e}")
    # Fallback for Willard, UT - loam
    return {"soil_name": "Willard Loam", "hydrologic_group": "B", "awc": 0.18, "water_holding_capacity": 0.18, "drainage": "Well drained", "source": "fallback"}

def adjust_yield_for_soil(base_yield: float, soil: dict):
    factor = 0.9 + soil.get("awc",0.15)  # higher AWC = higher yield
    return base_yield * factor
