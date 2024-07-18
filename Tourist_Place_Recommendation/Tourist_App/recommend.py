import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer

import numpy as np
np.random.seed(0)  # or any other seed value
from surprise import Reader, Dataset, SVD


def recommend(user_data):
    places_df = pd.read_csv('replaced_locations.csv')
    ratings_df = pd.read_csv("user_ratings5.csv") 
    new_user_data = pd.DataFrame({'ID': user_data['ID'], 'Place_Ratings': user_data['Place_Ratings']})

    new_user_id = ratings_df['user_id'].max() + 1
    new_user_data['user_id'] = new_user_id

    ratings_df = pd.concat([ratings_df, new_user_data.rename(columns={'ID': 'place_id', 'Place_Ratings': 'rating'})])
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(ratings_df[['user_id', 'place_id', 'rating']], reader)
    trainset = data.build_full_trainset()
    algo = SVD(n_factors=50, n_epochs=30, lr_all=0.01, reg_all=0.05)
    algo.fit(trainset)

    user_preferences_category = user_data['category_preferences']
    user_preferences_location = user_data['location_preferences']

    all_categories = sorted(set(places_df['Category'].explode().unique()))
    all_locations = sorted(set(places_df['City'].explode().unique()))

    mlb_categories = MultiLabelBinarizer(classes=all_categories)
    mlb_locations = MultiLabelBinarizer(classes=all_locations)

    places_df['Category_List'] = places_df['Category'].apply(lambda x: [x] if isinstance(x, str) else [])
    places_df['Location_List'] = places_df['City'].apply(lambda x: [x] if isinstance(x, str) else [])

    category_matrix = mlb_categories.fit_transform(places_df['Category_List'])
    location_matrix = mlb_locations.fit_transform(places_df['Location_List'])

    user_category_vector = mlb_categories.transform([user_preferences_category])
    user_location_vector = mlb_locations.transform([user_preferences_location])

    category_sim_scores = cosine_similarity(user_category_vector, category_matrix).flatten()
    location_sim_scores = cosine_similarity(user_location_vector, location_matrix).flatten()
    print("categroy scores", category_sim_scores, "location_sim_scores", location_sim_scores)

    def hybrid_recommendation(new_user_id, places_df, ratings_df, algo, category_sim_scores, location_sim_scores, top_n=10):
        places_visited = ratings_df[ratings_df['user_id'] == new_user_id]['place_id'].unique()
        places_to_predict = places_df[~places_df['ID'].isin(places_visited)]
        
        predictions = []
        for _, row in places_to_predict.iterrows():
            place_id = row['ID']
            predicted_rating = algo.predict(new_user_id, place_id).est
            
            idx = places_df[places_df['ID'] == place_id].index[0]
            content_score_category = category_sim_scores[idx]
            content_score_location = location_sim_scores[idx]
            
            content_score = 0.8 * content_score_category + 0.2 * content_score_location
            content_rating = content_score * 5
            
            hybrid_score = 0.5 * predicted_rating + 0.5 * content_rating
            
            predictions.append((place_id, hybrid_score, row['Category'], row['Ratings(5)']))
        
        predictions_df = pd.DataFrame(predictions, columns=['place_id', 'hybrid_score', 'Category', 'Rating'])
        
        predictions_df.sort_values(by='hybrid_score', ascending=False, inplace=True)
        
        top_recommendations = predictions_df.head(top_n)
        print(top_recommendations)

        sorted_place_ids = top_recommendations['place_id'].tolist()
        
        recommended_places = places_df.loc[places_df['ID'].isin(sorted_place_ids)]
        recommended_places = recommended_places.set_index('ID').loc[sorted_place_ids].reset_index()
        
        return recommended_places[['ID', 'Name', 'City', 'Category', 'Ratings(5)']]

    recommended_places = hybrid_recommendation(new_user_id, places_df, ratings_df, algo, category_sim_scores, location_sim_scores, top_n=30)
    print(recommended_places)
    return list(recommended_places['Name'])


















# import numpy as np
# import pandas as pd
# import pickle
# from scipy.sparse import csr_matrix
# from sklearn.neighbors import NearestNeighbors
# def recommend(user_data):
#     ratings_df = pd.read_csv('user_ratings5.csv')
#     user_data['User_Id'] = len(ratings_df['User_Id'].unique()) + 1
#     user_df = pd.DataFrame(user_data)
#     ratings_df = pd.concat([ratings_df, user_df], ignore_index=True)
#     places_df = pd.read_csv("review_dataset.csv")

#     model_knn = pickle.load(open('knnpickle_file(1)', 'rb'))

#     places_subset = places_df[['ID', 'Name']]
#     rating_places_df = ratings_df.merge(places_subset,
#                                         how="outer",
#                                         on="ID")
#     place_rating = rating_places_df.dropna(axis = 0, subset = ["Name"])
#     place_rating_count = place_rating.groupby(["Name"])["Place_Ratings"].count().reset_index().rename(columns = {'Place_Ratings': 'total_rating_count'})

#     rating_places_df =  rating_places_df.merge(place_rating_count, on="Name", how="right")
#     user_features_df = rating_places_df.pivot_table(index="User_Id", columns="Name", values="Place_Ratings").fillna(0.0)
#     user_features_matrix = csr_matrix(user_features_df)

#     model_knn = NearestNeighbors(metric = "cosine", algorithm = "brute", n_neighbors = 20, n_jobs=-1)
#     model_knn.fit(user_features_matrix)

#     query_index = user_data["User_Id"] -1
#     distances, indices = model_knn.kneighbors(user_features_df.iloc[query_index,:].values.reshape(1, -1), n_neighbors = 20)


#     user_ids = []
#     for index in range(0, len(distances.flatten())):
#         user_ids.append(user_features_df.index[indices.flatten()[index]])

#     candidate_user_ids = user_ids[1:]
#     sel_ratings = rating_places_df.loc[rating_places_df.User_Id.isin(candidate_user_ids)]
#     sel_ratings = sel_ratings.sort_values(by=["Place_Ratings", "total_rating_count"], ascending=False)
#     places_rated_by_targeted_user = list(rating_places_df.loc[rating_places_df.User_Id==user_ids[0]]["ID"].values)
#     sel_ratings = sel_ratings.loc[~sel_ratings.ID.isin(places_rated_by_targeted_user)]
#     agg_sel_ratings = sel_ratings.groupby(["Name", "Place_Ratings"])["total_rating_count"].max().reset_index()
#     agg_sel_ratings.columns = ["Name", "Place_Ratings", "total_ratings"]
#     agg_sel_ratings = agg_sel_ratings.sort_values(by=["Place_Ratings", "total_ratings"], ascending=False)
#     rec_list = agg_sel_ratings["Name"].head(20).values 
#     return rec_list




# def test():
#     from surprise import Reader, Dataset, SVD, accuracy
#     from surprise.model_selection import train_test_split
#     import pandas as pd
#     ratings_df = pd.read_csv("user_ratings5.csv") 

#     reader = Reader(rating_scale=(1, 5))
#     data = Dataset.load_from_df(ratings_df[['user_id', 'place_id', 'rating']], reader)

#     trainset, testset = train_test_split(data, test_size=0.25, random_state=42)

#     algo = SVD(n_factors=100, n_epochs=20, lr_all=0.005, reg_all=0.02)
#     algo.fit(trainset)

#     predictions = algo.test(testset)

#     rmse = accuracy.rmse(predictions)

#     mae = accuracy.mae(predictions)

#     print(f"RMSE: {rmse}")
#     print(f"MAE: {mae}")

# test()
# {'n_factors': 50, 'n_epochs': 30, 'lr_all': 0.01, 'reg_all': 0.02}



# import pandas as pd
# from surprise import SVD, Dataset, Reader, accuracy
# from surprise.model_selection import cross_validate, GridSearchCV

# # Load the data (example path, replace with your actual path)
# ratings_df = pd.read_csv("user_ratings5.csv")

# # Define the rating scale
# reader = Reader(rating_scale=(1, 5))

# # Load the dataset
# data = Dataset.load_from_df(ratings_df[['user_id', 'place_id', 'rating']], reader)

# param_grid = {
#     'n_factors': [50, 100, 150],
#     'n_epochs': [10, 20, 30],
#     'lr_all': [0.002, 0.005, 0.01],
#     'reg_all': [0.01, 0.02, 0.05]
# }

# gs = GridSearchCV(SVD, param_grid, measures=['rmse', 'mae'], cv=3)
# gs.fit(data)

# print("Best RMSE score attained: ", gs.best_score['rmse'])

# print("Parameters for best RMSE score: ", gs.best_params['rmse'])

# print("Best MAE score attained: ", gs.best_score['mae'])

# print("Parameters for best MAE score: ", gs.best_params['mae'])

# algo = gs.best_estimator['rmse']

# trainset = data.build_full_trainset()
# algo.fit(trainset)



# RMSE: 0.8543
# MAE:  0.6789
# RMSE: 0.8543343707775899
# MAE: 0.6788873470572399
# Best RMSE score attained:  0.8378465872475793
# Parameters for best RMSE score:  {'n_factors': 50, 'n_epochs': 30, 'lr_all': 0.01, 'reg_all': 0.05}
# Best MAE score attained:  0.6659489980848783
# Parameters for best MAE score:  {'n_factors': 50, 'n_epochs': 30, 'lr_all': 0.01, 'reg_all': 0.05}
