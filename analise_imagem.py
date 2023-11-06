import cv2


def analisar_imagem(nome_arquivo, a, b):
    nova_imagem = cv2.imread(nome_arquivo)
    nova_imagem_rgb = cv2.cvtColor(nova_imagem, cv2.COLOR_BGR2RGB)
    R_calibrado, G_calibrado, B_calibrado = calibrar_cor(*nova_imagem_rgb[0, 0], a, b)
    print("Valores RGB calibrados:", R_calibrado, G_calibrado, B_calibrado)


def calibrar_cor(R_original, G_original, B_original, a, b):
    R_calibrado = a * R_original + b
    G_calibrado = a * G_original + b
    B_calibrado = a * B_original + b
    return R_calibrado, G_calibrado, B_calibrado
