# Divine Node

**Engine name:** Parakleon

An Android project transformed into a full AI pipeline: training, evaluation, and serving via FastAPI, with CI/CD in GitHub Actions.
Automated builds and tests are enabled via GitHub Actions for every commit and pull request.

## Features

- **Machine Learning Pipeline**: Complete CIFAR10 image classification with PyTorch
- **LLM Integration**: OpenAI API integration for text generation, summarization, and code completion  
- **REST API**: FastAPI server with multiple endpoints
- **Android App**: Companion mobile application
- **CI/CD**: Automated builds and testing

## Quick Start

### 1. Install Dependencies
```bash
./scripts/build.sh
```

### 2. Start the API Server
```bash
cd src
uvicorn serve:app --host 0.0.0.0 --port 8000
```

The API will be available at http://localhost:8000

### 3. API Documentation
Visit http://localhost:8000/docs for interactive API documentation.

## API Endpoints

- **GET /**: Root endpoint with status
- **GET /health**: Health check with component status
- **POST /predict**: Image classification (upload image file)
- **POST /generate**: Text generation using LLM
- **POST /summarize**: Text summarization using LLM  
- **POST /code-complete**: Code completion using LLM

## Machine Learning Pipeline

### Training
```bash
cd src
python train.py --epochs 10 --batch_size 64
```

### Evaluation
```bash
cd src
python evaluate.py --checkpoint_path ../checkpoints/best.pth
```

### Serving
The trained model is automatically loaded by the API server for predictions.

## LLM Features

To enable LLM features, set your OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

## Development

### Project Structure
```
src/
├── train.py        # ML model training
├── evaluate.py     # Model evaluation
├── serve.py        # FastAPI server
├── model.py        # Model architecture and LLM utilities
├── data.py         # Data loading utilities
└── db.py           # Database layer

app/                # Android application
scripts/
└── build.sh        # Build automation script
```

### Building Android App
```bash
./scripts/build.sh --android
```

## Architecture

- **ML Model**: CNN for CIFAR10 classification (10 classes)
- **API Framework**: FastAPI with async support
- **Database**: SQLite with SQLAlchemy
- **LLM Provider**: OpenAI GPT-4
- **Mobile**: Android with Kotlin/Java
- **CI/CD**: GitHub Actions
