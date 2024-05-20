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


#########################################################CRIA ARQUIVO MULTIPLE#########################################################################################################
def create_multiple():
    # Create the file with compiled important data
    df_Multiple = pd.DataFrame(
        columns=['Type', 'Chip', 'Disp', 'Electrolyte', 'Potential [V]', 'Period [s]', 'Pulses #', 'IDSant (2-3s) [A]',
                 'Std IDSant [A]',
                 'IDSdep (+3, +4s) [A]', 'Std IDSdep [A]', 'delIDS [A]', 'Std del IDS [A]', 'RatioIDS', 'Std RazIDS'])

    # Export dataframe into a .txt file
    df_Multiple.to_csv('data_Multiple.txt', sep='\t', index=False)
########################################################################################################################################################################


####################################################################MULTIPLE###########################################################################################################

def analise_multiple(nomes_pastas):
    create_multiple()
    multiple = []

    l = 0
    for caminhos in nomes_pastas:
        if ("Pulsados/Multiple") in caminhos:
            # df_arquivo = pd.read_csv(caminhos, sep='\t')
            multiple.append(caminhos)
            l = l + 1

    l = 0


    for elemento in multiple:
        l = l + 1
        k = 0

        # Name of the folder and file name where the data is and use it as a pandas dataframe
        folder = elemento

        mid = '100msPe'

        # Iterate over all files created by these PPX boot and take maximum and minimum values
        period_values = ['0.25', '0.15', '0.125', '0.11', '0.105']
        n_pulses = ['10', '20', '50']
        potentials = ['-0.5', '0.5', '-0.8', '0.8']

        suf = ['ms.txt', 'ms (1).txt', 'ms (2).txt', 'ms (3).txt']

        # Append the dictionary to the DataFrame previously created
        df_comp = pd.read_csv('data_Multiple.txt', delimiter="\t")

        tipo_chip = get_type(elemento)
        valor_chip = get_chip(elemento)
        valor_disp = get_disp(elemento)
        tipo_eletrolito = get_eletrolito(elemento)
        i = 0
        for s in suf:
            for n in n_pulses:
                for v in period_values:
                    file_name = n + 'p' + mid + str(int(float(v) * 1000)) + s
                    df = pd.read_csv(folder + '/' + file_name, delimiter="\t")

                    IDSant = (df[(df["Timestamp (s)"] >= 2) & (df["Timestamp (s)"] <= 3)])['Current SMUb (A)'].mean()
                    Std_IDSant = (df[(df["Timestamp (s)"] >= 2) & (df["Timestamp (s)"] <= 3)])['Current SMUb (A)'].std()
                    IDSdep = (df[(df["Timestamp (s)"] >= (3 + int(n) * float(v) + 3)) & (
                                df["Timestamp (s)"] <= (3 + int(n) * float(v) + 4))])['Current SMUb (A)'].mean()
                    Std_IDSdep = (df[(df["Timestamp (s)"] >= (3 + int(n) * float(v) + 3)) & (
                                df["Timestamp (s)"] <= (3 + int(n) * float(v) + 4))])['Current SMUb (A)'].std()
                    delIDS = IDSdep - IDSant
                    Std_delIDS = sqrt(Std_IDSant ** 2 + Std_IDSdep ** 2)
                    RazIDS = IDSdep / IDSant
                    Std_RazIDS = sqrt((Std_IDSdep / IDSant) ** 2 + (Std_IDSant ** 2) * (IDSdep / (IDSant) ** 2) ** 2)

                    new_row = {'Type': tipo_chip, 'Chip': valor_chip, 'Disp': valor_disp, 'Electrolyte': tipo_eletrolito,
                               'Potential [V]': float(potentials[i]), 'Period [s]': float(v), 'Pulses #': int(n),
                               'IDSant (2-3s) [A]': IDSant, 'Std IDSant [A]': Std_IDSant, 'IDSdep (+3, +4s) [A]': IDSdep,
                               'Std IDSdep [A]': Std_IDSdep,
                               'delIDS [A]': delIDS, 'Std del IDS [A]': Std_delIDS, 'RatioIDS': RazIDS,
                               'Std RazIDS': Std_RazIDS}
                    df_comp = pd.concat([df_comp, pd.DataFrame([new_row])], ignore_index=True)

            i = i + 1

        # Reset the index
        df_comp = df_comp.reset_index(drop=True)

        # Export dataframe into a .txt file
        df_comp.to_csv('data_Multiple.txt', sep='\t', index=False)
        df_comp.to_csv('data_Multiple.csv', index=False)


        # Export the data that will be compiled
        data = pd.read_csv('data_Multiple.txt', delimiter="\t")

    # Group by the relevant columns and remove the columns that do not make sense
    data_2 = data.groupby(["Type","Electrolyte", "Potential [V]", "Period [s]", "Pulses #"], as_index=False).agg(['mean', 'std'])
    data_2 = data_2.drop(["Chip", "Disp", "Std IDSant [A]", "Std IDSdep [A]", "Std del IDS [A]", "Std RazIDS"], axis=1, level=0)

    # Reset the index
    new_dataframe = data_2.reset_index(drop=True)

    # Export dataframe into a .txt file
    new_dataframe.to_csv('data_Multiple_means.txt', sep='\t', index=False)
    new_dataframe.to_csv('data_Multiple_means.csv', index=False)


#################################################################FIM MULTIPLE###########################################################################################################
