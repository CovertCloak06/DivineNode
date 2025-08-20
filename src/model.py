import os
import torch
import torch.nn as nn
import torch.nn.functional as F
from openai import OpenAI


class CNNModel(nn.Module):
    """Simple CNN model for CIFAR10 classification"""
    def __init__(self, num_classes=10):
        super(CNNModel, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, 3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)
        self.conv3 = nn.Conv2d(64, 64, 3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(64 * 4 * 4, 512)
        self.fc2 = nn.Linear(512, num_classes)
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        x = x.view(-1, 64 * 4 * 4)
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x


def get_model(num_classes=10):
    """Get the CNN model for training/inference"""
    return CNNModel(num_classes=num_classes)


# LLM utilities (separated from model architecture)
class LLMUtils:
    def __init__(self, api_key=None):
        self.client = None
        if api_key or os.getenv("OPENAI_API_KEY"):
            try:
                self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
            except Exception as e:
                print(f"Warning: Could not initialize OpenAI client: {e}")

    def generate(self, prompt: str, model: str = "gpt-4"):
        """Generate text using OpenAI API"""
        if not self.client:
            return "Error: OpenAI client not initialized. Please set OPENAI_API_KEY environment variable."
        
        try:
            resp = self.client.chat.completions.create(
                model=model, messages=[{"role": "user", "content": prompt}]
            )
            return resp.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {e}"

    def summarize(self, text: str, model: str = "gpt-4"):
        """Summarize text using OpenAI API"""
        prompt = f"Please provide a concise summary of the following text:\n\n{text}"
        return self.generate(prompt, model)

    def code_complete(self, code: str, model: str = "gpt-4"):
        """Complete code using OpenAI API"""
        prompt = f"Please complete the following code:\n\n{code}"
        return self.generate(prompt, model)
