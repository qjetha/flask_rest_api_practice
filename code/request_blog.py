import requests
import threading

class Posts(threading.Thread):
	
	def __init__(self, tag_name):
		# Call the threading.Thread class's init function
		threading.Thread.__init__(self)
		
		self.tag = tag_name
		self.data = list()


	# over-ride run method
	def run(self):
		access_endpoint = r'https://api.team.io/blog/posts'
	
		params = {
			'tag' : f'{self.tag}'
		}

		response = requests.get(access_endpoint, params=params)

		if response.ok:
			posts = response.json()['posts']
	
			for post in posts:
				self.data.append(post)


	def __repr__(self):
		return f'Gets Blog Post Data for tag: {self.tag}'

