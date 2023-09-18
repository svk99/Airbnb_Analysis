import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static
import ast

df = pd.read_csv('.../airbnb.csv')

st.title('Airbnb Analysis')
t1,t2,t3,t4,t5=st.tabs(['Heatmap','Price table','Graphical Analysis','Geomapping','Insights'])

with t1:
    st.subheader('Heatmap')
    if st.button('Show',key='a'):
        col=['price', 'monthly_price', 'bedrooms', 'reviews_per_month', 'maximum_nights']
        fig, ax = plt.subplots(figsize=(12, 10))
        heatmap_data = df[col].corr()
        sns.heatmap(heatmap_data, cmap='crest', annot=True, fmt='.2f',ax=ax)
        plt.title('Heatmap of Column Relationships')
        st.pyplot(fig)
        plt.close(fig)
with t2:
    st.subheader('Price Table')
    country = st.selectbox('Select a country', df['country'].unique())
    room = st.selectbox('Select a roomtype', df['room_type'].unique())
    bedroom = st.selectbox('Select number of bedrooms', df['bedrooms'].unique())
    if st.button('Show table'):
        filtered_df = df[(df['country'] == country) & (df['room_type'] == room) & (df['bedrooms'] == bedroom)]
        columns_to_display = ['name', 'price', 'availability', 'reviews_per_month', 'maximum_nights']
        st.table(filtered_df[columns_to_display])
with t3:
    st.subheader('Graphical Analysis')
    df['price'] = df['price'].apply(lambda x: float(str(x)))
    category = st.selectbox('Select a category', ['None', 'property_type', 'room_type', 'bed_type', 'country'])
    if st.button('Show',key='b'):
        if category != 'None':
            sns.set(style="whitegrid")
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.barplot(x=category, y='price', data=df, ax=ax, ci=None)
            ax.set_xlabel(category)
            ax.set_ylabel('price')
            ax.set_title('Price Distribution')
            ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
            st.pyplot(fig)
            plt.close(fig)
with t4:
    st.subheader('Geomapping')
    df = df.sample(n=100, random_state=42)
    m = folium.Map(location=[0, 0], zoom_start=4)

    for index, row in df.iterrows():
        lon, lat = ast.literal_eval(row['coordinates'])
        tooltip_content = f"Name: {row['name']}<br>Country: {row['country']}<br>Price: {row['price']}" \
                          f"<br>Weekly_Price: {row['weekly_price']}<br>Monthly_Price: {row['monthly_price']}"

        folium.Marker(
            location=[lat, lon],
            tooltip=folium.Tooltip(tooltip_content, sticky=True)  # Display tooltip on hover
        ).add_to(m)

    folium_static(m, width=800, height=600)
with t5:
    st.subheader('Insights')
    df = pd.read_csv('C:/Users/admin/Desktop/zenclass/prj4_data/airbnb.csv')
    df['price']=df['price'].apply(lambda x:int(x))

    st.write('5 most expensive Airbnb')
    top_price = df.sort_values(by='price', ascending=False).head()
    st.table(top_price[['name', 'price', 'country']])

    st.write('5 least expensive Airbnb')
    least_price = df.sort_values(by='price', ascending=True).head()
    st.table(least_price[['name', 'price', 'country']])