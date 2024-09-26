import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.impute import SimpleImputer
from joblib import Memory

# Use joblib for caching to speed up repeated computations
memory = Memory(location='.cache', verbose=0)

@memory.cache
def load_and_preprocess_data():
    places_df = pd.read_csv('replaced_locations.csv')
    places_df['combined_features'] = places_df['Category'] + ' ' + places_df['City']
    ratings_df = pd.read_csv('user_ratings5.csv')
    return places_df, ratings_df

@memory.cache
def compute_tfidf_matrix(combined_features):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(combined_features)
    return tfidf, tfidf_matrix

def create_user_item_matrix(ratings_df):
    user_item_matrix = ratings_df.pivot(index='user_id', columns='place_id', values='rating').fillna(0)
    return user_item_matrix

def recommend(user_data):
    places_df, ratings_df = load_and_preprocess_data()
    tfidf, tfidf_matrix = compute_tfidf_matrix(places_df['combined_features'])

    # Content-based part
    user_preferences = ' '.join(user_data['category_preferences'] + user_data['location_preferences'])
    user_vector = tfidf.transform([user_preferences])
    content_similarity_scores = cosine_similarity(user_vector, tfidf_matrix).flatten()

    # Collaborative filtering part
    user_item_matrix = create_user_item_matrix(ratings_df)
    user_similarity = cosine_similarity(user_item_matrix)

    user_id = user_data['user_id']
    if user_id not in user_item_matrix.index:
        # New user, use only content-based filtering
        cf_scores = np.zeros(len(places_df))
    else:
        user_index = user_item_matrix.index.get_loc(user_id)
        similar_users = user_similarity[user_index].argsort()[::-1][1:11]  # top 10 similar users
        cf_scores = user_item_matrix.iloc[similar_users].mean().values

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
