import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.metrics.pairwise import euclidean_distances
from scipy.spatial import distance
import folium


df = pd.read_csv('open_pubs_cleaned.csv')

def home():
    st.title('Welcome to the Pubs of the UK')
    st.image('untitled-24 - Twin Perspectives.jpeg')
    st.write('There are a total of', len(df), 'pubs in the dataset')
    st.write('Here are some basic statistics about the dataset:')
    st.write(df.describe())


def pub_locations():
    st.title('Explore Pubs in the UK by Location')
    area = st.text_input('Enter a Postal Code or Local Authority')
    pubs = df[df['postcode'].str.contains(area, na=False, case=False)]
    fig = px.scatter_mapbox(pubs, lat='latitude', lon='longitude', hover_name='name', hover_data=['address', 'local_authority', 'postcode'], zoom=10)
    fig.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig)


def euclidean_distance(x1, y1, x2, y2):
    return distance.euclidean((x1, y1), (x2, y2))

def nearest_pub():
    st.title('Find the Nearest Pub')

    # get user input for latitude and longitude
    lat = st.number_input('Enter your latitude:')
    lon = st.number_input('Enter your longitude:')

    # calculate distances to all pubs and add as a column to the DataFrame
    df['distance_to_user'] = df.apply(lambda row: euclidean_distance(lat, lon, row['latitude'], row['longitude']), axis=1)
    nearest_pubs = df.sort_values(by='distance_to_user').head(5)

    # create a map centered on the user's location
    m = folium.Map(location=[lat, lon], zoom_start=13)

    # add markers for the nearest pubs to the map
    for index, row in nearest_pubs.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=row['name'],
            icon=folium.Icon(color='green')
        ).add_to(m)

    # display the map
    st.write('The nearest pubs to your location are:')
    st.write(nearest_pubs[['name', 'address', 'distance_to_user']])
    st.write(m)

