import requests
from config import api_key
from os.path import exists
import pickle

# Starts with Toy Story
# toy_story_id = 'tt0114709'

# api_url = 'https://imdb-api.com/en/API/Title'

# response = requests.get(f'{api_url}/{api_key}/{toy_story_id}')

# movie_title = response.json()['title']
# movie_id = response.json()['id']

# Add Toy Story title to a set of all titles
# movie_ids = set()
# movie_ids.add(movie_id)

# Add Toy Story json to all movie data
# movie_data = {}
# movie_data[movie_title] = response.json()

# Add similar movies to the set of all titles
# for similar in response.json()['similars']:
#     movie_ids.add(similar['id'])

# if there are no keys in the movie data dictionary, start the dict with Toy Story
# otherwise, check the movie_ids set and add items to the movie data dictionary


class MovieDict:
    """
    """

    def __init__(self):
        """
        """
        movie_dict_exists = exists("..\\data\\movie_data.p")
        if movie_dict_exists == True:
            with open("..\\data\\movie_data.p", 'rb') as p:
                self.movie_data = pickle.load(p)
            with open("..\\data\\movie_ids.p", 'rb') as p:
                self.movie_ids = pickle.load(p)
        else:
            self.movie_data = {}
            self.movie_ids = {}

        self.api_url = 'https://imdb-api.com/en/API/Title'
        self.api_key = api_key
        self.req_url = f'{self.api_url}/{self.api_key}'


    def get_movies(self):
        if len(self.movie_data.keys()) == 0:
            # Start with Toy Story
            toy_story_id = 'tt0114709'
            response = requests.get(f'{self.req_url}/{toy_story_id}')

            movie_title = response.json()['title']
            movie_id = response.json()['id']

            # Add first items to movie_data and movie_ids
            self.movie_data[movie_title] = response.json()
            self.movie_ids[movie_title] = movie_id

            for similar in response.json()['similars']:
                self.movie_ids[similar['title']] = similar['id']

        else:
            j = 1
            while j <= 3:
                # print(j)
                try:
                    for key, value in self.movie_ids.items():
                        # print("iteration ",j, " title: ",key)
                        if key not in self.movie_data.keys():
                            print("Adding title: ", key)

                            response = requests.get(f'{self.req_url}/{value}')
                            j+=1

                            movie_title = response.json()['title']
                            movie_id = response.json()['id']

                            # Add first items to movie_data and movie_ids
                            self.movie_data[movie_title] = response.json()
                            self.movie_ids[movie_title] = movie_id

                            for similar in response.json()['similars']:
                                self.movie_ids[similar['title']] = similar['id']
                except:
                    break

    def save_movie_data(self, filename='movie_data', filetype='p'):
        with open(f"..\\data\\{filename}.{filetype}", "wb") as p:
            pickle.dump(self.movie_data, p)
        print("movie data saved")

    
    def save_movie_ids(self, filename='movie_ids', filetype='p'):
        with open(f"..\\data\\{filename}.{filetype}", "wb") as p:
            pickle.dump(self.movie_ids, p)
            print("movie ids saved")



movies = MovieDict()

for i in range(0,20):
    movies.get_movies()
    i+=1

movies.save_movie_data()
movies.save_movie_ids()

# i=1
# while i <= 5:
#     print(i)
#     movies.get_movies()


# Skips Toy Story because it's already in the dataset - GOOD
# Adds Toy Story 3 because it's new - GOOD
# Gets hung up on Toy Story 2 because the movie_ids dict changed - PROBLEM





    # def add_movie_info(self, api_response):
    #     movie_title = api_response.json()['title']
    #     movie_id = api_response.json()['id']

    #     # Add first items to movie_data and movie_ids
    #     self.movie_data[movie_title] = api_response.json()
    #     self.movie_ids.add(movie_id)

    #     for similar in api_response.json()['similars']:
    #         self.movie_ids.add(similar['id'])

    #     return self.movie_data, self.movie_ids

