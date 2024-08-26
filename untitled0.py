# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 09:52:57 2024

@author: eduardo.neto
"""

for elemento in transfers:
    i = i + 1
    k = k + 1
    data = pd.read_csv(elemento, sep="\t")

    # Correct first column of cycles (Monstro software subscribe wrongly some values)

    df_c = correct_cycle_column(data)
    # Calculate relevant parameters and choose the appropriate data
    if "150transfer" in elemento:
        sweep = 1.0
    elif "151transfer" in elemento:
        sweep = 1.0
    elif "152transfer" in elemento:
        sweep = 1.0
    else:
        sweep = 2.0
    df_c = df_c[df_c["Cycle #"] == sweep]
    df_c = df_c.drop_duplicates(subset=['V'])
  
    print(df_c)
    tipo_chip = get_type(elemento)
    valor_chip = get_chip(elemento)
    valor_disp = get_disp(elemento)
    tipo_eletrolito = get_eletrolito(elemento)
    tipo_measure = get_measure(elemento)
    df_c = df_c.rename(columns={'ids_Oupt01__--0.1000' : tipo_measure})
    print(df_c)
    df_c.to_csv(f'dados_gerados'+versionador+'testetransfer.txt', sep='\t', index=False)

    if k < 5:
        lista_df.append(df_c[tipo_measure].reset_index(drop=True))
        df_final = pd.concat(lista_df, axis=1)
        print(df_final)
        
       
    if k == 5:
        lista_df.append(df_c[tipo_measure].reset_index(drop=True))
        df_final = pd.concat(lista_df, axis=1)
        df_final.insert(loc=0, column='Vgs',value= df_c['V'].to_numpy())
        df_final.to_csv(f'dados_gerados'+versionador+f'Dados Transfer Tempo de Retenção'+versionador+f'Retention Transfer {tipo_chip} Chip {valor_chip} Disp {valor_disp} {tipo_eletrolito}.csv', index=False)
        df_final.to_csv(f'dados_gerados'+versionador+f'Dados Transfer Tempo de Retenção'+versionador+f'Retention Transfer {tipo_chip} Chip {valor_chip} Disp {valor_disp} {tipo_eletrolito}.dat', index=False)
        df_final.to_csv(f'dados_gerados'+versionador+f'Dados Transfer Tempo de Retenção'+versionador+f'Retention Transfer {tipo_chip} Chip {valor_chip} Disp {valor_disp} {tipo_eletrolito}.txt', index=False)

        df_final = pd.DataFrame()
        lista_df = []
        k=0