import os
from pptx import Presentation
from pptx.util import Inches, Pt
import platform
from collections import defaultdict
import pandas as pd

sistema_operacional = platform.system()


if sistema_operacional == "Windows":
    versionador = '\\'
elif sistema_operacional == "Linux":
    versionador = '/'
elif sistema_operacional == "Darwin":
    print("Você está usando o macOS.")
else:
    print(f"Você está usando um sistema operacional desconhecido: {sistema_operacional}")
  
    


# Detecta o sistema operacional
sistema_operacional = platform.system()

# Define o separador de diretório com base no sistema operacional
versionador = os.sep

# Função para criar a apresentação de slides
def power_point(output_pptx):
    # Cria uma apresentação vazia
    current_directory = os.getcwd()

    prs = Presentation()
    
    # Adiciona um slide de título
    slide_layout = prs.slide_layouts[0]  # Layout 0 é um slide de título
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]

    title.text = "Título da Apresentação"
    subtitle.text = "Subtítulo ou Descrição da Apresentação"

    # Aumenta o tamanho da fonte do título
    title_shape = title.text_frame
    for paragraph in title_shape.paragraphs:
        for run in paragraph.runs:
            run.font.size = Pt(32)  # Tamanho da fonte do título

    # Aumenta o tamanho da fonte do subtítulo
    subtitle_shape = subtitle.text_frame
    for paragraph in subtitle_shape.paragraphs:
        for run in paragraph.runs:
            run.font.size = Pt(24)  # Tamanho da fonte do subtítulo

    # Define o tamanho das imagens em pixels (exemplo: 300x200 pixels)
    img_width_px = 320
    img_height_px = 320
    
    # Converte o tamanho das imagens de pixels para polegadas
    img_width = Pt(img_width_px / 96 * 72)  # 1 polegada = 96 pixels (resolução padrão) e 1 polegada = 72 pontos
    img_height = Pt(img_height_px / 96 * 72)
    
    # Define a posição inicial das imagens e o espaço entre elas
    margin_left = Inches(0.05)
    margin_top = Inches(0.8)
    horizontal_spacing = Inches(0.05)
    vertical_spacing = Inches(0.05)

    # Atualize este caminho conforme necessário
    image_folder = os.path.join(current_directory, 'C:\\Users\\eduardo.neto\\Desktop\\programa_v6\\graficos_gerados\\Graficos Single Pulse')
    
    # Lista todas as imagens na pasta especificada
    images = [f for f in os.listdir(image_folder) if f.endswith(('png', 'jpg', 'jpeg'))]
    
    

    
<<<<<<< HEAD

    # Lista de arquivos na pasta
    files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]

    # Criação do DataFrame
    df = pd.DataFrame(files, columns=['Filename'])



    # Extraindo o prefixo (parte antes do '_') para usar como chave de agrupamento
    df['Group'] = df['Filename'].apply(lambda x: x.split('_')[0])


    # Agrupando por 'Group'
    grouped = df.groupby('Group')
    # Realizando o agrupamento
    
    
    # Criando um único dicionário com todos os grupos
    combined_dict = {key: group.to_dict('list') for key, group in grouped}
    
    print("Dicionário combinado:")
    print(combined_dict)
    
    for key, value in combined_dict.items():
        print(f"Chave '{key}':")
        print(value)
        print()
    
    
    

      #







    
=======
>>>>>>> f556b472c18a9a0adbac58ba0cdac3da5313434e



