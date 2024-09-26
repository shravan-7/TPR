import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import csr_matrix
from joblib import Memory
import os

# Use joblib for caching to speed up repeated computations
cache_dir = os.path.join(os.path.dirname(__file__), '.cache')
memory = Memory(location=cache_dir, verbose=0)

@memory.cache
def load_and_preprocess_data():
    places_df = pd.read_csv('replaced_locations.csv', chunksize=10000)
    places_df = pd.concat([chunk for chunk in places_df])
    places_df['combined_features'] = places_df['Category'] + ' ' + places_df['City']

    ratings_df = pd.read_csv('user_ratings5.csv', chunksize=10000)
    ratings_df = pd.concat([chunk for chunk in ratings_df])
    return places_df, ratings_df

@memory.cache
def compute_tfidf_matrix(combined_features):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(combined_features)
    return tfidf, tfidf_matrix

def create_user_item_matrix(ratings_df):
    user_ids = ratings_df['user_id'].unique()
    place_ids = ratings_df['place_id'].unique()
    user_id_map = {id: index for index, id in enumerate(user_ids)}
    place_id_map = {id: index for index, id in enumerate(place_ids)}

    row = ratings_df['user_id'].map(user_id_map)
    col = ratings_df['place_id'].map(place_id_map)
    data = ratings_df['rating']

    return csr_matrix((data, (row, col)), shape=(len(user_ids), len(place_ids))), user_id_map, place_id_map

def get_cf_scores(user_item_matrix, user_id_map, user_id, n_similar=10):
    if user_id not in user_id_map:
        return np.zeros(user_item_matrix.shape[1])

    user_index = user_id_map[user_id]
    user_vector = user_item_matrix[user_index].toarray().flatten()
    similarities = cosine_similarity(user_vector.reshape(1, -1), user_item_matrix.toarray())[0]
    similar_users = np.argsort(similarities)[::-1][1:n_similar+1]
    return user_item_matrix[similar_users].mean(axis=0).A1

def recommend(user_data):
    places_df, ratings_df = load_and_preprocess_data()
    tfidf, tfidf_matrix = compute_tfidf_matrix(places_df['combined_features'])

    # Content-based part
    user_preferences = ' '.join(user_data['category_preferences'] + user_data['location_preferences'])
    user_vector = tfidf.transform([user_preferences])
    content_similarity_scores = cosine_similarity(user_vector, tfidf_matrix).flatten()

    # Collaborative filtering part
    user_item_matrix, user_id_map, _ = create_user_item_matrix(ratings_df)
    cf_scores = get_cf_scores(user_item_matrix, user_id_map, user_data['user_id'])

    # Combine scores
    combined_scores = 0.5 * content_similarity_scores + 0.5 * cf_scores

    # Create a DataFrame with combined scores
    recommendations_df = pd.DataFrame({
        'Name': places_df['Name'],
        'combined_score': combined_scores,
        'Ratings': places_df['Ratings(5)']
    })

    # Sort by combined score and then by rating
    recommendations_df = recommendations_df.sort_values(by=['combined_score', 'Ratings'], ascending=[False, False])

    # Filter based on ratings
    recommendations_df = recommendations_df[recommendations_df['Ratings'] >= 4.0]

    # Get top 30 recommendations
    top_recommendations = recommendations_df.head(30)

    return list(top_recommendations['Name'])

# Example usage
if __name__ == "__main__":
    user_data = {
        'user_id': 1,  # Assume this is a new user
        'category_preferences': ['Historical', 'Nature'],
        'location_preferences': ['New York', 'California']
    }
    recommendations = recommend(user_data)
    print(recommendations)
