
"""
Train U-Net on PlantVillage + custom phone photos
Run: python train_unet.py --data ./data/labeled --epochs 20
"""
import torch, os, glob, cv2
import segmentation_models_pytorch as smp
from torch.utils.data import Dataset, DataLoader

class FarmDataset(Dataset):
    def __init__(self, img_dir, mask_dir):
        self.imgs = sorted(glob.glob(f"{img_dir}/*.jpg"))
        self.masks = sorted(glob.glob(f"{mask_dir}/*.png"))
    def __len__(self): return len(self.imgs)
    def __getitem__(self, i):
        img = cv2.imread(self.imgs[i]); img = cv2.resize(img,(256,256))/255.0
        mask = cv2.imread(self.masks[i],0); mask = cv2.resize(mask,(256,256))/255.0
        return torch.tensor(img).permute(2,0,1).float(), torch.tensor(mask).unsqueeze(0).float()

def train():
    ds = FarmDataset("data/images","data/masks")
    dl = DataLoader(ds,batch_size=8,shuffle=True)
    model = smp.Unet(encoder_name="resnet34", in_channels=3, classes=1)
    opt = torch.optim.Adam(model.parameters(), lr=1e-4)
    loss = smp.losses.DiceLoss(mode="binary")
    for epoch in range(20):
        for x,y in dl:
            opt.zero_grad()
            pred = model(x)
            l = loss(pred,y)
            l.backward(); opt.step()
        print(f"Epoch {epoch} loss {l.item():.4f}")
    torch.save(model.state_dict(),"models/unet_stress.pt")
    print("Saved to models/unet_stress.pt")

if __name__=="__main__":
    os.makedirs("models",exist_ok=True)
    train()
