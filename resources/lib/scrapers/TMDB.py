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

	@staticmethod # gets the most popular movies
	def get_popular_movies(page=1):
		# stores our popular movies
		popular_movies = list()
		# creates search params
		popular_params = {'api_key': TMDB.api_key, 'page': page}
		# gets results from api
		popular_results = requests.get(TMDB.api_domain + '/movie/popular', params=popular_params).json()
		# iterates through results
		for movie in popular_results['results']:
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
				'https://image.tmdb.org/t/p/w1920/' + str(movie['poster_path']),
				# adds our movie backdrop
				'https://image.tmdb.org/t/p/w1920/' + str(movie['backdrop_path'])
			)
			# adds movie to our list
			popular_movies.append(newMovie)
		# returns our popular movies list
		return popular_movies

if __name__ == '__main__':
	# gets page two of the most popular movies
	movies = TMDB.get_popular_movies(2)
	# iterates through movies
	for movie in movies:
		# prints the movie string
		print(movie)