import requests
from config import api_key
from os.path import exists
import pickle

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
            print("Status Code:", response.status_code)

            movie_id = response.json()['id']
            movie_title = response.json()['title']

            # The unique movie ID is the key in both movie_data and movie_ids
            self.movie_data[movie_id] = response.json()
            self.movie_ids[movie_id] = movie_title

            for similar in response.json()['similars']:
                self.movie_ids[similar['id']] = similar['title']

        else:

            for key, value in self.movie_ids.items():
                print("\n----------------------")
                print("Key: ", key)
                print("Value: ", value)

                if key not in self.movie_data.keys():
                    # Add it to the movie_data dictionary with an API call
                    print("Adding title: ", value)
                    print(f'Request URL: {self.req_url}/{key}')

                    response = requests.get(f'{self.req_url}/{key}')
                    print("Status Code:", response.status_code)
                    print("Error Message: ", response.json()['errorMessage'])

                    movie_id = response.json()['id']
                    movie_title = response.json()['title']

                    # Add new item to movie_data and movie_ids
                    self.movie_data[movie_id] = response.json() # movie_id is the key
                    self.movie_ids[movie_id] = movie_title

                    # Add similar movies to movie_ids for future API requests
                    for similar in response.json()['similars']:
                        self.movie_ids[similar['id']] = similar['title']
                    # print('j: ',j)
                    break

                else:
                    print(value, 'is already in the movie_data dict')


    def save_movie_data(self, filename='movie_data', filetype='p'):
        with open(f"..\\data\\{filename}.{filetype}", "wb") as p:
            pickle.dump(self.movie_data, p)
        print("movie data saved")

    
    def save_movie_ids(self, filename='movie_ids', filetype='p'):
        with open(f"..\\data\\{filename}.{filetype}", "wb") as p:
            pickle.dump(self.movie_ids, p)
            print("movie ids saved")


movies = MovieDict()

for i in range(0,2):
    movies.get_movies()
    i+=1
    print('i: ', i)

movies.save_movie_data()
movies.save_movie_ids()




# Used this to pare down some fluff movie IDs - more to come, I'm sure

# ids_to_remove = ['tt3425332', 'tt5873098', 'tt5223342', 'tt6932874', 'tt7741824'
#                 , 'tt4428398', 'tt6467266', 'tt7214954'
#                 , 'tt8115900', 'tt13457952', 'tt5439480', 'tt4902964', 'tt13622958'
#                 , 'tt5531466', 'tt6135682', 'tt2341339', 'tt7165904', 'tt7042146'
#                 , 'tt3293184', 'tt5533228', 'tt2455546'
#                 , 'tt3807022'
#                 , 'tt0366005', 'tt2090578', 'tt1725156', 'tt1542599', 'tt1830577'
#                 , 'tt1980162', 'tt0438844', 'tt2486724', 'tt2087984', 'tt0307461'
#                 , 'tt6950338', 'tt3608838', 'tt1482967', 'tt5513770', 'tt6004806'
#                 , 'tt8271176', 'tt6963796', 'tt0328880', 'tt0371606'
#                 , 'tt5113040', 'tt11947282', 'tt5621544', 'tt0407398'
#                 , 'tt4718304', 'tt2869898', 'tt12027896', 'tt15341442', 'tt2850386'
#                 , 'tt3807034', 'tt5193172', 'tt5759196', 'tt2782214', 'tt2748608'
#                 , 'tt5021206', 'tt7741830', 'tt1679335', 'tt3597380', 'tt5814534'
#                 , 'tt3411444', 'tt0423294', 'tt1107365', 'tt1646926', 'tt0366548'
#                 , 'tt4007502', 'tt15758116', 'tt1710310'
#                 , 'tt13061790', 'tt1736313', 'tt3689498', 'tt1827536', 'tt4941804'
#                 , 'tt2388725', 'tt0455565', 'tt5452780', 'tt2980764'
#                 , 'tt0275847', 'tt0120855'
#                 , 'tt5242396', 'tt9540768', 'tt9227936', 'tt7411374'
#                 , 'tt4294236', 'tt6173116'
#                 ,'tt8115900', 'tt6467266', 'tt13622958', 'tt6467284', 'tt13606158'
#                 , 'tt12412888', 'tt4428398', 'tt10857164', 'tt7214954'
#                 , 'tt8641078', 'tt0107952', 'tt6139732', 'tt0105935'
#                 , 'tt2771200', 'tt0120131', 'tt1587310', 'tt4777008'
#                 , 'tt0131613', 'tt0760437'
#                 , 'tt0453556', 'tt0366005', 'tt3219170', 'tt1726839', 'tt1942683'
#                 , 'tt1825918', 'tt1817232', 'tt1710308'
#                 , 'tt0175058', 'tt1305826', 'tt0184111'
#                 , 'tt0419326', 'tt0312109', 'tt15057532', 'tt2279373'
#                 , 'tt4823776', 'tt16311516', 'tt0268397', 'tt0154061', 'tt0318233'
#                 , 'tt8337264', 'tt0385880'
#                 , 'tt0275847', 'tt0108598', 'tt0104361', 'tt0112691', 'tt1118511'
#                 , 'tt0339881', 'tt1789621', 'tt1430626']

# murph = {key: movies.movie_ids[key] for key in movies.movie_ids if key not in ids_to_remove}

# movies.movie_ids = murph