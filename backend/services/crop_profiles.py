
"""
GDD and trigger profiles for 6 crops - Willard/Brigham microclimate tuned
"""
CROP_PROFILES = {
    "alfalfa": {"base_temp": 5, "gdd_maturity": 800, "drought_spi": -1.5, "heat_temp": 38, "ndvi_healthy": 0.7},
    "wheat": {"base_temp": 0, "gdd_maturity": 1800, "drought_spi": -1.2, "heat_temp": 35, "ndvi_healthy": 0.75, "critical_window": "heading"},
    "barley": {"base_temp": 0, "gdd_maturity": 1600, "drought_spi": -1.3, "heat_temp": 34, "ndvi_healthy": 0.72},
    "cherries": {"base_temp": 4, "gdd_maturity": 1100, "drought_spi": -1.0, "heat_temp": 32, "ndvi_healthy": 0.65, "frost_trigger": -2},
    "apples": {"base_temp": 4, "gdd_maturity": 1400, "drought_spi": -1.1, "heat_temp": 35, "ndvi_healthy": 0.68},
    "safflower": {"base_temp": 8, "gdd_maturity": 1500, "drought_spi": -1.6, "heat_temp": 40, "ndvi_healthy": 0.6}, # drought tolerant, good for UT
}

def get_trigger_for_crop(crop_type: str, weather: dict, ndvi: float):
    profile = CROP_PROFILES.get(crop_type, CROP_PROFILES["alfalfa"])
    payout = 0
    if weather["spi_proxy"] < profile["drought_spi"]: payout = max(payout, 50)
    if weather.get("tmax_last",0) > profile["heat_temp"]: payout = max(payout, 60)
    if crop_type=="cherries" and weather.get("tmin_last",10) < profile.get("frost_trigger",-2): payout = max(payout, 70)
    if ndvi < profile["ndvi_healthy"]*0.6: payout = max(payout, 40)
    return payout
