import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title='Adverse_Effects',page_icon = "bar_chart",layout = "wide")
st.title(":bar_chart: Adverse Events EDA")
st.markdown('<style>dic.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

#os.chdir(r"C:\Users\Asus\PycharmProjects\pythonProject\venv")
df = pd.read_excel("Adverse_Events.xlsx")

col1,col2 = st.columns((2))
# df['ASTDT'] = pd.to_datetime(df["ASTDT"])
# df['AENDT'] = pd.to_datetime(df['AENDT'])

# startDate = pd.to_datetime((df['ASTDT']).min())
# endDate = pd.to_datetime((df['ASTDT']).max())

# with col1:
#     date1 = pd.to_datetime(st.date_input("Start Date",startDate))

# with col2:
#     date2 = pd.to_datetime(st.date_input("End Date",endDate))

# df = df[(df["ASTDT"]>= date1) & (df["ASTDT"]<= date2)].copy()
##sidebar for placebo,low and high dose
st.sidebar.header("Choose your filter: ")
subject = st.sidebar.multiselect("Pick your subject",df["USUBJID"].unique())
if not subject:
    df1 = df.copy()
else:
    df1 =df[df["USUBJID"].isin(subject)]
treatment = st.sidebar.multiselect("Pick your treatment",df["TRTA"].unique())
if not treatment:
    df2  = df1.copy()
else:
    df2 = df1[df1["TRTA"].isin(treatment)]
## aeterm
ae = st.sidebar.multiselect("Pick the adverse event term",df2["AETERM"].unique())
if not ae:
    df3 = df2.copy()
else:
    df3 = df2[df2["AETERM"].isin(ae)]

if not treatment and not ae and not subject:
    filter_df = df
elif not ae and not subject:
    filter_df = df[df["TRTA"].isin(treatment)]
elif not treatment and not subject:
    filter_df = df[df["AETERM"].isin(ae)]
elif ae and subject:
    filter_df = df[df["AETERM"].isin(ae) & df["USUBJID"].isin(subject)]
elif treatment and subject:
    filter_df = df[df["TRTA"].isin(treatment) & df["USUBJID"].isin(subject)]
elif treatment and ae:
    filter_df = df[df["TRTA"].isin(treatment) & df["AETERM"].isin(ae)]
elif subject:
    filter_df = df[df["USUBJID"].isin(subject)]
else:
    filter_df = df[df["TRTA"].isin(treatment) & df["AETERM"].isin(ae) & df["USUBJID"].isin(subject)]

category_df = filter_df.groupby(by = ["TRTA"],as_index = False)["BMIBL"].mean()
category_df1 = filter_df.groupby(by = ["TRTA"],as_index=False)["WGTBL"].mean()
category_df2 = filter_df.groupby(by = ["TRTA"],as_index=False)["HGTBL"].mean()

with col1:
    st.subheader("Treatment wise BMI")
    fig = px.bar(category_df,x = "TRTA",y = "BMIBL",template="seaborn")
    st.plotly_chart(fig,use_container_width=True,height = 200)

with col2:
    st.subheader("Treatment wise BMI Boxplot")
    fig = px.box(filter_df,x = "TRTA",y = "BMIBL",template = "seaborn")
    st.plotly_chart(fig,use_container_width=True,height = 200)

with col1:
    st.subheader("Treatment wise Weight")
    fig = px.bar(category_df1,x = "TRTA",y = "WGTBL" ,template = "seaborn")
    st.plotly_chart(fig,use_container_width=True,height = 200)

with col2:
    st.subheader("Treatment wise Weight Boxplot")
    fig = px.box(filter_df,x = "TRTA",y = "WGTBL",template = "seaborn")
    st.plotly_chart(fig,use_container_width=True,height = 200)

with col1:
    st.subheader("Treatment wise Height")
    fig = px.bar(category_df2,x = "TRTA",y = "HGTBL",template="seaborn")
    st.plotly_chart(fig,use_container_width=True,height = 200)

with col2:
    st.subheader("Treatment wise Height Boxplot")
    fig = px.box(filter_df,x = "TRTA",y = "HGTBL",template = "seaborn")
    st.plotly_chart(fig,use_container_width=True,height = 200)

with col1:
    st.subheader("Treatment wise Adverse event")
    fig = px.bar(filter_df.dropna(),x = "USUBJID",y = "AETERM",text = [i for i in filter_df.dropna()['ADURN']],template="seaborn")
    st.plotly_chart(fig,use_container_width=True,height = 200)

category__df3 = filter_df.groupby(by = ["USUBJID"],as_index = False)["AESEV"].value_counts()

with col2:
    st.subheader("Severity")
    fig = px.pie(category__df3,names = "AESEV",values="count",color = "AESEV",template="seaborn")
    st.plotly_chart(fig,use_container_width=True,height = 200)

category_df4 = filter_df.groupby(by = ["USUBJID"],as_index = False)["AEREL"].value_counts()

with col1:
    st.subheader("Remote")
    fig = px.pie(category_df4,names = "AEREL",values="count",color = "AEREL",template = "seaborn")
    st.plotly_chart(fig,use_container_width=True,height = 200)
