import streamlit as st
import pandas as pd
# import plotly.express as px
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from streamlit_folium import folium_static, st_folium
import folium



# Reading in the data
provisional_death = pd.read_csv('accurate_provisional.csv')
#Layout
st.set_page_config(
    page_title="US Death Overdoses",
    layout="centered",
    initial_sidebar_state="expanded")

# Cache 
@st.cache_data
def load_data(csv):
    df = pd.read_csv(csv) 
    return df


#adding Image: 
st.image('drug1.jpeg', use_column_width=True, width=200)
st.title('Overdose Deaths in the US 2015-2023')
st.subheader('Center of Disease Control and Prevention')

# #title 
# st.title('Overdose Deaths in the US 2015-2023')

#tabs options 
intro_tab, Analysis_tab, source_tab=st.tabs(['Intro 🎈','Analysis 🌍','Sources📜'])

# # Sidebar
# with st.sidebar:
#     st.title('Welcome!')
#     option = st.radio('Select Option', ['Intro 🎈', 'Analysis 🌍'])


with intro_tab:
    st.write('Introduction:  US deaths from 2015 to 2023 with a 12- month period ')
    st.write('This analysis delves into a dataset sourced from the Centers for Disease Control and Prevention The dataset, updated monthly, serves as a comprehensive resource illuminating the trajectory of overdose-related fatalities across the nation')
    st.write('Data/operation abstraction designWhere did you get your data/How did you prepare your data ')
    st.write('Downloaded data from CDC concerning Drug Overdoses in the US. Preparation steps were to clean the data convert certain columns into different types such as objects to int or to floats for visualization')
    st.write('Future work Plans are underway to augment the dataset by integrating demographic information, particularly pertaining to ethnicity and race, thus enriching our understanding of disparities and enabling more tailored interventions.')
    st.write('In essence, this analysis represents not only a retrospective examination of past trends but also a clarion call to action, signaling the imperative for continued vigilance, research, and concerted efforts to address the multifaceted challenge of drug overdoses in the United States')


# Content for the 'Analysis' tab
with Analysis_tab:
        
    if st.checkbox("Show Data"):
        provisional_death
    

    # st.subheader('This is the Data!')
    # st.write(provisional_death)  # Display the entire DataFrame

    # Create tabs
    detail_tab = st.tabs(['Details'])
  
   
    #  for graph purposes
    state_names = sorted(provisional_death['State Name'].unique())  
    selected_state = ('state_names')
    filtered_data = provisional_death[provisional_death['State Name'] == selected_state]
    
    plt.figure(figsize=(18, 6))
    sns.barplot(data=filtered_data, x='Year', y='Data Value', color='lightblue')
    plt.xlabel('Year', fontsize=20)
    plt.ylabel('Number of Deaths', fontsize=20) 
    plt.xticks(fontsize=20)  #x axis tick labels
    plt.yticks(fontsize=20)  #y-axis tick labels
    
    
    chart = alt.Chart(state_names).mark_area(color="blue").encode(
       x=alt.X("Year", axis=alt.Axis(format="")),
       y= alt.Y("Potentially Excess Deaths", scale=alt.Scale(zero=False)),       
   ).properties(
   
   )
    ######TRIAL FOR NATIONWIDE #######TRIAL FOR LINE CHART FOR THE NATION US  
#adding death for data value 
    death=provisional_death['Data Value']
    year=provisional_death['Year']
    predicted=provisional_death['Predicted Value']
    # Filter data
    filtered_data = provisional_death.copy()  # Make a copy of the original DataFrame
    filtered_data = filtered_data[filtered_data['Data Value'] == death]
    predicted_data = provisional_death.groupby('Year')['Predicted Value'].mean().reset_index()

    # Prepare the data for predicted values
    predicted_data = provisional_death.groupby('Year')['Predicted Value'].mean().reset_index()
    chart_data = filtered_data.groupby('Year')['Data Value'].mean().reset_index()

    # Plotting with Altair
    chart = alt.Chart(chart_data).mark_line().encode(
    x=alt.X("Year", axis=alt.Axis(format="")),
    y=alt.Y("Data Value", scale=alt.Scale(zero=False), title="Death"),
    color=alt.value("blue")  # Specify the color for the actual data
    )

    # Predicted chart with legend label
    predicted_chart = alt.Chart(predicted_data).mark_line().encode(
    x=alt.X("Year", axis=alt.Axis(format="")),
    y=alt.Y("Predicted Value", scale=alt.Scale(zero=False), title="Predicted Death"),
    color=alt.value("red"),  # Specify the color for the predicted data
    )

    # Display the legend using Markdown
    st.markdown("### Legend")
    st.markdown("- **Blue Line**: Actual Data")
    st.markdown("- **Red Line**: Predicted Data")
    # Combine both charts
    combined_chart = chart + predicted_chart

    # Display the chart with legend
    st.altair_chart(combined_chart)


        ###CREATING BAR CHART WITH EXAMPLE### 
    state = provisional_death['State Name'].unique() # get the unique values of the State column that will be used to filter dataframes
    state_choice = st.selectbox('Select an State/Territory for More Details', state, index=0) # add a selectbox widget

    filtered_state_df = provisional_death.loc[provisional_death['State Name'] == state_choice] # filter the dataframe by the selected value
    styled_state_df = filtered_state_df.style.format({'Year': lambda x: f"{x:.0f}"}) # remove commas from the years (treated as float/int)
    yearly_sums_df = filtered_state_df.groupby('Year')['Data Value'].mean().reset_index() # group by 'Year' and sum the values for each year 

    st.dataframe(styled_state_df, hide_index =True, use_container_width=True, height= 140) # display the filterable dataframe
    st.set_option('deprecation.showPyplotGlobalUse', False)
        #configure graph
    plt.figure(figsize=(18, 6))
    sns.barplot(data=yearly_sums_df, x='Year', y='Data Value', color='blue')
    plt.xlabel('Year', fontsize=20)
    plt.ylabel('Data Value', fontsize=20)
    plt.xticks(fontsize=20)  #x axis tick labels
    plt.yticks(fontsize=20)  #y-axis tick labels 

        #plot graph
    st.pyplot()


  
with source_tab: 
    st.write(' Ahmad FB, Cisewski JA, Rossen LM, Sutton P. Provisional drug overdose death counts. National Center for Health Statistics. 2024.')
    st.write('Designed by LM Rossen, A Lipphardt, FB Ahmad, JM Keralis, and Y Chong: National Center for Health Statistics.')
    st.image('vsrrimage.jpeg')
    st.write('Lizeth Ildefonso-Bacilio')







