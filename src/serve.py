from db import Session
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import io
from PIL import Image
import torch
from model import get_model, LLMUtils
import torchvision.transforms as transforms

app = FastAPI(title="DivineNode API", description="AI pipeline with ML and LLM capabilities")

# Initialize LLM utilities
llm_utils = LLMUtils()

# Request/Response models
class GenerateRequest(BaseModel):
    prompt: str
    model: str = "gpt-4"

class TextRequest(BaseModel):
    text: str
    model: str = "gpt-4"

class CodeRequest(BaseModel):
    code: str
    model: str = "gpt-4"


# on startup:
@app.on_event("startup")
async def init_db():
    Session()


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load ML model if checkpoint exists
model = None
checkpoint_path = "../checkpoints/best.pth"
try:
    model = get_model(num_classes=10).to(device)
    model.load_state_dict(torch.load(checkpoint_path, map_location=device))
    model.eval()
    print("ML model loaded successfully")
except Exception as e:
    print(f"Warning: Could not load ML model from {checkpoint_path}: {e}")

transform = transforms.Compose(
    [
        transforms.Resize((32, 32)),
        transforms.ToTensor(),
    ]
)


@app.get("/")
async def root():
    return {"message": "DivineNode API - Parakleon Engine", "status": "running"}


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "ml_model_loaded": model is not None,
        "llm_available": llm_utils.client is not None
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """Predict image class using the trained ML model"""
    if model is None:
        raise HTTPException(status_code=503, detail="ML model not available")
    
    img = Image.open(io.BytesIO(await file.read())).convert("RGB")
    x = transform(img).unsqueeze(0).to(device)
    with torch.no_grad():
        out = model(x)
        pred = out.argmax(1).item()
        confidence = torch.softmax(out, dim=1).max().item()
    return {"prediction": pred, "confidence": confidence}


@app.post("/generate")
async def generate_text(request: GenerateRequest):
    """Generate text using LLM"""
    response = llm_utils.generate(request.prompt, request.model)
    return {"response": response}


@app.post("/summarize")  
async def summarize_text(request: TextRequest):
    """Summarize text using LLM"""
    response = llm_utils.summarize(request.text, request.model)
    return {"summary": response}


@app.post("/code-complete")
async def code_complete(request: CodeRequest):
    """Complete code using LLM"""
    response = llm_utils.code_complete(request.code, request.model)
    return {"completion": response}
