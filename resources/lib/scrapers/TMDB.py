# imports requests
import requests
# imports our movie class
from Movie import Listing

# A class that gets movie and tv listing from the TMDB api
class TMDB:
	# creates static variables
	# the api key used to request data from tmdb
	api_key = 'efd7b2c16b633d58a353a0be86269bab'
	# the current api domain
	api_domain = 'http://api.tmdb.org/3'
	# sets the path and resolution of the images
	img_path = 'https://image.tmdb.org/t/p/w1280/'

	@staticmethod
	def get_genres(media='movie'):
		# stores our found genres
		found_genres = dict()
		# creates search params
		search_params = {'api_key': TMDB.api_key}
		# gets results from api
		search_results = requests.get('{0}/genre/{1}/list'.format(TMDB.api_domain, media), params=search_params).json()
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

	@staticmethod # returns listings filtered by category
	def get_by_category(media='movie', category='popular', page=1):
		# filters name
		category = '_'.join(category.split()).lower()
		# stores our found listings
		found_listings = set()
		# creates search params
		search_params = {'api_key': TMDB.api_key, 'page': page}
		# gets results from api
		search_results = requests.get('{0}/{1}/{2}'.format(TMDB.api_domain, media, category), params=search_params).json()
		# iterates through listings
		for listing in search_results['results']:
			# creates a listing instance
			newListing = Listing(
				# adds our movie title
				listing['title'],
				# adds our movie overview
				listing['overview'],
				# adds our movie date
				listing['release_date'],
				# adds our movie rating
				listing['vote_average'],
				# adds our movie poster
				TMDB.img_path + str(listing['poster_path']),
				# adds our movie backdrop
				TMDB.img_path + str(listing['backdrop_path'])
			)
			# adds listing to our list
			found_listings.add(newListing)
		# returns our found listings list
		return found_listings

	@staticmethod # filters listings by year
	def get_by_year(media='movie', year=2000, page=1):
		# stores our found listings
		found_listings = set()
		# creates search params
		search_params = {'api_key': TMDB.api_key, 'primary_release_year': year, 'sort_by': 'popularity.desc', 'page': page}
		# gets results from api
		search_results = requests.get('{0}/discover/{1}'.format(TMDB.api_domain, media), params=search_params).json()
		# iterates through listings
		for listing in search_results['results']:
			# creates a listing instance
			newListing = Listing(
				# adds our movie title
				listing['title'],
				# adds our movie overview
				listing['overview'],
				# adds our movie date
				listing['release_date'],
				# adds our movie rating
				listing['vote_average'],
				# adds our movie poster
				TMDB.img_path + str(listing['poster_path']),
				# adds our movie backdrop
				TMDB.img_path + str(listing['backdrop_path'])
			)
			# adds listing to our list
			found_listings.add(newListing)
		# returns our found listings list
		return found_listings

	@staticmethod # filters listings by genre
	def get_by_genre(media='movie', genre='Action', page=1):
		# stores our found listings
		found_listings = set()
		# creates search params
		search_params = {'api_key': TMDB.api_key, 'with_genres': TMDB.get_genres(media)[genre], 'sort_by': 'popularity.desc', 'page': page}
		# gets results from api
		search_results = requests.get('{0}/discover/{1}'.format(TMDB.api_domain, media), params=search_params).json()
		# iterates through listings
		for listing in search_results['results']:
			# creates a listing instance
			newListing = Listing(
				# adds our movie title
				listing['title'],
				# adds our movie overview
				listing['overview'],
				# adds our movie date
				listing['release_date'],
				# adds our movie rating
				listing['vote_average'],
				# adds our movie poster
				TMDB.img_path + str(listing['poster_path']),
				# adds our movie backdrop
				TMDB.img_path + str(listing['backdrop_path'])
			)
			# adds listing to our list
			found_listings.add(newListing)
		# returns our found listings list
		return found_listings

	@staticmethod # filters listings by search term
	def search(media='movie', query='John Wick', page=1):
		# stores our found listings
		found_listings = set()
		# creates search params
		search_params = {'api_key': TMDB.api_key, 'query': query}
		# gets results from api
		search_results = requests.get('{0}/search/{1}'.format(TMDB.api_domain, media), params=search_params).json()
		# iterates through listings
		for listing in search_results['results']:
			# creates a listing instance
			newListing = Listing(
				# adds our movie title
				listing['title'],
				# adds our movie overview
				listing['overview'],
				# adds our movie date
				listing['release_date'],
				# adds our movie rating
				listing['vote_average'],
				# adds our movie poster
				TMDB.img_path + str(listing['poster_path']),
				# adds our movie backdrop
				TMDB.img_path + str(listing['backdrop_path'])
			)
			# adds listing to our list
			found_listings.add(newListing)
		# returns our found listings list
		return found_listings

	@staticmethod
	def create_listings(results):
		# stores our found listings
		found_listings = set()
		# iterates through listings
		for listing in results:
			# creates a listing instance
			newListing = Listing(
				# adds our movie title
				listing['title'],
				# adds our movie overview
				listing['overview'],
				# adds our movie date
				listing['release_date'],
				# adds our movie rating
				listing['vote_average'],
				# adds our movie poster
				TMDB.img_path + str(listing['poster_path']),
				# adds our movie backdrop
				TMDB.img_path + str(listing['backdrop_path'])
			)
			# adds listing to our list
			found_listings.add(newListing)
		# returns our found listings list
		return found_listings
