from PIL import Image

# Valores RGB para as imagens
rgb_values = [
    (100, 76, 159),
    (96, 67, 158),
    (95, 62, 156),
    (93, 60, 151),
    (90, 56, 148),
]

# Loop para criar imagens
for i, rgb_value in enumerate(rgb_values):
    # Calcula a porcentagem de proteína
    concentration = 2 + i * 0.5

    # Nome do arquivo de imagem
    img_name = f'proteina_{concentration}%.jpg'

    # Cria uma nova imagem RGB
    img = Image.new('RGB', (100, 100), rgb_value)

    # Salva a imagem com base no nome
    img_path = img_name
    img.save(img_path)

    print(f'Imagem {img_name} criada com sucesso.')
