from multiprocessing import freeze_support
import torch
import torch.utils.data
from torchvision.utils import save_image

import os
from tqdm import tqdm

# cuda setup
if torch.cuda.is_available():
    device = torch.device("cuda")
else: device = torch.device("cpu")

kwargs = {'num_workers': 1, 'pin_memory': True} 

# hyper params
batch_size = 4
latent_size = 20
epochs = 50

if os.path.exists('/home/yiyu/'):
    path = '/home/yiyu/JustLM2D/'
else: path = '/Users/Marvin/NII_Code/JustLM2D/'

from CVAE import *

def train(epoch, model, train_loader, optimizer):
    model.train()
    train_loss = 0
    for batch_idx, item in enumerate(train_loader):
        lyrics, music, dance = item['lyrics'].to(device), item['music'].to(device), item['dance'].to(device)
        # labels = torch.concat(one_hot(music, 10), one_hot(lyrics, 10))
        labels = torch.concat((torch.flatten(music),torch.flatten(lyrics)),dim=0)
        dance = torch.flatten(dance)
        print(dance.shape)
        recon_batch, mu, logvar = model(dance, labels)
        optimizer.zero_grad()
        loss = loss_function(recon_batch, dance, mu, logvar)
        loss.backward()
        train_loss += loss.detach().cpu().numpy()
        optimizer.step()
        # if batch_idx % 20 == 0:
        #     print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
        #         epoch, batch_idx * len(data), len(train_loader.dataset),
        #         100. * batch_idx / len(train_loader),
        #         loss.item() / len(data)))

    # print('====> Epoch: {} Average loss: {:.4f}'.format(
        #   epoch, train_loss / len(train_loader.dataset)))


def test(epoch, model, test_loader):
    model.eval()
    test_loss = 0
    with torch.no_grad():
        for i, (data, labels) in enumerate(test_loader):
            data, labels = data.to(device), labels.to(device)
            labels = one_hot(labels, 10)
            recon_batch, mu, logvar = model(data, labels)
            test_loss += loss_function(recon_batch, data, mu, logvar).detach().cpu().numpy()
            if i == 0:
                n = min(data.size(0), 5)
                comparison = torch.cat([data[:n],
                                      recon_batch.view(-1, 1, 500, 72)[:n]])
                save_image(comparison.cpu(),
                         'reconstruction_' + str(epoch) + '.png', nrow=n)

    test_loss /= len(test_loader.dataset)
    # print('====> Test set loss: {:.4f}'.format(test_loss))

if __name__ == '__main__':
    # MuLy2Dance
    from LMD_Dataset import *
    dataset = torch.load(path+'Pipeline/LMD.pth')

    train_loader = DataLoader(dataset=dataset, batch_size=4, shuffle=True, num_workers=1)

    # create a CVAE model
    # feature_size, latent_size, class_size
    model = CVAE(500*72, latent_size, 409600).to(device)

    optimizer = optim.Adam(model.parameters(), lr=1e-3)

    model.train()
    freeze_support()

    for epoch in tqdm(range(1, epochs + 1)):
        print(epoch)
        train(epoch, model, train_loader, optimizer)
        # test(epoch, model, test_loader)
        with torch.no_grad():
            c = torch.eye(10, 10).to(device)
            sample = torch.randn(10, 20).to(device)
            sample = model.decode(sample, c).cpu()
            save_image(sample.view(10, 1, 500, 72),
                        'sample_' + str(epoch) + '.png')