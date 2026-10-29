
import requests
def get_triggers(polygon):
    lon = sum(p[0] for p in polygon)/len(polygon)
    lat = sum(p[1] for p in polygon)/len(polygon)
    url = "https://api.open-meteo.com/v1/forecast"
    params = {"latitude": lat, "longitude": lon, "daily": "temperature_2m_max,precipitation_sum", "past_days": 31, "timezone": "auto"}
    r = requests.get(url, params=params).json()
    daily = r.get("daily", {})
    precip = daily.get("precipitation_sum", [])
    tmax = daily.get("temperature_2m_max", [])
    precip_sum_21 = sum(precip[-21:]) if len(precip)>=21 else sum(precip)
    spi_proxy = (precip_sum_21 - 60)/20
    heat_days = sum(1 for t in tmax[-7:] if t and t>38)
    return {"lat": lat, "lon": lon, "precip_21d_mm": precip_sum_21, "spi_proxy": spi_proxy, "heat_days_7d": heat_days, "drought_trigger_met": spi_proxy < -1.5, "heat_trigger_met": heat_days >= 3}
