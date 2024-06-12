import os
from pptx import Presentation
from pptx.util import Inches, Pt

# Função para criar a apresentação de slides
def power_point(image_folder, output_pptx):
    # Cria uma apresentação vazia
    prs = Presentation()
    
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
    
    # Lista todas as imagens na pasta especificada
    images = [f for f in os.listdir(image_folder) if f.endswith(('png', 'jpg', 'jpeg'))]
    
    # Organiza as imagens em grupos de 6 para colocar em cada slide
    for i in range(0, len(images), 6):
        # Adiciona um slide vazio
        slide_layout = prs.slide_layouts[6]  # Layout 6 é um slide vazio
        slide = prs.slides.add_slide(slide_layout)
        
        for j in range(6):
            if i + j < len(images):
                # Calcula a posição da imagem
                col = j % 3  # Colunas (0, 1, 2)
                row = j // 3  # Linhas (0, 1)
                left = margin_left + col * (img_width + horizontal_spacing)
                top = margin_top + row * (img_height + vertical_spacing)
                
                # Adiciona a imagem ao slide
                img_path = os.path.join(image_folder, images[i + j])
                slide.shapes.add_picture(img_path, left, top, width=img_width, height=img_height)
    
    # Salva a apresentação
    prs.save(output_pptx)

# Especifica a pasta com as imagens e o arquivo de saída
image_folder = 'C:\\Users\\eduardo.neto\\Desktop\\programa_v5\\graficos_gerados\\Graficos Single Pulse'
output_pptx = 'Template\\presentation.pptx'

# Cria a apresentação
power_point(image_folder, output_pptx)

