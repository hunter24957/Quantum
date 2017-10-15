# imports requests and beautifulsoup
import requests
from bs4 import BeautifulSoup

class OneMovies:
	# A static class that scrapes streams from one movies
	@staticmethod # Takes a movie title and returns a link to the page
	def get_movie_page_url(title, year, series=False):
		# searches website for shows
		if series: results = requests.get('https://1movies.online/search_all/{}/series'.format(title))
		# searches website for movies
		else: results = requests.get('https://1movies.online/search_all/{}/movies'.format(title))
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
	def get_movie_stream_url(title, year, series=False, episode=None):
		# gets the movie page url
		movie_url = OneMovies.get_movie_page_url(title.strip().lower(), year.strip(), series)
		# if it is a series get the episode url
		if series: movie_url = '-'.join(OneMovies.get_episode_url(show_url, episode).split('-')[:-3])
		# if we have a link
		if movie_url:
			# makes sure we are sending an xml request
			xml_request = {'X-Requested-With': 'XMLHttpRequest'}
			# requests a link to the stream
			links = requests.get(movie_url + '-watch-online-free.html/newLink', headers=xml_request)
			# iterates through links
			for link in links.json():
				# return the first stream link (highest quality)
				return link['src']

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
	# gets a link to a movie stream
	stream_url = OneMovies.get_movie_stream_url(title='It', year='2017')
	# prints the stream url
	print(stream_url)
	# waits to exit
	input()