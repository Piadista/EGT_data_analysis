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
from function_stability import *
from function_decaimento import *
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


#############################################################DECAIMENTO#################################################################################################################
def create_decaimento():
    # Create the file with compiled important data
    df_Single = pd.DataFrame(
        columns=['Type', 'Chip', 'Disp', 'Electrolyte', 'Potential [V]', 'Width [s]', 'VDS [V]', 'IDSant (5sp 1sa) [A]',
                 'Std IDSant [A]',
                 'IDSdep (5sp 10sd) [A]', 'Std IDSdep [A]', 'delIDS [A]', 'Std del IDS [A]', 'RatioIDS', 'Std RazIDS'])

    # Export dataframe into a .txt file
    df_Single.to_csv('dados_gerados'+versionador+'data_Single.txt', sep='\t', index=False)
##########################################################################################################################################################################################


def analise_decaimento(nomes_pastas):
    create_decaimento()
    singlepulse = []

    l = 0
    for caminhos in nomes_pastas:
        if ('Decaimento'+versionador+'Single Pulse') in caminhos:
            # df_arquivo = pd.read_csv(caminhos, sep='\t')
            singlepulse.append(caminhos)
            l = l + 1

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

        pre = 'Single ('
        suf = ').txt'

        # Iterate over all files created by these Single_pulse boot and take maximum and minimum values
        vds = ['0.1', '0.05', '0.2', '0.4']
        widths = ['0.01', '0.1', '1', '10', '40']
        potentials = ['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8']

        # Append the dictionary to the DataFrame previously created
        df_comp = pd.read_csv('dados_gerados'+versionador+'data_Single.txt', delimiter="\t")

        i = 0
        # Loop to take the mean current values previous and after each stimulus
        for v_d in vds:
            for t_1 in widths:
                for v_g in potentials:
                    # Measure with both polarities
                    if (float(v_g) + float(v_d)) < 1.0:
                        for x in [1, -1]:
                            file_name = versionador+'Single (' + str(i) + ').txt'
                            df = pd.read_csv(folder + file_name, delimiter="\t")

                            IDSant = (df[(df["Timestamp (s)"] >= 10) & (df["Timestamp (s)"] <= 15)])[
                                'Current SMUb (A)'].mean()
                            Std_IDSant = (df[(df["Timestamp (s)"] >= 10) & (df["Timestamp (s)"] <= 15)])[
                                'Current SMUb (A)'].std()
                            IDSdep = (df[(df["Timestamp (s)"] >= (15 + 1 + float(t_1) + 10)) & (
                                        df["Timestamp (s)"] <= (15 + 1 + float(t_1) + 10 + 5))])['Current SMUb (A)'].mean()
                            Std_IDSdep = (df[(df["Timestamp (s)"] >= (15 + 1 + float(t_1) + 10)) & (
                                        df["Timestamp (s)"] <= (15 + 1 + float(t_1) + 10 + 5))])['Current SMUb (A)'].std()
                            delIDS = IDSdep - IDSant
                            Std_delIDS = sqrt(Std_IDSant ** 2 + Std_IDSdep ** 2)
                            RazIDS = IDSdep / IDSant
                            Std_RazIDS = sqrt(
                                (Std_IDSdep / IDSant) ** 2 + (Std_IDSant ** 2) * (IDSdep / (IDSant) ** 2) ** 2)

                            new_row = {'Type': tipo_chip, 'Chip': valor_chip, 'Disp': valor_disp, 'Electrolyte': tipo_eletrolito,
                                       'Potential [V]': (float(v_g) * x), 'Width [s]': float(t_1), 'VDS [V]': float(v_d),
                                       'IDSant (5sp 1sa) [A]': IDSant, 'Std IDSant [A]': Std_IDSant,
                                       'IDSdep (5sp 10sd) [A]': IDSdep, 'Std IDSdep [A]': Std_IDSdep,
                                       'delIDS [A]': delIDS, 'Std del IDS [A]': Std_delIDS, 'RatioIDS': RazIDS,
                                       'Std RazIDS': Std_RazIDS}

                            df_comp = pd.concat([df_comp, pd.DataFrame([new_row])], ignore_index=True)

                            i = i + 1

        # Reset the index
        df_comp = df_comp.reset_index(drop=True)

        # Export dataframe into a .txt file
        df_comp.to_csv('dados_gerados'+versionador+'data_Single.txt', sep='\t', index=False)
        df_comp.to_csv('dados_gerados'+versionador+'data_Single.csv', index=False)

        # Export the data that will be compiled
        data = pd.read_csv('dados_gerados'+versionador+'data_Single.txt', delimiter="\t")

    # Group by the relevant columns and remove the columns that do not make sense
    data_2 = data.groupby(["Type", "Electrolyte", "Potential [V]", "Width [s]", "VDS [V]"], as_index=False).agg(
        ['mean', 'std'])
    data_2 = data_2.drop(["Chip", "Disp", "Std IDSant [A]", "Std IDSdep [A]", "Std del IDS [A]", "Std RazIDS"], axis=1,
                         level=0)

    # Reset the index
    new_dataframe = data_2.reset_index(drop=True)

    # Export dataframe into a .txt file
    new_dataframe.to_csv('dados_gerados'+versionador+'data_Single_means.txt', sep='\t', index=False)
    new_dataframe.to_csv('dados_gerados'+versionador+'data_Single_means.csv', index=False)



##########################################################FIM DECAIMENTO################################################################################################################
