from fastapi import FastAPI, File, UploadFile
import io
from PIL import Image
import torch
from model import get_model
import torchvision.transforms as transforms

app = FastAPI()


# on startup:
@app.on_event("startup")
async def init_db():
    Session()


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = get_model(num_classes=10).to(device)
model.load_state_dict(torch.load("checkpoints/best.pth", map_location=device))
model.eval()

transform = transforms.Compose(
    [
        transforms.Resize((32, 32)),
        transforms.ToTensor(),
    ]
)


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    img = Image.open(io.BytesIO(await file.read())).convert("RGB")
    x = transform(img).unsqueeze(0).to(device)
    with torch.no_grad():
        out = model(x)
        pred = out.argmax(1).item()
    return {"prediction": pred}
