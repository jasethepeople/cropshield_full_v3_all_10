
"""
PRODUCTION Sentinel-2 L2A fetcher - drop-in replacement for satellite.py
Uses Copernicus Data Space + sentinelhub
pip install sentinelhub
"""
from sentinelhub import SHConfig, SentinelHubRequest, DataCollection, MimeType, BBox, CRS, bbox_to_dimensions
import numpy as np
from datetime import datetime, timedelta

config = SHConfig()
config.sh_client_id = "YOUR_COPERNICUS_CLIENT_ID"
config.sh_client_secret = "YOUR_COPERNICUS_CLIENT_SECRET"

def fetch_sentinel2_prod(polygon, days_back=5):
    # polygon = [[lon,lat],...]
    lons = [p[0] for p in polygon]
    lats = [p[1] for p in polygon]
    bbox = BBox(bbox=[min(lons), min(lats), max(lons), max(lats)], crs=CRS.WGS84)
    size = bbox_to_dimensions(bbox, resolution=10) # 10m

    evalscript = """
    //VERSION=3
    function setup(){ return { input: ["B04","B08","B11","SCL","dataMask"], output: { bands: 5 } } }
    function evaluatePixel(s){ return [s.B04, s.B08, s.B11, s.SCL, s.dataMask] }
    """

    request = SentinelHubRequest(
        evalscript=evalscript,
        input_data=[SentinelHubRequest.input_data(data_collection=DataCollection.SENTINEL2_L2A, time_interval=(f"{(datetime.utcnow()-timedelta(days=days_back)).isoformat()}", f"{datetime.utcnow().isoformat()}"), maxcc=0.2)],
        responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
        bbox=bbox, size=size, config=config
    )
    data = request.get_data()[0] # shape HxWx5
    red, nir, swir, scl, mask = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3], data[:,:,4]
    cloud_mask = (scl==3) | (scl==8) | (scl==9) # cloud shadow, cloud medium/high
    red = np.where(cloud_mask, np.nan, red)
    nir = np.where(cloud_mask, np.nan, nir)
    return {"red": red, "nir": nir, "swir": swir, "cloud_pct": float(np.mean(cloud_mask)*100), "date": datetime.utcnow().isoformat(), "mask": mask}

# Same compute_indices as before but handles NaN
def compute_indices_prod(img):
    red, nir, swir = img["red"], img["nir"], img["swir"]
    ndvi = (nir - red)/(nir + red + 1e-6)
    ndmi = (nir - swir)/(nir + swir + 1e-6)
    valid = ~np.isnan(ndvi)
    stress = np.mean(ndvi[valid] < 0.3)*100 if np.any(valid) else 0
    return {"ndvi_mean": float(np.nanmean(ndvi)), "ndmi_mean": float(np.nanmean(ndmi)), "stress_pct": float(stress), "cloud_pct": img["cloud_pct"]}
