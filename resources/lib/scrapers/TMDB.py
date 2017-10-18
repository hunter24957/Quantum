# imports requests
import requests
# imports our movie class
from resources.lib.modules.UI import *

# A class that gets movie and tv listing from the TMDB api
class TMDB:
	# creates static variables
	# the api key used to request data from tmdb
	api_key = 'efd7b2c16b633d58a353a0be86269bab'
	# the current api domain
	api_domain = 'http://api.tmdb.org/3'
	# sets the path and resolution of the images
	img_path = 'https://image.tmdb.org/t/p/w1280/'

	@staticmethod # returns listings filtered by category
	def get_movies_by_category(category='popular', page=1):
		# stores our found listings
		found_listings = set()
		# filters name
		category = '_'.join(category.split()).lower()
		# creates search params
		search_params = {'api_key': TMDB.api_key, 'page': page}
		# gets results from api
		search_results = requests.get('{0}/movie/{1}'.format(TMDB.api_domain, category), params=search_params).json()
		# iterates through listings
		for listing in search_results['results']:
			# creates a listing instance
			newListing = Listing(
				# adds our movie id
				listing['id'],
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
	def get_movies_by_year(year=2000, page=1):
		# stores our found listings
		found_listings = set()
		# creates search params
		search_params = {'api_key': TMDB.api_key, 'primary_release_year': year, 'sort_by': 'popularity.desc', 'page': page}
		# gets results from api
		search_results = requests.get('{0}/discover/movie'.format(TMDB.api_domain), params=search_params).json()
		# iterates through listings
		for listing in search_results['results']:
			# creates a listing instance
			newListing = Listing(
				# adds our movie id
				listing['id'],
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
	def get_movies_by_genre(genre='Action', page=1):
		# stores our found listings
		found_listings = set()
		# creates search params
		search_params = {'api_key': TMDB.api_key, 'with_genres': TMDB.get_genres('movie')[genre], 'sort_by': 'popularity.desc', 'page': page}
		# gets results from api
		search_results = requests.get('{0}/discover/movie'.format(TMDB.api_domain), params=search_params).json()
		# iterates through listings
		for listing in search_results['results']:
			# creates a listing instance
			newListing = Listing(
				# adds our movie id
				listing['id'],
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
	def search_movies(query='John Wick', page=1):
		# stores our found listings
		found_listings = set()
		# creates search params
		search_params = {'api_key': TMDB.api_key, 'query': query}
		# gets results from api
		search_results = requests.get('{0}/search/movie'.format(TMDB.api_domain), params=search_params).json()
		# iterates through listings
		for listing in search_results['results']:
			# creates a listing instance
			newListing = Listing(
				# adds our movie id
				listing['id'],
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

	@staticmethod # returns listings filtered by category
	def get_shows_by_category(category='popular', page=1):
		# stores our found listings
		found_listings = set()
		# filters name
		category = '_'.join(category.split()).lower()
		# creates search params
		search_params = {'api_key': TMDB.api_key, 'page': page}
		# gets results from api
		search_results = requests.get('{0}/tv/{1}'.format(TMDB.api_domain, category), params=search_params).json()
		# iterates through listings
		for listing in search_results['results']:
			# creates a listing instance
			newListing = Listing(
				# adds our movie id
				listing['id'],
				# adds our movie title
				listing['name'],
				# adds our movie overview
				listing['overview'],
				# adds our movie date
				listing['first_air_date'],
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
	def get_shows_by_year(year=2000, page=1):
		# stores our found listings
		found_listings = set()
		# creates search params
		search_params = {'api_key': TMDB.api_key, 'primary_release_year': year, 'sort_by': 'popularity.desc', 'page': page}
		# gets results from api
		search_results = requests.get('{0}/discover/tv'.format(TMDB.api_domain), params=search_params).json()
		# iterates through listings
		for listing in search_results['results']:
			# creates a listing instance
			newListing = Listing(
				# adds our movie id
				listing['id'],
				# adds our movie title
				listing['name'],
				# adds our movie overview
				listing['overview'],
				# adds our movie date
				listing['first_air_date'],
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
	def get_shows_by_genre(genre='Action', page=1):
		# stores our found listings
		found_listings = set()
		# creates search params
		search_params = {'api_key': TMDB.api_key, 'with_genres': TMDB.get_genres('tv')[genre], 'sort_by': 'popularity.desc', 'page': page}
		# gets results from api
		search_results = requests.get('{0}/discover/tv'.format(TMDB.api_domain), params=search_params).json()
		# iterates through listings
		for listing in search_results['results']:
			# creates a listing instance
			newListing = Listing(
				# adds our movie id
				listing['id'],
				# adds our movie title
				listing['name'],
				# adds our movie overview
				listing['overview'],
				# adds our movie date
				listing['first_air_date'],
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
	def search_shows(query='John Wick', page=1):
		# stores our found listings
		found_listings = set()
		# creates search params
		search_params = {'api_key': TMDB.api_key, 'query': query}
		# gets results from api
		search_results = requests.get('{0}/search/tv'.format(TMDB.api_domain), params=search_params).json()
		# iterates through listings
		for listing in search_results['results']:
			# creates a listing instance
			newListing = Listing(
				# adds our movie id
				listing['id'],
				# adds our movie title
				listing['name'],
				# adds our movie overview
				listing['overview'],
				# adds our movie date
				listing['first_air_date'],
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

	@staticmethod # filters listings by seasons
	def get_show_seasons(show_id):
		# stores our found listings
		found_listings = set()
		# creates search params
		search_params = {'api_key': TMDB.api_key}
		# gets results from api
		search_results = requests.get('{0}/tv/{1}'.format(TMDB.api_domain, show_id), params=search_params).json()
		# iterates through seasons
		for listing in search_results['seasons']:
			# gets the seasons details
			season = TMDB.get_season_details(show_id, listing['season_number'])
			# creates a season instance
			newListing = Season(
				# adds our season number
				season['season_number'],
				# adds our season id
				season['id'],
				# adds our season name
				season['name'],
				# adds our season overview
				season['overview'],
				# adds our season date
				season['air_date'],
				# adds our season poster
				TMDB.img_path + str(season['poster_path']),
			)
			# adds listing to our list
			found_listings.add(newListing)
		# returns our found listings list
		return found_listings

	@staticmethod
	def get_season_details(show_id, season_number):
		# creates search params
		search_params = {'api_key': TMDB.api_key}
		# gets results from api
		search_results = requests.get('{0}/tv/{1}/season/{2}'.format(TMDB.api_domain, show_id, season_number), params=search_params).json()
		# returns our results
		return search_results

	@staticmethod # filters listings by seasons
	def get_season_episodes(show_id, season_number):
		# stores our found listings
		found_listings = set()
		# creates search params
		search_params = {'api_key': TMDB.api_key}
		# gets results from api
		search_results = requests.get('{0}/tv/{1}/season/{2}'.format(TMDB.api_domain, show_id, season_number), params=search_params).json()
		# iterates through seasons
		for listing in search_results['episodes']:
			# creates a season instance
			newListing = Episode(
				# adds our episode number
				listing['episode_number'],
				# adds our episode id
				listing['id'],
				# adds our episode name
				listing['name'],
				# adds our episode overview
				listing['overview'],
				# adds our episode date
				listing['air_date'],
				# adds our average votes
				listing['vote_average'],
				# adds our episode poster
				TMDB.img_path + str(listing['still_path']),
			)
			# adds listing to our list
			found_listings.add(newListing)
		# returns our found listings list
		return found_listings

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
