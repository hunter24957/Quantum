import requests
from bs4 import BeautifulSoup

class MovieScraper:
	"""A class that scrapes streams to movies"""

	def __init__(self):
		pass

	@staticmethod
	def get_movie(title):
		# searches website
		results = requests.get('https://1movies.online/search_all/' + title)
		# adds results to parser
		results_parsed = BeautifulSoup(results.content, 'html.parser')
		# gets movies section
		results_movies = results_parsed.find('div', {'class': 'flex_offers search_flex_offers'})
		# iterates through movies
		for movie in results_movies.find_all('div', {'class': 'poster new'}):
			# if the title is equal to the title arg
			if movie['data-name'] == title:
				# return the link to the movie
				return 'https://1movies.online' + movie['data-href']

	@staticmethod
	def get_movie_stream(title):
		# gets the movie page url
		movie_url = MovieScraper.get_movie(title)
		# if we have a link
		if movie_url:
			# makes sure we are sending an xml request
			xml_request = {'X-Requested-With': 'XMLHttpRequest'}
			# requests a link to the stream
			links = requests.get(movie_url + '-watch-online-free.html/newLink', headers=xml_request)
			# iterates through links
			for link in links.json():
				try:
					# if this is a high resolution
					if link['res'] > 360:
						# return the stream link
						return link['src']
				except KeyError:
					# return the stream link
					return link['src']
		else:
			print("Movie not found.")

if __name__ == '__main__':
	# gets a movie stream
	print(MovieScraper.get_movie_stream('IT (2017)'))
	# waits to exit
	input()

