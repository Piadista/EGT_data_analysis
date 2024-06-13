from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
from tkinter.ttk import Style
import customtkinter as ctk
from math import sqrt
from scipy.optimize import curve_fit
from scipy import stats
import warnings
from function_transfer import *
from function_short_pulse import *

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



###############################################################FUNÇÕES AUXILIARES PULSO LONGO############################################################################################

# Auxiliary functions

# Correct timestamp values to allow values greather than the buffer size
def cor_timestamp(df):
    aux1 = df['Timestamp (s)'].max()
    ind = df['Timestamp (s)'].idxmax()
    aux2 = df['Timestamp (s)'][ind + 1]
    aux = aux1 + 0.1 - aux2

    # Correct the values of column timestamp, after a period they turn to 0 because of the size of the buffer => slow because is not vectorized but it is ok
    for i in range(0, df['Timestamp (s)'].size):
        if i > ind:
            df['Timestamp (s)'][i] = df['Timestamp (s)'][i] + aux

    return df


##################################################################FIM FUNÇÕES AXULIARES PULSO LONGO####################################################################################

####################################################################PULSO LONGO######################################################################################################

def long_pulse_graphic(nomes_arquivos):
    lista_df = []
    df_final = pd.DataFrame
    df_c = pd.DataFrame
    #Analise Pulso Longo
    pulso_longo = []

    i = 0
    for caminhos in nomes_arquivos:
        if ('Tempo de Retenção'+versionador+'Pulso Longo'+versionador) in caminhos and caminhos.endswith('.txt'):
            # df_arquivo = pd.read_csv(caminhos, sep='\t')
            pulso_longo.append(caminhos)
            i = i + 1

    i = 0
    j=0
    pulsos = []
    for i in range(len(pulso_longo)//3):
        i = i + 1
        j=j+1
        k = 0
        for elemento in pulso_longo[0:3]:
            
            # Name of the folder and file name where the data is and use it as a pandas dataframe
            if '120stability' in elemento:
                print("Estabilidade")
                df_sta = pd.read_csv(elemento, delimiter="\t")
                # Relevant parameters stability
                pulsos.append(elemento)
                tipo_chip = get_type(elemento)
                valor_chip = get_chip(elemento)
                valor_disp = get_disp(elemento)
                tipo_eletrolito = get_eletrolito(elemento)
                df_c = df_sta.rename(columns={'Current SMUb (A)' : 'Estabilidade'})
                lista_df.append(df_c['Estabilidade'].reset_index(drop=True))
                df_final = pd.concat(lista_df, axis=1)
            elif '131pulsonegativo' in elemento:
                print("Negativo")

                df_neg = pd.read_csv(elemento, delimiter="\t")
                # Relevant parameters negative
                pulsos.append(elemento)
                tipo_chip = get_type(elemento)
                valor_chip = get_chip(elemento)
                valor_disp = get_disp(elemento)
                tipo_eletrolito = get_eletrolito(elemento)
                df_c = df_neg.rename(columns={'Current SMUb (A)' : 'Negativo'})
                lista_df.append(df_c['Negativo'].reset_index(drop=True))
                df_final = pd.concat(lista_df, axis=1)

            elif '130pulsopositivo' in elemento:
                print("Positivo")

                df_pos = pd.read_csv(elemento, delimiter="\t")
                df_pos = cor_timestamp(df_pos)
                # Relevant parameters positive
                pulsos.append(elemento)
                tipo_chip = get_type(elemento)
                valor_chip = get_chip(elemento)
                valor_disp = get_disp(elemento)
                tipo_eletrolito = get_eletrolito(elemento)
                df_c = df_pos.rename(columns={'Current SMUb (A)' : 'Positivo'})
                lista_df.append(df_c['Positivo'].reset_index(drop=True))
                df_final = pd.concat(lista_df, axis=1)

        
       
        
        df_final.insert(loc=0, column='Time',value= df_pos['Timestamp (s)'].to_numpy())
        df_final.to_csv(f'dados_gerados'+versionador+f'Dados Pulso Longo'+versionador+f'Pulso Longo {tipo_chip} Chip {valor_chip} Disp {valor_disp} {tipo_eletrolito}.csv', index=False)
        df_final.to_csv(f'dados_gerados'+versionador+f'Dados Pulso Longo'+versionador+f'Pulso Longo {tipo_chip} Chip {valor_chip} Disp {valor_disp} {tipo_eletrolito}.dat', index=False)
        df_final.to_csv(f'dados_gerados'+versionador+f'Dados Pulso Longo'+versionador+f'Pulso Longo {tipo_chip} Chip {valor_chip} Disp {valor_disp} {tipo_eletrolito}.txt', index=False)

        df_final = pd.DataFrame()
        lista_df = []
        k=0

            
        
        
        
        pulsos = []
        del pulso_longo[0:3]

        
    # Set Origin instance visibility.
    # Important for only external Python.
    # Should not be used with embedded Python. 
    
    def origin_shutdown_exception_hook(exctype, value, traceback):
        '''Ensures Origin gets shut down if an uncaught exception'''
        op.exit()
        sys.__excepthook__(exctype, value, traceback)
    if op and op.oext:
        sys.excepthook = origin_shutdown_exception_hook
               
    
    
    file_names = []
    # Itera sobre os arquivos na pasta
    for nome_do_arquivo in os.listdir('dados_gerados'+versionador+'Dados Pulso Longo'):
        if nome_do_arquivo.endswith('.txt'):
            file_names.append(nome_do_arquivo)
    current_directory = os.getcwd()
    wb = op.new_book()
    wb.set_int('nLayers', len(file_names))  # Set number of sheets

    for wks, fn in zip(wb, file_names):
        file_path = os.path.join(current_directory+versionador+'dados_gerados'+versionador+'Dados Pulso Longo', fn)
        wks.from_file(file_path)
        print(f"Loaded: {file_path} into worksheet {wks}")
    
   # Lista de cores para diferenciação
    colors = ['#0000CD', '#000000', '#FF0000']
   
   # Lista para armazenar os gráficos
    graphs = []
    # Cria gráficos para cada planilha
    for i, wks in enumerate(wb):
        # Cria um novo gráfico
        gp = op.new_graph(template=current_directory+versionador+'Template'+versionador+'template_long_pulse.otp')
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
            gp[0].xlim = (0, None, None)
            gl_2 = gp[1]
            plot2 = gl_2.add_plot(wks, col, 0)
            plot2.color = colors[col % len(colors)]
            
            gl_2.set_int("link",0)
            gl_2.set_int("unit",7)
            gl_2.set_int("left", 50)
            gl_2.set_int("top",15)
            gl_2.set_int("width",30)
            gl_2.set_int("height",30)
            gl_2.rescale()
            gp[1].xlim = (6, 250, None)

    

        
        
        # Split the string at the specified character
        character = '.'
        parts = file_names[i].split(character)
        
        # Select the part up to the first occurrence of the character
        result = parts[0]
        lgnd = gp[0].label('Legend')
        lgnd.text=f'\l(1) %(1), 0V\n\l(2) %(2), 0.8V\n\l(3) %(3), -0.8V'
        gp[0].axis('y').title = f'Source-drain current, Ids (µA)'
        gp[0].axis('x').title = f'Time, t (minutes)'
        gp[1].axis('y').title = f'Source-drain current, Ids (µA)'
        gp[1].axis('x').title = f'Time, t (minutes)'
        gp[0].xlim=(0,None,None)
        lgnd.set_int('fsize', 13)
        lgnd.set_int('left',1400)
        lgnd.set_int('top',850)
        
        label = gl_1.label('text')
        label.text=f'Grafico '+result
        label.set_int('fsize', 18)
        label.set_int('left',1500)
        label.set_int('top',540)
        gp.save_fig(current_directory+versionador+'graficos_gerados'+versionador+'Graficos Pulso Longo'+versionador+f'{result}.png', width=800)
        
    


   
       
        
        
    # Save the project
    op.save(current_directory+versionador+'graficos_gerados'+versionador+'Graficos Pulso Longo'+versionador+'Grafico Pulso Longo.opju')
    
    
    
    # Exit running instance of Origin.
    # Required for external Python but don't use with embedded Python.
    
    
    
    
    op.exit()
   
##################################################################FIM PULSO LONGO##############################################