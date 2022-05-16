import tweepy
import random
import re

class TwitterBot:
	def __init__(self, api_key, api_key_secret, access_token, access_token_secret):
		# Authenticate account and create API object
		auth = tweepy.OAuthHandler(api_key, api_key_secret)
		auth.set_access_token(access_token, access_token_secret)
		api = tweepy.API(auth)
		self.api = api

	def request_user_input(self):
		task = input("Would you like to tweet, add or shuffle quotes? ")
		if task == "tweet":
			self.tweet_quote()
		elif task == "shuffle" or task == "shuffle quotes":
			self.shuffle_quotes()
		elif task == "add" or task == "add quote":
			self.add_quote()
		elif task == "exit":
			return
		else:
			print("I'm sorry, that wasn't one of the options.")
			self.request_user_input()

	def is_file_empty(self, lines):
		if not lines:
			add_quote = input("You have no quotes in your backlog. Would you like to add a quote? ")
			if add_quote == "yes":
				self.add_quote()
			else:
				return True # file is empty and user didn't want to add a quote.
		# File is not empty
		return False

	def shuffle_quotes(self):

		# Open file and check that it's not empty
		file = open('quotes.txt', 'r')
		lines = file.readlines()
		file.close()
		if self.is_file_empty(lines):
			return # if the file is empty, exit the function.
		# File is not empty, so we shuffle the lines.
		random.shuffle(lines)

		# Write shuffled lines to file
		new_file = open('quotes.txt', 'w')
		for line in lines:
			new_file.write(line)
		new_file.close()

		print("Shuffle complete.")
		self.request_user_input()

	def add_quote(self):

		# Collect information on the quote
		quote = input("Which quote do you wish to add? ")
		title = input("What's the book's title? ")
		author = input("Who's the author? ")
		# Ask user to review given input
		is_correct = input('Is the following correct: "{quote}" from {title} by {author}. ' \
							.format(quote = quote, title = title, author = author))

		# If everything is correct, add quote to file.
		if is_correct == "yes":

			new_line = '\n"' + quote + '",' + title + ',' + author
			file = open("test.txt", "a")
			file.write(new_line)
			file.close()

			print("Quote has been added.")
			self.request_user_input()

		# Return to beginning of program, to ask user which task to perform.
		elif is_correct == "exit":
			self.request_user_input()	
		# Return to beginning of this function, to ask user for quote information again.
		else: # handles case where is_correct == no 
			self.add_quote()

	def prepare_tweet(self, text):

		# Remove new lines
		text = text.strip("\n")

		# Find and extract quote
		quote_match = re.search(r'".*"', text)
		quote = quote_match.group()
		end_of_quote_idx = quote_match.end()

		# Split book title and author
		title, author = text[end_of_quote_idx + 1:].split(",")
		# Create hashtags
		title_hashtag = " #" + "".join([ch for ch in title if ch.isalnum()])
		author_hashtag = " #" + "".join([ch for ch in author if ch.isalnum()])

		return quote, title_hashtag, author_hashtag

	def tweet_quote(self):

		# Open file and check that it's not empty
		file = open('quotes.txt', 'r')
		lines = file.readlines()
		file.close()
		if self.is_file_empty(lines):
			return # if the file is empty, exit the function.
		# File is not empty, so we store the last line as a variable.
		line_to_tweet = lines[-1]
		# Delete the last line (so we don't try to tweet it again)
		del lines[-1]
		new_file = open('quotes.txt', 'w')
		for line in lines:
			new_file.write(line)
		new_file.close()

		# Prepare tweet by splitting line into quote, title, and author.
		quote, title, author = self.prepare_tweet(line_to_tweet)

		# Check that the quote doesn't exceed Twitter's character limit
		char_limit = 280
		if len(quote) > char_limit:
			print("Oops, that quote was too long. Let me try another.")
			self.tweet_quote()
		else: 
			# Let's tweet it!
			tweet = quote + title + author + " #Quote" + " #BookQuote" + " #BookRecommendation"
			self.api.update_status(status = tweet)
			print("Success! Your tweet has been posted.")
			self.request_user_input()

# Credentials to access Twitter account
api_key = ""
api_key_secret = ""
access_token = ""
access_token_secret = ""

my_twitter_bot = TwitterBot(api_key, api_key_secret, access_token, access_token_secret)	
my_twitter_bot.request_user_input()	
