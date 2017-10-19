# imports requests and beautifulsoup
import requests
from bs4 import BeautifulSoup

class OneMovies:
	# A static class that scrapes streams from one movies
	@staticmethod # Takes a movie title and returns a link to the page
	def get_movie_page_url(title, year):
		# searches website for movies
		results = requests.get('https://1movies.online/search_all/{0}/movies'.format('{0} {1}'.format(title, year)))
		# adds results to parser
		results_parsed = BeautifulSoup(results.content, 'html.parser')
		# gets movies section
		results_movies = results_parsed.find('div', {'class': 'flex_offers'})
		# iterates through movies
		for movie in results_movies.find_all('div', {'class': 'poster new'}):
			# if the title is equal to the title arg and year is equal to the year arg
			if title in movie['data-name'].strip().lower() and movie['data-year'].strip() == year:
				# return the link to the movie
				return 'https://1movies.online' + movie['data-href']

	@staticmethod # Takes a movie title and returns a link to the stream
	def get_movie_stream_url(title, year):
		# gets the movie page url
		movie_url = OneMovies.get_movie_page_url(title.strip().lower(), year.strip())
		print(movie_url)
		# if we have a link
		if movie_url:
			# makes sure we are sending an xml request
			xml_request = {'X-Requested-With': 'XMLHttpRequest'}
			# requests a link to the stream
			links = requests.get(movie_url + '-watch-online-free.html/newLink', headers=xml_request)
			# returns the links
			try: return {'OneMovies | {0} | {1}'.format(stream['label'], stream['type']):stream['file'] for stream in links.json()}
			# if there is a key error return other
			except KeyError: return {'OneMovies | {0}'.format(stream['type']):stream['file'] for stream in links.json()}

	@staticmethod # takes the url of an episode page and an episode number and gets the required episode
	def get_episode_url(url, episode_number):
		# gets show page
		show_page = requests.get(url)
		# adds page to parser
		show_page_parsed = BeautifulSoup(show_page.content, 'html.parser')
		# gets episodes section
		show_episodes = show_page_parsed.find('div', {'id': 'episodes'})
		# iterates through episodes
		for episode in show_episodes.find_all('a', {'class': 'episode '}):
			# if the episode numer is equal to the episode arg
			if episode['data-number'].strip() == episode_number.strip():
				# returns the url
				return 'https://1movies.online' + episode['href']

if __name__ == '__main__':
	movie_url = OneMovies.get_movie_stream_url('Wonder Woman', '2017')
	print(movie_url)