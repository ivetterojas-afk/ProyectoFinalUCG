import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


st.title("Proyecto final UCG")
st.sidebar.title("Parámetros")
st.sidebar.image("Python_logo.png")

# Carga de datos
st.sidebar.header("1. Carga del dataset")
archivo = st.sidebar.file_uploader("Suba el archivo CSV", type=["csv"])

if archivo:
    df = pd.read_csv(archivo)

    st.success("Dataset cargado correctamente")

    # Previsualización
    st.header("2. Previsualización del dataset")
    st.dataframe(df.head())


full_data = pd.read_csv("Churn_Modelling.csv", index_col=0)

# Previsualización
st.header("2. Previsualización del dataset")
st.dataframe(full_data.head())

resultado = full_data.groupby("IsActiveMember")["Exited"].mean()

fig, ax = plt.subplots()
resultado.plot(kind="bar", ax=ax)

st.pyplot(fig)
