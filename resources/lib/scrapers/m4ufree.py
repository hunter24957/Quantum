# imports requests and beautifulsoup
import requests
from bs4 import BeautifulSoup
import json

class m4ufree:
	# A static class that scrapes streams from m4ufree
	@staticmethod # Takes a movie title and returns a link to the page
	def get_movie_page_url(title, year):
		# creates search params
		search_params = {'keyword': '{0} {1}'.format(title, year)}
		# searches website for listings
		results = requests.get('http://m4ufree.com/', params=search_params)
		# adds results to parser
		results_parsed = BeautifulSoup(results.content, 'html.parser')
		# iterates through movies
		for listing in results_parsed.find_all('div', {'class': 'item'}):
			# gets the url
			listing_url = listing.find('a')
			# gets the listing title
			title = listing_url['title'].strip().lower()
			# if the title arg is in the title and year arg is in the title
			if title.strip().lower() in title and year.strip() in title:
				# return the link to the movie
				return 'http://m4ufree.com' + listing_url['href'][1:]

	@staticmethod # Takes a movie title and returns a link to the stream
	def get_movie_stream_url(title, year):
		# gets the listing page url
		listing_url = m4ufree.get_movie_page_url(title, year)
		# if we have a link
		if listing_url:
			# gets the page to extract tokens
			listing_page = requests.get(listing_url)
			# extracts token to request a stream
			token = listing_page.text.split('<span class="singlemv active" data="')[-1].split('" >')[0]
			# creates request stream data
			stream_request = {'m4u': token}
			# requests a link to the stream
			links = requests.post('http://m4ufree.com/ajax_new.php', data=stream_request)
			# extracts the json streams
			json_streams = json.loads(links.text.split('sources:')[-1].split('controls:')[0].strip()[:-1])
			# returns the links
			return {'m4ufree | {0} | {1}'.format(stream['label'], stream['type']):stream['file'] for stream in json_streams}

if __name__ == '__main__':
	movie_url = m4ufree.get_movie_stream_url('IT', '2017')
	print(movie_url)