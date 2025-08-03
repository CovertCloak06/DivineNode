import argparse, torch
from sklearn.metrics import confusion_matrix
from data import get_dataloader
from model import get_model

def evaluate(args):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = get_model(args.num_classes).to(device)
    model.load_state_dict(torch.load(args.checkpoint_path, map_location=device))
    model.eval()

    loader = get_dataloader(args.batch_size, train=False)
    all_preds, all_labels = [], []
    with torch.no_grad():
        for x, y in loader:
            x, y = x.to(device), y.to(device)
            out = model(x)
            preds = out.argmax(1)
            all_preds.extend(preds.cpu().tolist())
            all_labels.extend(y.cpu().tolist())

    acc = sum(p==l for p, l in zip(all_preds, all_labels)) / len(all_labels)
    cm  = confusion_matrix(all_labels, all_preds)
    print(f"Accuracy: {acc:.4f}\nConfusion Matrix:\n{cm}")

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--batch_size', type=int, default=64)
    p.add_argument('--num_classes', type=int, default=10)
    p.add_argument('--checkpoint_path', type=str, default='../checkpoints/best.pth')
    args = p.parse_args()
    evaluate(args)
