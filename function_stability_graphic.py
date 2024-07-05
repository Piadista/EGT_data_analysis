from math import sqrt
import pandas as pd
import os
import warnings
from function_transfer import *
import platform


sistema_operacional = platform.system()


if sistema_operacional == "Windows":
    versionador = '\\'
elif sistema_operacional == "Linux":
    versionador = '/'
elif sistema_operacional == "Darwin":
    print("Você está usando o macOS.")
else:
    print(f"Você está usando um sistema operacional desconhecido: {sistema_operacional}")


def stability_graphic(nomes_pastas):       
    # Set Origin instance visibility.
    # Important for only external Python.
    # Should not be used with embedded Python. 
    
    def origin_shutdown_exception_hook(exctype, value, traceback):
        '''Ensures Origin gets shut down if an uncaught exception'''
        op.exit()
        sys.__excepthook__(exctype, value, traceback)
    if op and op.oext:
        sys.excepthook = origin_shutdown_exception_hook
               
    tipos_stability = pd.read_csv('dados_gerados'+versionador+'data_Stability.txt', sep='\t')
    
   
    
    tipo = tipos_stability['Type']
    chip = tipos_stability['Chip']
    disp = tipos_stability['Disp']
    electrolyte = tipos_stability['Electrolyte']
    potential = tipos_stability['Potential [V]']
    pulse = tipos_stability['Pulse #']
    idsdep = tipos_stability['IDSdep (10sp 30sd) [A]']
    std = tipos_stability['Std IDSdep [A]']
    
    tipos_stability = pd.concat([tipo,chip,disp,electrolyte,potential,pulse,idsdep,std],axis=1)
    
    

    print(tipos_stability)
    # Função para dividir o DataFrame em blocos
    def split_dataframe(tipos_stability, chunk_size):
        chunks = []
        for start in range(0, len(tipos_stability), chunk_size):
            chunks.append(tipos_stability.iloc[start:start + chunk_size])
        return chunks
    
    # Dividindo o DataFrame em blocos de 10 linhas
    chunk_size = 100
    chunks = split_dataframe(tipos_stability, chunk_size)
    
    
    
    # Salvando cada bloco em um arquivo CSV separado
    for i, chunk in enumerate(chunks):
        tipo = str(chunks[i].iloc[0,0])
        chip = str(chunks[i].iloc[0,1])
        disp = str(chunks[i].iloc[0,2])
        electrolyte = str(chunks[i].iloc[0,3])
        potential = str(chunks[i].iloc[0,4])
        
        chunk.to_csv(os.path.join(f'dados_gerados'+versionador+f'Dados Estabilidade'+versionador+f'{tipo} Chip {chip} Disp {disp} {electrolyte} {potential}.txt'), index=False)
        print(f'Salvo chunk_{i}.csv')

        
        
 
    
    file_names = []
    
    # Itera sobre os arquivos na pasta
    for nome_do_arquivo in os.listdir('dados_gerados'+versionador+'Dados Estabilidade'):
        if nome_do_arquivo.endswith('.txt'):
            file_names.append(nome_do_arquivo)
    current_directory = os.getcwd()
    wb = op.new_book()
    wb.set_int('nLayers', len(file_names))  # Set number of sheets
    print(file_names)
    for wks, fn in zip(wb, file_names):
        file_path = os.path.join(current_directory+versionador+'dados_gerados'+versionador+'Dados Estabilidade', fn)
        wks.from_file(file_path)
        print(f"Loaded: {file_path} into worksheet {wks}")
    
   
    
    # Lista de cores para diferenciação
    colors = ['#FF0000']
    
    # Lista para armazenar os gráficos
    graphs = []
    
    # Cria gráficos para cada planilha
    for i, wks in enumerate(wb):
        # Cria um novo gráfico
        gp = op.new_graph(template=current_directory+versionador+'Template'+versionador+'template_stability.otp')
        graphs.append(gp)  # Armazena a referência ao gráfico
        
        # Adiciona todas as colunas da planilha ao gráfico, assumindo que a primeira coluna é X e as outras são Y
        for col in range(1, wks.cols):
            wks.cols_axis('nnnnnxyn')


            plot = gp[0].add_plot(wks, coly='IDSdep (10sp 30sd) [A]', colx='Pulse #',type=202)  # colx=0 assume que a primeira coluna é X
            # Adicione barras de erro
            plot.color = colors[0]
            plot.set_int('line.width', 2)
            plot.set_int('lineStyle', 1)
            plot.set_int('lineThickness', 6)
            gp[0].rescale()
            
        # Split the string at the specified character
        character = '.'
        parts = file_names[i].split(character)

        # Select the part up to the first occurrence of the character
        result = parts[0]+'.'+parts[1]
        
       
        
        
        gp[0].axis('y').title = f'IDSdep (10sp 30sd) [A]'
        gp[0].axis('x').title = f'Pulse #'
        gp[0].xlim=(0,None,None)
        
        
        label = gp[0].label('text')
        label.text=f'Grafico '+result+ ' V'
        label.set_int('fsize', 18)
        label.set_int('left',1600)
        label.set_int('top',450)
        gp.save_fig(current_directory+versionador+'graficos_gerados'+versionador+'Graficos Estabilidade'+versionador+f'Stability {result} V.png', width=800)

        
    # Save the project
    op.save(current_directory+versionador+'graficos_gerados'+versionador+'Graficos Estabilidade'+versionador+'Grafico Estabilidade.opju')
    
    
    
    
    
    
    
    op.exit()





# Exit running instance of Origin.
# Required for external Python but don't use with embedded Python.






