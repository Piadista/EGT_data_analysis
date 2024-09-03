from rotulos import *
import pandas as pd
import numpy as np
import platform
import originpro as op
import sys
import os


sistema_operacional = platform.system()


if sistema_operacional == "Windows":
    versionador = '\\'
elif sistema_operacional == "Linux":
    versionador = '/'
elif sistema_operacional == "Darwin":
    print("Você está usando o macOS.")
else:
    print(f"Você está usando um sistema operacional desconhecido: {sistema_operacional}")

#########################################################################FUNÇÕES AUXILIARES TRANSFERÊNCIA##############################################################################


# Correct the values from first column of cycles
def correct_cycle_column(df):
    x = df['Cycle #'].values[-1]
    for i in range(0, int(x + 1)):
        df['Cycle #'][
        int(i * len(df['Cycle #']) / (int(x) + 1)):int((i + 1) * len(df['Cycle #']) / (int(x) + 1))] = float(i)
    return df


################################################################FIM FUNÇÕES AUXILIARES TRANSFERÊNCIA##################################################################################




######################################################################TRANSFER#########################################################################################################
def transfer_retention_time_graphic(nomes_arquivos):
    #Analise Transfer
    transfers = []
    df_y = pd.DataFrame()
    lista_df = []

    i = 0
    for caminhos in nomes_arquivos:
        if ('Tempo de Retenção'+versionador+'Transfer'+versionador) in caminhos and ('110') in caminhos and caminhos.endswith('.txt'):
            # df_arquivo = pd.read_csv(caminhos, sep='\t')
            transfers.append(caminhos)
            i = i + 1

    i=0
    k=0

    for elemento in transfers:
        i = i + 1
        k = k + 1
        data = pd.read_csv(elemento, sep="\t")

        # Correct first column of cycles (Monstro software subscribe wrongly some values)

        df_c = correct_cycle_column(data)

        # Calculate relevant parameters and choose the appropriate data
        
        #sweep = 2.0
        #df_c = df_c[df_c["Cycle #"] == sweep]
        #df_c = df_c.drop_duplicates(subset=['V'])
        # Definir o tamanho do bloco
        
        # Dividir os dados em blocos
        
        df_r = pd.DataFrame()
        
        print("oi")
        
     
        
       
        
        df1 = pd.DataFrame(df_c.loc[242:302].reset_index(drop=True))
        df2 = pd.DataFrame(df_c.loc[303:362].reset_index(drop=True))
        

        
        # Crie DataFrames de NaNs
        nan_block = pd.DataFrame({'A': [np.nan] * 61})
        
        # Combine os DataFrames com blocos de NaNs entre eles
        
        df_ida= pd.concat([df1, nan_block], ignore_index=True)
        df_renamed = df_ida.rename(columns={'V': 'V Indo', 'ids_Oupt01__--0.1000': 'IDS Indo'},  inplace=True)
        df_volta= pd.concat([nan_block, df2], ignore_index=True)
        df_renamed = df_volta.rename(columns={'V': 'V Voltando', 'ids_Oupt01__--0.1000': 'IDS Voltando'},  inplace=True)
       
        df_todo =  pd.concat([df_ida, df_volta], axis=1)
        df_todo.to_csv(f'dados_gerados'+versionador+'datatodoc.txt', sep='\t', index=False)

        # Reordenar colunas
        cycle = df_todo['Cycle #']
        v_indo = df_todo['V Indo']
        v_voltando = df_todo['V Voltando']
        

        ids_indo = df_todo['IDS Indo']
        print("cheguei aqui")
        ids_voltando = df_todo['IDS Voltando']
        
       
        
        df_todo = pd.concat([df_c['V'], ids_indo, ids_voltando], axis=1)
        df_final = df_todo.reset_index(drop=True)

        tipo_chip = get_type(elemento)
        valor_chip = get_chip(elemento)
        valor_disp = get_disp(elemento)

        tipo_eletrolito = get_eletrolito(elemento)
        tipo_measure = get_measure(elemento)
        #df_c = df_c.rename(columns={'IDS_Oupt01__--0.2000' : tipo_measure})
        
        #lista_df.append(df_c[tipo_measure].reset_index(drop=True))
       # df_final = pd.concat(lista_df, axis=1)
        #df_final.insert(loc=0, column='Vgs',value= df_c['V'].to_numpy())
        df_final.to_csv(f'dados_gerados'+versionador+f'Dados Transfer Tempo de Retenção'+versionador+f'Retention Transfer&{tipo_chip} Chip {valor_chip} Disp {valor_disp} {tipo_eletrolito}.csv', index=False)
        df_final.to_csv(f'dados_gerados'+versionador+f'Dados Transfer Tempo de Retenção'+versionador+f'Retention Transfer&{tipo_chip} Chip {valor_chip} Disp {valor_disp} {tipo_eletrolito}.dat', index=False)
        df_final.to_csv(f'dados_gerados'+versionador+f'Dados Transfer Tempo de Retenção'+versionador+f'Retention Transfer&{tipo_chip} Chip {valor_chip} Disp {valor_disp} {tipo_eletrolito}.txt', index=False)

        df_final = pd.DataFrame()
        lista_df = []
        k=0
            
            
            
            
    



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
    for nome_do_arquivo in os.listdir('dados_gerados'+versionador+'Dados Transfer Tempo de Retenção'):
        if nome_do_arquivo.endswith('.txt'):
            file_names.append(nome_do_arquivo)
                
    current_directory = os.getcwd()
    
    wb = op.new_book()
    wb.set_int('nLayers', len(file_names))
    
    for wks, fn in zip(wb, file_names):
        file_path = os.path.join(current_directory+versionador+'dados_gerados'+versionador+'Dados Transfer Tempo de Retenção', fn)
        wks.from_file(file_path)
        print(f"Loaded: {file_path} into worksheet {wks}")
    
    # Lista de cores para diferenciação
    colors = ['#FF0000','#000000']
    
    # Lista para armazenar os gráficos
    graphs = []
    
    # Cria gráficos para cada planilha
    for i, wks in enumerate(wb):
        # Cria um novo gráfico
        gp = op.new_graph(template=current_directory+versionador+'Template'+versionador+'template_transfer_retention_time.otp')
        graphs.append(gp)  # Armazena a referência ao gráfico
        
        # Adiciona todas as colunas da planilha ao gráfico, assumindo que a primeira coluna é X e as outras são Y
        for col in range(1, wks.cols):
            plot = gp[0].add_plot(wks, coly=col, colx=0, type=201)  # colx=0 assume que a primeira coluna é X
            plot.color = colors[col % len(colors)]
            plot.set_int('symbol.size', 9)
            # Set marker symbol to circle
            plot.set_int('line.width', 5)
            plot.set_int('lineStyle', 1)
            plot.set_int('lineThickness', 5)
            gp[0].rescale()
        # Split the string at the specified character
        character = '.'
        parts = file_names[i].split(character)

        # Select the part up to the first occurrence of the character
        result = parts[0]
        lgnd = gp[0].label('Legend')
        lgnd.text=f'\l(1) -0.6V ---> 0.6V\n\l(2) 0.6V ---> -0.6V\n'
    
        gp[0].axis('y').title = f'Source-drain current, Ids (µA)'
        gp[0].axis('x').title = f'Vgs'
        lgnd.set_int('fsize', 17)
        lgnd.set_int('left',3000)
        lgnd.set_int('top',1650)
        
        label = gp[0].label('text')
        label.text=f'Grafico '+result
        label.set_int('fsize', 18)
        label.set_int('left',1050)
        label.set_int('top',350)
        gp.save_fig(current_directory+versionador+'graficos_gerados'+versionador+'Graficos Transfer Tempo de Retencao'+versionador+f'{result}.png', width=800)

    
   
        
        
    # Save the project
    op.save(current_directory+versionador+'graficos_gerados'+versionador+'Graficos Transfer Tempo de Retencao'+versionador+'Grafico Tempo de Retenção.opju')
    
    
    
    # Exit running instance of Origin.
    # Required for external Python but don't use with embedded Python.
    
    
    
    
    op.exit()

    
        
   
   
    
    

#####################################################################FIM TRANSFER##############################
