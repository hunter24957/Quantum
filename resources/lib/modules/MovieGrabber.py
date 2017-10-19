import threading

# imports all scrapers
from resources.lib.scrapers.OneMovies import *
from resources.lib.scrapers.m4ufree import *

class MovieGrabber:
	# stores our found streams
	streams = dict()
	# stores our scrapers
	scrapers = (OneMovies, m4ufree)
	# creates a write lock
	write_lock = threading.Lock()

	@staticmethod # gets movies streams
	def get_streams(title, year):
		# clears streams
		MovieGrabber.streams = dict()
		# stores our threads
		threads = list()
		# iterates through our scrapers
		for scraper in MovieGrabber.scrapers:
			# creates a new thread
			thread = threading.Thread(target=MovieGrabber.scrape_scraper, args=(scraper, title, year))
			# makes thread a daemon
			thread.daemon = True
			# starts our thread
			thread.start()
			# adds our thread to our list
			threads.append(thread)
		# iterates through threads
		for thread in threads:
			# if the thread is still alive
			if thread.is_alive():
				# waits until thread finish
				thread.join()
		# returns our streams
		return MovieGrabber.streams

	@staticmethod
	def scrape_scraper(scraper, title, year):
		# scrapes our scraper
		results = scraper.get_movie_stream_url(title, year)
		# engages our write lock
		with MovieGrabber.write_lock:
			# extends our streams
			MovieGrabber.streams.update(results)

