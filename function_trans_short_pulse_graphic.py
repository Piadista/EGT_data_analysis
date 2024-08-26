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

# Calculate the relevant parameters from a transfer curve
def transfer_extractor_values(data):
    # IDS min
    IDSMIN = data['ids_Oupt01__--0.1000'].min()
    values = np.array([('IDSMIN', IDSMIN)], dtype=[('name', 'U15'), ('value', 'f8')])
    # VGS min
    values = np.append(values,
                       np.array([('VGSMIN', data['V'][data['ids_Oupt01__--0.1000'].idxmin()])], dtype=values.dtype))
    # IDS max
    IDSMAX = data['ids_Oupt01__--0.1000'].max()
    values = np.append(values, np.array([('IDSMAX', IDSMAX)], dtype=values.dtype))
    # Razão on/off
    values = np.append(values, np.array([('RAZAO', IDSMAX / IDSMIN)], dtype=values.dtype))
    # Resistance with VDS = 0.1 V and VGS = 0V
    data_2 = data[data["V"] == 0.0]
    values = np.append(values, np.array([('RES', 0.1 / data_2.at[data_2.index[0], 'ids_Oupt01__--0.1000'])],
                                        dtype=values.dtype))
    # IDS (-0.6V)
    data_2 = data[data["V"] == -0.6]
    values = np.append(values,
                       np.array([('IDSN', data_2.at[data_2.index[0], 'ids_Oupt01__--0.1000'])], dtype=values.dtype))
    # IDS (+0.6V)
    data_2 = data[data["V"] == 0.6]
    values = np.append(values,
                       np.array([('IDSP', data_2.at[data_2.index[0], 'ids_Oupt01__--0.1000'])], dtype=values.dtype))

    # Calculate transconductance relevant parameters
    x = data["V"].to_numpy()
    y = data["ids_Oupt01__--0.1000"].to_numpy()
    gm = np.gradient(y, x)
    data["gm [S]"] = (pd.Series(gm)).tolist()
    data["|gm| [S]"] = (pd.Series(np.absolute(gm))).tolist()

    # |gm| min
    values = np.append(values, np.array([('GM_MOD_MIN', data['|gm| [S]'].min())], dtype=values.dtype))
    # VGS |gm| min
    values = np.append(values, np.array([('VGS_GM_MOD_MIN', data['V'][data['|gm| [S]'].idxmin()])], dtype=values.dtype))
    # gm min
    values = np.append(values, np.array([('GM_MIN', data['gm [S]'].min())], dtype=values.dtype))
    # VGS gm min
    values = np.append(values, np.array([('VGS_GM_MIN', data['V'][data['gm [S]'].idxmin()])], dtype=values.dtype))
    # gm max
    values = np.append(values, np.array([('GM_MAX', data['gm [S]'].max())], dtype=values.dtype))
    # VGS gm max
    values = np.append(values, np.array([('VGS_GM_MAX', data['V'][data['gm [S]'].idxmax()])], dtype=values.dtype))

    return data


######################################################################TRANSFER#########################################################################################################
def trans_short_pulse_graphic(nomes_arquivos):
    #Analise Transfer
    transfers = []
    df_y = pd.DataFrame()
    lista_df = []

    i = 0
    for caminhos in nomes_arquivos:
        if ('Tempo de Retenção'+versionador+'Transfer'+versionador) in caminhos and ('110') not in caminhos and ("140") not in caminhos and caminhos.endswith('.txt'):
            # df_arquivo = pd.read_csv(caminhos, sep='\t')
            transfers.append(caminhos)
            i = i + 1

    i=0
    k=0
    transfer = []
    #Pego os tres primeiros caminhos da string, já que os arquivos estão na mesma pasta, e no final retiro esses tres primeiros arquivos já que ja foi feita a analise
    for i in range(len(transfers)//3):
        print("AQUIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
        i = i + 1
        k = 0
        for elemento in transfers[0:3]:
            # Name of the folder and file name where the data is and use it as a pandas dataframe

            if '150' in elemento:
                df_150 = pd.read_csv(elemento, delimiter="\t")
                
                # Relevant parameters stability
                transfers.append(elemento)
                tipo_chip = get_type(elemento)
                valor_chip = get_chip(elemento)
                valor_disp = get_disp(elemento)
                tipo_eletrolito = get_eletrolito(elemento)
                
                
                
                df_c = df_150.rename(columns={'ids_Oupt01__--0.1000' : 'IDS 150'})
                lista_df.append(df_c['IDS 150'].reset_index(drop=True))
                df_final = pd.concat(lista_df, axis=1)

            elif '151' in elemento:
                df_151 = pd.read_csv(elemento, delimiter="\t")
                # Relevant parameters negative
                transfers.append(elemento)
                tipo_chip = get_type(elemento)
                valor_chip = get_chip(elemento)
                valor_disp = get_disp(elemento)
                tipo_eletrolito = get_eletrolito(elemento)
                
                
                
                
                
                df_c = df_151.rename(columns={'ids_Oupt01__--0.1000' : 'IDS 151'})
                lista_df.append(df_c['IDS 151'].reset_index(drop=True))
                df_final = pd.concat(lista_df, axis=1)

            elif '152' in elemento:
                df_152 = pd.read_csv(elemento, delimiter="\t")
                # Relevant parameters positive
                transfers.append(elemento)
                tipo_chip = get_type(elemento)
                valor_chip = get_chip(elemento)
                valor_disp = get_disp(elemento)
                tipo_eletrolito = get_eletrolito(elemento)
                
                
                
                
                df_c = df_152.rename(columns={'ids_Oupt01__--0.1000' : 'IDS 152'})
                lista_df.append(df_c['IDS 152'].reset_index(drop=True))
                df_final = pd.concat(lista_df, axis=1)




        df_final.insert(loc=0, column='V',value= df_150['V'].to_numpy())
        df_final.to_csv(f'dados_gerados'+versionador+f'Dados Trans Short Pulse'+versionador+f'Transfer Short Pulse {tipo_chip} Chip {valor_chip} Disp {valor_disp} {tipo_eletrolito}.csv', index=False)
        df_final.to_csv(f'dados_gerados'+versionador+f'Dados Trans Short Pulse'+versionador+f'Transfer Short Pulse {tipo_chip} Chip {valor_chip} Disp {valor_disp} {tipo_eletrolito}.dat', index=False)
        df_final.to_csv(f'dados_gerados'+versionador+f'Dados Trans Short Pulse'+versionador+f'Transfer Short Pulse {tipo_chip} Chip {valor_chip} Disp {valor_disp} {tipo_eletrolito}.txt', index=False)
        
        print(df_final)
        df_final = pd.DataFrame()
        lista_df = []
        k=0
        
        transfer = []
        del transfers[0:3]
                
            
            
            
    




    df_150 = pd.DataFrame()
    df_151 = pd.DataFrame()
    df_152 = pd.DataFrame()

    i=0
    k=0
    transfer = []
    #Pego os tres primeiros caminhos da string, já que os arquivos estão na mesma pasta, e no final retiro esses tres primeiros arquivos já que ja foi feita a analise
    for i in range(len(transfers)//3):
        print("AQUIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
        i = i + 1
        k = 0
        for elemento in transfers[0:3]:
            # Name of the folder and file name where the data is and use it as a pandas dataframe
    
            if '150' in elemento:
                df_150 = pd.read_csv(elemento, delimiter="\t")
                
                # Relevant parameters stability
                transfers.append(elemento)
                tipo_chip = get_type(elemento)
                valor_chip = get_chip(elemento)
                valor_disp = get_disp(elemento)
                tipo_eletrolito = get_eletrolito(elemento)
                
                df_150 = correct_cycle_column(df_150)
                transconduct = transfer_extractor_values(df_150)
                print(transconduct)
                
                df_c = df_150.rename(columns={'|gm| [S]' : 'gm 150'})
                lista_df.append(df_c['gm 150'].reset_index(drop=True))
                df_final = pd.concat(lista_df, axis=1)
    
            elif '151' in elemento:
                df_151 = pd.read_csv(elemento, delimiter="\t")
                # Relevant parameters negative
                transfers.append(elemento)
                tipo_chip = get_type(elemento)
                valor_chip = get_chip(elemento)
                valor_disp = get_disp(elemento)
                tipo_eletrolito = get_eletrolito(elemento)
                
                df_151 = correct_cycle_column(df_151)
                transconduct = transfer_extractor_values(df_151)
                
                
                df_c = df_151.rename(columns={'|gm| [S]' : 'gm 151'})
                lista_df.append(df_c['gm 151'].reset_index(drop=True))
                df_final = pd.concat(lista_df, axis=1)
                
    
            elif '152' in elemento:
                df_152 = pd.read_csv(elemento, delimiter="\t")
                # Relevant parameters positive
                transfers.append(elemento)
                tipo_chip = get_type(elemento)
                valor_chip = get_chip(elemento)
                valor_disp = get_disp(elemento)
                tipo_eletrolito = get_eletrolito(elemento)
                
                
                df_152 = correct_cycle_column(df_152)
                transconduct = transfer_extractor_values(df_152)
                
                df_c = df_152.rename(columns={'|gm| [S]' : 'gm 152'})
                lista_df.append(df_c['gm 152'].reset_index(drop=True))
                df_final = pd.concat(lista_df, axis=1)
    
    
    
    
        df_final.insert(loc=0, column='V',value= df_150['V'].to_numpy())
        df_final.to_csv(f'dados_gerados'+versionador+f'Dados Trans Short Pulse'+versionador+f'Transconduct Short Pulse {tipo_chip} Chip {valor_chip} Disp {valor_disp} {tipo_eletrolito}.csv', index=False)
        df_final.to_csv(f'dados_gerados'+versionador+f'Dados Trans Short Pulse'+versionador+f'Transconduct Short Pulse {tipo_chip} Chip {valor_chip} Disp {valor_disp} {tipo_eletrolito}.dat', index=False)
        df_final.to_csv(f'dados_gerados'+versionador+f'Dados Trans Short Pulse'+versionador+f'Transconduct Short Pulse {tipo_chip} Chip {valor_chip} Disp {valor_disp} {tipo_eletrolito}.txt', index=False)
        
        print(df_final)

        df_final = pd.DataFrame()
        lista_df = []
        k=0
        
        transfer = []
        del transfers[0:3]


















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
    for nome_do_arquivo in os.listdir('dados_gerados'+versionador+'Dados Trans Short Pulse'):
        if nome_do_arquivo.endswith('.txt'):
            file_names.append(nome_do_arquivo)
                
    current_directory = os.getcwd()
    
    wb = op.new_book()
    wb.set_int('nLayers', len(file_names))
    
    for wks, fn in zip(wb, file_names):
        file_path = os.path.join(current_directory+versionador+'dados_gerados'+versionador+'Dados Trans Short Pulse', fn)
        wks.from_file(file_path)
        print(f"Loaded: {file_path} into worksheet {wks}")
    
    # Lista de cores para diferenciação
    colors = ['#0000CD', '#000000', '#FF0000']
    
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
            plot.set_int('symbol.size', 7)
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
        lgnd.text=f'\l(1) After 0V\n\l(2) After +0.8V\n\l(3) After -0.8V\n'
    
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
        gp.save_fig(current_directory+versionador+'graficos_gerados'+versionador+'Grafico Trans Short Pulse'+versionador+f'{result}.png', width=800)

    
   
        
        
    # Save the project
    op.save(current_directory+versionador+'graficos_gerados'+versionador+'Grafico Trans Short Pulse'+versionador+'Grafico Trans Short Pulse.opju')
    
    
    
    # Exit running instance of Origin.
    # Required for external Python but don't use with embedded Python.
    
    
    
    
    op.exit()

    
        
   
   
    
    

#####################################################################FIM TRANSFER##############################
