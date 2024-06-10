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



###############################################################FUNÇÕES AUXILIARES PULSO LONGO############################################################################################

# Auxiliary functions

# Correct timestamp values to allow values greather than the buffer size
def cor_timestamp(df):
    aux1 = df['Timestamp (s)'].max()
    ind = df['Timestamp (s)'].idxmax()
    aux2 = df['Timestamp (s)'][ind + 1]
    aux = aux1 + 0.1 - aux2

    # Correct the values of column timestamp, after a period they turn to 0 because of the size of the buffer => slow because is not vectorized but it is ok
    for i in range(0, df['Timestamp (s)'].size):
        if i > ind:
            df['Timestamp (s)'][i] = df['Timestamp (s)'][i] + aux

    return df


# Function to find the mean and standard deviation values of current in a interval time
def find_current_mean(df, ini, end, column):
    df = df[(df["Timestamp (s)"] >= ini) & (df["Timestamp (s)"] <= end)]
    return (df[column].mean()), (df[column].std())


# Defina a função exponencial
def exp(x, a, b, c):
    return a * np.exp(-b * x) + c

def exp_fit(df, ini, fin):
    df = df[(df["Timestamp (s)"] >= ini) & (df["Timestamp (s)"] <= fin)]
    # Trying a trick to turn the current at the same magnitude of the value of the constant time, artificial, but maybe is enough for the parameters
    x0 = df["Timestamp (s)"][df["Timestamp (s)"].index[0]]
    x = df["Timestamp (s)"].to_numpy()
    x = x - x0
    y = df["Current SMUb (A)"]
    y = y * 10 ** 6

    # Aware, trick to overcome issue about the convergence of fit data in a large range
    if fin - ini > 500:
        popt, pcov = curve_fit(exp, x, y, p0=[3e+00, 2e-03, 10], maxfev=4000)
    else:
        popt, pcov = curve_fit(exp, x, y, p0=[1e+00, 2e-1, 10],maxfev=4000)
    perr = np.sqrt(np.diag(pcov))

    # residual sum of squares
    ss_res = np.sum((y - exp(x, *popt)) ** 2)
    # total sum of squares
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    # r-squared
    r2 = 1 - (ss_res / ss_tot)
    
    # Return a, std_a, const_time, std_const_time, c, std_c, r2, with I(t) = a*exp(-t/const_time) + c
    return popt[0], perr[0], 1 / popt[1], (perr[1] / popt[1] ** 2), popt[2], perr[2], r2,x0


# Find the relevant parameters for the linear adjust
def linear_fit(df, ini, fin):
    df = df[(df['Timestamp (s)'] > ini) & (df['Timestamp (s)'] < fin)]

    x = df["Timestamp (s)"].to_numpy()
    y = df["Current SMUb (A)"]
    y = y * 10 ** 6

    res = stats.linregress(x, y)
    return res.slope, res.stderr, (res.rvalue ** 2)

##################################################################FIM FUNÇÕES AXULIARES PULSO LONGO####################################################################################


##############################################################CRIA ARQUIVO PULSO LONGO##################################################################################################

def create_long_pulse():
    # Create the file with compiled important data
    df_long = pd.DataFrame(columns=['Type','Chip','Disp', 'Electrolyte', 'IDSmed (100s - 600s) [A]', 'Std IDSmed [A]', 'IGSmed (100s - 600s) [A]', 
                                'Std IGSmed [A]', 'IDSmed_pos (90s - 100s) [A]', 'Std IDSmed_pos_b [A]', 'IDSmed_pos (130s - 140s) [A]', 'Std IDSmed_pos_d [A]', 
                                'IDSmed_pos (150s - 160s) [A]', 'Std IDSmed_pos_a [A]', 'IDSmed_pos (7150s - 7160s) [A]', 'Std IDSmed_pos_f [A]', 
                                'IGSmed_pos (7150s - 7160s) [A]', 'Std IGSmed_pos_f [A]', 'delIDSmed_pos (f-b) [A]', 'Std delIDSmed_pos [A]', 'a trans pos [muA]', 
                                'Std a trans pos [muA]', 'Tau trans pos [s]', 'Std Tau trans pos [s]', 'c trans pos [muA]', 'Std c trans pos [muA]', 'r2 trans pos', 
                                'a long pos [muA]', 'Std a long pos [muA]', 'Tau long pos [s]', 'Std Tau long pos [s]', 'c long pos [muA]', 'Std c long pos [muA]', 
                                'r2 long pos', 'Slope pos [muA/s]', 'Std Slope pos [muA/s]', 'r2 linear pos',
                                'IDSmed_neg (90s - 100s) [A]', 'Std IDSmed_neg_b [A]', 'IDSmed_neg (130s - 140s) [A]', 'Std IDSmed_neg_d [A]', 
                                'IDSmed_neg (150s - 160s) [A]', 'Std IDSmed_neg_a [A]', 'IDSmed_neg (2990s - 3000s) [A]', 'Std IDSmed_neg_f [A]', 
                                'IGSmed_neg (2990s - 3000s) [A]', 'Std IGSmed_neg_f [A]', 'delIDSmed_neg (f-b) [A]', 'Std delIDSmed_neg [A]', 'a trans neg [muA]', 
                                'Std a trans neg [muA]', 'Tau trans neg [s]', 'Std Tau trans neg [s]', 'c trans neg [muA]', 'Std c trans neg [muA]', 'r2 trans neg', 
                                'a long neg [muA]', 'Std a long neg [muA]', 'Tau long neg [s]', 'Std Tau long neg [s]', 'c long neg [muA]', 'Std c long neg [muA]', 
                                'r2 long neg', 'Slope neg [muA/s]', 'Std Slope neg [muA/s]', 'r2 linear neg'])

    # Export dataframe into a .txt file
    df_long.to_csv('dados_gerados'+versionador+'data_long_pulses.txt', sep='\t', index=False)

#######################################################################################################################################################################

####################################################################PULSO LONGO######################################################################################################

def analise_long_pulse(nomes_arquivos):
    create_long_pulse()
    #Analise Pulso Longo
    pulso_longo = []

    i = 0
    for caminhos in nomes_arquivos:
        if ('Tempo de Retenção'+versionador+'Pulso Longo'+versionador) in caminhos and caminhos.endswith('.txt'):
            # df_arquivo = pd.read_csv(caminhos, sep='\t')
            pulso_longo.append(caminhos)
            i = i + 1

    i = 0
    j=0
    pulsos = []
    for i in range(len(pulso_longo)//3):
        i = i + 1
        j=j+1
        k = 0
        for elemento in pulso_longo[0:3]:
            
            print(elemento)
            # Name of the folder and file name where the data is and use it as a pandas dataframe
            if '120stability' in elemento:
                df_sta = pd.read_csv(elemento, delimiter="\t")
                # Relevant parameters stability
                pulsos.append(elemento)
                tipo_chip = get_type(elemento)
                valor_chip = get_chip(elemento)
                valor_disp = get_disp(elemento)
                tipo_eletrolito = get_eletrolito(elemento)

            elif '131pulsonegativo' in elemento:
                df_neg = pd.read_csv(elemento, delimiter="\t")
                # Relevant parameters negative
                pulsos.append(elemento)
                tipo_chip = get_type(elemento)
                valor_chip = get_chip(elemento)
                valor_disp = get_disp(elemento)
                tipo_eletrolito = get_eletrolito(elemento)

            elif '130pulsopositivo' in elemento:
                df_pos = pd.read_csv(elemento, delimiter="\t")
                # Relevant parameters positive
                pulsos.append(elemento)
                tipo_chip = get_type(elemento)
                valor_chip = get_chip(elemento)
                valor_disp = get_disp(elemento)
                tipo_eletrolito = get_eletrolito(elemento)


        # Relevant parameters stability
        IDSm_s, stdIDSm_s = find_current_mean(df_sta, 100, 600, 'Current SMUb (A)')
        IGSm_s, stdIGSm_s = find_current_mean(df_sta, 100, 600, 'Current SMUA (A)')
        # Relevant parameters positive
        df_pos = cor_timestamp(df_pos)
        IDSm_p_b, stdIDSm_p_b = find_current_mean(df_pos, 90, 100, 'Current SMUb (A)')
        IGSm_p_b, stdIGSm_p_b = find_current_mean(df_pos, 90, 100, 'Current SMUA (A)')
        IDSm_p_d, stdIDSm_p_d = find_current_mean(df_pos, 130, 140, 'Current SMUb (A)')
        IGSm_p_d, stdIGSm_p_d = find_current_mean(df_pos, 130, 140, 'Current SMUA (A)')
        IDSm_p_a, stdIDSm_p_a = find_current_mean(df_pos, 150, 160, 'Current SMUb (A)')
        IGSm_p_a, stdIGSm_p_a = find_current_mean(df_pos, 150, 160, 'Current SMUA (A)')
        IDSm_p_f, stdIDSm_p_f = find_current_mean(df_pos, 7150, 7160, 'Current SMUb (A)')
        IGSm_p_f, stdIGSm_p_f = find_current_mean(df_pos, 7150, 7160, 'Current SMUA (A)')
        delIDSm_p = IDSm_p_f - IDSm_p_b
        stdDelIDSm_p = sqrt(stdIDSm_p_b**2 + stdIDSm_p_f**2)

        a_tra_pos, std_a_tra_pos, tau_tra_pos, std_tau_tra_pos, c_tra_pos, std_c_tra_pos, r2_tra_pos,x01 = exp_fit(df_pos, 145.5, 170)
        a_long_pos, std_a_long_pos, tau_long_pos, std_tau_long_pos, c_long_pos, std_c_long_pos, r2_long_pos,x011 = exp_fit(df_pos, 170, 1170)
        slo_pos, std_slope_pos, r2_pos_lin = linear_fit(df_pos, 3170, 6170)
        # Agora, vamos plotar os dados originais e a curva ajustada
        
        plt.figure(figsize=(10, 6))

        # Plot dos dados originais
        plt.scatter(df_pos["Timestamp (s)"], df_pos["Current SMUb (A)"] * 10**6, label='Dados Originais', color='blue')
        
        # Cálculo dos valores da curva ajustada
        x_values = np.linspace(145.5, 170, 100)
        y_values = exp(x_values - x01, a_tra_pos, 1/tau_tra_pos, c_tra_pos) 
        
        # Plot da curva ajustada
        plt.plot(x_values, y_values, label='Curva Ajustada (Exponencial)', color='red')
        
        plt.xlabel('Tempo (s)')
        plt.ylabel('Corrente (uA)')
        plt.xlim(145.5, 220)
        plt.title('Ajuste Exponencial da Corrente ao Tempo')
        plt.legend([f'Tau: {tau_tra_pos} a: {a_tra_pos} c: {c_tra_pos}', f'Chip: {tipo_chip} Valor Chip: {valor_chip} Valor Disp: {valor_disp} Tipo Eletrolito: {tipo_eletrolito}'])
        plt.grid(True)
        plt.savefig(f'graficos_gerados'+versionador+f'graficopos_{i}.png')
       
        plt.show()
        
       
        # Relevant parameters negative
        IDSm_n_b, stdIDSm_n_b = find_current_mean(df_neg, 90, 100, 'Current SMUb (A)')
        IGSm_n_b, stdIGSm_n_b = find_current_mean(df_neg, 90, 100, 'Current SMUA (A)')
        IDSm_n_d, stdIDSm_n_d = find_current_mean(df_neg, 130, 140, 'Current SMUb (A)')
        IGSm_n_d, stdIGSm_n_d = find_current_mean(df_neg, 130, 140, 'Current SMUA (A)')
        IDSm_n_a, stdIDSm_n_a = find_current_mean(df_neg, 150, 160, 'Current SMUb (A)')
        IGSm_n_a, stdIGSm_n_a = find_current_mean(df_neg, 150, 160, 'Current SMUA (A)')
        IDSm_n_f, stdIDSm_n_f = find_current_mean(df_pos, 2990, 3000, 'Current SMUb (A)')
        IGSm_n_f, stdIGSm_n_f = find_current_mean(df_pos, 2990, 3000, 'Current SMUA (A)')
        delIDSm_n = IDSm_n_f - IDSm_n_b
        stdDelIDSm_n = sqrt(stdIDSm_n_b**2 + stdIDSm_n_f**2)

        a_tra_neg, std_a_tra_neg, tau_tra_neg, std_tau_tra_neg, c_tra_neg, std_c_tra_neg, r2_tra_neg,x02 = exp_fit(df_neg, 145.5, 170)
        a_long_neg, std_a_long_neg, tau_long_neg, std_tau_long_neg, c_long_neg, std_c_long_neg, r2_long_neg,x022 = exp_fit(df_neg, 170, 1170)
        slo_neg, std_slope_neg, r2_neg_lin = linear_fit(df_neg, 1500, 3000)

        #Plot Gráfico Negativo
        plt.figure(figsize=(10, 6))
        
        # Plot dos dados originais
        plt.scatter(df_neg["Timestamp (s)"], df_neg["Current SMUb (A)"] * 10**6, label='Dados Originais', color='blue')
         
        # Cálculo dos valores da curva ajustada
        x_values = np.linspace(145.5, 170, 100)
        y_values = exp(x_values - x02, a_tra_neg, 1/tau_tra_neg, c_tra_neg) 
         
        # Plot da curva ajustada
        plt.plot(x_values, y_values, label='Curva Ajustada (Exponencial)', color='red')
         
        plt.xlabel('Tempo (s)')
        plt.ylabel('Corrente (uA)')
        plt.xlim(130, 220)
        plt.title('Ajuste Exponencial da Corrente ao Tempo')
        plt.legend([f'Tau: {tau_tra_neg} a: {a_tra_neg} c: {c_tra_neg}', f'Chip: {tipo_chip} Valor Chip: {valor_chip} Valor Disp: {valor_disp} Tipo Eletrolito: {tipo_eletrolito}'])
        plt.grid(True)
        plt.savefig(f'graficos_gerados'+versionador+f'graficoneg_{j}.png')
        
        plt.show()
       

        # Create a dictionary with the data for the new row
        new_row = {'Type': tipo_chip,'Chip': valor_chip,'Disp': valor_disp, 'Electrolyte': tipo_eletrolito, 'IDSmed (100s - 600s) [A]': IDSm_s, 'Std IDSmed [A]': stdIDSm_s, 'IGSmed (100s - 600s) [A]': IGSm_s, 
           'Std IGSmed [A]': stdIGSm_s, 'IDSmed_pos (90s - 100s) [A]': IDSm_p_b, 'Std IDSmed_pos_b [A]': stdIDSm_p_b , 'IDSmed_pos (130s - 140s) [A]': IDSm_p_d, 
           'Std IDSmed_pos_d [A]': stdIDSm_p_d, 'IDSmed_pos (150s - 160s) [A]': IDSm_p_a, 'Std IDSmed_pos_a [A]': stdIDSm_p_a, 
           'IDSmed_pos (7150s - 7160s) [A]': IDSm_p_f, 'Std IDSmed_pos_f [A]': stdIDSm_p_f, 'IGSmed_pos (7150s - 7160s) [A]': IGSm_p_f, 
           'Std IGSmed_pos_f [A]': stdIGSm_p_f, 'delIDSmed_pos (f-b) [A]': delIDSm_p, 'Std delIDSmed_pos [A]': stdDelIDSm_p, 'a trans pos [muA]': a_tra_pos, 
           'Std a trans pos [muA]': std_a_tra_pos, 'Tau trans pos [s]': tau_tra_pos, 'Std Tau trans pos [s]': std_tau_tra_pos, 'c trans pos [muA]': c_tra_pos, 
           'Std c trans pos [muA]': std_c_tra_pos, 'r2 trans pos': r2_tra_pos, 'a long pos [muA]': a_long_pos, 'Std a long pos [muA]': std_a_long_pos, 
           'Tau long pos [s]': tau_long_pos, 'Std Tau long pos [s]': std_tau_long_pos, 'c long pos [muA]': c_long_pos, 'Std c long pos [muA]': std_c_long_pos, 
           'r2 long pos': r2_long_pos, 'Slope pos [muA/s]': slo_pos, 'Std Slope pos [muA/s]': std_slope_pos, 'r2 linear pos': r2_pos_lin,
           'IDSmed_neg (90s - 100s) [A]': IDSm_n_b, 'Std IDSmed_neg_b [A]': stdIDSm_n_b , 'IDSmed_neg (130s - 140s) [A]': IDSm_n_d, 
           'Std IDSmed_neg_d [A]': stdIDSm_n_d, 'IDSmed_neg (150s - 160s) [A]': IDSm_n_a, 'Std IDSmed_neg_a [A]': stdIDSm_n_a,
           'IDSmed_neg (2990s - 3000s) [A]': IDSm_n_f, 'Std IDSmed_neg_f [A]': stdIDSm_n_f, 'IGSmed_neg (2990s - 3000s) [A]': IGSm_n_f, 
           'Std IGSmed_neg_f [A]': stdIGSm_n_f, 'delIDSmed_neg (f-b) [A]': delIDSm_n, 'Std delIDSmed_neg [A]':stdDelIDSm_n, 'a trans neg [muA]': a_tra_neg, 
           'Std a trans neg [muA]': std_a_tra_neg, 'Tau trans neg [s]': tau_tra_neg, 'Std Tau trans neg [s]': std_tau_tra_neg, 'c trans neg [muA]': c_tra_neg, 
           'Std c trans neg [muA]': std_c_tra_neg, 'r2 trans neg': r2_tra_neg, 'a long neg [muA]': a_long_neg, 'Std a long neg [muA]': std_a_long_neg, 
           'Tau long neg [s]': tau_long_neg, 'Std Tau long neg [s]': std_tau_long_neg, 'c long neg [muA]': c_long_neg, 'Std c long neg [muA]': std_c_long_neg, 
           'r2 long neg': r2_long_neg, 'Slope neg [muA/s]': slo_neg, 'Std Slope neg [muA/s]': std_slope_neg, 'r2 linear neg': r2_neg_lin
          }

        # Append the dictionary to the DataFrame previously created
        df = pd.read_csv('dados_gerados'+versionador+'data_long_pulses.txt', delimiter="\t")
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        # Reset the index
        df = df.reset_index(drop=True)

        # Export dataframe i: nto a .txt file
        df.to_csv('dados_gerados'+versionador+'data_long_pulses.txt', sep='\t', index=False)
        df.to_csv('dados_gerados'+versionador+'data_long_pulses.csv', index=False)


        # Export the data that will be compiled
        data = pd.read_csv('dados_gerados'+versionador+'data_long_pulses.txt', delimiter="\t")



        pulsos = []
        del pulso_longo[0:3]

    # Group by the relevant columns and remove the columns that do not make sense
    data_2 = data.groupby(["Type","Electrolyte"], as_index=False).agg(['mean', 'std'])
    data_2 = data_2.drop(['Chip','Disp', 'Std IDSmed [A]', 'Std IGSmed [A]', 'Std IDSmed_pos_b [A]', 'Std IDSmed_pos_d [A]', 'Std IDSmed_pos_f [A]', 'Std IGSmed_pos_f [A]',
                          'Std delIDSmed_pos [A]', 'Std IDSmed_pos_a [A]', 'Std a trans pos [muA]', 'Std Tau trans pos [s]', 'Std c trans pos [muA]', 'Std a long pos [muA]',
                          'Std Tau long pos [s]', 'Std c long pos [muA]', 'Std Slope pos [muA/s]', 'Std IDSmed_neg_b [A]', 'Std IDSmed_neg_d [A]', 'Std IDSmed_neg_f [A]',
                          'Std IDSmed_neg_a [A]', 'Std a trans neg [muA]', 'Std Tau trans neg [s]', 'Std c trans neg [muA]', 'Std a long neg [muA]',
                          'Std IGSmed_neg_f [A]', 'Std delIDSmed_neg [A]', 'Std Tau long neg [s]', 'Std c long neg [muA]', 'Std Slope neg [muA/s]'] , axis=1, level=0)

    # Reset the index
    new_dataframe = data_2.reset_index(drop=True)

    # Export dataframe into a .txt file
    new_dataframe.to_csv('dados_gerados'+versionador+'data_long_pulses_means.txt', sep='\t', index=False)
    new_dataframe.to_csv('dados_gerados'+versionador+'data_long_pulses_means.csv', index=False)
##################################################################FIM PULSO LONGO######################################################################################################
