# DivineNode Usage Examples

This guide shows practical examples of using the DivineNode (Parakleon Engine) API and ML pipeline.

## Quick Setup

```bash
# 1. Build the project
./scripts/build.sh

# 2. Start the API server
cd src
uvicorn serve:app --host 0.0.0.0 --port 8000
```

The API will be available at http://localhost:8000

## API Usage Examples

### 1. Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "ml_model_loaded": true,
  "llm_available": false
}
```

### 2. Image Classification

```bash
# Upload an image for classification
curl -X POST "http://localhost:8000/predict" -F "file=@your_image.png"
```

Response:
```json
{
  "prediction": 6,
  "confidence": 0.91594
}
```

Classes: 0=airplane, 1=automobile, 2=bird, 3=cat, 4=deer, 5=dog, 6=frog, 7=horse, 8=ship, 9=truck

### 3. Text Generation (requires OPENAI_API_KEY)

```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Write a Python function to calculate fibonacci numbers"}'
```

### 4. Text Summarization (requires OPENAI_API_KEY)

```bash
curl -X POST "http://localhost:8000/summarize" \
  -H "Content-Type: application/json" \
  -d '{"text": "Your long text to summarize..."}'
```

### 5. Code Completion (requires OPENAI_API_KEY)

```bash
curl -X POST "http://localhost:8000/code-complete" \
  -H "Content-Type: application/json" \
  -d '{"code": "def calculate_area(radius):"}'
```

## ML Pipeline Usage

### Training a Model

```bash
cd src
python train.py --epochs 10 --batch_size 64 --lr 0.001
```

Options:
- `--epochs`: Number of training epochs (default: 10)
- `--batch_size`: Batch size for training (default: 64)
- `--lr`: Learning rate (default: 1e-3)
- `--weight_decay`: Weight decay for regularization (default: 1e-4)
- `--num_classes`: Number of classes (default: 10)
- `--checkpoint_dir`: Directory to save checkpoints (default: ../checkpoints)
- `--log_dir`: Directory for TensorBoard logs (default: ../logs)

### Evaluating a Model

```bash
cd src
python evaluate.py --checkpoint_path ../checkpoints/best.pth
```

### Monitoring Training

```bash
# View TensorBoard logs
tensorboard --logdir logs/
```

## Python API Usage

### Direct ML Model Usage

```python
import torch
from model import get_model
from data import get_dataloader

# Load model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = get_model(num_classes=10).to(device)
model.load_state_dict(torch.load("checkpoints/best.pth", map_location=device))
model.eval()

# Make prediction
dataloader = get_dataloader(batch_size=1, train=False)
x, y = next(iter(dataloader))
x = x.to(device)

with torch.no_grad():
    output = model(x)
    prediction = output.argmax(1).item()
    print(f"Predicted class: {prediction}")
```

### LLM Utilities Usage

```python
import os
from model import LLMUtils

# Initialize with API key
os.environ["OPENAI_API_KEY"] = "your-api-key"
llm = LLMUtils()

# Generate text
response = llm.generate("Write a haiku about AI")
print(response)

# Summarize text
summary = llm.summarize("Your long text here...")
print(summary)

# Complete code
completion = llm.code_complete("def factorial(n):")
print(completion)
```

## Testing

Run the integration test suite:

```bash
python test_integration.py
```

This tests:
- Build script functionality
- ML pipeline (training/evaluation)  
- All API endpoints
- Error handling

## Production Deployment

### Using Docker

```bash
# Build Docker image
docker build -t divinenode .

# Run container
docker run -p 8000:8000 -e OPENAI_API_KEY=your-key divinenode
```

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key for LLM features

## Android App

The Android app is located in the `app/` directory. Build with:

```bash
./scripts/build.sh --android
```

## Troubleshooting

### Common Issues

1. **ImportError**: Run `./scripts/build.sh` to install all dependencies
2. **Model not found**: Train a model first with `python train.py`
3. **API timeout**: Increase timeout or check if model is loading properly
4. **LLM errors**: Set `OPENAI_API_KEY` environment variable

### Logs

Check logs for debugging:
- Training logs: `logs/` directory
- API logs: stdout when running uvicorn
- Build logs: output from `./scripts/build.sh`