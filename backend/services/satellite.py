
import numpy as np
from datetime import datetime
def fetch_sentinel2(polygon):
    return {"red": np.random.rand(100,100)*0.3+0.05, "nir": np.random.rand(100,100)*0.4+0.3, "swir": np.random.rand(100,100)*0.2+0.1, "cloud_pct": 12.3, "date": datetime.utcnow().isoformat()}
def compute_indices(img):
    red, nir, swir = img["red"], img["nir"], img["swir"]
    ndvi = (nir - red)/(nir + red + 1e-6)
    ndmi = (nir - swir)/(nir + swir + 1e-6)
    stress_mask = ndvi < 0.3
    return {"ndvi_mean": float(np.mean(ndvi)), "ndmi_mean": float(np.mean(ndmi)), "stress_pct": float(np.mean(stress_mask)*100), "cloud_pct": img["cloud_pct"]}
