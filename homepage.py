import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import io

# streamlit run /Users/gulden/Desktop/Python_1sem/FinalProject_Prog_DataScience_1semestr/homepage.py
# colors: blue, green, orange, red, violet, gray, grey, rainbow


# --------Import database--------
not_clean_database = pd.read_csv("jobs_in_data.csv")
not_clean_database = pd.DataFrame(not_clean_database, dtype=object)

# --------Some functions--------
#    This function prints unique values for each column in the given DataFrame.
def print_unique_values(dataframe):
    for column in dataframe.columns:
        unique_values = dataframe[column].unique()
        st.write(f"**{column.lower()} unique values:** {', '.join(map(str, unique_values))}")



# --------Start work with Streamlit--------

st.set_option('deprecation.showPyplotGlobalUse', False)


# ----Here folder design----
st.set_page_config(
    page_title="Jobs and Salaries in Data Science",
    page_icon="👩‍💻",
    layout="wide",
)


# ----Try to create menu----

# Manual item selection
if st.session_state.get('switch_button', False):
    st.session_state['menu_option'] = (st.session_state.get('menu_option', 0) + 1) % 4
    manual_select = st.session_state['menu_option']
else:
    manual_select = None

# Add on_change callback
def on_change(key):
    selection = st.session_state[key]
    st.write(f"Selection changed to {selection}")

# for easily change name of options 
Exploring = 'Exploring the dataset'
Cleaning = 'Data set cleaning'
Plots = 'Interesting plots'
Models = 'Models explaining the data'

# Menu
with st.sidebar:
    selected = option_menu(
        None, [Exploring, Cleaning, Plots, Models], 
        icons=['1-circle', '2-circle', '3-circle', '4-circle'],
        menu_icon="none",
        default_index=0,
        manual_select=manual_select,
        on_change=on_change,
        key='menu_main',
        styles={
        "container": {"padding": "15px!important", "background-color": "#00BF48"},
        "icon": {"color": "orange", "font-size": "20px"}, 
        "nav-link": {"font-size": "20px",  "color": "white", "text-align": "left", "margin":"0px", "--hover-color": "#076A2D"},
        "nav-link-selected": {"background-color": "#fafafa", "color": "black" , "font-weight": "normal"},
        }
    ) 
    selected

# 1 page
if selected == Exploring:
    st.header('Research about :green[Jobs and Salaries in Data Science] ', divider='green')
    st.subheader(Exploring)

    st.write('We will work with this database, here link to [Kaggle](https://www.kaggle.com/datasets/hummaamqaasim/jobs-in-data/data)')
    st.write(f"**Database have {not_clean_database.shape[1]} columns and {not_clean_database.shape[0]} rows**")


    #See first rows
    st.write(":green[**Let's see first 5 rows:**]")
    st.dataframe(not_clean_database.head())


    # See some statistics
    st.write(':green[**Summary statistics**]')
    st.write(not_clean_database.describe().T)

    #Missing values check
    st.write(":green[**Check for missing values:**]")
    st.dataframe(not_clean_database.isnull().sum())

    # Vizualization of histogram of salary
    st.write(":green[**Salary schedule:**]")
    fig, ax = plt.subplots(figsize=(6, 4))
    not_clean_database['salary_in_usd'].hist(ax=ax, bins=100,color='green')
    st.pyplot(fig)

    # Max and min
    st.write(":green[**Maximum and minimum salary in USD:**]")
    st.write(f"Maximum = {not_clean_database.salary_in_usd.max()} USD")
    st.write(f"Minimum = {not_clean_database.salary_in_usd.min()} USD")

    # Rename columns
    st.write(":green[**Let's rename the columns to something more convenient**]")
    not_clean_database.columns = not_clean_database.columns.str.replace('_', ' ').str.lower().str.title()
    st.dataframe(not_clean_database.head())

    # Info
    st.write(':green[**Some info**]')
    db_info_buffer = io.StringIO()
    not_clean_database.info(buf=db_info_buffer)
    st.text(db_info_buffer.getvalue())

    # Unique data too long output(not beautiful)
    #st.write(':green[**Unique data**]')
    #print_unique_values(not_clean_database)

    st.write(':green[**Job categories**]')
    fig, ax = plt.subplots(figsize=(6, 4))
    not_clean_database['Job Category'].value_counts().plot(kind='bar', ax=ax, color='green')
    ax.set_xlabel('Category')
    ax.set_ylabel('Number')
    ax.set_title('Info about job categories')
    st.pyplot(fig)
    


# 2 page
if selected == Cleaning:
    st.header('Research about :green[Jobs and Salaries in Data Science] ', divider='green')
    st.subheader(Cleaning)

# 3 page
if selected == Plots:
    st.header('Research about :green[Jobs and Salaries in Data Science] ', divider='green')
    st.subheader(Plots)

# 4 page
if selected == Models:
    st.header('Research about :green[Jobs and Salaries in Data Science] ', divider='green')
    st.subheader(Models)

