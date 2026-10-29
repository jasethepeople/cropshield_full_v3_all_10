
"""
U-Net stress segmentation + Autoencoder anomaly
Requires: torch, segmentation-models-pytorch, rasterio
"""
import torch
import segmentation_models_pytorch as smp
import numpy as np

class StressUnet:
    def __init__(self):
        self.model = smp.Unet(encoder_name="resnet34", encoder_weights="imagenet", in_channels=4, classes=1)
        # Load fine-tuned weights if exists: self.model.load_state_dict(torch.load("models/unet_stress.pt"))
        self.model.eval()
    
    def predict(self, ndvi_stack): # [T,H,W] time series
        # Convert to tensor [1,4,H,W] - NDVI, NDMI, temporal mean, std
        x = torch.randn(1,4,256,256) # placeholder
        with torch.no_grad():
            mask = torch.sigmoid(self.model(x))
        return (mask.squeeze().numpy() > 0.5).astype(np.uint8) * 100

class PestAutoencoder(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.enc = torch.nn.Sequential(torch.nn.Linear(30,16), torch.nn.ReLU(), torch.nn.Linear(16,4))
        self.dec = torch.nn.Sequential(torch.nn.Linear(4,16), torch.nn.ReLU(), torch.nn.Linear(16,30))
    def forward(self,x): return self.dec(self.enc(x))
    
    def anomaly_score(self, ndvi_curve): # 30-day curve
        import torch.nn.functional as F
        x = torch.tensor(ndvi_curve, dtype=torch.float32).unsqueeze(0)
        recon = self.forward(x)
        return F.mse_loss(recon, x).item()
