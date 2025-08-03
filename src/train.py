import argparse
import os
import torch
from torch import nn, optim
from torch.utils.tensorboard import SummaryWriter
from data import get_dataloader
from model import get_model


def train(args):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    train_loader = get_dataloader(args.batch_size, train=True)
    val_loader = get_dataloader(args.batch_size, train=False)

    model = get_model(args.num_classes).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(
        model.parameters(), lr=args.lr, weight_decay=args.weight_decay
    )
    writer = SummaryWriter(log_dir=args.log_dir)

    best_acc = 0.0
    for epoch in range(1, args.epochs + 1):
        model.train()
        total_loss, correct = 0, 0
        for x, y in train_loader:
            x, y = x.to(device), y.to(device)
            optimizer.zero_grad()
            out = model(x)
            loss = criterion(out, y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item() * x.size(0)
            correct += (out.argmax(1) == y).sum().item()
        train_loss = total_loss / len(train_loader.dataset)
        train_acc = correct / len(train_loader.dataset)

        model.eval()
        val_loss, val_correct = 0, 0
        with torch.no_grad():
            for x, y in val_loader:
                x, y = x.to(device), y.to(device)
                out = model(x)
                val_loss += criterion(out, y).item() * x.size(0)
                val_correct += (out.argmax(1) == y).sum().item()
        val_loss /= len(val_loader.dataset)
        val_acc = val_correct / len(val_loader.dataset)

        writer.add_scalars("Loss", {"train": train_loss, "val": val_loss}, epoch)
        writer.add_scalars("Accuracy", {"train": train_acc, "val": val_acc}, epoch)
        print(
            f"Epoch {epoch}: train_loss={train_loss:.4f}, train_acc={train_acc:.4f} | val_loss={val_loss:.4f}, val_acc={val_acc:.4f}"
        )

        if val_acc > best_acc:
            best_acc = val_acc
            os.makedirs(args.checkpoint_dir, exist_ok=True)
            torch.save(
                model.state_dict(), os.path.join(args.checkpoint_dir, "best.pth")
            )

    writer.close()


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--batch_size", type=int, default=64)
    p.add_argument("--lr", type=float, default=1e-3)
    p.add_argument("--weight_decay", type=float, default=1e-4)
    p.add_argument("--epochs", type=int, default=10)
    p.add_argument("--num_classes", type=int, default=10)
    p.add_argument("--checkpoint_dir", type=str, default="../checkpoints")
    p.add_argument("--log_dir", type=str, default="../logs")
    args = p.parse_args()
    train(args)
