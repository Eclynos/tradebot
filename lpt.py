import torch

matrice1 = torch.tensor([[1, 2, 3, 4]])
matrice2 = torch.tensor([[5, 6, 7, 8]])

resultat = torch.mul(matrice1, matrice2)

print(resultat)