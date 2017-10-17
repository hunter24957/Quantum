from urllib import urlencode
import string

# imports xbmc api
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon

from resources.lib.scrapers.TMDB import TMDB
from datetime import datetime

# class for storing a menu item actions
class MenuItem:
	# initalizes our menu item
	def __init__(self, title, action, function, icon='\\resources\\media\\icon.jpg'):
		# sets up our attributes
		self.title = title
		self.action = action
		self.function = function
		self.icon = icon

# class contains UI methods
class UI:
	# instantiates our class
	def __init__(self, handle, address):
		# sets up our attributes
		self.handle = handle
		self.address = address
		# gets the addon path
		self.path = xbmcaddon.Addon().getAddonInfo('path')

	# creates main menu
	def build_menu(self, title, *args):
		# sets the title of the category
		xbmcplugin.setPluginCategory(self.handle, title)
		# sets the content of this category
		xbmcplugin.setContent(self.handle, 'albums')
		# iterates through categories
		for category in args:
			# creates a list item
			category_item = xbmcgui.ListItem(category.title)
			# sets images
			category_item.setArt({
				'thumb': self.path + category.icon,
				#'icon': self.path + category.icon,
				#'fanart': self.path + category.icon,
			})
			# adds list item as directory
			xbmcplugin.addDirectoryItem(
				# adds our application handle
				self.handle,
				# where we're doign and where we're going
				self.create_params(action=category.action, title=category.title, function=category.function, page=1),
				# adds our created item
				category_item,
				# THIS IS A FOLDER!
				True
			)
		# ends the directory
		xbmcplugin.endOfDirectory(self.handle)

	# creates a page
	def build_movie_page(self, title, function, page, *args):
		# sets the title of the category
		xbmcplugin.setPluginCategory(self.handle, title)
		# sets the content of this category
		xbmcplugin.setContent(self.handle, 'movies')
		# iterates through movies
		for movie in args:
			# creates a list item
			category_item = xbmcgui.ListItem(movie.title)
			# sets images
			category_item.setArt({'thumb': movie.poster, 'icon': movie.poster, 'fanart': movie.backdrop, 'poster': movie.poster, 'banner': movie.backdrop})
			# sets the list item info
			category_item.setInfo('video', {'title': movie.title, 'plot': movie.overview, 'year': movie.date.split('-')[0], 'rating': movie.rating})
			# adds list item as directory
			xbmcplugin.addDirectoryItem(self.handle, self.create_params(action='play_media', title=UI.make_printable(movie.title), date=movie.date), category_item)
		# creates a next page button
		category_item = xbmcgui.ListItem('Next Page')
		# increments page
		page = int(page) + 1
		# adds list item as directory
		xbmcplugin.addDirectoryItem(self.handle, self.create_params(action='build_movie_page', title=title, function=function, page=page), category_item, True)
		# sorts our listings by title (ignores "the")
		xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_TITLE_IGNORE_THE)
		# ends the directory
		xbmcplugin.endOfDirectory(self.handle)

	# creates a page
	def build_tv_page(self, title, function, page, *args):
		# sets the title of the category
		xbmcplugin.setPluginCategory(self.handle, title)
		# sets the content of this category
		xbmcplugin.setContent(self.handle, 'tvshows')
		# iterates through shows
		for show in args:
			# creates a list item
			category_item = xbmcgui.ListItem(show.title)
			# sets images
			category_item.setArt({'thumb': show.poster, 'icon': show.poster, 'fanart': show.backdrop, 'poster': show.poster, 'banner': show.backdrop})
			# sets the list item info
			category_item.setInfo('video', {'title': show.title, 'plot': show.overview, 'year': show.date.split('-')[0], 'rating': show.rating})
			# adds list item as directory
			xbmcplugin.addDirectoryItem(self.handle, self.create_params(action='build_series_page', title=UI.make_printable(show.title), id=show.id, backdrop=show.backdrop), category_item, True)
		# creates a next page button
		category_item = xbmcgui.ListItem('Next Page')
		# increments page
		page = int(page) + 1
		# adds list item as directory
		xbmcplugin.addDirectoryItem(self.handle, self.create_params(action='build_tv_page', title=title, function=function, page=page), category_item, True)
		# sorts our listings by title (ignores "the")
		xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_TITLE_IGNORE_THE)
		# ends the directory
		xbmcplugin.endOfDirectory(self.handle)

	# creates a page
	def build_series_page(self, title, iden, backdrop, *args):
		# sets the title of the category
		xbmcplugin.setPluginCategory(self.handle, title)
		# sets the content of this category
		xbmcplugin.setContent(self.handle, 'episodes')
		# iterates through seasons
		for season in args:
			# creates a list item
			category_item = xbmcgui.ListItem(season.title)
			# sets images
			category_item.setArt({'thumb': season.poster, 'icon': season.poster, 'fanart': backdrop, 'poster': season.poster, 'banner': backdrop})
			# sets the list item info
			category_item.setInfo('video', {'title': season.title, 'plot': season.overview, 'year': str(season.date).split('-')[0]})
			# adds list item as directory
			xbmcplugin.addDirectoryItem(self.handle, self.create_params(action='build_episode_page', title=UI.make_printable(season.title), id=iden, season=season.number, backdrop=backdrop), category_item, True)
		# sorts our listings by title (ignores "the")
		xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_TITLE_IGNORE_THE)
		# ends the directory
		xbmcplugin.endOfDirectory(self.handle)

	# creates a page
	def build_episode_page(self, title, backdrop, *args):
		# sets the title of the category
		xbmcplugin.setPluginCategory(self.handle, title)
		# sets the content of this category
		xbmcplugin.setContent(self.handle, 'episodes')
		# iterates through episodes
		for episode in args:
			# creates a list item
			category_item = xbmcgui.ListItem(episode.title)
			# sets images
			category_item.setArt({'thumb': episode.poster, 'icon': episode.poster, 'fanart': backdrop, 'poster': episode.poster, 'banner': backdrop})
			# sets the list item info
			category_item.setInfo('video', {'title': episode.title, 'plot': episode.overview, 'year': episode.date.split('-')[0], 'rating': episode.rating})
			# adds list item as directory
			xbmcplugin.addDirectoryItem(self.handle, self.create_params(action='play_media', title=UI.make_printable(episode.title), date=episode.date), category_item)
		# sorts our listings by title (ignores "the")
		xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_TITLE_IGNORE_THE)
		# ends the directory
		xbmcplugin.endOfDirectory(self.handle)

	def text_entry(self, title):
		# creates on screen keyboard
		kb = xbmc.Keyboard(heading=title)
		# shows keyboard to user
		kb.doModal()
		# if the user has confimed
		if (kb.isConfirmed()):
			# returns the text entered
			return kb.getText()

	# creates base parameters
	def create_params(self, **kwargs):
		# returns addon launch parameters
		return '{0}?{1}'.format(self.address, urlencode(kwargs))

	@staticmethod # filters string to printable characters
	def make_printable(unicode_string):
		# returns a filters ascii string
		return ''.join(x for x in unicode_string if x in string.printable)