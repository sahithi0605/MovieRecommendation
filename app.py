# importing the libraries
import  pickle
import streamlit as st
import requests
import pandas as pd
import time
from config import API_KEY


# set page configurations
st.set_page_config(
     page_title="Recommender System",
     layout="wide",
     initial_sidebar_state="auto"
 )

# fetch poster from api using movie_id and api key 
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key={}".format(movie_id, API_KEY)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    if poster_path is not None:
        full_path = "https://image.tmdb.org/t/p/original" + poster_path
    else:
        full_path = "https://image.tmdb.org/t/p/original"    
    return full_path


# function for recommendation
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:10]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters

st.markdown("<h1 style='text-align: center; color: white;'> MovieZone</h1>", unsafe_allow_html=True)
#st.title('MovieZone')
st.markdown("<h2 style='text-align: left; color: brown;'>Movie Recommendation System</h2>", unsafe_allow_html=True)
movies = pd.read_pickle(open('movie_list.pkl','rb'))
similarity = pd.read_pickle(open('similarity.pkl','rb'))
crews = pd.read_pickle(open('cast.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Search",
    movie_list
    ) 

# function to call fetch_poster
def selected(movie):
    index = movies[movies['title'] == movie].index[0]
    movie_id = movies.iloc[index].movie_id
    return fetch_poster(movie_id)

# function returning details of selected movie
def load_details(movie):
    index = movies[movies['title'] == movie].index[0]
    movie_id = movies.iloc[index].movie_id
    url = "https://api.themoviedb.org/3/movie/{}?api_key=a70cc3ea856f2db01379a6eef22257d8".format(movie_id)
    data = requests.get(url)
    data = data.json()
    a = data['overview']
    b = data['title']
    c = data['release_date']
    aa = data['tagline']
    bb = data['vote_average']
    link = data['homepage']
    return a,b,c,aa,bb,link

# function to get cast crew and director details
def crew_details(movie):
    r = []
    s = []
    mov = crews[crews['title'] == movie].index[0]
    url = "https://api.themoviedb.org/3/movie/{}?api_key=a70cc3ea856f2db01379a6eef22257d8".format(mov)
    data = requests.get(url)
    data = data.json()
    r = crews.loc[mov].crew
    s = crews.loc[mov].cast
    genres = []
    for i in range (0,len(data['genres'])):
        genres.append(data['genres'][i]['name'])
    return r[0],s,str(genres)[1:-1]


poster = selected(selected_movie)
x, y, z ,xx,yy,link= load_details(selected_movie)
a1, b1,c1 = crew_details(selected_movie)
st.subheader(selected_movie)
st.write(xx)
col1, col2 = st.columns(2)
with col1:
    st.image(poster,width=400)
with col2:
    st.markdown("<h6 style='text-align: left; color: brown;'>Overview:</h6>", unsafe_allow_html=True)
    st.write(x)
    st.markdown("<h6 style='text-align: left; color: brown;'>Release Date:</h6>", unsafe_allow_html=True)
    st.write(z)
    st.markdown("<h6 style='text-align: left; color: brown;'>Genres:</h6>", unsafe_allow_html=True)
    st.write(c1)
    st.markdown("<h6 style='text-align: left; color: brown;'>Director:</h6>", unsafe_allow_html=True)
    st.write(a1)
    st.markdown("<h6 style='text-align: left; color: brown;'>Cast:</h6>", unsafe_allow_html=True)
    st.write(b1[0],',',b1[1],',',b1[2])
    st.markdown("<h6 style='text-align: left; color: brown;'>Rating:</h6>", unsafe_allow_html=True)
    st.write(yy,"/10")
    st.markdown("<h6 style='text-align: left; color: brown;'></h6>", unsafe_allow_html=True)
    st.write(link)
 
 
if st.button('Recommend'):
    #with st.spinner('Loading....'):
     #   time.sleep(0.5)    
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4= st.columns(4)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0],width=200)
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1],width=200)

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2],width=200)
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3],width=200)

    col5, col6, col7, col8= st.columns(4)
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4],width=200)
    with col6:
        st.text(recommended_movie_names[5])
        st.image(recommended_movie_posters[5],width=200)  
    with col7:
        st.text(recommended_movie_names[6])
        st.image(recommended_movie_posters[6],width=200)
    with col8:
        st.text(recommended_movie_names[7])
        st.image(recommended_movie_posters[7],width=200)
    
# for sentiment analysis
from textblob import TextBlob
st.write(" Real Time Sentiment Analyzer ")
input = st.text_input("Enter Your Review...")
score = TextBlob(input).sentiment.polarity
if score==0:st.write("Neutral 😐")
elif score<0:st.write("Negative 😫")
elif score>0:st.write("Positive 😀")      
