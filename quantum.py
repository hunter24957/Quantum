# this script will deal with the parameters passed into our addon
import sys
from urlparse import parse_qsl
from datetime import datetime

# imports our scrapers and modules
from resources.lib.scrapers.OneMovies import OneMovies
from resources.lib.scrapers.TMDB import TMDB
from resources.lib.modules.UI import UI

# class for storing a menu item actions
class MenuItem:
	# initalizes our menu item
	def __init__(self, title, action, function='', icon='\\resources\\media\\icon2.jpg'):
		# sets up our attributes
		self.title = title
		self.action = action
		self.function = function
		self.icon = icon


# GETS MOVIE GENRES TO BE USED LATER
movie_genres = TMDB.get_genres()

# CONTAINS OUR UI CATEGORIES WITH THEIR SELECTIONS
categories = {
	'Menu': (
		MenuItem('Movies', 'create_menu'),
		MenuItem('Television', 'create_menu')
	),
	'Movies': (
		MenuItem('Popular', 'create_page', 'get_movies'),
		MenuItem('Top Rated', 'create_page', 'get_movies'),
		MenuItem('Now Playing', 'create_page', 'get_movies'),
		MenuItem('Upcoming', 'create_page', 'get_movies'),
		MenuItem('Genres', 'create_menu'),
		MenuItem('Year', 'create_menu')
	),
	'Television': (
		MenuItem('Popular', 'create_page', 'get_movies'),
		MenuItem('Top Rated', 'create_page', 'get_movies'),
		MenuItem('Now Playing', 'create_page', 'get_movies'),
		MenuItem('Upcoming', 'create_page', 'get_movies'),
		MenuItem('Genres', 'create_menu'),
		MenuItem('Year', 'create_menu')
	),
	'Genres': set(MenuItem(genre, 'create_page', 'get_movies') for genre in movie_genres.keys()),
	'Year': set(MenuItem(str(year), 'create_page', 'get_movies_by_year') for year in xrange(datetime.now().year, 1900, -1))
	}

functions = {'get_movies': TMDB.get_movies,
'get_movies_by_year': TMDB.get_movies_by_year}

# KODI WORKS BY CALLING OUR ADDON WHEN A USER CLICKS IT
# THE ADDONS SETS THE STATES (SETS UP UI) THEN CALLS KODI
# WHEN A USER INTERACT KODI CALLS OUR ADDON WITH PARAMETERS THAT WE WILL PARSE HERE
def parse_parameters(params):
	# if there is any parameters
	if params:
		# if this is a create_menu action for us to perform
		if params['action'] == 'create_menu':
			# gets our category destination
			category = params['destination']
			# build our new menu
			interface.build_menu(category, *categories[category])
		# if this is a create_page action for us to perform
		elif params['action'] == 'create_page':
			# gets our category destination
			category = params['destination']
			# gets our page number to build
			page_number = params['page_number']
			# gets our function call
			function = params['function']
			# build our new page
			interface.build_page(category, page_number, 'movies', *functions[function]('_'.join(str(category).split()).lower(), page_number))
		# if this is a play media action for us to perform
		elif params['action'] == 'play_media':
			# here we play the media the user has chosen
			pass
	# else we create our main menu (application has been launched)
	else: interface.build_menu('Menu', *categories['Menu'])

if __name__ == '__main__':
	# gets addon handle
	addon_handle = int(sys.argv[1])
	# gets the addon base address
	base_address = sys.argv[0]
	# instantiates our UI with our addon handle and base address
	interface = UI(addon_handle, base_address)
	# checks the passed parameters
	parse_parameters(dict(parse_qsl(sys.argv[2][1:])))