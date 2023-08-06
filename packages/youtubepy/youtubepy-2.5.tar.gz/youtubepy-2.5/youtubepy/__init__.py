from urllib.request import urlopen
import youtube_dl

class Video:
	def __init__(self, search):
		self.query = search
		url = "https://www.youtube.com/results?search_query=" + self.query.replace(' ','+')
		html = urlopen(url)
		nonecode = html.read()
		code = str(nonecode)
		f = code.find("watch?v")
		url = "https://www.youtube.com/" + code[f] + code[f+1] + code[f+2] + code[f+3] + code[f+4] + code[f+5] + code[f+6] + code[f+7] + code[f+8] + code[f+9] + code[f+10] + code[f+11] + code[f+12] + code[f+13] + code[f+14] + code[f+15] + code[f+16] + code[f+17] + code[f+18]
		opts = {}
		with youtube_dl.YoutubeDL(opts) as ytdl:
			data = ytdl.extract_info(url, download=False)
		self.url = url
		self.data = data
	def search(self):
		if self.url.endswith("'b'<!doctype html><"):
			return None
		else:
			return self.url
	def title(self):
		data = self.data
		title = data["title"]
		return title
	def channel_url(self):
		data = self.data
		url = data["channel_url"]
		return url
	def thumbnail(self):
		data = self.data
		thumb = data["thumbnail"]
		return thumb
	def duration(self):
		data = self.data
		duration = data["duration"]
		return duration
	def view_count(self):
		data = self.data
		count = data["view_count"]
		return count
	def like_count(self):
		data = self.data
		count = data["like_count"]
		return count
	def dislike_count(self):
		data = self.data
		count = data["dislike_count"]
		return count
	def average_rating(self):
		data = self.data
		rating = data["average_rating"]
		return rating
	def channel_name(self):
		data = self.data
		name = data["uploader"]
		return name
class ExtractInfo:
	def __init__(self,url):
		opts = {}
		with youtube_dl.YoutubeDL(opts) as ytdl:
			self.data = ytdl.extract_info(url, download=False)
			self.url = url
	def title(self):
		data = self.data
		title = data["title"]
		return title
	def channel_url(self):
		data = self.data
		url = data["channel_url"]
		return url
	def thumbnail(self):
		data = self.data
		thumb = data["thumbnail"]
		return thumb
	def duration(self):
		data = self.data
		duration = data["duration"]
		return duration
	def view_count(self):
		data = self.data
		count = data["view_count"]
		return count
	def like_count(self):
		data = self.data
		count = data["like_count"]
		return count
	def dislike_count(self):
		data = self.data
		count = data["dislike_count"]
		return count
	def average_rating(self):
		data = self.data
		rating = data["average_rating"]
		return rating
	def channel_name(self):
		data = self.data
		name = data["uploader"]
		return name