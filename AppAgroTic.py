import time  # to simulate a real time data, time loop
import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development
from PIL import Image


st.set_page_config(
    page_title="AgroTic Dashboard",
    page_icon="✅",
    layout="wide",
)

# read csv from a github repo
dataset_url = "DataOpCul.csv"
dataset_urlD = "DatafE.csv"
dataset_urlT = "temperatura.csv"
dataset_urlC = "costo2.csv"
image = Image.open('Printl-Plant.png')

# read csv from a URL
@st.experimental_memo
def get_data(url) -> pd.DataFrame:
    return pd.read_csv(url)

df = get_data(dataset_url)
dfD = get_data(dataset_urlD)
dfT = get_data(dataset_urlT)
dfC = get_data(dataset_urlC)
dfD = dfD.dropna()

# dashboard title
st.title("MakeSens")

st.image(image)


st.write('Para poder obtener los datos historicos, seleccione el cultivo a analizar: ')
# top-level filters
device_filter = st.selectbox("Seleccione el cultivo", pd.unique(df["Cultivo"]))
#device_filterD = st.selectbox("Seleccione el dispositivo", pd.unique(dfD["Name"]))

# creating a single-element container
placeholder = st.empty()

# dataframe filter
df = df[df["Cultivo"] == device_filter]
condicion = df["Valor"].idxmax()
dfC = dfC[dfC["Nombre"] == device_filter]
dfD = dfD[dfD["Name"] == df["Dispositivo"][condicion]]
dfT = dfT[dfT["Nombre"] == device_filter]
# near real-time / live feed simulation


# Parrafo

for seconds in range(200):

    with placeholder.container():
        st.info('Para el cultivo de: '+device_filter+', la zona más efectiva es la que mide el dispositivo: '+df["Dispositivo"][condicion])
        # create three columns
        #
        #st.success('Del cultivo: '+device_filter+' se pueden producir '+str(int(dfC["Peso.hectarea"][0]))+' pesos por hectaria')
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)

        # fill in those three columns with respective metrics or KPIs
        kpi1.metric(
            label="Cultivo ",
            value=device_filter,
        )

        kpi2.metric(
            label="Temperatua Mínima ＄",
            value=dfT["temperatura.min"],
        )

        kpi3.metric(
            label="Temperatua Máxima 💍",
            value=dfT["temperatura.max"],
        )

        kpi4.metric(
            label="Zona óptima",
            value=df["Dispositivo"][condicion],
        )

        # create two columns for charts
        fig_col1, fig_col2 = st.columns(2)
        with fig_col1:
            st.markdown("## Eficacia Dispotivos")
            fig = px.line(
                data_frame=df, y="Valor", x="Dispositivo"
            )
            st.write(fig)

        with fig_col2:
            st.markdown("## Zona óptima ⏳")
            fig2 = px.line(
                data_frame=dfD, y="temperatura", x="Fecha"
                #color = 'country'
            )
            st.write(fig2)
        st.markdown("### Detailed Data View")
        st.dataframe(df)
        st.markdown("### Detailed Data View")
        st.dataframe(dfD)
        time.sleep(1)
