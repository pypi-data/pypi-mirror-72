from urllib.request import urlopen

query = None
class Video:
	def __init__(self, search):
		global query
		query = search
	def search(self):
		global query
		url = "https://youtube.com/results?search_query=" + query.replace(' ','+')
		html = urlopen(url)
		nonecode = html.read()
		code = str(nonecode)
		f = code.find("watch?v")
		url = "https://youtube.com/" + code[f] + code[f+1] + code[f+2] + code[f+3] + code[f+4] + code[f+5] + code[f+6] + code[f+7] + code[f+8] + code[f+9] + code[f+10] + code[f+11] + code[f+12] + code[f+13] + code[f+14] + code[f+15] + code[f+16] + code[f+17] + code[f+18]
		
		if url.endswith("'b'<!doctype html><"):
			return None
		else:
			return url