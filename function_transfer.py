from rotulos import *
import pandas as pd
import numpy as np
import platform
import originpro as op
import sys
import os

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

#########################################################################FUNÇÕES AUXILIARES TRANSFERÊNCIA##############################################################################


# Correct the values from first column of cycles
def correct_cycle_column(df):
    x = df['Cycle #'].values[-1]
    for i in range(0, int(x + 1)):
        df['Cycle #'][
        int(i * len(df['Cycle #']) / (int(x) + 1)):int((i + 1) * len(df['Cycle #']) / (int(x) + 1))] = float(i)
    return df


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

    return values


################################################################FIM FUNÇÕES AUXILIARES TRANSFERÊNCIA##################################################################################

#####################################################CRIA O ARQUIVO TRANSFERÊNCIA#########################################################################################################
def create_transfer():
    # Create the file with compiled important data
    df_transfer = pd.DataFrame(columns=['Type','Chip','Disp', 'Electrolyte','Measure','Sweep','VGSmin [V]',
                                          'IDSmin [A]', 'IDSmax [A]','Ronoff', 'Res [ohm]', 'IDS(-0.6V) [A]', 'IDS(+0.6V) [A]',
                                         'VGS min |gm| [V]','min |gm| [S]', 'VGS min gm [V]','min gm [S]', 'VGS max gm [V]', 'max gm [S]'])


    # Export dataframe into a .txt file
    df_transfer.to_csv('dados_gerados'+versionador+'data_transfer.txt', sep='\t', index=False)
    

##############################################################################################################################################

######################################################################TRANSFER#########################################################################################################
def analise_transfer(nomes_arquivos):
    create_transfer()
    #Analise Transfer
    transfers = []

    i = 0
    for caminhos in nomes_arquivos:
        if ('Transfer'+versionador) in caminhos and caminhos.endswith('.txt'):
            # df_arquivo = pd.read_csv(caminhos, sep='\t')
            transfers.append(caminhos)
            i = i + 1

    i=0


    for elemento in transfers:
        i = i +1

        data = pd.read_csv(elemento, sep="\t")

        # Correct first column of cycles (Monstro software subscribe wrongly some values)

        df_c = correct_cycle_column(data)
        # Calculate relevant parameters and choose the appropriate data
        if "150transfer" in elemento:
            sweep = 1.0
        elif "151transfer" in elemento:
            sweep = 1.0
        elif "152transfer" in elemento:
            sweep = 1.0
        else:
            sweep = 2.0
        df_c = df_c[df_c["Cycle #"] == sweep]
        df_c = df_c.drop_duplicates(subset=['V'])

       

        # Relevant parameters calculation
        values = transfer_extractor_values(df_c)

        # Extract the data into variables
        VGSMIN = values[values['name'] == 'VGSMIN']['value'][0]
        IDSMIN = values[values['name'] == 'IDSMIN']['value'][0]
        IDSMAX = values[values['name'] == 'IDSMAX']['value'][0]
        RAZAO = values[values['name'] == 'RAZAO']['value'][0]
        RES = values[values['name'] == 'RES']['value'][0]
        IDSN = values[values['name'] == 'IDSN']['value'][0]
        IDSP = values[values['name'] == 'IDSP']['value'][0]
        VGS_GM_MOD_MIN = values[values['name'] == 'VGS_GM_MOD_MIN']['value'][0]
        GM_MOD_MIN = values[values['name'] == 'GM_MOD_MIN']['value'][0]
        VGS_GM_MIN = values[values['name'] == 'VGS_GM_MIN']['value'][0]
        GM_MIN = values[values['name'] == 'GM_MIN']['value'][0]
        VGS_GM_MAX = values[values['name'] == 'VGS_GM_MAX']['value'][0]
        GM_MAX = values[values['name'] == 'GM_MAX']['value'][0]

        tipo_chip = get_type(elemento)
        valor_chip = get_chip(elemento)
        valor_disp = get_disp(elemento)
        tipo_eletrolito = get_eletrolito(elemento)
        tipo_measure = get_measure(elemento)
        # Create a dictionary with the data for the new row
        new_row = {'Type': tipo_chip, 'Chip': valor_chip, 'Disp': valor_disp, 'Electrolyte': tipo_eletrolito, 'Measure': tipo_measure, 'Sweep': int(sweep),
                   'VGSmin [V]': VGSMIN, 'IDSmin [A]': IDSMIN,
                   'IDSmax [A]': IDSMAX, 'Ronoff': RAZAO, 'Res [ohm]': RES, 'IDS(-0.6V) [A]': IDSN,
                   'IDS(+0.6V) [A]': IDSP,
                   'VGS min |gm| [V]': VGS_GM_MOD_MIN, 'min |gm| [S]': GM_MOD_MIN, 'VGS min gm [V]': VGS_GM_MIN,
                   'min gm [S]': GM_MIN, 'VGS max gm [V]': VGS_GM_MAX, 'max gm [S]': GM_MAX}

        # Append the dictionary to the DataFrame previously created
        df = pd.read_csv('dados_gerados'+versionador+'data_transfer.txt', delimiter="\t")
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        # Reset the index
        df = df.reset_index(drop=True)

        # Export dataframe into a .txt file
        df.to_csv(f'dados_gerados'+versionador+'data_transfer.txt', sep='\t', index=False)
        df.to_csv(f'dados_gerados'+versionador+'data_transfer.csv', index=False)

        # Export the data that will be compiled
        data = pd.read_csv('dados_gerados'+versionador+'data_transfer.txt', delimiter="\t")

    # Group by the relevant columns and remove the columns that do not make sense
    data_2 = data.groupby(["Type", "Electrolyte", "Measure", "Sweep"], as_index=False).agg(['mean', 'std'])
    data_2 = data_2.drop(["Chip", "Disp"], axis=1, level=0)

    # Reset the index
    new_dataframe = data_2.reset_index(drop=True)

    # Export dataframe into a .txt file
    new_dataframe.to_csv(f'dados_gerados'+versionador+'data_transfer_means.txt', sep='\t', index=False)
    new_dataframe.to_csv(f'dados_gerados'+versionador+'data_transfer_means.csv', index=False)

   
    
   
####################################################################FIM TRANSFER###################################################################################################


