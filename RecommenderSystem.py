import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import collections
import operator

rating_file = "C:\Users\dano\Dropbox\Datasets\ml-100k\u.csv"
movieinfo_file = "C:\Users\dano\Dropbox\Datasets\ml-100k\u_item.csv"

ratings_data = pd.read_csv(rating_file, sep='	')
movies_data = pd.read_csv(movieinfo_file, sep='\t')

mov_categories = ['Adventure', 'Animation', 'Children', 'Comedy', 'Crime','Documentary',
                  'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical',
                  'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']

rating_samples, rating_features = ratings_data.shape
movie_samples, movie_features = movies_data.shape

num_categories = 16

def ratings_set(users):
    user_info = {}

    for idx, user in users.iterrows():
        user_id = user['user_id']
        rating = user['rating']
        movie_id = user['item_id']

        if user_id in user_info:
            user_info[user_id].append([movie_id, rating])
        else:
            user_info[user_id] = [[movie_id, rating]]

    return user_info

def preference_set(usr_ratings, movies):
    user_prefs = {}
    for user, ratings in usr_ratings.iteritems():
        user_prefs[user] = np.zeros(16)

        for rating in ratings:
            mov_id = int(rating[0]) - 1 #check
            rate = rating[1]

            title = movies.iloc[mov_id][1]
            categories = movies.iloc[mov_id][4:]

            try:
                categ_prefs = [float(x) for x in categories.values]
            except ValueError:
                continue

            if rate > 3:
                user_prefs[user] += categ_prefs
            else:
                user_prefs[user] -= categ_prefs

    return user_prefs

def find_similar(target_prefs, prefs_collection):
    user_similarity = {}

    for u_id, u_prefs in prefs_collection.iteritems():
        similarity = np.sqrt(np.abs(sum(u_prefs - target_prefs)))  #how similar are user x and the target user?
        user_similarity[u_id] = np.round(similarity, 5)

    ordered_dict = sorted(user_similarity.items(), key=operator.itemgetter(1))

    return ordered_dict

def find_recommendations(sim_users, target_user):
    recommendations = {}

    #for u_id, similarity in sim_users:
    #    highly_rated = [x['item_id'] for x in ratings_data[ratings_data['user_id'] == u_id] if x['rating'] >= 4]
    #return highly_rated


user_ratings = ratings_set(ratings_data)

user_prefs = preference_set(user_ratings, movies_data)

target_prefs = np.array(([ -7.,  -8., -41.,  -4.,  -8.,  -1.,   0.,  -3., -12.,  -7.,  -1.,
       -11., -12., -13.,   0.,  -3.]))

similar_users = find_similar(target_prefs, user_prefs)

recommended_movies = find_recommendations(similar_users, target_prefs)

print recommended_movies


"""
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

pca = PCA().fit_transform(ratings_data)

clstr = KMeans(n_clusters=(12), max_iter=300, random_state=42)

clstr.fit(pca)
"""











