import cv2
import numpy as np
import matplotlib.pyplot as plt

# Cores de referência e seus valores RGB conhecidos
cores_referencia = {
    "proteina_2.0": (100, 76, 159),
    "proteina_2.5": (96, 67, 158),
    "proteina_3.0": (95, 62, 156),
    "proteina_3.5": (93, 60, 151),
    "proteina_4.0": (90, 56, 148)
}

# Caminho para as fotos no seu projeto
caminho_fotos = ["photo_1.jpg", "photo_2.jpg", "photo_3.jpg", "photo_4.jpg", "photo_5.jpg"]

# Listas para armazenar os valores RGB das fotos de referência
valores_referencia = []
for foto in caminho_fotos:
    img = cv2.imread(foto)
    # Convertendo a imagem para RGB (OpenCV carrega em BGR por padrão)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Pegando o valor médio de cor da imagem
    valor_medio = np.mean(img_rgb, axis=(0, 1))
    valores_referencia.append(valor_medio)

# Calculando os coeficientes da função de calibração
valores_referencia = np.array(valores_referencia)
cores_referencia = np.array(list(cores_referencia.values()))
a, b = np.linalg.lstsq(valores_referencia, cores_referencia, rcond=None)[0]

# Função de calibração
def calibrar_cor(R_original, G_original, B_original):
    R_calibrado = a * R_original + b
    G_calibrado = a * G_original + b
    B_calibrado = a * B_original + b
    return R_calibrado, G_calibrado, B_calibrado

# Exemplo de uso da função de calibração para uma nova imagem
nova_imagem = cv2.imread("nova_imagem.jpg")
nova_imagem_rgb = cv2.cvtColor(nova_imagem, cv2.COLOR_BGR2RGB)

# Calibrando a nova imagem
R_calibrado, G_calibrado, B_calibrado = calibrar_cor(*nova_imagem_rgb[0, 0])

# Resultados
print("Valores RGB calibrados:", R_calibrado, G_calibrado, B_calibrado)

# Visualização da curva de calibração
plt.scatter(valores_referencia[:, 0], cores_referencia[:, 0], color='red', label='R')
plt.scatter(valores_referencia[:, 1], cores_referencia[:, 1], color='green', label='G')
plt.scatter(valores_referencia[:, 2], cores_referencia[:, 2], color='blue', label='B')
plt.xlabel('Valores RGB das Imagens de Referência')
plt.ylabel('Valores RGB Conhecidos')
plt.legend()
plt.show()
