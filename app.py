import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


st.title("Proyecto final UCG")
st.sidebar.title("Parámetros")
st.sidebar.image("Python_logo.png")

# 1.- cargar un dataset
st.sidebar.header("1. Carga del dataset")
archivo = st.sidebar.file_uploader("Suba el archivo CSV", type=["csv"])

if archivo:
    df = pd.read_csv(archivo)

    st.success("Dataset cargado correctamente")

    # Previsualización
    st.header("2. Previsualización del dataset")
    st.dataframe(df.head())


full_data = pd.read_csv("Churn_Modelling.csv", index_col=0)
st.header("2. Previsualización del dataset")
st.dataframe(full_data.head())

# 2.- Exploración inicial de Datos
modulo = st.sidebar.selectbox("Exploración inicial de Datos.. Seleccione:", ["Relación de Miembros Activos versus Clientes que se han ido", "Relación de Años de permanencia laboral versus Clientes que se han ido", "Relación de Número de Productos versus Clientes que se han ido"] )

if modulo  == "Relación de Miembros Activos versus Clientes que se han ido":
    # 2.1. Relación de Miembros Activos versus Clientes que se han ido
    st.subheader("2.1. Relación de Clientes Activos versus Clientes que se han ido")
    resultado = (
        full_data.groupby("IsActiveMember")["Exited"]
        .mean()
        .mul(100)
        .round(2)
        .reset_index()
    )
    resultado["Exited"] = resultado["Exited"].astype(str) + "%"
    st.dataframe(resultado)
# 2.2. Relación de Años de permanencia laboral versus Clientes que se han ido
elif modulo  == "Relación de Años de permanencia laboral versus Clientes que se han ido":
    st.subheader("\n2.2. Relación de Años de permanencia laboral versus Clientes que se han ido")
    resultado = (
        full_data.groupby("Tenure")["Exited"]
        .mean()
        .mul(100)
        .round(2)
        .reset_index()
    )
    resultado["Exited"] = resultado["Exited"].astype(str) + "%"
    st.dataframe(resultado)
# 2.3. Relación de Número de Productos versus Clientes que se han ido
elif modulo  == "Relación de Número de Productos versus Clientes que se han ido":
    st.subheader("\n2.3. Relación de Número de Productos versus Clientes que se han ido")
    resultado = (
        full_data.groupby("NumOfProducts")["Exited"]
        .mean()
        .mul(100)
        .round(2)
        .reset_index()
    )
    resultado["Exited"] = resultado["Exited"].astype(str) + "%"
    st.dataframe(resultado)
    
