# class that contains listing details
class Listing:
	# instantiates our listing class
	def __init__(self, title, overview, date, rating, poster, backdrop):
		# sets up class attributes
		self.title = title
		self.overview = overview
		self.date = date
		self.rating = rating
		self.poster = poster
		self.backdrop = backdrop

	# the string method of our class
	def __str__(self):
		# returns our string
		return 'Title: {} - Overview: {} - Release Date: {} - Rating: {} - Poster: {} - Backdrop: {}'.format(
			self.title,
			self.overview,
			self.date,
			self.rating,
			self.poster,
			self.backdrop
		)