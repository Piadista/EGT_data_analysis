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
from function_long_pulse import *
from function_ppx import *
from function_multiple import *
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


###################################################CRIA ARQUIVO LGT_PULSED#############################################################################################################
def create_lgt_pulsed():
    # Create the file with compiled important data
    df_Resistor = pd.DataFrame(columns=['Type', 'Chip', 'Disp', 'Electrolyte', 'Width [s]', 'Interval [s]', 'Train pulses #', 'Resistor', 'Measure #',
                 'Polarization', 'IDSmed [A]', 'Std IDS [A]', 'delIDS [A]', 'Std delIDS [A]', 'Gn [S]', 'Std Gn [S]'])

    # Export dataframe into a .txt file
    df_Resistor.to_csv('dados_gerados'+versionador+'data_Resistor.txt', sep='\t', index=False)
#########################################################################################################################################################################


##############################################################LGT_PUlSED#################################################################################################################

def analise_lgt_pulsed(nomes_pastas):
    create_lgt_pulsed()
    lgt = []

    l = 0
    for caminhos in nomes_pastas:
        if ('Pulsados'+versionador+'LGT Pulsed') in caminhos:
            # df_arquivo = pd.read_csv(caminhos, sep='\t')
            lgt.append(caminhos)
            l = l + 1

    l = 0

    print("Estou rodando")
    for elemento in lgt:
        l = l + 1
        k = 0

        # Name of the folder and file name where the data is and use it as a pandas dataframe
        folder = elemento

        tipo_chip = get_type(elemento)
        valor_chip = get_chip(elemento)
        valor_disp = get_disp(elemento)
        tipo_eletrolito = get_eletrolito(elemento)

        file_list = []
        for file in os.listdir(folder):
            if file.endswith('.xlsx'):
                file = versionador + file
                file_list.append(file)
        # Append the dictionary to the DataFrame previously created
        df_comp = pd.read_csv('dados_gerados'+versionador+'data_Resistor.txt', delimiter="\t")

        file_list = sorted(file_list)

        au = 0
        for file_name in file_list:
            fin = file_name.find('#')
            ini = file_name.find('cycle') + 6
            file = file_name[ini:fin].split('p_100-')  # first element is the number of pulse and the second the interval in ms

            df = pd.read_excel(folder + file_name)
            df['diffVMeasCh1'] = df['VMeasCh1'].diff()
            df['Conductance2'] = df['IMeasCh2'] / df['VMeasCh2']

            # use this values to know when the stimulus change from 0 to their activated state
            times1 = (df[(abs(df['diffVMeasCh1']) > 0.04) & (abs(df['VMeasCh1']) < 0.04)])['TimeOutput'].tolist()
            times2 = (df[(abs(df['diffVMeasCh1']) > 0.04) & (abs(df['VMeasCh1']) > 0.04)])['TimeOutput'].tolist()
            times2 = times2[1:]

            for i in range(0, len(times1)):
                # calculate the mean and standard deviation of the normalized and swift condutctance
                if i == 0:
                    G0 = df[(df['TimeOutput'] > (times1[i] + 0.005)) & (df['TimeOutput'] < (times2[i] - 0.005))][
                        'Conductance2'].mean()
                    G = 0
                    Std_G = Std_G0 = df[(df['TimeOutput'] > (times1[i] + 0.005)) & (df['TimeOutput'] < (times2[i] - 0.005))][
                        'Conductance2'].std()
                if i != 0:
                    G = df[(df['TimeOutput'] > (times1[i] + 0.005)) & (df['TimeOutput'] < (times2[i] - 0.005))][
                            'Conductance2'].mean() - G0
                    Std_G = sqrt((df[(df['TimeOutput'] > (times1[i] + 0.005)) & (df['TimeOutput'] < (times2[i] - 0.005))][
                                      'Conductance2'].std()) ** 2 + Std_G0 ** 2)

                # calculate the mean and standard deviation of the current step from this state and the previous one
                if i != 0:
                    IDSpre = IDSmean
                    Std_IDSpre = Std_IDSmean

                IDSmean = df[(df['TimeOutput'] > (times1[i] + 0.005)) & (df['TimeOutput'] < (times2[i] - 0.005))][
                    'IMeasCh2'].mean()
                Std_IDSmean = df[(df['TimeOutput'] > (times1[i] + 0.005)) & (df['TimeOutput'] < (times2[i] - 0.005))][
                    'IMeasCh2'].std()

                if i == 0:
                    delIDS = 0
                    Std_delIDS = 0
                else:
                    delIDS = IDSmean - IDSpre
                    Std_delIDS = sqrt(Std_IDSmean ** 2 + Std_IDSpre ** 2)

                if int(i / int(file[0])) % 2 == 0:
                    pol = 'neg'
                else:
                    pol = 'pos'

                if au % 2 == 0:
                    res = 0
                else:
                    res = 1

                new_row = {'Type': tipo_chip, 'Chip': valor_chip, 'Disp': valor_disp, 'Electrolyte': tipo_eletrolito, 'Width [s]': 0.1,
                           'Interval [s]': float(file[1]) / 1000,
                           'Train pulses #': int(file[0]), 'Resistor': res, 'Measure #': (i + 1), 'Polarization': pol,
                           'IDSmed [A]': IDSmean,
                           'Std IDS [A]': Std_IDSmean, 'delIDS [A]': delIDS, 'Std delIDS [A]': Std_delIDS, 'Gn [S]': G,
                           'Std Gn [S]': Std_G}
                df_comp = pd.concat([df_comp, pd.DataFrame([new_row])], ignore_index=True)

            au = au + 1

        # Reset the index
        df_comp = df_comp.reset_index(drop=True)

        # Export dataframe into a .txt file
        df_comp.to_csv('dados_gerados'+versionador+'data_Resistor.txt', sep='\t', index=False)
        df_comp.to_csv('dados_gerados'+versionador+'data_Resistor.csv', index=False)


        # Export the data that will be compiled
        data = pd.read_csv('dados_gerados'+versionador+'data_Resistor.txt', delimiter="\t")

    # Group by the relevant columns and remove the columns that do not make sense
    data_2 = data.groupby(["Type","Electrolyte", "Width [s]", "Interval [s]", "Train pulses #", "Resistor", "Measure #", "Polarization"], as_index=False).agg(['mean', 'std'])
    data_2 = data_2.drop(["Chip", "Disp", "Std IDS [A]", "Std delIDS [A]", "Std Gn [S]"], axis=1, level=0)

    # Reset the index
    new_dataframe = data_2.reset_index(drop=True)

    # Export dataframe into a .txt file
    new_dataframe.to_csv('dados_gerados'+versionador+'data_Resistor_means.txt', sep='\t', index=False)
    new_dataframe.to_csv('dados_gerados'+versionador+'data_Resistor_means.csv', index=False)


################################################################FIM LGT_PULSED###########################################################################################################
