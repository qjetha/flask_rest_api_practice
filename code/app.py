from flask import Flask, jsonify, request
from request_blog import Posts

import json

app = Flask(__name__)



@app.route('/api/ping')
def check_status():
	return jsonify({'success': 'true'}), 200



@app.route('/api/posts', methods=['GET'])
def return_posts():
	
	# get arguments from get request and vet that they are specified correctly
	try:
		tags = request.args['tags']							# 'tags' => required argument
	except:
		return jsonify({'error': 'Tags parameter is required'}), 400
	else:
		tags = tags.split(',')

	sort_by = request.args.get('sortBy')					# 'sortBy' => optional argument
	if sort_by not in [None, 'id', 'reads', 'likes', 'popularity']:
		return jsonify({'error': "sortBy parameter is invalid"}), 400

	direction = request.args.get('direction') 				# 'direction' => optional argument
	if direction not in [None, 'desc', 'asc']:
		return jsonify({'error': "direction parameter is invalid"}), 400


	# for each tag in tags, get all posts associated with that tag (parallelized)
	tags_plus_instance = dict()

	for tag in tags:
		tags_plus_instance[tag] = Posts(tag)			# instantiate Posts class and add to dict
		tags_plus_instance[tag].start()					# start thread to invoke run method

	all_posts_across_tags = list()
	for thread in tags_plus_instance.values():			
		thread.join()									# join each thread
		all_posts_across_tags.extend(thread.data)		# append data instance attribute to master list

	
	# Remove duplicate nested dicts within list where uniqueness is defined by id key
	all_U_posts_across_tags = list({v['id']:v for v in all_posts_across_tags}.values())


	# Sort list object by specified field and direction
	if sort_by is not None:
		if (direction is None) or (direction=='asc'):
			all_U_posts_across_tags.sort(key=lambda x : x[sort_by])
		else:
			all_U_posts_across_tags.sort(key=lambda x : x[sort_by], reverse=True)


	# Return list of dicts as a json object
	return json.dumps({'posts': all_U_posts_across_tags}), 200



if __name__ == "__main__":
	app.run(debug=True)