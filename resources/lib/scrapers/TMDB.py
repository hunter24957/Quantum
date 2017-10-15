# imports requests
import requests
# imports our movie class
from Movie import Movie

# A class that gets movie and tv listing from the TMDB api
class TMDB:
	# creates static variables
	# the api key used to request data from tmdb
	api_key = 'efd7b2c16b633d58a353a0be86269bab'
	# the current api domain
	api_domain = 'http://api.tmdb.org/3'
	# sets the path and resolution of the images
	img_path = 'https://image.tmdb.org/t/p/w1280/'

	@staticmethod # returns movies filtered by category
	def get_movies(category='popular', page=1):
		# stores our found movies
		found_movies = list()
		# creates search params
		search_params = {'api_key': TMDB.api_key, 'page': page}
		# gets results from api
		search_results = requests.get(TMDB.api_domain + '/movie/' + category, params=search_params).json()
		# iterates through results
		for movie in search_results['results']:
			# creates a movie instance
			newMovie = Movie(
				# adds our movie title
				movie['title'],
				# adds our movie overview
				movie['overview'],
				# adds our movie date
				movie['release_date'],
				# adds our movie rating
				movie['vote_average'],
				# adds our movie poster
				TMDB.img_path + str(movie['poster_path']),
				# adds our movie backdrop
				TMDB.img_path + str(movie['backdrop_path'])
			)
			# adds movie to our list
			found_movies.append(newMovie)
		# returns our found movies list
		return found_movies

	@staticmethod # filters movies by year
	def get_movies_by_year(year=2000, page=1):
		# stores our found movies
		found_movies = list()
		# creates search params
		search_params = {'api_key': TMDB.api_key, 'primary_release_year': year, 'sort_by': 'popularity.desc', 'page': page}
		# gets results from api
		search_results = requests.get(TMDB.api_domain + '/discover/movie', params=search_params).json()
		# iterates through results
		for movie in search_results['results']:
			# creates a movie instance
			newMovie = Movie(
				# adds our movie title
				movie['title'],
				# adds our movie overview
				movie['overview'],
				# adds our movie date
				movie['release_date'],
				# adds our movie rating
				movie['vote_average'],
				# adds our movie poster
				TMDB.img_path + str(movie['poster_path']),
				# adds our movie backdrop
				TMDB.img_path + str(movie['backdrop_path'])
			)
			# adds movie to our list
			found_movies.append(newMovie)
		# returns our found movies list
		return found_movies

	@staticmethod
	def get_genres():
		# stores our found genres
		found_genres = dict()
		# creates search params
		search_params = {'api_key': TMDB.api_key}
		# gets results from api
		search_results = requests.get(TMDB.api_domain + '/genre/movie/list', params=search_params).json()
		# iterates through genres
		for genre in search_results['genres']:
			# gets the id
			genre_id = genre['id']
			# gets the name
			genre_name = genre['name']
			# adds genre id to our dict
			found_genres[genre_name] = genre_id
		# returns our found genres dict
		return found_genres

if __name__ == '__main__':
	# gets page two of the most popular movies
	movies = TMDB.get_popular_movies(2)
	# iterates through movies
	for movie in movies:
		# prints the movie string
		print(movie)