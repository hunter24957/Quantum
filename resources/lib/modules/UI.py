from urllib import urlencode
import string

# imports xbmc api
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon

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
				'icon': self.path + category.icon,
				'fanart': self.path + category.icon,
				'poster': self.path + category.icon,
				'banner': self.path + category.icon
			})
			# adds list item as directory
			xbmcplugin.addDirectoryItem(
				# adds our application handle
				self.handle,
				# where we're doign and where we're going
				self.create_params(action=category.action, destination=category.title, function=category.function, page_number=1),
				# adds our created item
				category_item,
				# THIS IS A FOLDER!
				True
			)
		# ends the directory
		xbmcplugin.endOfDirectory(self.handle)

	# creates a page
	def build_page(self, title, page, category='movies', *args):
		# sets the title of the category
		xbmcplugin.setPluginCategory(self.handle, title)
		# sets the content of this category
		xbmcplugin.setContent(self.handle, category)
		# iterates through movies
		for movie in args:
			# creates a list item
			category_item = xbmcgui.ListItem(movie.title)
			# sets images
			category_item.setArt({'thumb': movie.poster, 'icon': movie.poster, 'fanart': movie.backdrop, 'poster': movie.poster, 'banner': movie.backdrop})
			# sets the list item info
			category_item.setInfo('video', {'title': movie.title, 'plot': movie.overview, 'year': int(movie.date.split('-')[0]), 'rating': movie.rating})
			# adds list item as directory
			xbmcplugin.addDirectoryItem(self.handle, self.create_params(action='play', title=UI.make_printable(movie.title), date=movie.date), category_item)
		# creates a next page button
		category_item = xbmcgui.ListItem('Next Page')
		# increments page
		page = int(page) + 1
		# adds list item as directory
		xbmcplugin.addDirectoryItem(self.handle, self.create_params(action='listing', category=title, page=page), category_item, True)
		# ends the directory
		xbmcplugin.endOfDirectory(self.handle)

	# creates base parameters
	def create_params(self, **kwargs):
		# returns addon launch parameters
		return '{0}?{1}'.format(self.address, urlencode(kwargs))

	@staticmethod # filters string to printable characters
	def make_printable(unicode_string):
		# returns a filters ascii string
		return ''.join(x for x in unicode_string if x in string.printable)