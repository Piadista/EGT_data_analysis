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
from function_lgt_pulsed import *
from function_transfer_stability import *
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

#################################################CRIA ARQUIVO TRANSFERÊNCIA ESTABILIDADE#################################################################################################
def create_transfer_stability():
    # Create the file with compiled important data
    df_transfer_estabilidade = pd.DataFrame(columns=['Type','Chip','Disp', 'Electrolyte','Measure','Sweep','VGSmin [V]',
                                          'IDSmin [A]', 'IDSmax [A]','Ronoff', 'Res [ohm]', 'IDS(-0.6V) [A]', 'IDS(+0.6V) [A]',
                                         'VGS min |gm| [V]','min |gm| [S]', 'VGS min gm [V]','min gm [S]', 'VGS max gm [V]', 'max gm [S]'])

    # Export dataframe into a .txt file
    df_transfer_estabilidade.to_csv('dados_gerados'+versionador+'data_transfer_endurance.txt', sep='\t', index=False)
#########################################################################################################################################################################

######################################################TRANSFERÊNCIA ESTABILIDADE########################################################################################################
def analise_transfer_stability(nomes_arquivos):
    # Analise Transfer
    create_transfer_stability()
    transfers_estabilidade = []

    i = 0
    for caminhos in nomes_arquivos:
        if ("410transfer") in caminhos and caminhos.endswith('.txt'):
            # df_arquivo = pd.read_csv(caminhos, sep='\t')
            transfers_estabilidade.append(caminhos)
            i = i + 1

    k = 0
    i = 0
    controle = []

    for elemento in transfers_estabilidade:
        i = i + 1

        data = pd.read_csv(elemento, sep="\t")



        df = pd.read_csv('dados_gerados'+versionador+'data_transfer_endurance.txt', delimiter="\t")

        # Correct first column of cycles (Monstro software subscribe wrongly some values)
        df_cor1 = correct_cycle_column(data)

        tipo_chip = get_type(elemento)
        valor_chip = get_chip(elemento)
        valor_disp = get_disp(elemento)
        tipo_eletrolito = get_eletrolito(elemento)
        tipo_measure = get_measure(elemento)

        for i in range(0, 200):
            # Calculate relevant parameters and choose the appropriate data
            sweep = float(int(float(i) / 2))
            df_c = df_cor1[df_cor1["Cycle #"] == sweep]
            if i % 2 == 0:
                df_c = df_c.drop_duplicates(subset=['V'])
            if i % 2 == 1:
                df_c = df_c.drop_duplicates(subset=['V'], keep='last')

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

            # Create a dictionary with the data for the new row
            new_row = {'Type': tipo_chip, 'Chip': valor_chip, 'Disp': valor_disp, 'Electrolyte': tipo_eletrolito, 'Measure': tipo_measure, 'Sweep': int(sweep),
                       'VGSmin [V]': VGSMIN, 'IDSmin [A]': IDSMIN,
                       'IDSmax [A]': IDSMAX, 'Ronoff': RAZAO, 'Res [ohm]': RES, 'IDS(-0.6V) [A]': IDSN,
                       'IDS(+0.6V) [A]': IDSP,
                       'VGS min |gm| [V]': VGS_GM_MOD_MIN, 'min |gm| [S]': GM_MOD_MIN, 'VGS min gm [V]': VGS_GM_MIN,
                       'min gm [S]': GM_MIN, 'VGS max gm [V]': VGS_GM_MAX, 'max gm [S]': GM_MAX}

            # Append the dictionary to the DataFrame previously created
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        # Reset the index
        df = df.reset_index(drop=True)

        # Export dataframe into a .txt file
        df.to_csv('dados_gerados'+versionador+'data_transfer_endurance.txt', sep='\t', index=False)
        df.to_csv('dados_gerados'+versionador+'data_transfer_endurance.csv', index=False)

    df_arrumar = pd.read_csv('dados_gerados'+versionador+'data_transfer_endurance.txt', sep="\t")
    for i in range(0, len(df_arrumar) // 200):
        # Calculate relevant parameters and choose the appropriate data
        for j in range(0 + (200 * i), 200 + (200 * i)):
            if j >= 200:
                k = j - 200 * i
            else:
                k = j
            nome_novo = f'{k}'
            df_arrumar.at[j, "Sweep"] = nome_novo

    # Export dataframe into a .txt file
    df_arrumar.to_csv('dados_gerados'+versionador+'data_transfer_endurance.txt', sep='\t', index=False)
    df_arrumar.to_csv('dados_gerados'+versionador+'data_transfer_endurance.csv', index=False)

    # Export the data that will be compiled
    data = pd.read_csv('dados_gerados'+versionador+'data_transfer_endurance.txt', delimiter="\t")

    # Group by the relevant columns and remove the columns that do not make sense calculate the mean and std
    data_2 = data.groupby(["Type", "Electrolyte", "Measure", "Sweep"], as_index=False).agg(['mean', 'std'])
    data_2 = data_2.drop(["Chip", "Disp"], axis=1, level=0)

    # Reset the index
    new_dataframe = data_2.reset_index(drop=True)

    # Export dataframe into a .txt file
    new_dataframe.to_csv('dados_gerados'+versionador+'data_transfer_endurance_means.txt', sep='\t', index=False)
    new_dataframe.to_csv('dados_gerados'+versionador+'data_transfer_endurance_means.csv', index=False)



    ###########################################################FIM TRANSFERÊNCIA ESTABILIDADE###############################################################################################
