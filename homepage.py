import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import io

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

    # Rename columns (because it is in "if" it doesnt work for another pages)
    # st.write(":green[**Let's rename the columns to something more convenient**]")
    # not_clean_database.columns = not_clean_database.columns.str.replace('_', ' ').str.lower().str.title()
    # st.dataframe(not_clean_database.head())

    # Info
    st.write(':green[**Some info**]')
    db_info_buffer = io.StringIO()
    not_clean_database.info(buf=db_info_buffer)
    st.text(db_info_buffer.getvalue())

    # see categories in plot
    st.write(':green[**Job categories**]')
    fig, ax = plt.subplots(figsize=(6, 4))
    not_clean_database['job_category'].value_counts().plot(kind='bar', ax=ax, color='green')
    ax.set_xlabel('Category')
    ax.set_ylabel('Number')
    ax.set_title('Info about job categories')
    plt.xticks(rotation=80)
    st.pyplot(fig)

    # Experience level on plot
    st.write(':green[**Experience level**]')
    fig, ax = plt.subplots(figsize=(6, 4))
    not_clean_database['experience_level'].value_counts().sort_index().plot(kind='bar', ax=ax, color='green')
    ax.set_xlabel('Level')
    ax.set_ylabel('Number')
    ax.set_title('Experience Levels')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    #Employment type on plot
    st.write(':green[**Employment type**]')
    fig, ax = plt.subplots(figsize=(6,4))
    db_employment_type = not_clean_database['employment_type'].value_counts().sort_index()
    db_employment_type.plot(kind='bar',color='green',ax=ax)
    ax.set_xlabel('Type')
    ax.set_ylabel('Number')
    ax.set_title('Employment type')
    plt.xticks(rotation=45)
    # Adding numbers
    for i, v in enumerate(db_employment_type):
        ax.text(i, v + 0.1, str(v), ha='center', color='black')
    st.pyplot(fig)

    # Years and work count
    st.write("**:green[Work years]**")
    fig, ax = plt.subplots(figsize=(6,4))
    not_clean_database['work_year'].value_counts().sort_index().plot(ax=ax,color='green',kind='bar')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number')
    ax.set_title('Work years')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Average Salaries per year in USD
    st.write("**:green[Average salaries]**")
    average_salary_per_year = not_clean_database[['work_year','salary_in_usd']].groupby('work_year').mean()
    st.dataframe(average_salary_per_year)

#i wrote it here because inside of "if" statement it will not work for another pages. I'm cleaning db here
clean_database = not_clean_database.drop(columns=['salary', 'salary_currency'])
usd_to_euro_exchange_rate = 0.92
clean_database['salary_in_euro'] = clean_database['salary_in_usd'] * usd_to_euro_exchange_rate
clean_database = clean_database.drop(columns=['salary_in_usd'])

#deleting all non EU countries
european_union_countries = [
    'Germany', 'Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic',
    'Denmark', 'Estonia', 'Finland', 'France', 'Greece', 'Hungary', 'Ireland', 'Italy',
    'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 'Netherlands', 'Poland', 'Portugal',
    'Romania', 'Slovakia', 'Slovenia', 'Spain', 'Sweden'
]
european_union_db = clean_database[clean_database['company_location'].isin(european_union_countries)]


# 2 page
if selected == Cleaning:
    st.header('Research about :green[Jobs and Salaries in Data Science] ', divider='green')
    st.subheader(Cleaning)

    st.write("**:green[Let's remove some columns that we won't use: 'salary' , 'salary_in_usd' and 'salary_currency'. Since we did 'salary_in_euro', here is our new database:]**")
    st.dataframe(clean_database)

    # Unique data too long output(not beautiful)
    #st.write(':green[**Unique data**]')
    #print_unique_values(clean_database)
    
    st.write("**:green[I want to work only with EU countries, so we will remove all rows containing information about working outside the European Union]**")
    st.dataframe(european_union_db)

    st.write(f"**Now database have {european_union_db.shape[1]} columns and {european_union_db.shape[0]} rows**")



# 3 page
if selected == Plots:
    st.header('Research about :green[Jobs and Salaries in Data Science] ', divider='green')
    st.subheader(Plots)

    # Pie type plot for showing salary per year in european countries
    st.write("**:green[Average Salary Per Year]**")
    fig, ax = plt.subplots()
    european_union_db.groupby('work_year')['salary_in_euro'].mean().plot(kind='pie', autopct='%1.1f%%')
    st.pyplot(fig)

    # Top Job Titles
    st.write("**:green[Top 5 Job Titles]**")
    fig, ax = plt.subplots(figsize=(6, 4))
    top_job_titles = european_union_db['job_title'].value_counts().head(5)
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(top_job_titles.index, top_job_titles.values, color='green')
    ax.set_xlabel('Job Title')
    ax.set_ylabel('Count')
    ax.set_title('Top 5 Job Titles')
    plt.xticks(rotation=45)
    st.pyplot(fig)


# 4 page
if selected == Models:
    st.header('Research about :green[Jobs and Salaries in Data Science] ', divider='green')
    st.subheader(Models)

