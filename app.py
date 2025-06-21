import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 CSV Data Viewer & Visualizer")

# for not load data everytime
@st.cache_data
def load_data(file):
    return pd.read_csv(file)

file = st.file_uploader("Upload File",type=["csv"], accept_multiple_files=False)

if file is not None:
    pf = load_data(file)

    st.subheader("🔍 Data Preview")

    n_rows = st.slider("Choose number of rows", min_value=1, max_value=len(pf), step=1, value=5)
    columns_show = st.multiselect("Choose columns", pf.columns.to_list(), default=pf.columns.to_list())
    st.dataframe(pf.loc[:n_rows - 1, columns_show])


    st.subheader("📈 Scatter Plot")

    numeric_cols = pf.select_dtypes(include=["number"]).columns.tolist()
    if len(numeric_cols) < 2:
        st.warning("Need at least 2 numeric columns to create scatter plot.")
    else:
        col1, col2, col3 = st.columns(3)

        with col1:
            x_col = st.selectbox("X-axis", numeric_cols)
        with col2:
            y_col = st.selectbox("Y-axis", numeric_cols, index=1 if len(numeric_cols) > 1 else 0)
        with col3:
            color = st.selectbox("Color by", pf.columns.to_list())

        fig = px.scatter(pf, x=x_col, y=y_col, color=color, title=f"{y_col} vs {x_col}")
        st.plotly_chart(fig, use_container_width=True)