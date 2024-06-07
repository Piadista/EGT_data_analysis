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
    singlepulse = []
    l = 0
    for caminhos in nomes_pastas:
        if ('Decaimento'+versionador+'Single Pulse') in caminhos:
            # df_arquivo = pd.read_csv(caminhos, sep='\t')
            singlepulse.append(caminhos)
            l = l + 1
            print(caminhos)
    l = 0
    
        
    for elemento in singlepulse:
        l = l + 1
        k = 0

        # Name of the folder and file name where the data is and use it as a pandas dataframe
        folder = elemento

        tipo_chip = get_type(elemento)
        valor_chip = get_chip(elemento)
        valor_disp = get_disp(elemento)
        tipo_eletrolito = get_eletrolito(elemento)
        
        # Define o tamanho da figura
        total_y = []
        df_final = pd.DataFrame
        k = -1
        
        # Loop para plotar 16 gráficos
        for i in range(0, 16):
            # Crie um subplot na posição i
            # plt.subplot(4, 4, i)
            # Carregue os dados do arquivo usando Pandas
            if i%2 == 0:
              k = k + 1
              file_path = elemento+f"\\Single ({64+i}).txt"
              df_single = pd.read_csv(file_path, delimiter="\t")
              eixo_x = df_single['Timestamp (s)']
              eixo_y = df_single['Current SMUb (A)']
              total_y.append(eixo_y.reset_index(drop=True))
              df_final = pd.concat(total_y, axis=1)
              #data = pd.read_csv(file_path,sep='\t')
              #data.to_csv('dados_gerados'+versionador+f'Dados Single Pulse'+versionador+f'Single Pulse {64+i}.csv', index=False)
             # wks.from_file(file_path)

       
        df_final.insert(loc=0, column='Time',value= df_single['Timestamp (s)'].to_numpy())
        df_final.to_csv('dados_gerados'+versionador+f'Dados Single Pulse'+versionador+f'Single Pulse 1.csv', index=False)
        print(df_final.shape)
        
        df_final = pd.DataFrame()
        total_y = []

        # Define o tamanho da figura
        k = -1
        # Loop para plotar 16 gráficos
        for i in range(0, 16):
            # Crie um subplot na posição i
            # plt.subplot(4, 4, i)
            # Carregue os dados do arquivo usando Pandas
            if i%2 != 0:
              k = k + 1
        
              file_path = elemento+f"\\Single ({64+i}).txt"
              df_single = pd.read_csv(file_path, delimiter="\t")
              eixo_x = df_single['Timestamp (s)']
              eixo_y = df_single['Current SMUb (A)']
              total_y.append(eixo_y.reset_index(drop=True))
              df_final = pd.concat(total_y, axis=1)
              #data = pd.read_csv(file_path,sep='\t')
              #data.to_csv('dados_gerados'+versionador+f'Dados Single Pulse'+versionador+f'Single Pulse {64+i}.csv', index=False)
             # wks.from_file(file_path)

       
        df_final.insert(loc=0, column='Time',value= df_single['Timestamp (s)'].to_numpy())
        df_final.to_csv('dados_gerados'+versionador+f'Dados Single Pulse'+versionador+f'Single Pulse 2.csv', index=False)
        print(df_final.shape)
        
        df_final = pd.DataFrame()
        total_y = []
          
        
        
        
        
        
        
        
        # Define o tamanho da figura
        k = -1
        # Loop para plotar 16 gráficos
        for i in range(0, 16):
            # Crie um subplot na posição i
            # plt.subplot(4, 4, i)
            # Carregue os dados do arquivo usando Pandas
            if i%2 == 0:
              k = k + 1
        
              file_path = elemento+f"\\Single ({48+i}).txt"
              data = pd.read_csv(file_path,sep='\t')
              data.to_csv('dados_gerados'+versionador+f'Dados Single Pulse'+versionador+f'Single Pulse Positivo {tipo_chip} Chip {valor_chip} Disp {valor_disp} {tipo_eletrolito}.csv', index=False)

         
        
        # Define o tamanho da figura
        k = -1
        # Loop para plotar 16 gráficos
        for i in range(0, 16):
            # Crie um subplot na posição i
            # plt.subplot(4, 4, i)
            # Carregue os dados do arquivo usando Pandas
            if i%2 != 0:
              k = k + 1
        
              file_path = elemento+f"\\Single ({48+i}).txt"
              data = pd.read_csv(file_path,sep='\t')
              data.to_csv('dados_gerados'+versionador+f'Dados Single Pulse'+versionador+f'Single Pulse Negativo {tipo_chip} Chip {valor_chip} Disp {valor_disp} {tipo_eletrolito}.csv', index=False)

        
        
        
        
        
        
        
        
        
        
        # Define o tamanho da figura
        k = -1
        # Loop para plotar 16 gráficos
        for i in range(0, 16):
            # Crie um subplot na posição i
            # plt.subplot(4, 4, i)
            # Carregue os dados do arquivo usando Pandas
            if i%2 == 0:
              k = k + 1
        
              file_path = elemento+f"\\Single ({32+i}).txt"
              data = pd.read_csv(file_path,sep='\t')
              data.to_csv('dados_gerados'+versionador+f'Dados Single Pulse'+versionador+f'Single Pulse Positivo {tipo_chip} Chip {valor_chip} Disp {valor_disp} {tipo_eletrolito}.csv', index=False)

            
        
        
        # Define o tamanho da figura
        k = -1
        # Loop para plotar 16 gráficos
        for i in range(0, 16):
            # Crie um subplot na posição i
            # plt.subplot(4, 4, i)
            # Carregue os dados do arquivo usando Pandas
            if i%2 != 0:
              k = k + 1
        
              file_path = elemento+f"\\Single ({32+i}).txt"
              data = pd.read_csv(file_path,sep='\t')
              data.to_csv('dados_gerados'+versionador+f'Dados Single Pulse'+versionador+f'Single Pulse Negativo {tipo_chip} Chip {valor_chip} Disp {valor_disp} {tipo_eletrolito}.csv', index=False)

        
        
        
        
        
        
        
        
        
        
        # Define o tamanho da figura
        k = -1
        # Loop para plotar 16 gráficos
        for i in range(0, 16):
            # Crie um subplot na posição i
            # plt.subplot(4, 4, i)
            # Carregue os dados do arquivo usando Pandas
            if i%2 == 0:
              k = k + 1
        
              file_path = elemento+f"\\Single ({32+i}).txt"
              data = pd.read_csv(file_path,sep='\t')
              data.to_csv('dados_gerados'+versionador+f'Dados Single Pulse'+versionador+f'Single Pulse Positivo {tipo_chip} Chip {valor_chip} Disp {valor_disp} {tipo_eletrolito}.csv', index=False)

        
        
        # Define o tamanho da figura
        k = -1
        # Loop para plotar 16 gráficos
        for i in range(0, 16):
            # Crie um subplot na posição i
            # plt.subplot(4, 4, i)
            # Carregue os dados do arquivo usando Pandas
            if i%2 != 0:
              k = k + 1
        
              file_path = elemento+f"\\Single ({32+i}).txt"
              data = pd.read_csv(file_path,sep='\t')
              data.to_csv('dados_gerados'+versionador+f'Dados Single Pulse'+versionador+f'Single Pulse Negativo {tipo_chip} Chip {valor_chip} Disp {valor_disp} {tipo_eletrolito}.csv', index=False)
           
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        # Define o tamanho da figura
        k = -1
        # Loop para plotar 16 gráficos
        for i in range(0, 16):
            # Crie um subplot na posição i
            # plt.subplot(4, 4, i)
            # Carregue os dados do arquivo usando Pandas
            if i%2 == 0:
              k = k + 1
        
              file_path = elemento+f"\\Single ({0+i}).txt"
              data = pd.read_csv(file_path,sep='\t')
              data.to_csv('dados_gerados'+versionador+f'Dados Single Pulse'+versionador+f'Single Pulse Positivo {tipo_chip} Chip {valor_chip} Disp {valor_disp} {tipo_eletrolito}.csv', index=False)

        
        # Define o tamanho da figura
        k = -1
        # Loop para plotar 16 gráficos
        for i in range(0, 16):
            # Crie um subplot na posição i
            # plt.subplot(4, 4, i)
            # Carregue os dados do arquivo usando Pandas
            if i%2 != 0:
              k = k + 1
        
              file_path = elemento+f"\\Single ({0+i}).txt"
              data = pd.read_csv(file_path,sep='\t')
              data.to_csv('dados_gerados'+versionador+f'Dados Single Pulse'+versionador+f'Single Pulse Negativo {tipo_chip} Chip {valor_chip} Disp {valor_disp} {tipo_eletrolito}.csv', index=False)

        
        
        
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
            gp = op.new_graph(template='C:\\Users\\eduardo.neto\\Desktop\\Teste\\template_long_pulse.otp')
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
            label.set_int('top',350)
            gp.save_fig(current_directory+versionador+'graficos_gerados'+versionador+'Graficos Pulso Longo'+versionador+f'{result}.png', width=800)
            
        


       
           
            
            
        # Save the project
        op.save(current_directory+versionador+'graficos_gerados'+versionador+'Graficos Pulso Longo'+versionador+'Grafico Pulso Longo.opju')
        
        
        
        # Exit running instance of Origin.
        # Required for external Python but don't use with embedded Python.
        
        
        
        
        op.exit()