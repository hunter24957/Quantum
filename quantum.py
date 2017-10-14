import sys
from urllib import urlencode
from urlparse import parse_qsl
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
from resources.lib.scrapers.OneMovies import OneMovies
from resources.lib.scrapers.TMDB import TMDB

# gets addon, addon name and icon
__addon__ = xbmcaddon.Addon()
__addonname__ = __addon__.getAddonInfo('name')
__icon__ = __addon__.getAddonInfo('icon')
# gets addon handle
__handle__ = int(sys.argv[1])
# gets the addon base address
__addr__ = sys.argv[0]

# creates actions
actions = {'Movies': TMDB.get_popular_movies}

# creates main menu
def init_main_menu(*args):
	# sets the title of the category
	xbmcplugin.setPluginCategory(__handle__, 'Menu')
	# sets the content of this category
	xbmcplugin.setContent(__handle__, 'movies')
	# iterates through categories
	for category in args:
		# creates a list item
		category_item = xbmcgui.ListItem(category)
		# sets images
		category_item.setArt({'thumb': 'movie.poster', 'icon': 'movie.poster', 'fanart': 'movie.backdrop'})
		# adds list item as directory
		xbmcplugin.addDirectoryItem(__handle__, create_params(action='listing', category=category, page=1), category_item, True)
	# sorts the categories
	xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_VIDEO_TITLE)
	# ends the directory
	xbmcplugin.endOfDirectory(__handle__)

# creates a category
def init_category(title, category='movies', *args):
	# sets the title of the category
	xbmcplugin.setPluginCategory(__handle__, title)
	# sets the content of this category
	xbmcplugin.setContent(__handle__, category)
	# iterates through movies
	for movie in args:
		# creates a list item
		category_item = xbmcgui.ListItem(movie.title)
		# sets images
		category_item.setArt({'thumb': movie.poster, 'icon': movie.poster, 'fanart': movie.backdrop})
		# sets the list item info
		category_item.setInfo('video', {'title': movie.title, 'genre': movie.overview})
		# adds list item as directory
		xbmcplugin.addDirectoryItem(__handle__, create_params(action='play', title=movie.title, date=movie.date), category_item)
	# creates a next page button
	category_item = xbmcgui.ListItem('Next Page')
	# sets images
	# category_item.setArt({'thumb': movie.poster, 'icon': movie.poster, 'fanart': movie.backdrop})
	# adds list item as directory
	xbmcplugin.addDirectoryItem(__handle__, create_params(action='listing', category=title, page=3), category_item, True)
	# ends the directory
	xbmcplugin.endOfDirectory(__handle__)

# parses parameters
def create_params(**kwargs):
	# returns addon launch parameters
    return '{0}?{1}'.format(__addr__, urlencode(kwargs))

# parses parameters
def check_params(params):
	# if params exits
	if params:
		# if the action is listing
		if params['action'] == 'listing':
			# gets page one of the most popular movies
			movies = actions[params['category']](params['page'])
			# creates our category
			init_category(params['category'], 'movies', *movies)
		# if the action is play a movie
		if params['action'] == 'play':
			# sest movie url to none
			movie_url = None
			# loops while movie url is none
			while not movie_url:
				# invokes scraper
				movie_url = OneMovies.get_movie_stream_url(title=params['title'], year=params['date'].split('-')[0])
			# plays movie
			xbmc.Player().play(item=movie_url)
	else:
		# creates our main menu
		init_main_menu('Movies', 'Television')


if __name__ == '__main__':
	# checks the passed parameters
	check_params(dict(parse_qsl(sys.argv[2][1:])))