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
def transconduct_graphic(nomes_arquivos):
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
        transconduct = transfer_extractor_values(df_c)
        print(transconduct)
        transconduct.to_csv(f'dados_gerados'+versionador+'transconduct.txt', sep='\t', index=False)

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
        df_renamed = df_ida.rename(columns={'V': 'V Indo', 'gm [S]': 'gm [S] Indo'},  inplace=True)
        df_volta= pd.concat([nan_block, df2], ignore_index=True)
        df_renamed = df_volta.rename(columns={'V': 'V Voltando', 'gm [S]': 'gm [S] Voltando'},  inplace=True)
       
        df_todo =  pd.concat([df_ida, df_volta], axis=1)
        df_todo.to_csv(f'dados_gerados'+versionador+'datatodoc.txt', sep='\t', index=False)

        # Reordenar colunas
        cycle = df_todo['Cycle #']
        v_indo = df_todo['V Indo']
        v_voltando = df_todo['V Voltando']
        

        ids_indo = df_todo['gm [S] Indo']
        print("cheguei aqui")
        ids_voltando = df_todo['gm [S] Voltando']
        
       
        
        df_todo = pd.concat([df_c['V'], ids_indo, ids_voltando], axis=1)
        df_final = df_todo.reset_index(drop=True)

        tipo_chip = get_type(elemento)
        valor_chip = get_chip(elemento)
        valor_disp = get_disp(elemento)

        tipo_eletrolito = get_eletrolito(elemento)
        tipo_measure = get_measure(elemento)
        
        
        
        
        
        
        
        
        
        # Combine os DataFrames com blocos de NaNs entre eles
        
        df_ida= pd.concat([df1, nan_block], ignore_index=True)
        df_renamed = df_ida.rename(columns={'V': 'V Indo', '|gm| [S]': '|gm| [S] Indo'},  inplace=True)
        df_volta= pd.concat([nan_block, df2], ignore_index=True)
        df_renamed = df_volta.rename(columns={'V': 'V Voltando', '|gm| [S]': '|gm| [S] Voltando'},  inplace=True)
       
        df_todo =  pd.concat([df_ida, df_volta], axis=1)
        df_todo.to_csv(f'dados_gerados'+versionador+'datatodoc.txt', sep='\t', index=False)

        # Reordenar colunas
        cycle = df_todo['Cycle #']
        v_indo = df_todo['V Indo']
        v_voltando = df_todo['V Voltando']
        

        ids_indo = df_todo['|gm| [S] Indo']
        print("cheguei aqui")
        ids_voltando = df_todo['|gm| [S] Voltando']
        
       
        
        df_todo = pd.concat([df_c['V'], ids_indo, ids_voltando], axis=1)
        df_final2 = df_todo.reset_index(drop=True)

        tipo_chip = get_type(elemento)
        valor_chip = get_chip(elemento)
        valor_disp = get_disp(elemento)

        tipo_eletrolito = get_eletrolito(elemento)
        tipo_measure = get_measure(elemento)
        
        
        
        
        
        
        
        
        
        
        # Combine os DataFrames com blocos de NaNs entre eles
        
        df_ida= pd.concat([df1, nan_block], ignore_index=True)
        df_renamed = df_ida.rename(columns={'V': 'V Indo', 'igs_Oupt02__--0.1000': 'IGS Indo'},  inplace=True)
        df_volta= pd.concat([nan_block, df2], ignore_index=True)
        df_renamed = df_volta.rename(columns={'V': 'V Voltando', 'igs_Oupt02__--0.1000': 'IGS Voltando'},  inplace=True)
       
        df_todo =  pd.concat([df_ida, df_volta], axis=1)
        df_todo.to_csv(f'dados_gerados'+versionador+'datatodoc.txt', sep='\t', index=False)

        # Reordenar colunas
        cycle = df_todo['Cycle #']
        v_indo = df_todo['V Indo']
        v_voltando = df_todo['V Voltando']
        

        ids_indo = df_todo['IGS Indo']*1000
        print("cheguei aqui")
        ids_voltando = df_todo['IGS Voltando']*1000
        
       
        
        df_todo = pd.concat([df_c['V'], ids_indo, ids_voltando], axis=1)
        df_final3 = df_todo.reset_index(drop=True)

        tipo_chip = get_type(elemento)
        valor_chip = get_chip(elemento)
        valor_disp = get_disp(elemento)

        tipo_eletrolito = get_eletrolito(elemento)
        tipo_measure = get_measure(elemento)
        
        
        
        
        
        
        
        
        df_final.to_csv(f'dados_gerados'+versionador+f'Dados Transcondutancia'+versionador+f'Transconduct&{tipo_chip} Chip {valor_chip} Disp {valor_disp} {tipo_eletrolito}.csv', index=False)
        df_final.to_csv(f'dados_gerados'+versionador+f'Dados Transcondutancia'+versionador+f'Transconduct&{tipo_chip} Chip {valor_chip} Disp {valor_disp} {tipo_eletrolito}.dat', index=False)
        df_final.to_csv(f'dados_gerados'+versionador+f'Dados Transcondutancia'+versionador+f'Transconduct&{tipo_chip} Chip {valor_chip} Disp {valor_disp} {tipo_eletrolito}.txt', index=False)
        df_final2.to_csv(f'dados_gerados'+versionador+f'Dados Transcondutancia'+versionador+f'Absolut Transconduct&{tipo_chip} Chip {valor_chip} Disp {valor_disp} {tipo_eletrolito}.csv', index=False)
        df_final2.to_csv(f'dados_gerados'+versionador+f'Dados Transcondutancia'+versionador+f'Absolut Transconduct&{tipo_chip} Chip {valor_chip} Disp {valor_disp} {tipo_eletrolito}.dat', index=False)
        df_final2.to_csv(f'dados_gerados'+versionador+f'Dados Transcondutancia'+versionador+f'Absolut Transconduct&{tipo_chip} Chip {valor_chip} Disp {valor_disp} {tipo_eletrolito}.txt', index=False)
        df_final3.to_csv(f'dados_gerados'+versionador+f'Dados Transcondutancia'+versionador+f'IGS&{tipo_chip} Chip {valor_chip} Disp {valor_disp} {tipo_eletrolito}.csv', index=False)
        df_final3.to_csv(f'dados_gerados'+versionador+f'Dados Transcondutancia'+versionador+f'IGS&{tipo_chip} Chip {valor_chip} Disp {valor_disp} {tipo_eletrolito}.dat', index=False)
        df_final3.to_csv(f'dados_gerados'+versionador+f'Dados Transcondutancia'+versionador+f'IGS&{tipo_chip} Chip {valor_chip} Disp {valor_disp} {tipo_eletrolito}.txt', index=False)
        df_final = pd.DataFrame()
        df_final2 = pd.DataFrame()
        df_final3 = pd.DataFrame()

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
    for nome_do_arquivo in os.listdir('dados_gerados'+versionador+'Dados Transcondutancia'):
        if nome_do_arquivo.endswith('.txt'):
            file_names.append(nome_do_arquivo)
                
    current_directory = os.getcwd()
    
    wb = op.new_book()
    wb.set_int('nLayers', len(file_names))
    
    for wks, fn in zip(wb, file_names):
        file_path = os.path.join(current_directory+versionador+'dados_gerados'+versionador+'Dados Transcondutancia', fn)
        wks.from_file(file_path)
        print(f"Loaded: {file_path} into worksheet {wks}")
    
    # Lista de cores para diferenciação
    colors = ['#FF0000','#000000']
    
    # Lista para armazenar os gráficos
    graphs = []
    
    # Cria gráficos para cada planilha
    for i, wks in enumerate(wb):
        # Cria um novo gráfico
        gp = op.new_graph(template=current_directory+versionador+'Template'+versionador+'template_transconduct.otp')
        graphs.append(gp)  # Armazena a referência ao gráfico
        
        # Adiciona todas as colunas da planilha ao gráfico, assumindo que a primeira coluna é X e as outras são Y
        for col in range(1, wks.cols):
            plot = gp[0].add_plot(wks, coly=col, colx=0, type=201)  # colx=0 assume que a primeira coluna é X
            plot.color = colors[col % len(colors)]
            plot.set_int('symbol.size', 9)
            # Set marker symbol to circle
            plot.set_int('symbol.type', 0)  # Define o símbolo como círculo

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
        if "Absolut" in result:
            gp[0].axis('y').title = f'Transcondutance, |gm| (µS)'
        elif "Transconduct" in result:
            gp[0].axis('y').title = f'Transcondutance, gm (µS)'
        else:
            gp[0].axis('y').title = f'Gate-source current, IGS (nA)'
            


        gp[0].axis('x').title = f'Gate-source voltage, Vgs (V)'
        
        lgnd.set_int('fsize', 13)
        if "Absolut" in result:
            lgnd.set_int('left',3400)
        else:
            lgnd.set_int('left',2000)

        lgnd.set_int('top',1650)
        
        label = gp[0].label('text')
        label.text=f'Grafico '+result
        label.set_int('fsize', 18)
        label.set_int('left',1050)
        label.set_int('top',350)
        if "Absolut" in result:
            gp.save_fig(current_directory+versionador+'graficos_gerados'+versionador+'Graficos Transcondutancia'+versionador+'Grafico Transcondutancia Absoluta'+versionador+f'{result}.png', width=800)
        elif "Transconduct" in result: 
            gp.save_fig(current_directory+versionador+'graficos_gerados'+versionador+'Graficos Transcondutancia'+versionador+f'{result}.png', width=800)     
        else: 
            gp.save_fig(current_directory+versionador+'graficos_gerados'+versionador+'Grafico IGS'+versionador+f'{result}.png', width=800)

    
   
        
        
    # Save the project
    op.save(current_directory+versionador+'graficos_gerados'+versionador+'Graficos Transcondutancia'+versionador+'Grafico Transcondutancia.opju')
    
    
    
    # Exit running instance of Origin.
    # Required for external Python but don't use with embedded Python.
    
    
    
    
    op.exit()

    
        
