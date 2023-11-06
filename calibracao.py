import cv2
import numpy as np


def calibrar_imagens(caminho_fotos):
    valores_referencia = []
    for caminho in caminho_fotos:
        img = cv2.imread(caminho)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        valor_medio = np.mean(img_rgb, axis=(0, 1))
        valores_referencia.append(valor_medio)

    valores_referencia = np.array(valores_referencia)
    cores_referencia = np.array([[100, 76, 159], [96, 67, 158], [95, 62, 156], [93, 60, 151], [90, 56, 148]])
    a, b = np.linalg.lstsq(valores_referencia, cores_referencia, rcond=None)[0]
    return a, b


def salvar_coeficientes(a, b):
    with open('coeficientes.txt', 'w') as f:
        f.write(f'{a},{b}')


def carregar_coeficientes():
    with open('coeficientes.txt', 'r') as f:
        data = f.readline().split(',')
        a, b = float(data[0]), float(data[1])
        return a, b
