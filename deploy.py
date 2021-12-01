#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import streamlit as st
import joblib

# modelo = joblib.load('modelo.joblib')

        
x_numericos = {'latitude': 0, 'longitude': 0, 'accommodates': 0, 'bathrooms': 0, 'bedrooms': 0, 'beds': 0, 'extra_people': 0,
               'minimum_nights': 0, 'ano': 0, 'mes': 0, 'qtd_amenities': 0, 'host_listings_count': 0}

x_tf = {'host_is_superhost': 0, 'instant_bookable': 0}

x_listas = {'property_type': ['Apartment', 'Bed and breakfast', 'Condominium', 'Guest suite', 'Guesthouse', 'Hostel', 'House', 'Loft', 'Outros', 'Serviced apartment'],
            'room_type': ['Entire home/apt', 'Hotel room', 'Private room', 'Shared room'],
            'cancelation_policy': ['flexible', 'moderate', 'Strict', 'strict_14_with_grace_period']
            }

#criar dicionario para armazenar os valores que serão preenchidos no streamlit
dicionario = {}
#concatenar chave e valor (Ex: property_type_Apartment) para que esse
#valor corresponda ao nome da coluna dummy na base de dados
for item in x_listas:
    for valor in x_listas[item]:
        dicionario[f'{item}_{valor}'] = 0

#criar campos numericos
for item in x_numericos:
	#para cada item do dic, criar um campo que recebe o dado da variavel 'valor'
	#se o campo for latitude/longitude, receber o dado neste formato
    if item == 'latitude' or item == 'longitude':
        valor = st.number_input(f'{item}', step=0.00001, value=0.0, format="%.5f") # 5 casas decimais
    elif item == 'extra_people':
        valor = st.number_input(f'{item}', step=0.01, value=0.0) # 2 casas decimais (padrao)
    else:
        valor = st.number_input(f'{item}', step=1, value=0)
    x_numericos[item] = valor

#criar campos booleanos
for item in x_tf:
    valor = st.selectbox(f'{item}', ('Sim', 'Não'))
    if valor == "Sim":
        x_tf[item] = 1
    else:
        x_tf[item] = 0
    
#criar campos de listas
for item in x_listas:
    valor = st.selectbox(f'{item}', x_listas[item])
    dicionario[f'{item}_{valor}'] = 1

#criar botao prever valor
botao = st.button('Prever Valor')

if botao:
    dicionario.update(x_numericos)
    dicionario.update(x_tf)
    valores_x = pd.DataFrame(dicionario, index=[0])
    modelo = joblib.load("modelo_v3_compressed.joblib")
    preco = modelo.predict(valores_x)
    st.write(preco[0])
