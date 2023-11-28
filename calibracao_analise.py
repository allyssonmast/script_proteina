import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from tkinter import Tk, filedialog
import pickle


def func(x, a, b):
    return a * x + b


def blank_rgb_mean_funct(image_path='blank.jpg') -> float:
    # Ler a imagem padrão (blank) e calcular a média do RGB
    blank_image = cv2.imread(image_path)
    if blank_image is None:
        raise FileNotFoundError(f'Imagem não encontrada: {image_path}')

    blank_rgb = np.mean(blank_image, axis=(0, 1))
    return np.sum(blank_rgb) / 3


def ajustar_curva(concentrations, log_ratios):
    # Ajustar a curva aos dados
    params, covariance = curve_fit(func, xdata=concentrations, ydata=log_ratios, p0=[2, 0])

    # Parâmetros da curva ajustada
    a, b = params

    # Calcular os valores preditos pela curva ajustada
    predicted_values = np.vectorize(func)(concentrations, a, b)

    # Calcular o coeficiente de determinação (R^2)
    residuals = log_ratios - predicted_values
    ss_residual = np.sum(residuals ** 2)
    ss_total = np.sum((log_ratios - np.mean(log_ratios)) ** 2)
    r_squared = 1 - (ss_residual / ss_total)

    return a, b, predicted_values, r_squared


def salvar_parametros(concentrations, log_ratios, a, b, r_squared):
    # Salvar os pontos e os parâmetros em um arquivo usando o módulo pickle
    dados_calibracao = {'concentrations': concentrations, 'log_ratios': log_ratios, 'a': a, 'b': b,
                        'r_squared': r_squared}
    with open('dados_calibracao.pickle', 'wb') as file:
        pickle.dump(dados_calibracao, file)


def carregar_parametros():
    # Carregar os parâmetros do arquivo usando o módulo pickle
    with open('dados_calibracao.pickle', 'rb') as file:
        dados_calibracao = pickle.load(file)
    return dados_calibracao['concentrations'], dados_calibracao['log_ratios'], dados_calibracao['a'], dados_calibracao[
        'b'], dados_calibracao['r_squared']


def analisar_imagem(a, b):
    # Pedir ao usuário para selecionar uma imagem para análise
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title='Selecione a imagem para análise',
                                           filetypes=[('Imagens JPEG', '*.jpg')])
    root.destroy()

    # Calcular o log10(media_rgb_imagem/blank_rgb_mean_funct)
    image = cv2.imread(file_path)
    if image is None:
        raise FileNotFoundError(f'Imagem não encontrada: {file_path}')

    image_rgb = np.mean(image, axis=(0, 1))
    image_rgb_mean = np.sum(image_rgb) / 3
    blank_rgb_mean_value = blank_rgb_mean_funct()
    log_ratio = np.log10(blank_rgb_mean_value / image_rgb_mean)

    # Calcular o valor de proteína usando a função y = a*x + b
    concentration = (log_ratio - b) / a

    print(f'Concentração estimada de proteína: {concentration:.2f}%')


def plotar_calibracao(concentrations, log_ratios, a, b, predicted_values, r_squared):
    # Plotar os dados e a curva ajustada da calibração
    plt.scatter(concentrations, log_ratios, label='Dados Experimentais')
    plt.plot(concentrations, predicted_values, color='red', label=f'Curva Ajustada (y = {a:.4f}x + {b:.4f})')
    plt.xlabel('Concentração de Proteína (%)')
    plt.ylabel('Log(RGB Padrão / Média do RGB)')
    plt.legend()
    plt.title(f'Curva de Concentração x RGB Parameter\nR² = {r_squared:.4f}')
    plt.show()


def main():
    while True:
        # Perguntar ao usuário qual ação ele deseja realizar
        escolha = input('Escolha uma opção:\n1 - Calibrar\n2 - Analisar\n3 - Ver calibração\n4 - Sair\nOpção: ')

        if escolha == '1':
            # Calibrar o sistema
            root = Tk()
            root.withdraw()
            file_paths = filedialog.askopenfilenames(title='Selecione as imagens de calibração',
                                                     filetypes=[('Imagens JPEG', '*.jpg')])
            root.destroy()

            if len(file_paths) < 2:
                print('Selecione pelo menos duas imagens para calibração.')
                continue

            concentrations = [float(path.split('_')[-1].replace('%.jpg', '')) for path in file_paths]
            log_ratios = []

            for file_path in file_paths:
                image = cv2.imread(file_path)

                if image is None:
                    print(f'Imagem não encontrada: {file_path}')
                    continue

                image_rgb = np.mean(image, axis=(0, 1))
                image_rgb_mean = np.sum(image_rgb) / 3
                blank_rgb_mean_value = blank_rgb_mean_funct()
                log_ratio = np.log10(blank_rgb_mean_value / image_rgb_mean)

                log_ratios.append(log_ratio)

            log_ratios = np.array(log_ratios)
            a, b, predicted_values, r_squared = ajustar_curva(concentrations, log_ratios)

            # Salvar os pontos e os parâmetros para uso futuro
            salvar_parametros(concentrations, log_ratios, a, b, r_squared)

            # Plotar os dados e a curva ajustada
            plotar_calibracao(concentrations, log_ratios, a, b, predicted_values, r_squared)

        elif escolha == '2':
            # Analisar uma imagem
            try:
                # Carregar os parâmetros previamente calibrados
                concentrations, log_ratios, a, b, r_squared = carregar_parametros()
            except FileNotFoundError:
                print('Calibração não encontrada. Calibre o sistema antes de analisar uma imagem.')
                continue

            # Analisar a imagem
            analisar_imagem(a, b)

        elif escolha == '3':
            # Ver a calibração
            try:
                # Carregar os parâmetros da calibração
                concentrations, log_ratios, a, b, r_squared = carregar_parametros()
            except FileNotFoundError:
                print('Calibração não encontrada. Calibre o sistema antes de ver a calibração.')
                continue

            # Calcular os valores preditos pela curva ajustada
            predicted_values = np.vectorize(func)(concentrations, a, b)

            # Plotar os dados e a curva ajustada
            plotar_calibracao(concentrations, log_ratios, a, b, predicted_values, r_squared)

        elif escolha == '4':
            # Sair do programa
            break

        else:
            print('Escolha inválida. Por favor, escolha uma opção válida.')


if __name__ == "__main__":
    main()
