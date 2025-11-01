
import streamlit as st   
import pickle            
import pandas as pd     
import requests 




movies_dict = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))


if isinstance(movies_dict, dict):
    movies = pd.DataFrame(movies_dict)
else:
    movies = movies_dict  


TMDB_API_KEY = 'e628486ad8e5ce2027fece58aa50c0ab'  # Your API key
TMDB_BASE_URL = "https://api.themoviedb.org/3/movie/"

def fetch_poster(movie_id):
    """
    Fetch poster URL from TMDB given a movie ID.
    """
    url = f"{TMDB_BASE_URL}{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    response = requests.get(url)
    data = response.json()
    if 'poster_path' in data and data['poster_path']:
        return "https://image.tmdb.org/t/p/w500" + data['poster_path']
    else:
        return "https://via.placeholder.com/150"  # fallback placeholder
    



def recommend(movie):
    
    movie_index = movies[movies['title'] == movie].index[0]

    
    distances = similarity[movie_index]

    
    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    
    recommended_movies = []
    posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].get('movie_id', None)  # Use .get in case column missing
        recommended_movies.append(movies.iloc[i[0]].title)
        if movie_id:
            posters.append(fetch_poster(movie_id))
        else:
            posters.append("https://via.placeholder.com/150")  # fallback if movie_id missing

    return recommended_movies, posters

st.set_page_config(page_title="🎥 Movie Recommender", layout="wide")
st.title("🎬 Movie Recommender System")
st.write("Find movies similar to your favorites!")

# Dropdown for selecting a movie
selected_movie_name = st.selectbox(
    "Select a movie to get recommendations:",
    movies['title'].tolist()  # convert to list for selectbox
)

# Recommend button
if st.button('Recommend 🎯'):
    recommendations, posters = recommend(selected_movie_name)

    # Display recommended movies with posters
    if recommendations:
        st.subheader("Recommended Movies:")
        cols = st.columns(5)  # display in 5 columns

        for col, movie, poster in zip(cols, recommendations, posters):
            col.image(poster, use_column_width=True)
            col.markdown(f"**{movie}**")