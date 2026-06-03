import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


st.title("ANÁLISIS ABANDONO BANCARIO")
st.sidebar.title("OPCIONES")

# 1.- cargar un dataset
st.sidebar.header("1. Carga del dataset")
archivo = st.sidebar.file_uploader("Suba el archivo CSV", type=["csv"])

if archivo:
    df = pd.read_csv(archivo)

    st.success("Dataset cargado correctamente")

    # Previsualización
    st.header("1. Previsualización del dataset")
    st.dataframe(df.head())


full_data = pd.read_csv("Churn_Modelling.csv", index_col=0)
st.header("1. Previsualización del dataset")
st.dataframe(full_data.head())

# 2.- Exploración inicial de datos
exploracion = st.sidebar.selectbox("2.- Exploración inicial de Datos", ["Selecciona",
                                                                    "Filas y Columnas",
                                                                    "Tipos de Datos", 
                                                                    "Valores Nulos",
                                                                    "Datos Duplicados",
                                                                    "Valores Atípicos (outliers)",
                                                                    "Variables Balanceadas"])

if exploracion  == "Selecciona":
    pass
# ==========================================
# FILAS Y COLUMNAS
# ==========================================
elif exploracion == "Filas y Columnas":

    st.subheader("Dimensiones del Dataset")

    filas, columnas = full_data.shape

    st.metric("Número de Filas", filas)
    st.metric("Número de Columnas", columnas)

    st.write("Primeras filas del dataset:")
    st.dataframe(full_data.head())

# ==========================================
# TIPOS DE DATOS
# ==========================================
elif exploracion == "Tipos de Datos":

    st.subheader("Tipos de Datos")

    tipos = pd.DataFrame({
        "Variable": full_data.columns,
        "Tipo de Dato": full_data.dtypes.values
    })

    st.dataframe(tipos)

# ==========================================
# VALORES NULOS
# ==========================================
elif exploracion == "Valores Nulos":

    st.subheader("Valores Nulos")

    nulos = full_data.isnull().sum()

    tabla_nulos = pd.DataFrame({
        "Variable": nulos.index,
        "Valores Nulos": nulos.values
    })

    st.dataframe(tabla_nulos)

    st.write("Total de valores nulos:", int(nulos.sum()))

    fig, ax = plt.subplots()
    nulos.plot(kind="bar", ax=ax)
    ax.set_title("Valores Nulos por Variable")
    st.pyplot(fig)

# ==========================================
# DATOS DUPLICADOS
# ==========================================
elif exploracion == "Datos Duplicados":

    st.subheader("Datos Duplicados")

    duplicados = full_data.duplicated().sum()

    st.metric("Registros Duplicados", duplicados)

    if duplicados > 0:
        st.write(full_data[full_data.duplicated()].head())

# ==========================================
# OUTLIERS
# ==========================================
elif exploracion == "Valores Atípicos (Outliers)":

    st.subheader("Detección de Outliers")

    columnas_numericas = full_data.select_dtypes(
        include=["int64", "float64"]
    ).columns

    variable = st.selectbox(
        "Seleccione una variable numérica",
        columnas_numericas
    )

    Q1 = full_data[variable].quantile(0.25)
    Q3 = full_data[variable].quantile(0.75)
    IQR = Q3 - Q1

    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR

    outliers = full_data[
        (full_data[variable] < limite_inferior)
        | (full_data[variable] > limite_superior)
    ]

    st.metric(
        "Cantidad de Outliers",
        len(outliers)
    )

    fig, ax = plt.subplots()
    ax.boxplot(full_data[variable])
    ax.set_title(f"Boxplot de {variable}")
    st.pyplot(fig)

    st.write("Primeros registros considerados outliers:")
    st.dataframe(outliers.head())

# ==========================================
# VARIABLES BALANCEADAS
# ==========================================
elif exploracion == "Variables Balanceadas":

    st.subheader("Balance de la Variable Objetivo")

    if "Exited" in full_data.columns:

        conteo = full_data["Exited"].value_counts()

        porcentaje = (
            full_data["Exited"]
            .value_counts(normalize=True)
            * 100
        ).round(2)

        resumen = pd.DataFrame({
            "Cantidad": conteo,
            "Porcentaje (%)": porcentaje
        })

        st.dataframe(resumen)

        fig, ax = plt.subplots()
        conteo.plot(kind="bar", ax=ax)
        ax.set_title("Distribución de la Variable Exited")
        ax.set_xlabel("Exited")
        ax.set_ylabel("Cantidad")
        st.pyplot(fig)

        st.write("""
        Interpretación:
        - Exited = 0 → Cliente permanece en el banco.
        - Exited = 1 → Cliente abandona el banco.
        """)

    else:
        st.error("La columna 'Exited' no existe en el dataset.")
# 3.- Visualización de información relevante
modulo = st.sidebar.selectbox("3.- Visualización de información Relevante:", ["Selecciona",
                                                                          "Relación de Clientes Activos versus Clientes que se han ido", 
                                                                          "Relación de Años de permanencia laboral versus Clientes que han abandonado", 
                                                                             "Relación de Número de Productos versus Clientes que se han abandonado", 
                                                                             "Relación de Género del Cliente versus Clientes que se han abandonado", 
                                                                             "Cantidad de clientes que permanecen (0) vs. clientes que abandonaron (1)", 
                                                                             "Graficar la distribución de edades según el estado de abandono", 
                                                                             "Graficar la distribución de Balance según el estado de abandono"] )

if modulo  == "Selecciona":
    pass
elif modulo  == "Relación de Clientes Activos versus Clientes que han abandonado":
    pass
    # 2.1. Relación de Miembros Activos versus Clientes que se han ido
    st.subheader("2.1. Relación de Clientes Activos versus Clientes que se han abandonado")
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
elif modulo  == "Relación de Años de permanencia laboral versus Clientes que se han abandonado":
    pass
    st.subheader("\n2.2. Relación de Años de permanencia laboral versus Clientes que se han abandonado")
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
elif modulo  == "Relación de Número de Productos versus Clientes que se han abandonado":
    st.subheader("\n2.3. Relación de Número de Productos versus Clientes que se han abandonado")
    resultado = (
        full_data.groupby("NumOfProducts")["Exited"]
        .mean()
        .mul(100)
        .round(2)
        .reset_index()
    )
    resultado["Exited"] = resultado["Exited"].astype(str) + "%"
    st.dataframe(resultado)
# 2.4. Relación de Género del Cliente versus Clientes que se han ido
elif modulo  == "Relación de Género del Cliente versus Clientes que se han abandonado":
    st.subheader("\n2.4. Relación de Género del Cliente versus Clientes que se han abandonado")
    resultado = (
        full_data.groupby("Gender")["Exited"]
        .mean()
        .mul(100)
        .round(2)
        .reset_index()
    )
    resultado["Exited"] = resultado["Exited"].astype(str) + "%"
    st.dataframe(resultado)
# 2.5. Cantidad de clientes que permanecen (0) vs. clientes que abandonaron (1)
elif modulo  == "Cantidad de clientes que permanecen (0) vs. clientes que abandonaron (1)":
    st.write("Distribución de Clientes:")
    resultado = full_data["Exited"].value_counts().reset_index()
    resultado.columns = ["Exited", "Cantidad"]
    st.dataframe(resultado)
    # Edad promedio (según estado de abandono):
    st.write("Edad promedio (según estado de abandono):")
    resultado = (
        full_data.groupby("Exited")["Age"]
        .mean()
        .reset_index()
    )
    st.dataframe(resultado)    # ¿Los clientes que tienen tarjeta de crédito son más leales?
    st.write("Tasa de abandono según tenencia de tarjeta de crédito:")
    resultado = (
        pd.crosstab(
            full_data["HasCrCard"],
            full_data["Exited"],
            normalize="index"
        ) * 100
    ).round(2)
    st.dataframe(resultado)
# 2.6. Graficar la distribución de edades según el estado de abandono
elif modulo  == "Graficar la distribución de edades según el estado de abandono":
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.kdeplot(
    data=full_data,
    x="Age",
    hue="Exited",
    fill=True,
    ax=ax
    )
    ax.set_title("Distribución de edades según abandono")
    ax.set_xlabel("Edad")
    ax.set_ylabel("Densidad")
    st.pyplot(fig)
elif modulo == "Graficar la distribución de Balance según el estado de abandono":
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.kdeplot(
    data=full_data,
    x="Balance",
    hue="Exited",
    fill=True,
    ax=ax
    )
    ax.set_title("Distribución de Balance según el estado de abandono")
    ax.set_xlabel("Balance")
    ax.set_ylabel("Densidad")
    st.pyplot(fig)

# 4.- Presentación Resultados
moduloPresentacionResultados = st.sidebar.selectbox("4.- Presentación Resultados:", 
                                                    ["Selecciona",
                                                     "Modelo Random Forest"]) 
# Espacio donde se mostrará todo
contenido = st.empty()

# Si no hay selección → pantalla limpia
if exploracion =="Selecciona" and modulo == "Selecciona" and moduloPresentacionResultados == "Selecciona":
    contenido.empty()
    
if moduloPresentacionResultados  == "Selecciona":
    pass
elif moduloPresentacionResultados  == "Modelo Random Forest":
        # Espacio donde se mostrará todo
        with contenido.container():
            st.title("Random Forest")
            st.write("Aquí salen los datos del modelo")

        # 2.1. Modelo 1
        from sklearn.model_selection import train_test_split
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.metrics import (
            classification_report,
            confusion_matrix,
            accuracy_score
        )
        
        # Eliminar columnas que no sirven
        full_data = full_data.drop(['Surname', 'CustomerId'], axis=1)
        
        # Convertir texto a números
        full_data = pd.get_dummies(
            full_data,
            columns=['Geography', 'Gender'],
            drop_first=True
        )
        
        # Variable objetivo
        X = full_data.drop('Exited', axis=1)
        y = full_data['Exited']
        
        # Revisar vacíos
        X = X.fillna(0)
        
        # Separar datos
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.5,
            random_state=42
        )
        
        # Crear modelo
        model = RandomForestClassifier(
            n_estimators=100,
            random_state=42
        )
        
        # Entrenar
        model.fit(X_train, y_train)
        
        # Predicción
        y_pred = model.predict(X_test)
        
        # Mostrar predicciones
        st.write("Predicciones:")
        st.write(y_pred)
        
        # Comparación
        resultado = X_test.copy()
        resultado["Real"] = y_test.values
        resultado["Predicción"] = y_pred
        
        st.write("Comparación:")
        st.dataframe(resultado.head(20))
        
        # Precisión
        accuracy = accuracy_score(y_test, y_pred)
        
        st.write("Precisión del modelo:")
        st.write(accuracy)
        
        # Matriz de confusión
        cm = confusion_matrix(y_test, y_pred)
        
        st.write("Matriz de confusión:")
        st.write(cm)
        
        # Reporte
        st.text(classification_report(y_test, y_pred))
