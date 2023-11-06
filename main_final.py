import calibracao
import analise_imagem
import tkinter as tk
from tkinter import filedialog


def selecionar_opcao():
    print("Escolha uma opção:")
    print("1 - Calibrar imagens")
    print("2 - Analisar uma imagem")
    opcao = input("Digite o número da opção: ")
    return int(opcao)


def openFile():
    caminho_arquivo = filedialog.askopenfilename()
    print(caminho_arquivo)


def obter_caminho_imagem():
    root = tk.Tk()

    caminho_arquivo = filedialog.askopenfilename()

    button = tk.Button(text='Open', command=caminho_arquivo)
    button.pack()
    root.mainloop()
    return caminho_arquivo


if __name__ == "__main__":
    opcao = selecionar_opcao()

    if opcao == 1:
        caminho_fotos = []
        while True:
            print("Selecione uma imagem de referência para calibração:")
            caminho = obter_caminho_imagem()
            caminho_fotos.append(caminho)
            continuar = input("Deseja adicionar outra imagem de referência? (s/n): ")
            if continuar.lower() != 's':
                break

        a, b = calibracao.calibrar_imagens(caminho_fotos)
        calibracao.salvar_coeficientes(a, b)
        print("Calibração concluída. Coeficientes salvos.")
    elif opcao == 2:
        try:
            a, b = calibracao.carregar_coeficientes()
        except FileNotFoundError:
            print("Erro: Calibração não encontrada. Calibre as imagens primeiro.")
        else:
            print("Selecione a imagem que deseja analisar:")
            nome_arquivo = obter_caminho_imagem()
            analise_imagem.analisar_imagem(nome_arquivo, a, b)
    else:
        print("Opção inválida. Por favor, escolha uma opção válida.")
