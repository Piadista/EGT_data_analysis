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



#####################################################CRIA ARQUIVO ESTABILIDADE###########################################################################################################
# Create the file with compiled important data
def create_stability():
    df_Single = pd.DataFrame(columns=['Type','Chip','Disp', 'Electrolyte','Potential [V]', 'Pulse #', 'Polarization', 'IDSant (10sp 5sa) [A]', 'Std IDSant [A]',
                                        'IDSdur (10sp 15sa) [A]', 'Std IDSdur [A]', 'IDSdep (10sp 30sd) [A]', 'Std IDSdep [A]', 'delIDS [A]', 'Std del IDS [A]',
                                      'RatioIDS', 'Std RazIDS'])

    # Export dataframe into a .txt file
    df_Single.to_csv('data_Stability.txt', sep='\t', index=False)
####################################################################################################################################################################



##########################################################ESTABILIDADE##################################################################################################################

def analise_stability(nomes_pastas):

    create_stability()
    endurance = []

    l = 0
    for caminhos in nomes_pastas:
        if ("Estabilidade/Endurance") in caminhos:
            # df_arquivo = pd.read_csv(caminhos, sep='\t')
            endurance.append(caminhos)
            l = l + 1

    l = 0


    for elemento in endurance:
        l = l + 1
        k = 0

        # Name of the folder and file name where the data is and use it as a pandas dataframe
        folder = elemento

        tipo_chip = get_type(elemento)
        valor_chip = get_chip(elemento)
        valor_disp = get_disp(elemento)
        tipo_eletrolito = get_eletrolito(elemento)
        valor_potencial = get_potential(elemento)



        pre = 'Stability ('
        suf = ').txt'

        # Append the dictionary to the DataFrame previously created
        df_comp = pd.read_csv('data_Stability.txt', delimiter="\t")

        # Loop to take the mean current values previous and after each stimulus
        for i in range(0, 100):
            try:

                file_name = '/Stability (' + str(i) + ').txt'
                df = pd.read_csv(folder + file_name, delimiter="\t")
                IDSant = (df[(df["Timestamp (s)"] >= 15) & (df["Timestamp (s)"] <= 25)])['Current SMUb (A)'].mean()
                Std_IDSant = (df[(df["Timestamp (s)"] >= 15) & (df["Timestamp (s)"] <= 25)])['Current SMUb (A)'].std()
                IDSdur = (df[(df["Timestamp (s)"] >= 45) & (df["Timestamp (s)"] <= 55)])['Current SMUb (A)'].mean()
                Std_IDSdur = (df[(df["Timestamp (s)"] >= 45) & (df["Timestamp (s)"] <= 55)])['Current SMUb (A)'].std()
                IDSdep = (df[(df["Timestamp (s)"] >= 100) & (df["Timestamp (s)"] <= 110)])['Current SMUb (A)'].mean()
                Std_IDSdep = (df[(df["Timestamp (s)"] >= 100) & (df["Timestamp (s)"] <= 110)])['Current SMUb (A)'].std()
                delIDS = IDSdep - IDSant
                Std_delIDS = sqrt(Std_IDSant ** 2 + Std_IDSdep ** 2)
                RazIDS = IDSdep / IDSant
                Std_RazIDS = sqrt((Std_IDSdep / IDSant) ** 2 + (Std_IDSant ** 2) * (IDSdep / (IDSant) ** 2) ** 2)

                if i % 2 == 0:
                    pol = 'pos'
                if i % 2 == 1:
                    pol = 'neg'

                new_row = {'Type': tipo_chip, 'Chip': valor_chip, 'Disp': valor_disp, 'Electrolyte': tipo_eletrolito, 'Potential [V]': valor_potencial,
                           'Pulse #': (i + 1), 'Polarization': pol, 'IDSant (10sp 5sa) [A]': IDSant,
                           'Std IDSant [A]': Std_IDSant, 'IDSdur (10sp 15sa) [A]': IDSdur, 'Std IDSdur [A]': Std_IDSdur,
                           'IDSdep (10sp 30sd) [A]': IDSdep,
                           'Std IDSdep [A]': Std_IDSdep, 'delIDS [A]': delIDS, 'Std del IDS [A]': Std_delIDS,
                           'RatioIDS': RazIDS, 'Std RazIDS': Std_RazIDS}

                df_comp = pd.concat([df_comp, pd.DataFrame([new_row])], ignore_index=True)

            except:
                pass

        # Reset the index
        df_comp = df_comp.reset_index(drop=True)

        # Export dataframe into a .txt file
        df_comp.to_csv('data_Stability.txt', sep='\t', index=False)
        df_comp.to_csv('data_Stability.csv', index=False)



#########################################################FIM ESTABILIDADE################################################################################################################
