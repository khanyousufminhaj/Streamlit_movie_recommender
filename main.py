import pandas as pd
import random
import difflib #to find similar movie names
from sklearn.feature_extraction.text import TfidfVectorizer #to convert textual data to vectors
from sklearn.metrics.pairwise import cosine_similarity #to find similarity of movie
import streamlit as st

st.title("Ineractive Movie Recommendation Website")
st.write("""# Explore movies similar to your favoirate movies
         """)

#loading dataset into a pandas dataframe
data=pd.read_csv("./movies.csv")
selected_features=['genres','keywords','original_title','tagline','cast','director']

#replacing null values with '' string
from sklearn.impute import SimpleImputer
imputer=SimpleImputer(fill_value='',strategy='constant')
movies_data=pd.DataFrame(imputer.fit_transform(data),columns=data.columns)

#combining features
combined_features = movies_data['genres']+' '+movies_data['keywords']+' '+movies_data['tagline']+' '+movies_data['cast']+' '+movies_data['director']+movies_data['original_title']

#converting text data to feature vectors
vectorizer=TfidfVectorizer()
feature_vectors=vectorizer.fit_transform(combined_features)

similarity=cosine_similarity(feature_vectors)

user_input=st.text_input("Give name of your favoirate movie: ")

#creating a list of all movie names in the dataset
list_of_titles=movies_data['original_title'].tolist()

#finding close match to the name of movie 
find_close_match=difflib.get_close_matches(user_input,list_of_titles)

def get_recommendation_list(number_of_recommendation,mode):
    if mode=='Creative':
        recommended=sorted_similarity_score[11:number_of_recommendations+10]
        random.shuffle(recommended)
    else:
        recommended=sorted_similarity_score[1:number_of_recommendations]
    
    return recommended

if find_close_match:
    close_match=find_close_match[0]

    #find index of close__match movie 
    close_match_index=close_match_index=movies_data[movies_data.original_title==close_match]['index'].values[0]

    similarity_score=list(enumerate(similarity[close_match_index]))

    sorted_similarity_score=sorted(similarity_score,key=lambda x:x[1],reverse=True)

    number_of_recommendations=st.slider('Number of Recomendations',5,100,value=25)
    mode=st.selectbox('Recommendation Mode',{'Classic','Creative'},index=1)
    recommended=get_recommendation_list(number_of_recommendations,mode)
    st.write("## Recommended movies:")
    for movie in recommended:
        index=movie[0]
        title_from_index=movies_data[movies_data.index==index]['title'].values[0]
        st.write(title_from_index)


