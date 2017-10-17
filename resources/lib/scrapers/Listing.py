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