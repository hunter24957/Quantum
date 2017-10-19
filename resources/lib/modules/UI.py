from urllib import urlencode
import string

# imports xbmc api
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon

# class for storing a menu item actions
class MenuItem:
	# initalizes our menu item
	def __init__(self, title, action, icon='icon.png'):
		# sets up our attributes
		self.title = title
		self.action = action
		self.icon = icon

# class that contains listing details
class Listing:
	# instantiates our listing class
	def __init__(self, iden, title, overview, date, rating, poster, backdrop):
		# sets up class attributes
		self.id = iden
		self.title = title
		self.overview = overview
		self.date = date
		self.rating = rating
		self.poster = poster
		self.backdrop = backdrop

# class that contains season details
class Season:
	# instantiates our season class
	def __init__(self, number, iden, title, overview, date, poster):
		# sets up class attributes
		self.number = number
		self.id = iden
		self.title = title
		self.overview = overview
		self.date = date
		self.poster = poster

# class that contains episode details
class Episode:
	# instantiates our episode class
	def __init__(self, number, iden, title, overview, date, rating, poster):
		# sets up class attributes
		self.number = number
		self.id = iden
		self.title = title
		self.overview = overview
		self.date = date
		self.rating = rating
		self.poster = poster

# class contains UI methods
class UI:
	# instantiates our class
	def __init__(self, handle, address):
		# sets up our attributes
		self.handle = handle
		self.address = address
		# gets the addon media path
		self.media_path = xbmcaddon.Addon().getAddonInfo('path') + '\\resources\\media\\'

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
			category_item.setArt({'thumb': self.media_path + category.icon, 'icon': self.media_path +  category.icon, 'fanart': self.media_path + 'fanart.jpg'})
			# adds list item as directory
			xbmcplugin.addDirectoryItem(self.handle, self.create_params(action=category.action, title=category.title, page=1), category_item, True)
		# sets the view to wall
		xbmc.executebuiltin("Container.SetViewMode(500)")
		# ends the directory
		xbmcplugin.endOfDirectory(self.handle)

	# creates a page
	def build_movie_page(self, title, action, page, *args):
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
			xbmcplugin.addDirectoryItem(self.handle, self.create_params(action='movie.play', title=UI.make_printable(movie.title), date=movie.date), category_item)
		# builds a next page button
		self.build_next_page_button(action, title, page)
		# sets the view to wall
		xbmc.executebuiltin('Container.SetViewMode(500)') 
		# ends the directory
		xbmcplugin.endOfDirectory(self.handle)

	# creates a page
	def build_tv_page(self, title, action, page, *args):
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
			xbmcplugin.addDirectoryItem(self.handle, self.create_params(action='tv.season', title=UI.make_printable(show.title), id=show.id, backdrop=show.backdrop), category_item, True)
		# builds a next page button
		self.build_next_page_button(action, title, page)
		# sets the view to wall
		xbmc.executebuiltin('Container.SetViewMode(500)')
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
			xbmcplugin.addDirectoryItem(self.handle, self.create_params(action='tv.episodes', title=UI.make_printable(season.title), id=iden, season=season.number, backdrop=backdrop), category_item, True)
		# sets the view to wall
		xbmc.executebuiltin('Container.SetViewMode(500)')
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
			xbmcplugin.addDirectoryItem(self.handle, self.create_params(action='tv.play', title=UI.make_printable(episode.title), date=episode.date), category_item)
		# sets the view to wall
		xbmc.executebuiltin('Container.SetViewMode(500)')
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

	# builds a next page button
	def build_next_page_button(self, action, title, page):
		# creates a next page button
		category_item = xbmcgui.ListItem('Next Page')
		# sets the list item info
		category_item.setArt({'fanart': self.media_path + 'fanart.jpg'})
		# increments page
		page = int(page) + 1
		# adds list item as directory
		xbmcplugin.addDirectoryItem(self.handle, self.create_params(action=action, title=title, page=page), category_item, True)

	# creates base parameters
	def create_params(self, **kwargs):
		# returns addon launch parameters
		return '{0}?{1}'.format(self.address, urlencode(kwargs))

	@staticmethod # filters string to printable characters
	def make_printable(unicode_string):
		# returns a filters ascii string
		return ''.join(x for x in unicode_string if x in string.printable)