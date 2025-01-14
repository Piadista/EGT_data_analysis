
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

##############################################################FUNÇÕES AUXILIARES PULSO CURTO##########################################################################################
# Auxiliary function to return the values into the numpy array
def aux(vec, name):
    return vec[vec['name'] == name]['value'][0]


# Calculate the relevant parameters from stability short pulse curve
def short_pulse_sta_extractor_values(df_sta):
    # Calculate the current during stability test
    df_sta = df_sta[(df_sta["Timestamp (s)"] >= 10.0) & (df_sta["Timestamp (s)"] <= 160)]
    meanIDS = df_sta['Current SMUb (A)'].mean()
    values = np.array([('meanIDS', meanIDS)], dtype=[('name', 'U20'), ('value', 'f8')])
    stdIDS = df_sta['Current SMUb (A)'].std()
    values = np.append(values, np.array([('stdIDS', stdIDS)], dtype=values.dtype))
    meanIGS = df_sta['Current SMUA (A)'].mean()
    values = np.append(values, np.array([('meanIGS', meanIGS)], dtype=values.dtype))
    stdIGS = df_sta['Current SMUA (A)'].std()
    values = np.append(values, np.array([('stdIGS', stdIGS)], dtype=values.dtype))
    return values


# Auxiliary function to calculate parameter for both positive and negative functions
def pola_values_calc(df):
    values = np.array([])
    IDS_ant = aux = (df[(df["Timestamp (s)"] >= 35) & (df["Timestamp (s)"] <= 50)])['Current SMUb (A)'].mean()
    values = np.append(values, aux)
    std_IDS_ant = aux = (df[(df["Timestamp (s)"] >= 35) & (df["Timestamp (s)"] <= 50)])['Current SMUb (A)'].std()
    values = np.append(values, aux)
    IDS_dep = aux = (df[(df["Timestamp (s)"] >= 150) & (df["Timestamp (s)"] <= 165)])['Current SMUb (A)'].mean()
    values = np.append(values, aux)
    std_IDS_dep = aux = (df[(df["Timestamp (s)"] >= 150) & (df["Timestamp (s)"] <= 165)])['Current SMUb (A)'].std()
    values = np.append(values, aux)
    aux = IDS_dep - IDS_ant
    values = np.append(values, aux)
    aux = sqrt(std_IDS_ant ** 2 + std_IDS_dep ** 2)
    values = np.append(values, aux)

    IGS_ant = aux = (df[(df["Timestamp (s)"] >= 35) & (df["Timestamp (s)"] <= 50)])['Current SMUA (A)'].mean()
    values = np.append(values, aux)
    std_IGS_ant = aux = (df[(df["Timestamp (s)"] >= 35) & (df["Timestamp (s)"] <= 50)])['Current SMUA (A)'].std()
    values = np.append(values, aux)
    IGS_dep = aux = (df[(df["Timestamp (s)"] >= 150) & (df["Timestamp (s)"] <= 165)])['Current SMUA (A)'].mean()
    values = np.append(values, aux)
    std_IGS_dep = aux = (df[(df["Timestamp (s)"] >= 150) & (df["Timestamp (s)"] <= 165)])['Current SMUA (A)'].std()
    values = np.append(values, aux)
    aux = IGS_dep - IGS_ant
    values = np.append(values, aux)
    aux = sqrt(std_IGS_ant ** 2 + std_IGS_dep ** 2)
    values = np.append(values, aux)
    # Mean current during VGS != 0V. When the device is on
    aux = (df[(df["Timestamp (s)"] >= 75) & (df["Timestamp (s)"] <= 85)])['Current SMUA (A)'].mean()
    values = np.append(values, aux)
    aux = (df[(df["Timestamp (s)"] >= 75) & (df["Timestamp (s)"] <= 85)])['Current SMUA (A)'].std()
    values = np.append(values, aux)

    return values


# Calculate the relevant parameters from positive short pulse curve (now it is easier to make more modulable, but still not really good)
def short_pulse__extractor_values(df, name):
    # Call the function to calculate the mean and std Values
    aux = pola_values_calc(df)

    # IDS values
    values = np.array([('IDS_ant_' + name, aux[0])], dtype=[('name', 'U20'), ('value', 'f8')])
    values = np.append(values, np.array([('stdIDS_ant_' + name, aux[1])], dtype=values.dtype))
    values = np.append(values, np.array([('IDS_dep_' + name, aux[2])], dtype=values.dtype))
    values = np.append(values, np.array([('stdIDS_dep_' + name, aux[3])], dtype=values.dtype))
    values = np.append(values, np.array([('IDS_del_' + name, aux[4])], dtype=values.dtype))
    values = np.append(values, np.array([('stdIDS_del_' + name, aux[5])], dtype=values.dtype))

    # IGS values
    values = np.append(values, np.array([('IGS_ant_' + name, aux[6])], dtype=values.dtype))
    values = np.append(values, np.array([('stdIGS_ant_' + name, aux[7])], dtype=values.dtype))
    values = np.append(values, np.array([('IGS_dep_' + name, aux[8])], dtype=values.dtype))
    values = np.append(values, np.array([('stdIGS_dep_' + name, aux[9])], dtype=values.dtype))
    values = np.append(values, np.array([('IGS_del_' + name, aux[10])], dtype=values.dtype))
    values = np.append(values, np.array([('stdIGS_del_' + name, aux[11])], dtype=values.dtype))
    values = np.append(values, np.array([('IGS_dur_' + name, aux[12])], dtype=values.dtype))
    values = np.append(values, np.array([('stdIGS_dur_' + name, aux[13])], dtype=values.dtype))

    if name == 'pos':
        values = np.append(values,
                           np.array([('IGS_pic_ant_' + name, df['Current SMUA (A)'].max())], dtype=values.dtype))
        values = np.append(values,
                           np.array([('IGS_pic_dep_' + name, df['Current SMUA (A)'].min())], dtype=values.dtype))

    if name == 'neg':

        values = np.append(values,
                           np.array([('IGS_pic_ant_' + name, df['Current SMUA (A)'].min())], dtype=values.dtype))
        values = np.append(values,
                           np.array([('IGS_pic_dep_' + name, df['Current SMUA (A)'].max())], dtype=values.dtype))

    return values

################################################################FIM FUNÇÕES AUXILIARES PULSO CURTO########################################################################################


############################################################CRIA O ARQUIVO PULSO CURTO#################################################################################################
# Create the file with compiled important data
def create_short_pulse():
    df_short = pd.DataFrame(columns=['Type','Chip','Disp', 'Electrolyte', 'IDSmed (10s - 160s) [A]', 'Std IDSmed [A]', 'IGSmed (10s - 160s) [A]',
                                    'Std IGSmed [A]', 'IDSant_pos (35s - 50s) [A]', 'Std IDSant_pos [A]', 'IDSdep_pos (150s - 165s) [A]', 'Std IDSdep_pos [A]',
                                    'delIDS_pos [A]', 'Std delIDS_pos [A]', 'IGSant_pos (35s - 50s) [A]', 'Std IGSant_pos [A]', 'IGSdur_pos (75s - 85s) [A]',
                                    'Std IGSdur_pos [A]','IGSdep_pos (150s - 165s) [A]', 'Std IGSdep_pos [A]', 'delIGS_pos [A]', 'Std delIGS_pos [A]',
                                    'IGS_pico_ant_pos [A]', 'IGS_pico_dep_pos [A]', 'IDSant_neg (35s - 50s) [A]', 'Std IDSant_neg [A]', 'IDSdep_neg (150s - 165s) [A]',
                                    'Std IDSdep_neg [A]', 'delIDS_neg [A]', 'Std delIDS_neg [A]', 'IGSant_neg (35s - 50s) [A]', 'Std IGSant_neg [A]',
                                    'IGSdur_neg (75s - 85s) [A]', 'Std IGSdur_neg [A]','IGSdep_neg (150s - 165s) [A]', 'Std IGSdep_neg [A]', 'delIGS_neg [A]',
                                    'Std delIGS_neg [A]', 'IGS_pico_ant_neg [A]', 'IGS_pico_dep_neg [A]'])


    # Export dataframe into a .txt file
    df_short.to_csv('dados_gerados'+versionador+'data_short_pulses.txt', sep='\t', index=False)
########################################################################################################################################################################


###################################################################PULSO CURTO######################################################################################################

def analise_short_pulse(nomes_arquivos):
    #Analise Pulso Curto
    create_short_pulse()
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
                values_short = short_pulse_sta_extractor_values(df_sta)
                pulsos.append(elemento)
                tipo_chip = get_type(elemento)
                valor_chip = get_chip(elemento)
                valor_disp = get_disp(elemento)
                tipo_eletrolito = get_eletrolito(elemento)

            elif '152pulsonegativo' in elemento:
                df_neg = pd.read_csv(elemento, delimiter="\t")
                # Relevant parameters negative
                values_neg = short_pulse__extractor_values(df_neg, 'neg')
                pulsos.append(elemento)
                tipo_chip = get_type(elemento)
                valor_chip = get_chip(elemento)
                valor_disp = get_disp(elemento)
                tipo_eletrolito = get_eletrolito(elemento)

            elif '151pulsopositivo' in elemento:
                df_pos = pd.read_csv(elemento, delimiter="\t")
                # Relevant parameters positive
                values_pos = short_pulse__extractor_values(df_pos, 'pos')
                pulsos.append(elemento)
                tipo_chip = get_type(elemento)
                valor_chip = get_chip(elemento)
                valor_disp = get_disp(elemento)
                tipo_eletrolito = get_eletrolito(elemento)


        # Create a dictionary with the data for the new row
        new_row = {'Type': tipo_chip,'Chip': valor_chip,'Disp': valor_disp, 'Electrolyte': tipo_eletrolito, 'IDSmed (10s - 160s) [A]': aux(values_short, 'meanIDS'), 'Std IDSmed [A]': aux(values_short, 'stdIDS'),
                   'IGSmed (10s - 160s) [A]': aux(values_short, 'meanIGS'), 'Std IGSmed [A]': aux(values_short, 'stdIGS'), 'IDSant_pos (35s - 50s) [A]': aux(values_pos, 'IDS_ant_pos'),
                   'Std IDSant_pos [A]': aux(values_pos, 'stdIDS_ant_pos'), 'IDSdep_pos (150s - 165s) [A]': aux(values_pos, 'IDS_dep_pos'),
                   'Std IDSdep_pos [A]': aux(values_pos, 'stdIDS_dep_pos'), 'delIDS_pos [A]': aux(values_pos, 'IDS_del_pos'), 'Std delIDS_pos [A]': aux(values_pos, 'stdIDS_del_pos'),
                   'IGSant_pos (35s - 50s) [A]': aux(values_pos, 'IGS_ant_pos'), 'Std IGSant_pos [A]': aux(values_pos, 'stdIGS_ant_pos'),
                   'IGSdur_pos (75s - 85s) [A]': aux(values_pos, 'IGS_dur_pos'), 'Std IGSdur_pos [A]': aux(values_pos, 'stdIGS_dur_pos'),
                   'IGSdep_pos (150s - 165s) [A]': aux(values_pos, 'IGS_dep_pos'), 'Std IGSdep_pos [A]': aux(values_pos, 'stdIGS_dep_pos'),
                   'delIGS_pos [A]': aux(values_pos, 'IGS_del_pos'), 'Std delIGS_pos [A]': aux(values_pos, 'stdIGS_del_pos'), 'IGS_pico_ant_pos [A]': aux(values_pos, 'IGS_pic_ant_pos'),
                   'IGS_pico_dep_pos [A]': aux(values_pos, 'IGS_pic_dep_pos'), 'IDSant_neg (35s - 50s) [A]': aux(values_neg, 'IDS_ant_neg'), 'Std IDSant_neg [A]': aux(values_neg, 'stdIDS_ant_neg'),
                   'IDSdep_neg (150s - 165s) [A]': aux(values_neg, 'IDS_dep_neg'), 'Std IDSdep_neg [A]': aux(values_neg, 'stdIDS_dep_neg'),
                   'delIDS_neg [A]': aux(values_neg, 'IDS_del_neg'), 'Std delIDS_neg [A]': aux(values_neg, 'stdIDS_del_neg'), 'IGSant_neg (35s - 50s) [A]': aux(values_neg, 'IGS_ant_neg'),
                   'Std IGSant_neg [A]': aux(values_neg, 'stdIGS_ant_neg'), 'IGSdur_neg (75s - 85s) [A]': aux(values_neg, 'IGS_dur_neg'), 'Std IGSdur_neg [A]': aux(values_neg, 'stdIGS_dur_neg'),
                   'IGSdep_neg (150s - 165s) [A]': aux(values_neg, 'IGS_dep_neg'), 'Std IGSdep_neg [A]': aux(values_neg, 'stdIGS_dep_neg'), 'delIGS_neg [A]': aux(values_neg, 'IGS_del_neg'),
                   'Std delIGS_neg [A]': aux(values_neg, 'stdIGS_del_neg'), 'IGS_pico_ant_neg [A]': aux(values_neg, 'IGS_pic_ant_neg'), 'IGS_pico_dep_neg [A]': aux(values_neg, 'IGS_pic_dep_neg')}

        # Append the dictionary to the DataFrame previously created
        df = pd.read_csv('dados_gerados'+versionador+'data_short_pulses.txt', delimiter="\t")
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        # Reset the index
        df = df.reset_index(drop=True)

        # Export dataframe into a .txt file
        df.to_csv('dados_gerados'+versionador+'data_short_pulses.txt', sep='\t', index=False)
        df.to_csv('dados_gerados'+versionador+'data_short_pulses.csv', index = False)


        pulsos = []
        del pulso_curto[0:3]

    # Export the data that will be compiled
    data = pd.read_csv('dados_gerados'+versionador+'data_short_pulses.txt', delimiter="\t")

    # Group by the relevant columns and remove the columns that do not make sense
    data_2 = data.groupby(["Type","Electrolyte"], as_index=False).agg(['mean', 'std'])
    data_2 = data_2.drop(["Chip", "Disp", "Std IDSmed [A]", "Std IGSmed [A]", "Std IDSant_pos [A]", "Std IDSdep_pos [A]", "Std delIDS_pos [A]",
                          "Std IGSant_pos [A]", "Std IGSdur_pos [A]", "Std IGSdep_pos [A]", "Std delIGS_pos [A]", "Std IDSant_neg [A]", "Std IDSdep_neg [A]",
                          "Std delIDS_neg [A]", "Std IGSant_neg [A]", "Std IGSdur_neg [A]", "Std IGSdep_neg [A]", "Std delIGS_neg [A]"] , axis=1, level=0)

    # Reset the index
    new_dataframe = data_2.reset_index(drop=True)

    # Export dataframe into a .txt file
    new_dataframe.to_csv('dados_gerados'+versionador+'data_short_pulses_means.txt', sep='\t', index=False)
    new_dataframe.to_csv('dados_gerados'+versionador+'data_short_pulses_means.csv', index=False)


######################################################################FIM PULSO CURTO###############################################################################################
