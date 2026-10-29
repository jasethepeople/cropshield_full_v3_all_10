
def predict_yield(indices, weather, crop_type="alfalfa"):
    base = {"alfalfa": 6.0, "wheat": 55, "barley": 70}.get(crop_type, 50)
    ndvi_factor = max(0.2, indices["ndvi_mean"]/0.7)
    water_factor = max(0.3, 1 + weather["spi_proxy"]*0.15)
    return round(base * ndvi_factor * water_factor, 2)
