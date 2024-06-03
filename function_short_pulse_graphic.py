
from math import sqrt

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




###################################################################PULSO CURTO######################################################################################################

def short_pulse_graphic(nomes_arquivos):
    #Analise Pulso Curto
    lista_df = []
    df_final = pd.DataFrame
    df_c = pd.DataFrame
    pulso_curto = []

    i = 0
    for caminhos in nomes_arquivos:
        if ('Tempo de Retenção'+versionador+'Pulso Curto'+versionador) in caminhos and caminhos.endswith('.txt'):
            # df_arquivo = pd.read_csv(caminhos, sep='\t')
            pulso_curto.append(caminhos)
            i = i + 1

    i = 0

    pulsos = []

    #Pego os tres primeiros caminhos da string, já que os arquivos estão na mesma pasta, e no final retiro esses tres primeiros arquivos já que ja foi feita a analise
    for i in range(len(pulso_curto)//3):
        print("AQUIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
        i = i + 1
        k = 0
        for elemento in pulso_curto[0:3]:
            # Name of the folder and file name where the data is and use it as a pandas dataframe
            if '150stability' in elemento:
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

            elif '152pulsonegativo' in elemento:
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

            elif '151pulsopositivo' in elemento:
                df_pos = pd.read_csv(elemento, delimiter="\t")
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
        df_final.to_csv(f'dados_gerados'+versionador+f'Dados Pulso Curto'+versionador+f'Pulso Curto {tipo_chip} Chip {valor_chip} Disp {valor_disp} {tipo_eletrolito}.csv', index=False)
        df_final.to_csv(f'dados_gerados'+versionador+f'Dados Pulso Curto'+versionador+f'Pulso Curto {tipo_chip} Chip {valor_chip} Disp {valor_disp} {tipo_eletrolito}.dat', index=False)
        df_final.to_csv(f'dados_gerados'+versionador+f'Dados Pulso Curto'+versionador+f'Pulso Curto {tipo_chip} Chip {valor_chip} Disp {valor_disp} {tipo_eletrolito}.txt', index=False)

        df_final = pd.DataFrame()
        lista_df = []
        k=0

        pulsos = []
        del pulso_curto[0:3]

  
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
    for nome_do_arquivo in os.listdir('dados_gerados'+versionador+'Dados Pulso Curto'):
        if nome_do_arquivo.endswith('.txt'):
            file_names.append(nome_do_arquivo)
    current_directory = os.getcwd()
    wb = op.new_book()
    wb.set_int('nLayers', len(file_names))  # Set number of sheets

    for wks, fn in zip(wb, file_names):
        file_path = os.path.join(current_directory+versionador+'dados_gerados'+versionador+'Dados Pulso Curto', fn)
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
            plot = gp[0].add_plot(wks, coly=col, colx=0)  # colx=0 assume que a primeira coluna é X
            plot.color = colors[col % len(colors)]
            plot.set_int('line.width', 2)
            plot.set_int('lineStyle', 1)
            plot.set_int('lineThickness', 6)
        
        gp[0].rescale()
        # Split the string at the specified character
        character = '.'
        parts = file_names[i].split(character)

        # Select the part up to the first occurrence of the character
        result = parts[0]
        lgnd = gp[0].label('Legend')
        lgnd.text=f'Grafico '+result+'\n\l(1) %(1)\n\l(2) %(2)\n\l(3) %(3)'
        gp[0].axis('y').title = f'Ids (A)'
        gp[0].axis('x').title = f'Time (s)'
        gp[0].xlim=(0,None,None)
        lgnd.set_int('fsize', 13)
        lgnd.set_int('left',3200)
        lgnd.set_int('top',1000)
        lgnd.set_int('showframe',0)
        gp.save_fig(current_directory+versionador+'graficos_gerados'+versionador+'Graficos Pulso Curto'+versionador+f'{result}.png', width=800)

    
    
    
    
    
    
    
        
        
    # Save the project
    op.save(current_directory+versionador+'graficos_gerados'+versionador+'Graficos Pulso Curto'+versionador+'Grafico Pulso Curto.opju')
    
    
    
    # Exit running instance of Origin.
    # Required for external Python but don't use with embedded Python.
    
    
    
    
    op.exit()