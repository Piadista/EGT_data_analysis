from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Progressbar, Style
from PIL import ImageTk, Image
import os
import pandas as pd
import matplotlib.pyplot as plt
from tkinter.ttk import Style
import customtkinter as ctk
from function_transfer import *
from function_short_pulse import *
from function_long_pulse import *
from function_ppx import *
from function_multiple import *
from function_lgt_pulsed import *
from function_transfer_stability import *
from function_stability import *
from function_decaimento import *
from function_retention_time_graphic import *
from function_power_point import *
import time
import platform



# Filtrar e ignorar todos os FutureWarnings
warnings.filterwarnings("ignore", category=FutureWarning)
# Auxiliary functions


sistema_operacional = platform.system()


if sistema_operacional == "Windows":
    print("Você está usando o Windows.")
    from function_retention_time_graphic import *
    from function_long_pulse_graphic import *
    from function_short_pulse_graphic import *
    from function_stability_graphic import *
    from function_ppx_graphic import *
    from function_single_pulse_graphic import *
    versionador = '\\'
elif sistema_operacional == "Linux":
    print("Você está usando o Linux.")
    versionador = '/'
elif sistema_operacional == "Darwin":
    print("Você está usando o macOS.")
else:
    print(f"Você está usando um sistema operacional desconhecido: {sistema_operacional}")



def criar_pasta(nome_pasta):
    try:
        os.mkdir(nome_pasta)
        print(f"Pasta '{nome_pasta}' criada com sucesso!")
    except FileExistsError:
        print(f"A pasta '{nome_pasta}' já existe.")

if __name__ == "__main__":
    nome_da_pasta = "dados_gerados"  # Você pode alterar o nome da pasta conforme necessário
    criar_pasta(nome_da_pasta)
    
    
    

def criar_pasta_graficos(nome_pasta):
    try:
        os.mkdir(nome_pasta)
        print(f"Pasta graficos '{nome_pasta}' criada com sucesso!")
    except FileExistsError:
        print(f"A pasta graficos '{nome_pasta}' já existe.")

if __name__ == "__main__":
    nome_da_pasta = "graficos_gerados"  # Você pode alterar o nome da pasta conforme necessário
    criar_pasta(nome_da_pasta)    
    
    
    

    
# Especifica o caminho da subpasta
sub_pasta_tempo_retencao = os.path.join('dados_gerados', 'Dados Transfer Tempo de Retenção')

# Cria a subpasta dentro da pasta principal
os.makedirs(sub_pasta_tempo_retencao, exist_ok=True)

# Especifica o caminho da subpasta
sub_pasta_pulso_longo = os.path.join('dados_gerados', 'Dados Pulso Longo')

# Cria a subpasta dentro da pasta principal
os.makedirs(sub_pasta_pulso_longo, exist_ok=True)  

# Especifica o caminho da subpasta
sub_pasta_pulso_curto = os.path.join('dados_gerados', 'Dados Pulso Curto')

# Cria a subpasta dentro da pasta principal
os.makedirs(sub_pasta_pulso_curto, exist_ok=True) 

# Especifica o caminho da subpasta
sub_pasta_stability = os.path.join('dados_gerados', 'Dados Estabilidade')

# Cria a subpasta dentro da pasta principal
os.makedirs(sub_pasta_stability, exist_ok=True)

# Especifica o caminho da subpasta
sub_pasta_ppx = os.path.join('dados_gerados', 'Dados PPX')

# Cria a subpasta dentro da pasta principal
os.makedirs(sub_pasta_ppx, exist_ok=True)

# Especifica o caminho da subpasta
sub_pasta_single_pulse = os.path.join('dados_gerados', 'Dados Single Pulse')

# Cria a subpasta dentro da pasta principal
os.makedirs(sub_pasta_single_pulse, exist_ok=True)



    






# Especifica o caminho da subpasta
sub_pasta_grafico_tempo_retencao = os.path.join('graficos_gerados', 'Graficos Transfer Tempo de Retencao')

# Cria a subpasta dentro da pasta principal
os.makedirs(sub_pasta_grafico_tempo_retencao, exist_ok=True)


# Especifica o caminho da subpasta
sub_pasta_grafico_pulso_longo = os.path.join('graficos_gerados', 'Graficos Pulso Longo')

# Cria a subpasta dentro da pasta principal
os.makedirs(sub_pasta_grafico_pulso_longo, exist_ok=True)


# Especifica o caminho da subpasta
sub_pasta_grafico_pulso_curto = os.path.join('graficos_gerados', 'Graficos Pulso Curto')

# Cria a subpasta dentro da pasta principal
os.makedirs(sub_pasta_grafico_pulso_curto, exist_ok=True)


# Especifica o caminho da subpasta
sub_pasta_grafico_stability = os.path.join('graficos_gerados', 'Graficos Estabilidade')

# Cria a subpasta dentro da pasta principal
os.makedirs(sub_pasta_grafico_stability, exist_ok=True)


# Especifica o caminho da subpasta
sub_pasta_grafico_ppx = os.path.join('graficos_gerados', 'Graficos PPX')

# Cria a subpasta dentro da pasta principal
os.makedirs(sub_pasta_grafico_ppx, exist_ok=True)

# Especifica o caminho da subpasta
sub_pasta_grafico_single_pulse = os.path.join('graficos_gerados', 'Graficos Single Pulse')

# Cria a subpasta dentro da pasta principal
os.makedirs(sub_pasta_grafico_single_pulse, exist_ok=True)


    
    
    


# Funções para escolha de qual parte do codigo rodar
def switch_transfer(option):
    analise_transfer(option)
def switch_short_pulse(option):
    analise_short_pulse(option)
def switch_long_pulse(option):
    analise_long_pulse(option)
def switch_ppx(option):
    analise_ppx(option)
def switch_multiple(option):
    analise_multiple(option)
def switch_lgt_pulsed(option):
    analise_lgt_pulsed(option)
def switch_transfer_stability(option):
    analise_transfer_stability(option)
def switch_stability(option):
    analise_stability(option)
def switch_decaimento(option):
    analise_decaimento(option)
    
    
# Funções para escolha de qual parte do código rodar gráficos   
def switch_retention_time_graphic(option):
    retention_time_graphic(option)
def switch_long_pulse_graphic(option):
    long_pulse_graphic(option)
def switch_short_pulse_graphic(option):
    short_pulse_graphic(option)
def switch_stability_graphic(option):
    stability_graphic(option)
def switch_ppx_graphic(option):
    ppx_graphic(option)
def switch_single_pulse_graphic(option):
    single_pulse_graphic(option)
    
    
    
def switch_power_point(option):
    power_point(option)
    
    
    
# Função para análise dos arquivos em uma pasta
def analisar_arquivos_em_pasta(filepath, funcoes_selecionadas):
    # Lista para armazenar os nomes dos arquivos
    tempo_inicial = time.time()
    nomes_arquivos = []
    nomes_pastas = []
    # Itera recursivamente sobre todos os arquivos e subpastas na pasta
    for pasta_atual, subpastas, arquivos in os.walk(filepath):
        # Itera sobre cada arquivo na pasta atual
        nomes_pastas.append(pasta_atual)
        for arquivo in arquivos:
            # Adiciona o nome do arquivo à lista

            nomes_arquivos.append(os.path.join(pasta_atual, arquivo))

    # Itera sobre os arquivos na pasta
    for nome_do_arquivo in os.listdir(filepath):
        substring = nome_do_arquivo[0:16]
        nomes_pastas.append(substring)

    pd.set_option('display.float_format', lambda x: '%.12f' % x)
    pd.set_option('display.precision', 12)

    # Funções a serem executadas com base nas seleções do usuário
    funcoes_executadas = []
    if funcoes_selecionadas["transfer"]:
        funcoes_executadas.append(switch_transfer)
    if funcoes_selecionadas["short_pulse"]:
        funcoes_executadas.append(switch_short_pulse)
    if funcoes_selecionadas["long_pulse"]:
        funcoes_executadas.append(switch_long_pulse)
    if funcoes_selecionadas["ppx"]:
        funcoes_executadas.append(switch_ppx)
    if funcoes_selecionadas["multiple"]:
        funcoes_executadas.append(switch_multiple)
    if funcoes_selecionadas["lgt_pulsed"]:
        funcoes_executadas.append(switch_lgt_pulsed)
    if funcoes_selecionadas["transfer_stability"]:
        funcoes_executadas.append(switch_transfer_stability)
    if funcoes_selecionadas["stability"]:
        funcoes_executadas.append(switch_stability)
    if funcoes_selecionadas["decaimento"]:
        funcoes_executadas.append(switch_decaimento)
    if funcoes_selecionadas["retention_time_graphic"]:
        funcoes_executadas.append(switch_retention_time_graphic)
    if funcoes_selecionadas["long_pulse_graphic"]:
        funcoes_executadas.append(switch_long_pulse_graphic)
    if funcoes_selecionadas["short_pulse_graphic"]:
        funcoes_executadas.append(switch_short_pulse_graphic)
    if funcoes_selecionadas["stability_graphic"]:
        funcoes_executadas.append(switch_stability_graphic)
    if funcoes_selecionadas["ppx_graphic"]:
        funcoes_executadas.append(switch_ppx_graphic)
    if funcoes_selecionadas["single_pulse_graphic"]:
        funcoes_executadas.append(switch_single_pulse_graphic)
    if funcoes_selecionadas["power_point"]:
        funcoes_executadas.append(switch_power_point)

    total_funcoes = len(funcoes_executadas)
    progresso = 0

    # Executar as funções selecionadas
    for funcao in funcoes_executadas:
        if funcao == switch_transfer:
            funcao(nomes_arquivos)
            progress_label.config(text="Transferência Concluído")
        elif funcao == switch_short_pulse:
            funcao(nomes_arquivos)
            progress_label.config(text="Pulso Curto Concluído")
        elif funcao == switch_long_pulse:
            funcao(nomes_arquivos)
            progress_label.config(text="Pulso Longo Concluído")
        elif funcao == switch_ppx:
            funcao(nomes_pastas)
            progress_label.config(text="PPX Concluído")
        elif funcao == switch_multiple:
            funcao(nomes_pastas)
            progress_label.config(text="Multiple Concluído")
        elif funcao == switch_lgt_pulsed:
            funcao(nomes_pastas)
            progress_label.config(text="LGT Pulsed Concluído")
        elif funcao == switch_transfer_stability:
            funcao(nomes_arquivos)
            progress_label.config(text="Transferência da Estabilidade Concluído")
        elif funcao == switch_stability:
            funcao(nomes_pastas)
            progress_label.config(text="Estabilidade Concluído")
        elif funcao == switch_decaimento:
            funcao(nomes_pastas)
            progress_label.config(text="Decaimento Concluído")
        elif funcao == switch_retention_time_graphic:
            funcao(nomes_arquivos)
            progress_label.config(text="Gráfico Tempo de Retenção Concluído")
        elif funcao == switch_long_pulse_graphic:
            funcao(nomes_arquivos)
            progress_label.config(text="Gráfico Pulso Longo Concluído")
        elif funcao == switch_short_pulse_graphic:
            funcao(nomes_arquivos)
            progress_label.config(text="Gráfico Pulso Curto Concluído")
        elif funcao == switch_stability_graphic:
            funcao(nomes_arquivos)
            progress_label.config(text="Gráfico Estabilidade Concluído")
        elif funcao == switch_ppx_graphic:
            funcao(nomes_arquivos)
            progress_label.config(text="Gráfico PPX Concluído")
        elif funcao == switch_single_pulse_graphic:
            funcao(nomes_pastas)
            progress_label.config(text="Gráfico Single Pulse Concluído")
        elif funcao == switch_power_point:
            funcao(nomes_pastas)
            progress_label.config(text="Relatorio Concluído")

            
        else:
            funcao()

        # Atualizar a barra de progresso
        progresso += 1
        progresso_percentual = (progresso / total_funcoes) * 100
        progress_bar["value"] = progresso_percentual
        progress_bar.update()
        # Gravar o tempo final
        tempo_final = time.time()

        # Calcular o tempo decorrido em segundos
        tempo_decorrido = tempo_final - tempo_inicial

        # Converter o tempo decorrido para um formato mais legível (horas:minutos:segundos)
        horas, tempo_decorrido = divmod(tempo_decorrido, 3600)
        minutos, segundos = divmod(tempo_decorrido, 60)
    # Agendar a atualização da mensagem de conclusão após 2 segundos
    window.after(5000, lambda: progress_label.config(text=f"Processo concluído. Tempo decorrido: {int(horas)}h {int(minutos)}m {int(segundos)}s."))

# Função chamada quando o usuário clica no botão para escolher o arquivo
def openFile():
    filepath = filedialog.askdirectory(initialdir="", title="Open")
    funcoes_selecionadas = {
        "transfer": transfer_var.get(),
        "short_pulse": short_pulse_var.get(),
        "long_pulse": long_pulse_var.get(),
        "ppx": ppx_var.get(),
        "multiple": multiple_var.get(),
        "lgt_pulsed": lgt_pulsed_var.get(),
        "transfer_stability": transfer_stability_var.get(),
        "stability": stability_var.get(),
        "decaimento": decaimento_var.get(),
        "retention_time_graphic": retention_time_graphic_var.get(),
        "long_pulse_graphic": long_pulse_graphic_var.get(),
        "short_pulse_graphic": short_pulse_graphic_var.get(),
        "stability_graphic": stability_graphic_var.get(),
        "ppx_graphic": ppx_graphic_var.get(),
        "single_pulse_graphic": single_pulse_graphic_var.get(),
        "power_point": power_point_var.get()
    }
    analisar_arquivos_em_pasta(filepath, funcoes_selecionadas)


# Criar a janela principal
window = ctk.CTk()
window.title("Data Analyzer")

# Adicionar uma imagem à janela
#img = PhotoImage(file=r"C:\Users\eduardo.neto\Desktop\programa_teste\programa_teste\lnnano.png")
#label_imagem = ctk.CTkLabel(window, image=img, bg_color="transparent", text="")
#label_imagem.place(x=80, y=35)

# Definir o tema
style = Style()
window.resizable(width=True, height=False)
window.configure(background="D2691E")

# Definir a largura e a altura da janela
largura = 1000
altura = 400
window.geometry(f"{largura}x{altura}")




# Criar variáveis de controle para as caixas de seleção
windows_var = ctk.BooleanVar()
linux_var = ctk.BooleanVar()

# Criar variáveis de controle para as caixas de seleção
transfer_var = BooleanVar()
short_pulse_var = BooleanVar()
long_pulse_var = BooleanVar()
ppx_var = BooleanVar()
multiple_var = BooleanVar()
lgt_pulsed_var = BooleanVar()
transfer_stability_var = BooleanVar()
stability_var = BooleanVar()
decaimento_var = BooleanVar()
retention_time_graphic_var = BooleanVar()
long_pulse_graphic_var = BooleanVar()
short_pulse_graphic_var = BooleanVar()
stability_graphic_var = BooleanVar()
ppx_graphic_var = BooleanVar()
single_pulse_graphic_var = BooleanVar()
power_point_var = BooleanVar()


# Função chamada quando o botão "Todos" é clicado
def selecionar_todos():
    transfer_var.set(True)
    short_pulse_var.set(True)
    long_pulse_var.set(True)
    ppx_var.set(True)
    multiple_var.set(True)
    lgt_pulsed_var.set(True)
    transfer_stability_var.set(True)
    stability_var.set(True)
    decaimento_var.set(True)
    retention_time_graphic_var.set(True)
    long_pulse_graphic_var.set(True)
    short_pulse_graphic_var.set(True)
    stability_graphic_var.set(True)
    ppx_graphic_var.set(True)
    single_pulse_graphic_var.set(True)
    power_point_var.set(True)






# Criar o botão "Todos"
button_todos = ctk.CTkButton(window, text="Todos", command=selecionar_todos, bg_color="#D2691E", fg_color="#D2691E", hover_color="green", font=(("Arial Bold"), 15))
button_todos.place(x=400, y=290)


# Criar caixas de seleção para cada função
check_transfer = ctk.CTkCheckBox(window, text="Transfer", variable=transfer_var, onvalue=True, offvalue=False, bg_color="#D2691E", fg_color="green", font=("Arial", 12))
check_transfer.place(x=400, y=20)

check_short_pulse = ctk.CTkCheckBox(window, text="Short Pulse", variable=short_pulse_var, onvalue=True, offvalue=False, bg_color="#D2691E", fg_color="green", font=("Arial", 12))
check_short_pulse.place(x=400, y=50)

check_long_pulse = ctk.CTkCheckBox(window, text="Long Pulse", variable=long_pulse_var, onvalue=True, offvalue=False, bg_color="#D2691E", fg_color="green", font=("Arial", 12))
check_long_pulse.place(x=400, y=80)

check_long_pulse = ctk.CTkCheckBox(window, text="PPX", variable=ppx_var, onvalue=True, offvalue=False, bg_color="#D2691E", fg_color="green", font=("Arial", 12))
check_long_pulse.place(x=400, y=110)

check_long_pulse = ctk.CTkCheckBox(window, text="Multiple", variable=multiple_var, onvalue=True, offvalue=False, bg_color="#D2691E", fg_color="green", font=("Arial", 12))
check_long_pulse.place(x=400, y=140)

check_long_pulse = ctk.CTkCheckBox(window, text="LGT Pulsed", variable=lgt_pulsed_var, onvalue=True, offvalue=False, bg_color="#D2691E", fg_color="green", font=("Arial", 12))
check_long_pulse.place(x=400, y=170)

check_long_pulse = ctk.CTkCheckBox(window, text="Transfer Stability", variable=transfer_stability_var, onvalue=True, offvalue=False, bg_color="#D2691E", fg_color="green", font=("Arial", 12))
check_long_pulse.place(x=400, y=200)

check_long_pulse = ctk.CTkCheckBox(window, text="Stability", variable=stability_var, onvalue=True, offvalue=False, bg_color="#D2691E", fg_color="green", font=("Arial", 12))
check_long_pulse.place(x=400, y=230)

check_long_pulse = ctk.CTkCheckBox(window, text="Decaimento", variable=decaimento_var, onvalue=True, offvalue=False, bg_color="#D2691E", fg_color="green", font=("Arial", 12))
check_long_pulse.place(x=400, y=260)

check_long_pulse = ctk.CTkCheckBox(window, text="Transfer Retention Time Graphic", variable=retention_time_graphic_var, onvalue=True, offvalue=False, bg_color="#D2691E", fg_color="green", font=("Arial", 12))
check_long_pulse.place(x=600, y=20)

check_long_pulse = ctk.CTkCheckBox(window, text="Long Pulse Graphic", variable=long_pulse_graphic_var, onvalue=True, offvalue=False, bg_color="#D2691E", fg_color="green", font=("Arial", 12))
check_long_pulse.place(x=600, y=50)

check_long_pulse = ctk.CTkCheckBox(window, text="Short Pulse Graphic", variable=short_pulse_graphic_var, onvalue=True, offvalue=False, bg_color="#D2691E", fg_color="green", font=("Arial", 12))
check_long_pulse.place(x=600, y=80)

check_long_pulse = ctk.CTkCheckBox(window, text="Stability Graphic", variable=stability_graphic_var, onvalue=True, offvalue=False, bg_color="#D2691E", fg_color="green", font=("Arial", 12))
check_long_pulse.place(x=600, y=110)

check_long_pulse = ctk.CTkCheckBox(window, text="PPX Graphic", variable=ppx_graphic_var, onvalue=True, offvalue=False, bg_color="#D2691E", fg_color="green", font=("Arial", 12))
check_long_pulse.place(x=600, y=140)

check_long_pulse = ctk.CTkCheckBox(window, text="Single Pulse Graphic", variable=single_pulse_graphic_var, onvalue=True, offvalue=False, bg_color="#D2691E", fg_color="green", font=("Arial", 12))
check_long_pulse.place(x=600, y=170)

check_long_pulse = ctk.CTkCheckBox(window, text="Relatorio", variable=power_point_var, onvalue=True, offvalue=False, bg_color="#D2691E", fg_color="green", font=("Arial", 12))
check_long_pulse.place(x=850, y=20)

# Criar o botão para escolher o arquivo
button = ctk.CTkButton(window, text="Escolher Arquivo", command=openFile, bg_color="#D2691E", fg_color="#D2691E", hover_color="gray", font=(("Arial Bold"), 15))
button.place(x=125, y=250)

# Criar o rótulo para indicar o progresso
progress_label = Label(window, text="Aguardando...", bg = "green", fg="white", font=("Arial", 9))
progress_label.place(x=100, y=300)

# Criar a barra de progresso
progress_bar = Progressbar(window, orient=HORIZONTAL, length=200, mode='determinate')
progress_bar.place(x=100, y=330)


assinatura = Label(window, text="by Eduardo Lourenço e Guilherme Selmi", bg = "white", fg="black", font=("Arial", 8))
assinatura.place(x=370, y=380)




window.mainloop()
