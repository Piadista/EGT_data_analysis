from math import sqrt
import pandas as pd
import os
import warnings
from function_transfer import *
import platform


sistema_operacional = platform.system()


if sistema_operacional == "Windows":
    print("Você está usando o Windows.")
    versionador = '\\'
elif sistema_operacional == "Linux":
    print("Você está usando o Linux.")
    versionador = '/'
elif sistema_operacional == "Darwin":
    print("Você está usando o macOS.")
else:
    print(f"Você está usando um sistema operacional desconhecido: {sistema_operacional}")


def ppx_graphic(nomes_pastas):       
    # Set Origin instance visibility.
    # Important for only external Python.
    # Should not be used with embedded Python. 
    
    def origin_shutdown_exception_hook(exctype, value, traceback):
        '''Ensures Origin gets shut down if an uncaught exception'''
        op.exit()
        sys.__excepthook__(exctype, value, traceback)
    if op and op.oext:
        sys.excepthook = origin_shutdown_exception_hook
               
    tipos_ppx = pd.read_csv('dados_gerados'+versionador+'data_PPX_means.txt', sep='\t')
    
    
    type_ppx = tipos_ppx['Type']
    electrolyte_ppx = tipos_ppx['Electrolyte']
    std_ppx = tipos_ppx['Potential [V]']
    period_ppx = tipos_ppx['Period [s]']
    rat_first = tipos_ppx['Rat_first']
   
    tipos_ppx = pd.concat([type_ppx,electrolyte_ppx,std_ppx,period_ppx,rat_first],axis=1)
    
    tipos_ppx = tipos_ppx.drop(index=0)
    print(len(tipos_ppx))
    

    
    # Função para dividir o DataFrame em blocos
    def split_dataframe(tipos_ppx, chunk_size):
        p = 0
        chunks = []
        for start in range(0, len(tipos_ppx), chunk_size):
            p = p + 1
            chunks.append(tipos_ppx.iloc[start:start + chunk_size])
            print(p)
        return chunks
    
    # Dividindo o DataFrame em blocos de 10 linhas
    chunk_size = 16
    chunks = split_dataframe(tipos_ppx, chunk_size)
    print(chunks)
    print(len(chunks))
    
    
    # Salvando cada bloco em um arquivo CSV separado
    for i, chunk in enumerate(chunks):
        tipo = str(chunks[i].iloc[0,0])
        eletrolito = str(chunks[i].iloc[0,1])
        potential = str(chunks[i].iloc[0,2])
        chunk.to_csv(os.path.join(f'dados_gerados'+versionador+f'Dados PPX'+versionador+f'{tipo} {eletrolito} {potential}.txt'), index=False)

        
        
 
    
    file_names = []
    
    # Itera sobre os arquivos na pasta
    for nome_do_arquivo in os.listdir('dados_gerados'+versionador+'Dados PPX'):
        if nome_do_arquivo.endswith('.txt'):
            file_names.append(nome_do_arquivo)
    current_directory = os.getcwd()
    wb = op.new_book()
    wb.set_int('nLayers', len(file_names))  # Set number of sheets
    print(file_names)
    for wks, fn in zip(wb, file_names):
        file_path = os.path.join(current_directory+versionador+'dados_gerados'+versionador+'Dados PPX', fn)
        wks.from_file(file_path)
        print(f"Loaded: {file_path} into worksheet {wks}")
    
   
    
    # Lista de cores para diferenciação
    colors = ['#335eff', '#ff5733', '#33ff57', '#ff33a1', '#ff9633', '#3380ff']
    
    # Lista para armazenar os gráficos
    graphs = []
    
    # Cria gráficos para cada planilha
    for i, wks in enumerate(wb):
        # Cria um novo gráfico
        gp = op.new_graph(template='Origin')
        graphs.append(gp)  # Armazena a referência ao gráfico
        
        # Adiciona todas as colunas da planilha ao gráfico, assumindo que a primeira coluna é X e as outras são Y
        for col in range(1, wks.cols):
            plot = gp[0].add_plot(wks, coly='Rat_first', colx='Period [s]')  # colx=0 assume que a primeira coluna é X
            plot.color = colors[col % len(colors)]
            plot.set_int('line.width', 2)
            plot.set_int('lineStyle', 1)
            plot.set_int('lineThickness', 6)
        
        gp[0].rescale()
        # Split the string at the specified character
        character = '.'
        parts = file_names[i].split(character)

        # Select the part up to the first occurrence of the character
        result = parts[0]+'.'+parts[1] + 'V'
        lgnd = gp[0].label('Legend')
        lgnd.text=f'Grafico '+result
        gp[0].xlim=(0,None,None)
        lgnd.set_int('fsize', 20)
        lgnd.set_int('left',2200)
        lgnd.set_int('top',700)
        lgnd.set_int('showframe',0)
        gp.save_fig(current_directory+versionador+'graficos_gerados'+versionador+'Graficos PPX'+versionador+f'PPX {result}.png', width=800)

        
    # Save the project
    op.save(current_directory+versionador+'graficos_gerados'+versionador+'Graficos PPX'+versionador+'Grafico PPX.opju')
    
    
    
    
    
    
    
    op.exit()
