import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Ler a imagem padrão (blank) e calcular a média do RGB
blank_image = cv2.imread('blank.jpg')
blank_rgb = np.mean(blank_image, axis=(0, 1))
blank_rgb_mean = np.sum(blank_rgb) / 3

# Concentrações conhecidas de proteína (em porcentagem)
concentrations = np.array([2.0, 2.5, 3.0, 3.5, 4.0])

# Lista para armazenar os valores de log10(RGB padrão / Média do RGB) para cada concentração
log_ratios = []

# Processar cada imagem e calcular log10(RGB padrão / Média do RGB)
for concentration in concentrations:
    # Ler a imagem da concentração atual
    image_path = f'proteina_{concentration}%.jpg'
    image = cv2.imread(image_path)

    # Calcular a média do RGB para a imagem atual
    image_rgb = np.mean(image, axis=(0, 1))

    print(image_rgb)

    image_rgb_mean = np.sum(image_rgb) / 3

    # Calcular log10(RGB padrão / Média do RGB) e adicionar à lista log_ratios
    log_ratio = np.log10(blank_rgb_mean / image_rgb_mean)

    log_ratios.append(log_ratio)

# Converter log_ratios para um array numpy
log_ratios = np.array(log_ratios)


# Definir a função da curva para o ajuste (uma linha reta neste caso)
def func(x, a, b):
    return a * x + b


# Ajustar a curva aos dados
params, covariance = curve_fit(func, xdata=concentrations, ydata=log_ratios, p0=[2, 0])

# Parâmetros da curva ajustada
a, b = params

# Calcular os valores preditos pela curva ajustada
predicted_values = func(concentrations, a, b)

# Calcular o coeficiente de determinação (R^2)
residuals = log_ratios - predicted_values
ss_residual = np.sum(residuals ** 2)
ss_total = np.sum((log_ratios - np.mean(log_ratios)) ** 2)
r_squared = 1 - (ss_residual / ss_total)

# Plotar os dados e a curva ajustada
plt.scatter(concentrations, log_ratios, label='Dados Experimentais')
plt.plot(concentrations, predicted_values, color='red', label='Curva Ajustada (y = {:.4f}x + {:.4f})'.format(a, b))
plt.xlabel('Concentração de Proteína (%)')
plt.ylabel('Log(RGB Padrão / Média do RGB)')
plt.legend()
plt.title(f'Curva de Concentração x RGB Parameter\nR² = {r_squared:.4f}')
plt.show()

# Exibir os parâmetros da curva e o coeficiente de determinação
print(f'Parâmetro "a" da curva ajustada: {a:.4f}')
print(f'Parâmetro "b" da curva ajustada: {b:.4f}')
print(f'Coeficiente de Determinação (R²): {r_squared:.4f}')
