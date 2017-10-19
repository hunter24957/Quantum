# this script will deal with the parameters passed into our addon
import sys
from urlparse import parse_qsl
from datetime import datetime

import xbmcgui

# imports our scrapers and modules
from resources.lib.modules.MovieGrabber import *
from resources.lib.scrapers.TMDB import *
from resources.lib.modules.UI import *

# KODI WORKS BY CALLING OUR ADDON WHEN A USER CLICKS IT
# THE ADDONS SETS THE STATES (SETS UP UI) THEN CALLS KODI
# WHEN A USER INTERACT KODI CALLS OUR ADDON WITH PARAMETERS THAT WE WILL PARSE HERE

# gets addon handle
addon_handle = int(sys.argv[1])
# gets the addon base address
base_address = sys.argv[0]
# instantiates our UI with our addon handle and base address
GUI = UI(addon_handle, base_address)
# passed decoded parameters into the parser
params = dict(parse_qsl(sys.argv[2][1:]))

# builds the main menu
if not params:
	# creates our menu
	menu = (
		# adds movie selection
		MenuItem('Movies', 'menu.movies'),
		# adds television selection
		MenuItem('Television', 'menu.tv'),
		# adds search selection
		# MenuItem('Search People', 'build_text', 'search_people')
	)
	# builds our menu
	GUI.build_menu('Menu', *menu)

# builds the movie menu
elif params['action'] == 'menu.movies':
	# creates our menu
	menu = (
		# adds popular selection
		MenuItem('Popular', 'movies.popular'),
		# adds top rated selection
		MenuItem('Top Rated', 'movies.top_rated'),
		# adds now playing selection
		MenuItem('Now Playing', 'movies.now_playing'),
		# adds upcoming selection
		MenuItem('Upcoming', 'movies.upcoming'),
		# adds genres selection
		MenuItem('Genres', 'movies.genres'),
		# adds years selection
		MenuItem('Years', 'movies.years'),
		# adds search selection
		# MenuItem('Search', 'build_text')
	)
	# builds our menu
	GUI.build_menu('Movies', *menu)

# builds the tv menu
elif params['action'] == 'menu.tv':
	# creates our menu
	menu = (
		# adds popular selection
		MenuItem('Popular', 'tv.popular', 'popular.png'),
		# adds top rated selection
		MenuItem('Top Rated', 'tv.top_rated'),
		# adds now playing selection
		MenuItem('Now Playing', 'tv.now_playing'),
		# adds upcoming selection
		MenuItem('Upcoming', 'tv.upcoming'),
		# adds genres selection
		MenuItem('Genres', 'tv.genres'),
		# adds years selection
		MenuItem('Years', 'tv.years'),
		# adds search selection
		# MenuItem('Search', 'build_text', 'search_shows')
	)
	# builds our menu
	GUI.build_menu('Television', *menu)

# builds the movie genre menu
elif params['action'] == 'movies.genres':
	# creates our menu
	menu = (MenuItem(genre, 'movies.genre') for genre in TMDB.get_genres('movie').keys())
	# builds our menu
	GUI.build_menu('Genres', *menu)

# builds the movie years menu
elif params['action'] == 'movies.years':
	# creates our menu
	menu = (MenuItem(str(year), 'movies.year') for year in xrange(datetime.now().year, 1900, -1))
	# builds our menu
	GUI.build_menu('Years', *menu)

# builds the tv years menu
elif params['action'] == 'tv.genres':
	# creates our menu
	menu = (MenuItem(genre, 'tv.genre') for genre in TMDB.get_genres('tv').keys())
	# builds our menu
	GUI.build_menu('Genres', *menu)

# builds the tv years menu
elif params['action'] == 'tv.years':
	# creates our menu
	menu = (MenuItem(str(year), 'tv.year') for year in xrange(datetime.now().year, 1900, -1))
	# builds our menu
	GUI.build_menu('Years', *menu)

# builds a popular movie page
elif params['action'] == 'movies.popular':
	# gets the popuar movie listings
	listings = TMDB.get_movies_by_category('popular', params['page'])
	# builds a movie page with the listings
	GUI.build_movie_page('Popular', 'movies.popular', params['page'], *listings)

# builds a top rated movie page
elif params['action'] == 'movies.top_rated':
	# gets the top rated movie listings
	listings = TMDB.get_movies_by_category('top_rated', params['page'])
	# builds a movie page with the listings
	GUI.build_movie_page('Top Rated', 'movies.top_rated', params['page'], *listings)

# builds a now playing movie page
elif params['action'] == 'movies.now_playing':
	# gets the now playing movie listings
	listings = TMDB.get_movies_by_category('now_playing', params['page'])
	# builds a movie page with the listings
	GUI.build_movie_page('Now Playing', 'movies.now_playing', params['page'], *listings)

# builds a upcoming movie page
elif params['action'] == 'movies.upcoming':
	# gets the upcoming show listings
	listings = TMDB.get_movies_by_category('upcoming', params['page'])
	# builds a movie page with the listings
	GUI.build_movie_page('Upcoming', 'movies.upcoming', params['page'], *listings)

# builds a movie genre page
elif params['action'] == 'movies.genre':
	# gets the movie listings by genre
	listings = TMDB.get_movies_by_genre(params['title'], params['page'])
	# builds a movie page with the listings
	GUI.build_movie_page(params['title'], 'movies.genre', params['page'], *listings)

# builds a movie year page
elif params['action'] == 'movies.year':
	# gets the movie listings by year
	listings = TMDB.get_movies_by_year(params['title'], params['page'])
	# builds a movie page with the listings
	GUI.build_movie_page(params['title'], 'movies.year', params['page'], *listings)

# builds a popular movie page
elif params['action'] == 'tv.popular':
	# gets the popuar show listings
	listings = TMDB.get_shows_by_category('popular', params['page'])
	# builds a movie page with the listings
	GUI.build_tv_page('Popular', 'movies.popular', params['page'], *listings)

# builds a top rated tv page
elif params['action'] == 'tv.top_rated':
	# gets the top rated show listings
	listings = TMDB.get_shows_by_category('top_rated', params['page'])
	# builds a movie page with the listings
	GUI.build_tv_page('Top Rated', 'movies.top_rated', params['page'], *listings)

# builds a now playing tv page
elif params['action'] == 'tv.now_playing':
	# gets the now playing show listings
	listings = TMDB.get_shows_by_category('now_playing', params['page'])
	# builds a movie page with the listings
	GUI.build_tv_page('Now Playing', 'movies.now_playing', params['page'], *listings)

# builds a upcoming tv page
elif params['action'] == 'tv.upcoming':
	# gets the upcoming show listings
	listings = TMDB.get_shows_by_category('upcoming', params['page'])
	# builds a movie page with the listings
	GUI.build_tv_page('Upcoming', 'movies.upcoming', params['page'], *listings)

# builds a tv genre page
elif params['action'] == 'tv.genre':
	# gets the show listings by genre
	listings = TMDB.get_shows_by_genre(params['title'], params['page'])
	# builds a movie page with the listings
	GUI.build_tv_page(params['title'], 'movies.genre', params['page'], *listings)

# builds a tv year page
elif params['action'] == 'tv.year':
	# gets the show listings by year
	listings = TMDB.get_shows_by_year(params['title'], params['page'])
	# builds a movie page with the listings
	GUI.build_tv_page(params['title'], 'movies.year', params['page'], *listings)

elif params['action'] == 'tv.season':
	# gets listings of category
	listings = TMDB.get_show_seasons(params['id'])
	# builds a page with the listings
	GUI.build_series_page(params['title'], params['id'], params['backdrop'], *listings)

elif params['action'] == 'tv.episodes':
	# gets listings of category
	listings = TMDB.get_season_episodes(params['id'], params['season'])
	# builds a page with the listings
	GUI.build_episode_page(params['title'], params['backdrop'], *listings)

elif params['action'] == 'tv.play':
	pass

elif params['action'] == 'movie.play':
	# gets the movie streams
	streams = MovieGrabber.get_streams(params['title'], params['date'].split('-')[0])
	# if there are any streams
	if streams:
		# stores our stream titles
		stream_titles = list()
		# stores our stream urls
		stream_urls = list()
		# iterates through dict
		for title, url in streams.iteritems():
			# appends title
			stream_titles.append(title)
			# appends url
			stream_urls.append(url)
		# creates a dialog box
		selected_item = xbmcgui.Dialog().select(params['title'], stream_titles)
		# indexes our list
		selected_stream = stream_urls[selected_item]
		# plays the movie
		xbmc.Player().play(selected_stream)
	# else we notifiy the user
	else: xbmcgui.Dialog().notification('Sorry', 'No stream found')