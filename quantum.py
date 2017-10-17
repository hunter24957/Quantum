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
'get_by_category': TMDB.get_by_category,
'get_by_year': TMDB.get_by_year,
'get_by_genre': TMDB.get_by_genre,
'search': TMDB.search
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
		MenuItem('Search People', 'build_text', 'people', 'search')
		),
	'menu.movie': (
		# adds popular selection
		MenuItem('Popular', 'build_page', 'movie', 'get_by_category'),
		# adds top rated selection
		MenuItem('Top Rated', 'build_page', 'movie', 'get_by_category'),
		# adds now playing selection
		MenuItem('Now Playing', 'build_page', 'movie', 'get_by_category'),
		# adds upcoming selection
		MenuItem('Upcoming', 'build_page', 'movie', 'get_by_category'),
		# adds genres selection
		MenuItem('Genres', 'build_menu', 'movie.genres'),
		# adds years selection
		MenuItem('Years', 'build_menu', 'movie.years'),
		# adds search selection
		MenuItem('Search', 'build_text', 'movie', 'search')
		),
	'menu.tv': (
		# adds popular selection
		MenuItem('Popular', 'build_page', 'tv', 'get_by_category'),
		# adds top rated selection
		MenuItem('Top Rated', 'build_page', 'tv', 'get_by_category'),
		# adds now playing selection
		MenuItem('Now Playing', 'build_page', 'tv', 'get_by_category'),
		# adds upcoming selection
		MenuItem('Upcoming', 'build_page', 'tv', 'get_by_category'),
		# adds genres selection
		MenuItem('Genres', 'build_menu', 'tv.genres'),
		# adds years selection
		MenuItem('Years', 'build_menu', 'tv.years'),
		# adds search selection
		MenuItem('Search', 'build_text', 'tv', 'search')
		),
	'movie.genres': tuple(
		# build our genre selection items
		MenuItem(genre, 'build_page', 'movie', 'get_by_genre') for genre in movie_genres.keys()
		),
	'movie.years': tuple(
		# build our year selection items
		MenuItem(str(year), 'build_page', 'movie', 'get_by_year') for year in xrange(datetime.now().year, 1900, -1)
		),
	'tv.genres': tuple(
		# build our genre selection items
		MenuItem(genre, 'build_page', 'tv', 'get_by_genre') for genre in tv_genres.keys()
		),
	'tv.years': tuple(
		# build our year selection items
		MenuItem(str(year), 'build_page', 'tv', 'get_by_year') for year in xrange(datetime.now().year, 1900, -1)
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
			GUI.build_menu(params['title'], *layout[params['id']])
		# checks the passed parameters
		elif params['action'] == 'build_page':
			# extracts function from actions
			get_listings = actions[params['function']]
			# gets listings of category
			listings = get_listings(params['id'], params['title'], params['page'])
			# builds a page with the listings
			GUI.build_page(params['title'], params['id'], params['function'], params['page'], params['action'], *listings)
		# checks the passed parameters
		elif params['action'] == 'build_text':
			# prompts user with text box
			query = GUI.text_entry(params['title'])
			# extracts function from actions
			get_listings = actions[params['function']]
			# gets listings of category
			listings = get_listings(params['id'], params['title'], params['page'])
			# builds a page with the listings
			GUI.build_page(params['title'], params['id'], params['function'], params['page'], params['action'], *listings)
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