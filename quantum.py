# this script will deal with the parameters passed into our addon
import sys
from urlparse import parse_qsl
from datetime import datetime

# imports our scrapers and modules
from resources.lib.scrapers.OneMovies import OneMovies
from resources.lib.scrapers.TMDB import TMDB
from resources.lib.modules.UI import UI, MenuItem

# stores movie genres for indexing
movie_genres = TMDB.get_genres('movie')
# stores tv genres for indexing
tv_genres = TMDB.get_genres('tv')
# stores our methods as strings for indexing
actions = {
'get_movies_by_category': TMDB.get_movies_by_category,
'get_movies_by_year': TMDB.get_movies_by_year,
'get_movies_by_genre': TMDB.get_movies_by_genre,
'get_shows_by_category': TMDB.get_shows_by_category,
'get_shows_by_year': TMDB.get_shows_by_year,
'get_shows_by_genre': TMDB.get_shows_by_genre,
#'search_people': TMDB.search_people,
'search_movies': TMDB.search_movies,
'search_shows': TMDB.search_shows,
}

# THIS IS A WORK IN PROGRESS LAYOUT OF THE ADDON
# THE CLASS STORES EACH SECTIONS BUTTONS AND WHAT ACTION THEY TRIGGER
layout = {
	'main.menu': (
		# adds movie selection
		MenuItem('Movies', 'build_menu', 'menu.movie'),
		# adds television selection
		MenuItem('Television', 'build_menu', 'menu.tv'),
		# adds search selection
		MenuItem('Search People', 'build_text', 'search_people')
		),
	'menu.movie': (
		# adds popular selection
		MenuItem('Popular', 'build_movie_page', 'get_movies_by_category'),
		# adds top rated selection
		MenuItem('Top Rated', 'build_movie_page', 'get_movies_by_category'),
		# adds now playing selection
		MenuItem('Now Playing', 'build_movie_page', 'get_movies_by_category'),
		# adds upcoming selection
		MenuItem('Upcoming', 'build_movie_page', 'get_movies_by_category'),
		# adds genres selection
		MenuItem('Genres', 'build_menu', 'movie.genres'),
		# adds years selection
		MenuItem('Years', 'build_menu', 'movie.years'),
		# adds search selection
		MenuItem('Search', 'build_text', 'search_movies')
		),
	'menu.tv': (
		# adds popular selection
		MenuItem('Popular', 'build_tv_page', 'get_shows_by_category'),
		# adds top rated selection
		MenuItem('Top Rated', 'build_tv_page', 'get_shows_by_category'),
		# adds now playing selection
		MenuItem('Now Playing', 'build_tv_page', 'get_shows_by_category'),
		# adds upcoming selection
		MenuItem('Upcoming', 'build_tv_page', 'get_shows_by_category'),
		# adds genres selection
		MenuItem('Genres', 'build_menu', 'tv.genres'),
		# adds years selection
		MenuItem('Years', 'build_menu', 'tv.years'),
		# adds search selection
		MenuItem('Search', 'build_text', 'search_shows')
		),
	'movie.genres': tuple(
		# build our genre selection items
		MenuItem(genre, 'build_movie_page', 'get_movies_by_genre') for genre in movie_genres.keys()
		),
	'movie.years': tuple(
		# build our year selection items
		MenuItem(str(year), 'build_movie_page', 'get_movies_by_year') for year in xrange(datetime.now().year, 1900, -1)
		),
	'tv.genres': tuple(
		# build our genre selection items
		MenuItem(genre, 'build_tv_page', 'get_shows_by_genre') for genre in tv_genres.keys()
		),
	'tv.years': tuple(
		# build our year selection items
		MenuItem(str(year), 'build_tv_page', 'get_shows_by_year') for year in xrange(datetime.now().year, 1900, -1)
		),
}

# KODI WORKS BY CALLING OUR ADDON WHEN A USER CLICKS IT
# THE ADDONS SETS THE STATES (SETS UP UI) THEN CALLS KODI
# WHEN A USER INTERACT KODI CALLS OUR ADDON WITH PARAMETERS THAT WE WILL PARSE HERE

# THIS FUNCTION WILL PARSE THE PARAMETERS GIVEN
def parse_parameters(params):
	# if there are existent parameters
	if params:
		# checks the passed parameters
		if params['action'] == 'build_menu':
			# builds the given menu
			GUI.build_menu(params['title'], *layout[params['function']])
		# checks the passed parameters
		elif params['action'] == 'build_movie_page':
			# extracts function from actions
			get_listings = actions[params['function']]
			# gets listings of category
			listings = get_listings(params['title'], params['page'])
			# builds a page with the listings
			GUI.build_movie_page(params['title'], params['function'], params['page'], *listings)
		# checks the passed parameters
		elif params['action'] == 'build_tv_page':
			# extracts function from actions
			get_listings = actions[params['function']]
			# gets listings of category
			listings = get_listings(params['title'], params['page'])
			# builds a page with the listings
			GUI.build_tv_page(params['title'], params['function'], params['page'], *listings)
		# checks the passed parameters
		elif params['action'] == 'build_series_page':
			# gets listings of category
			listings = TMDB.get_shows_seasons(params['id'])
			# builds a page with the listings
			GUI.build_series_page(params['title'], params['id'], params['backdrop'], *listings)
		# checks the passed parameters
		elif params['action'] == 'build_episode_page':
			# gets listings of category
			listings = TMDB.get_season_episodes(params['id'], params['season'])
			# builds a page with the listings
			GUI.build_episode_page(params['title'], params['backdrop'], *listings)
		# checks the passed parameters
		elif params['action'] == 'build_text':
			# extracts function from actions
			get_listings = actions[params['function']]
			# gets user input
			search_term = GUI.text_entry(params['title'])
			# gets listings of category
			listings = get_listings(search_term, params['page'])
	# else we build the main menu
	else: GUI.build_menu('Menu', *layout['main.menu'])

if __name__ == '__main__':
	# gets addon handle
	addon_handle = int(sys.argv[1])
	# gets the addon base address
	base_address = sys.argv[0]
	# instantiates our UI with our addon handle and base address
	GUI = UI(addon_handle, base_address)
	# passed decoded parameters into the parser
	parse_parameters(dict(parse_qsl(sys.argv[2][1:])))