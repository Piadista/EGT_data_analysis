import pandas as pd
import matplotlib.pyplot as plt

# Define o tamanho da figura
k = -1
# Loop para plotar 16 gráficos
for i in range(0, 16):
    # Crie um subplot na posição i
    # plt.subplot(4, 4, i)
    # Carregue os dados do arquivo usando Pandas
    if i%2 == 0:
      k = k + 1


      file_path = f"/content/Single_pulse ({64+i}).txt"
      data = pd.read_csv(file_path,sep='\t')
      lista = ["0.1 V", "0.2 V", "0.3 V", "0.4 V", "0.5 V", "0.6 V", "0.7 V", "0.8 V"]
      # Plote os dados
      plt.xlim(0,80)
      plt.ylim(2.1e-5,3e-5)
      plt.plot(data["Timestamp (s)"], data["Current SMUb (A)"], label= lista[k], alpha=0.8)
      plt.legend()
      plt.title(f"Δt = 40s")  # Adicione um título único para cada gráfico

# # Exibe o gráfico
plt.tight_layout()  # Ajusta o layout para evitar sobreposição de texto
plt.savefig("Grafico de 40s Positivo cCNF gate2 comparacao.png")
plt.show()

# Define o tamanho da figura
k = -1
# Loop para plotar 16 gráficos
for i in range(0, 16):
    # Crie um subplot na posição i
    # plt.subplot(4, 4, i)
    # Carregue os dados do arquivo usando Pandas
    if i%2 != 0:
      k = k + 1

      file_path = f"/content/Single_pulse ({64+i}).txt"
      data = pd.read_csv(file_path,sep='\t')
      lista = ["-0.1 V", "-0.2 V", "-0.3 V", "-0.4 V", "-0.5 V", "-0.6 V", "-0.7 V", "-0.8 V"]
      # Plote os dados
      plt.xlim(0,75)
      plt.ylim(2e-5,4.5e-5)
      plt.plot(data["Timestamp (s)"], data["Current SMUb (A)"], label= lista[k], alpha=0.8)
      plt.legend()
      plt.title(f"Δt = 40s")  # Adicione um título único para cada gráfico

# # Exibe o gráfico
plt.tight_layout()  # Ajusta o layout para evitar sobreposição de texto
plt.savefig("Grafico de 40s Negativo cCNF gate2 comparacao.png")
plt.show()

# Define o tamanho da figura
k = -1
# Loop para plotar 16 gráficos
for i in range(0, 16):
    # Crie um subplot na posição i
    # plt.subplot(4, 4, i)
    # Carregue os dados do arquivo usando Pandas
    if i%2 == 0:
      k = k + 1

      file_path = f"/content/Single_pulse ({48+i}).txt"
      data = pd.read_csv(file_path,sep='\t')
      lista = ["0.1 V", "0.2 V", "0.3 V", "0.4 V", "0.5 V", "0.6 V", "0.7 V", "0.8 V"]
      # Plote os dados
      plt.xlim(10,35)
      plt.ylim(2e-5,3e-5)


      plt.plot(data["Timestamp (s)"], data["Current SMUb (A)"], label= lista[k], alpha=0.8)
      plt.legend()
      plt.title(f"Δt = 10s")  # Adicione um título único para cada gráfico

# # Exibe o gráfico
plt.tight_layout()  # Ajusta o layout para evitar sobreposição de texto
plt.savefig("Grafico de 10s Positivo cCNF gate2 comparacao.png")
plt.show()

# Define o tamanho da figura
k = -1
# Loop para plotar 16 gráficos
for i in range(0, 16):
    # Crie um subplot na posição i
    # plt.subplot(4, 4, i)
    # Carregue os dados do arquivo usando Pandas
    if i%2 != 0:
      k = k + 1

      file_path = f"/content/Single_pulse ({48+i}).txt"
      data = pd.read_csv(file_path,sep='\t')
      lista = ["-0.1 V", "-0.2 V", "-0.3 V", "-0.4 V", "-0.5 V", "-0.6 V", "-0.7 V", "-0.8 V"]
      # Plote os dados
      plt.xlim(10,32)
      plt.ylim(2e-5,4.5e-5)
      plt.plot(data["Timestamp (s)"], data["Current SMUb (A)"], label= lista[k], alpha=0.8)
      plt.legend()
      plt.title(f"Δt = 10s")  # Adicione um título único para cada gráfico

# # Exibe o gráfico
plt.tight_layout()  # Ajusta o layout para evitar sobreposição de texto
plt.savefig("Grafico de 10s Negativo cCNF gate2 comparacao.png")
plt.show()

# Define o tamanho da figura
k = -1
# Loop para plotar 16 gráficos
for i in range(0, 16):
    # Crie um subplot na posição i
    # plt.subplot(4, 4, i)
    # Carregue os dados do arquivo usando Pandas
    if i%2 == 0:
      k = k + 1

      file_path = f"/content/Single_pulse ({32+i}).txt"
      data = pd.read_csv(file_path,sep='\t')
      lista = ["0.1 V", "0.2 V", "0.3 V", "0.4 V", "0.5 V", "0.6 V", "0.7 V", "0.8 V"]
      # Plote os dados
      plt.xlim(13,20)
      plt.ylim(1.5e-5,4.5e-5)


      plt.plot(data["Timestamp (s)"], data["Current SMUb (A)"], label= lista[k], alpha=0.8)
      plt.legend()
      plt.title(f"Δt = 1s")  # Adicione um título único para cada gráfico

# # Exibe o gráfico
plt.tight_layout()  # Ajusta o layout para evitar sobreposição de texto
plt.savefig("Grafico de 1s Positivo cCNF.png")
plt.show()


# Define o tamanho da figura
k = -1
# Loop para plotar 16 gráficos
for i in range(0, 16):
    # Crie um subplot na posição i
    # plt.subplot(4, 4, i)
    # Carregue os dados do arquivo usando Pandas
    if i%2 != 0:
      k = k + 1

      file_path = f"/content/Single_pulse ({32+i}).txt"
      data = pd.read_csv(file_path,sep='\t')
      lista = ["-0.1 V", "-0.2 V", "-0.3 V", "-0.4 V", "-0.5 V", "-0.6 V", "-0.7 V", "-0.8 V"]
      # Plote os dados
      plt.xlim(13,20)
      plt.ylim(1.5e-5,4.5e-5)

      plt.plot(data["Timestamp (s)"], data["Current SMUb (A)"], label= lista[k], alpha=0.8)
      plt.legend()
      plt.title(f"Δt = 1s")  # Adicione um título único para cada gráfico

# # Exibe o gráfico
plt.tight_layout()  # Ajusta o layout para evitar sobreposição de texto
plt.savefig("Grafico de 1s Negativo cCNFgate3 canal.png")
plt.show()

# Define o tamanho da figura
k = -1
# Loop para plotar 16 gráficos
for i in range(0, 16):
    # Crie um subplot na posição i
    # plt.subplot(4, 4, i)
    # Carregue os dados do arquivo usando Pandas
    if i%2 != 0:
      k = k + 1

      file_path = f"/content/Single_pulse ({32+i}).txt"
      data = pd.read_csv(file_path,sep='\t')
      lista = ["-0.1 V", "-0.2 V", "-0.3 V", "-0.4 V", "-0.5 V", "-0.6 V", "-0.7 V", "-0.8 V"]
      # Plote os dados
      plt.xlim(13,20)
      plt.ylim(1.5e-5,4.5e-5)

      plt.plot(data["Timestamp (s)"], data["Current SMUb (A)"], label= lista[k], alpha=0.8)
      plt.legend()
      plt.title(f"Δt = 1s")  # Adicione um título único para cada gráfico

# # Exibe o gráfico
plt.tight_layout()  # Ajusta o layout para evitar sobreposição de texto
plt.savefig("Grafico de 1s Negativo cCNFgate3 canal.png")
plt.show()


# Define o tamanho da figura
k = -1
# Loop para plotar 16 gráficos
for i in range(0, 16):
    # Crie um subplot na posição i
    # plt.subplot(4, 4, i)
    # Carregue os dados do arquivo usando Pandas
    if i%2 != 0:
      k = k + 1

      file_path = f"/content/Single_pulse ({32+i}).txt"
      data = pd.read_csv(file_path,sep='\t')
      lista = ["-0.1 V", "-0.2 V", "-0.3 V", "-0.4 V", "-0.5 V", "-0.6 V", "-0.7 V", "-0.8 V"]
      # Plote os dados
      plt.xlim(13,20)
      plt.ylim(1.5e-5,4.5e-5)

      plt.plot(data["Timestamp (s)"], data["Current SMUb (A)"], label= lista[k], alpha=0.8)
      plt.legend()
      plt.title(f"Δt = 1s")  # Adicione um título único para cada gráfico

# # Exibe o gráfico
plt.tight_layout()  # Ajusta o layout para evitar sobreposição de texto
plt.savefig("Grafico de 1s Negativo cCNFgate3 canal.png")
plt.show()


# Define o tamanho da figura
k = -1
# Loop para plotar 16 gráficos
for i in range(0, 16):
    # Crie um subplot na posição i
    # plt.subplot(4, 4, i)
    # Carregue os dados do arquivo usando Pandas
    if i%2 != 0:
      k = k + 1

      file_path = f"/content/Single_pulse ({16+i}).txt"
      data = pd.read_csv(file_path,sep='\t')
      lista = ["-0.1 V", "-0.2 V", "-0.3 V", "-0.4 V", "-0.5 V", "-0.6 V", "-0.7 V", "-0.8 V"]
      # Plote os dados
      plt.xlim(15.95,16.15)
      plt.ylim(-1.5e-5,6e-5)


      plt.plot(data["Timestamp (s)"], data["Current SMUb (A)"], label= lista[k], alpha=0.8)
      plt.legend()
      plt.title(f"Δt = 0.1s")  # Adicione um título único para cada gráfico

# # Exibe o gráfico
plt.tight_layout()  # Ajusta o layout para evitar sobreposição de texto
plt.savefig("Grafico de 0.1s Negativo cCNFgate3 canal.png")
plt.show()

# Define o tamanho da figura
k = -1
# Loop para plotar 16 gráficos
for i in range(0, 16):
    # Crie um subplot na posição i
    # plt.subplot(4, 4, i)
    # Carregue os dados do arquivo usando Pandas
    if i%2 == 0:
      k = k + 1

      file_path = f"/content/Single_pulse ({0+i}).txt"
      data = pd.read_csv(file_path,sep='\t')
      lista = ["0.1 V", "0.2 V", "0.3 V", "0.4 V", "0.5 V", "0.6 V", "0.7 V", "0.8 V"]
      # Plote os dados
      plt.xlim(15.995,16.020)
      plt.ylim(-16.0e-5,21.5e-5)


      plt.plot(data["Timestamp (s)"], data["Current SMUb (A)"], label= lista[k], alpha=0.8)
      plt.legend()
      plt.title(f"Δt = 0.01s")  # Adicione um título único para cada gráfico

# # Exibe o gráfico
plt.tight_layout()  # Ajusta o layout para evitar sobreposição de texto
plt.savefig("Grafico de 0.01s Positivo cCNFgate3 canal.png")
plt.show()



# Define o tamanho da figura
k = -1
# Loop para plotar 16 gráficos
for i in range(0, 16):
    # Crie um subplot na posição i
    # plt.subplot(4, 4, i)
    # Carregue os dados do arquivo usando Pandas
    if i%2 != 0:
      k = k + 1

      file_path = f"/content/Single_pulse ({0+i}).txt"
      data = pd.read_csv(file_path,sep='\t')
      lista = ["-0.1 V", "-0.2 V", "-0.3 V", "-0.4 V", "-0.5 V", "-0.6 V", "-0.7 V", "-0.8 V"]
      # Plote os dados
      plt.xlim(15.995,16.020)
      plt.ylim(-16.0e-5,21.5e-5)


      plt.plot(data["Timestamp (s)"], data["Current SMUb (A)"], label= lista[k], alpha=0.8)
      plt.legend()
      plt.title(f"Δt = 0.01s")  # Adicione um título único para cada gráfico

# # Exibe o gráfico
plt.tight_layout()  # Ajusta o layout para evitar sobreposição de texto
plt.savefig("Grafico de 0.01s Negativo cCNFgate3 canal.png")
plt.show()