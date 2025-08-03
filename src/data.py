from torchvision import datasets, transforms
from torch.utils.data import DataLoader

def get_dataloader(batch_size: int, data_dir: str = '../data', train: bool = True):
    transform = transforms.Compose([
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
    ])
    dataset = datasets.CIFAR10(root=data_dir, train=train, download=True, transform=transform)
    return DataLoader(dataset, batch_size=batch_size, shuffle=train, num_workers=4)
