from math import sqrt
import pandas as pd
import os
import warnings
from function_transfer import *
import platform
import matplotlib.pyplot as plt


sistema_operacional = platform.system()


if sistema_operacional == "Windows":
    versionador = '\\'
elif sistema_operacional == "Linux":
    versionador = '/'
elif sistema_operacional == "Darwin":
    print("Você está usando o macOS.")
else:
    print(f"Você está usando um sistema operacional desconhecido: {sistema_operacional}")
    
    
    
def single_pulse_graphic(nomes_pastas):
    
        
        
        
        def origin_shutdown_exception_hook(exctype, value, traceback):
            '''Ensures Origin gets shut down if an uncaught exception'''
            op.exit()
            sys.__excepthook__(exctype, value, traceback)
        if op and op.oext:
            sys.excepthook = origin_shutdown_exception_hook
                   
        
        
        file_names = []
        # Itera sobre os arquivos na pasta
        for nome_do_arquivo in os.listdir('dados_gerados'+versionador+'Dados Single Pulse'):
            if nome_do_arquivo.endswith('.txt'):
                file_names.append(nome_do_arquivo)
        current_directory = os.getcwd()
        wb = op.new_book()
        wb.set_int('nLayers', len(file_names))  # Set number of sheets

        for wks, fn in zip(wb, file_names):
            file_path = os.path.join(current_directory+versionador+'dados_gerados'+versionador+'Dados Single Pulse', fn)
            wks.from_file(file_path)
            print(f"Loaded: {file_path} into worksheet {wks}")
        
       # Lista de cores para diferenciação
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#bcbd22']
       
       # Lista para armazenar os gráficos
        graphs = []
        # Cria gráficos para cada planilha
        for i, wks in enumerate(wb):
            # Cria um novo gráfico
            gp = op.new_graph(template='Template\\template_single_pulse.otp')
            graphs.append(gp)  # Armazena a referência ao gráfico
            
            
          
            print("AQUIIASASASSSASAS")
            # Adiciona todas as colunas da planilha ao gráfico, assumindo que a primeira coluna é X e as outras são Y
            for col in range(1, wks.cols):
                gl_1 = gp[0]
                plot = gl_1.add_plot(wks, coly=col, colx=0)  # colx=0 assume que a primeira coluna é X
                plot.color = colors[col % len(colors)]
                plot.set_int('line.width', 1)
                plot.set_int('lineStyle', 1)
                plot.set_int('lineThickness', 1)
                gl_1.rescale()
                
                if '10ms' in file_names[i]:
                    gp[0].xlim = (14.99, 15.01, None)
                    #gp[0].ylim = (0, 2, None)
                if '100ms' in file_names[i]:
                    gp[0].xlim = (15.84, 16.4, None)
                if '1s' in file_names[i]:
                    gp[0].xlim = (12.5, 22.5, None)
                if '10s' in file_names[i]:
                    gp[0].xlim = (10, 30, None)
                if '40s' in file_names[i]:
                    gp[0].xlim = (0, 110, None)
                
                
               

        

            
            
            # Split the string at the specified character
            character = '.'
            parts = file_names[i].split(character)
            
            # Select the part up to the first occurrence of the character
            result = parts[0]
            lgnd = gp[0].label('Legend')
            
            if '200mV' in file_names[i]:
                lgnd.text=f'\l(1) |0.1| V\n\l(2) |0.2| V\n\l(3) |0.3| V\n\l(4) |0.4| V\n\l(5) |0.5| V\n\l(6) |0.6| V\n\l(7) |0.7| V'
            elif '400mV' in file_names[i]:
                lgnd.text=f'\l(1) |0.1| V\n\l(2) |0.2| V\n\l(3) |0.3| V\n\l(4) |0.4| V\n\l(5) |0.5| V\n\l(6) |0.6| V'
            else:
                lgnd.text=f'\l(1) |0.1| V\n\l(2) |0.2| V\n\l(3) |0.3| V\n\l(4) |0.4| V\n\l(5) |0.5| V\n\l(6) |0.6| V\n\l(7) |0.7| V\n\l(8) |0.8| V'
            gp[0].axis('y').title = f'Source-drain current, Ids (µA)'
            gp[0].axis('x').title = f'Time, t (seconds)'
            
            if '40s' in file_names[i]:
                lgnd.set_int('left',4500)
            if '10s' in file_names[i]:
                lgnd.set_int('left',1500)
            else:
                lgnd.set_int('left',4000)
            
            
            lgnd.set_int('fsize', 12)
            lgnd.set_int('top',1100)
            label = gl_1.label('text')
            label.text=f'Grafico '+result
            label.set_int('fsize', 15)
            label.set_int('left',1200)
            label.set_int('top',540)
            gp.save_fig(current_directory+versionador+'graficos_gerados'+versionador+'Graficos Single Pulse'+versionador+f'{result}.png', width=800)
            
        


       
           
            
            
        # Save the project
        op.save(current_directory+versionador+'graficos_gerados'+versionador+'Graficos Single Pulse'+versionador+'Grafico Single Pulse.opju')
        
        
        
        # Exit running instance of Origin.
        # Required for external Python but don't use with embedded Python.
        
        
        
        
        op.exit()