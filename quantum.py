# this script will deal with the parameters passed into our addon
import sys
from urlparse import parse_qsl

# imports our scrapers and modules
from resources.lib.scrapers.OneMovies import OneMovies
from resources.lib.scrapers.TMDB import TMDB
from resources.lib.modules.UI import UI

# class for storing a menu item actions
class MenuItem:
	# initalizes our menu item
	def __init__(self, title, action, icon='\\resources\\media\\icon2.jpg'):
		# sets up our attributes
		self.title = title
		self.action = action
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
		MenuItem('Popular', 'create_page'),
		MenuItem('Top Rated', 'create_page'),
		MenuItem('Now Playing', 'create_page'),
		MenuItem('Upcoming', 'create_page'),
		MenuItem('Genres', 'create_menu'),
		MenuItem('Year', 'create_menu')
	),
	'Television': (
		MenuItem('Popular', 'create_page'),
		MenuItem('Top Rated', 'create_page'),
		MenuItem('Now Playing', 'create_page'),
		MenuItem('Upcoming', 'create_page'),
		MenuItem('Genres', 'create_menu'),
		MenuItem('Year', 'create_menu')
	),
	'Genres': set((genre, 'create_page') for genre in movie_genres.keys()),
	'Year': set((str(year), 'create_page') for year in xrange(2018, 1900, -1))
	}

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
			# build our new page
			interface.build_page(category, page_number, 'movies', *TMDB.get_movies('_'.join(category.split()).lower()))
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
	interface = UI(handle=addon_handle, address=base_address)
	# checks the passed parameters
	parse_parameters(params=dict(parse_qsl(sys.argv[2][1:])))