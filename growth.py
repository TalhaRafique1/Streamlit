import streamlit as st      
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout="wide" )

# custom css
st.markdown(
    """
    <style>
    .stApp {
    background-color: #f0f6f6;
    color: #000000;
        max-width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description
st.title("📀 Datasweeper Sterling Integrator By Talha Rafique")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization Creating the project for quarter 3!.")

# file uploader
uploaded_file = st.file_uploader("Upload your files (accepts CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=(True))

if uploaded_file:
    for file in uploaded_file:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:       
            st.error("unsupported file format: {file_ext}")
            continue

        # file details
        st.write(f"🔍 Preview the head of the Dataframe")
        st.dataframe(df.head())

        # data cleaning
        st.subheader("🧹 Data Cleaning options")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Remove duplicates from the file : {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates removed !")

            with col2:  
                if st.button(f"Fill missing values for : {file.name}"):
                    numeric_cols = df.select_dtypes(includes=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values have been filled!")

        st.subheader(" Select the columns to keep")
        columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]


        # data visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show data visualization for {file.name}"):
            st.bar_chart(df).select_dtypes(include=['number'].iloc[:, :2])

            # Conversion options
            st.subheader("🔄 Conversion Options")
            Conversion_type = st.radio(f"Convert {file.name} to: ", ["CSV", "Excel"], key=file.name)
            if st.button(f"Convert {file.name}"):
                buffer = BytesIO()
                if Conversion_type == "CSV":
                    df.to_csv(buffer, index=False)
                    file.name = file.name.replace(file_ext, ".csv")
                    mime_type = "text/csv"

                elif Conversion_type == "Excel":
                    df.to_excel(buffer, index=False)
                    file.name = file.name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                buffer.seek(0)
                     
                st.download_button(
                    label=f"Click here to download {file.name} as {Conversion_type}",
                    data=buffer,
                    file_name=file.name,
                    mime=mime_type
                )

                st.success("All files have been processed successfully!")
                