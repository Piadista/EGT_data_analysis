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


#################################################################CRIA ARQUIVO PPX######################################################################################################
def create_ppx():
    # Create the file with compiled important data
    df_PPX = pd.DataFrame(columns=['Type', 'Chip', 'Disp', 'Electrolyte', 'Potential [V]', 'Period [s]',
                                   'A1_first [A]', 'A2_first [A]', 'Rat_first', 'A1_last [A]', 'A2_last [A]',
                                   'Rat_last'])

    # Export dataframe into a .txt file
    df_PPX.to_csv('dados_gerados'+versionador+'data_PPX.txt', sep='\t', index=False)
########################################################################################################################################################################

##################################################################PPX###################################################################################################################
def analise_ppx(nomes_pastas):
    create_ppx()
    #Análise PPX
    pulsados = []

    l = 0
    for caminhos in nomes_pastas:
        if ('Pulsados'+versionador+'PPX') in caminhos:
            # df_arquivo = pd.read_csv(caminhos, sep='\t')
            pulsados.append(caminhos)
            l = l + 1

    l = 0

    for elemento in pulsados:
        l = l + 1

        # Name of the folder and file name where the data is and use it as a pandas dataframe
        folder = elemento

        pre = '100ms'
        mid = 'Pe'

        # Iterate over all files created by these PPX boot and take maximum and minimum values
        potentials = ['-0.5', '0.5', '-0.8', '0.8']
        period_values = ['2.1', '1.6', '1.1', '0.85', '0.6', '0.5', '0.3', '0.2', '0.18', '0.15', '0.14', '0.12', '0.11',
                         '0.105', '0.102', '0.101']
        suf = ['ms.txt', 'ms (1).txt', 'ms (2).txt', 'ms (3).txt']

        # Append the dictionary to the DataFrame previously created
        df_comp = pd.read_csv('dados_gerados'+versionador+'data_PPX.txt', delimiter="\t")

        tipo_chip = get_type(elemento)
        valor_chip = get_chip(elemento)
        valor_disp = get_disp(elemento)
        tipo_eletrolito = get_eletrolito(elemento)

        i = 0
        for s in suf:
            for v in period_values:
                file_name = pre + mid + str(int(float(v) * 1000)) + s
                df = pd.read_csv(folder + versionador + file_name, delimiter="\t")
                # ini_cur is used to calculate current variation to the peak
                ini_cur = (df[(df["Timestamp (s)"] > (1.0 + float(v) - 0.1 - 0.4)) & (
                            df["Timestamp (s)"] < (1.0 + float(v) - 0.1 - 0.1))])['Current SMUb (A)'].mean()
                # Note that for simplicity current before stimulus was used to find the current variation
                if(float(v) < 1.05):
                    df2 = df[(df["Timestamp (s)"] > (1 + float(v) + 0.002))]
                    df = df[(df["Timestamp (s)"] > (1 - 0.01)) & (df["Timestamp (s)"] <= (1.0 + float(v) + 0.002))]
                else:
                    df2 = df[(df["Timestamp (s)"] > (1 + float(v) + (float(v)-0.1)/2))]
                    df = df[(df["Timestamp (s)"] > (1 - 0.01)) & (df["Timestamp (s)"] <= (1.0 + float(v) + (float(v)-0.1)/2))]

                # first the maximum current and then the minimum (VGS < 0)
                if i % 2 == 0:
                    A1_first = df['Current SMUb (A)'].max() - ini_cur
                    A2_first = df2['Current SMUb (A)'].max() - ini_cur
                    A1_last = df['Current SMUb (A)'].min() - ini_cur
                    A2_last = df2['Current SMUb (A)'].min() - ini_cur
                    Rat_first = A2_first / A1_first
                    Rat_last = A2_last / A1_last

                # first the minimum current and then the maximum (VGS > 0)
                if i % 2 != 0:
                    A1_first = df['Current SMUb (A)'].min() - ini_cur
                    A2_first = df2['Current SMUb (A)'].min() - ini_cur
                    A1_last = df['Current SMUb (A)'].max() - ini_cur
                    A2_last = df2['Current SMUb (A)'].max() - ini_cur
                    Rat_first = A2_first / A1_first
                    Rat_last = A2_last / A1_last

                new_row = {'Type': tipo_chip, 'Chip': valor_chip, 'Disp': valor_disp, 'Electrolyte': tipo_eletrolito, 'Potential [V]': float(potentials[i]),
                           'Period [s]': float(v),
                           'A1_first [A]': A1_first, 'A2_first [A]': A2_first, 'Rat_first': Rat_first, 'A1_last [A]': A1_last,
                           'A2_last [A]': A2_last, 'Rat_last': Rat_last}
                df_comp = pd.concat([df_comp, pd.DataFrame([new_row])], ignore_index=True)

            i = i + 1

        # Reset the index
        df_comp = df_comp.reset_index(drop=True)

        # Export dataframe into a .txt file
        df_comp.to_csv('dados_gerados'+versionador+'data_PPX.txt', sep='\t', index=False)
        df_comp.to_csv('dados_gerados'+versionador+'data_PPX.csv', index = False)
        # Export the data that will be compiled
        data = pd.read_csv('dados_gerados'+versionador+'data_PPX.txt', delimiter="\t")

    # Group by the relevant columns and remove the columns that do not make sense
    data_2 = data.groupby(["Type","Electrolyte", "Potential [V]", "Period [s]"], as_index=False).agg(['mean', 'std'])
    data_2 = data_2.drop(["Chip", "Disp"], axis=1, level=0)

    # Reset the index
    new_dataframe = data_2.reset_index(drop=True)

    # Export dataframe into a .txt file
    new_dataframe.to_csv('dados_gerados'+versionador+'data_PPX_means.txt', sep='\t', index=False)
    new_dataframe.to_csv('dados_gerados'+versionador+'data_PPX_means.csv', index=False)

#####################################################################FIM PPX###########################################################################################################

