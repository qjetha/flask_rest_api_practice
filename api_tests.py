'''
TESTING:
	(0) Ensuire that the ping endpoint works as intended
	(1) Ensure that tags is a required parameter to get request
	(2) Ensure that we have correct error handling for incorrectly specified optional arguments
	(3) Ensure that get requests to my API and the original API returns congruent results
			-test various cases including sorting in ascending/descending order
			-test various cases of tags that do not exist in data
'''

import requests, json


endpoint_url_my_api_posts = 'http://127.0.0.1:5000/api/posts'
endpoint_url_my_api_ping = 'http://127.0.0.1:5000/api/ping'
endpoint_url_original = 'https://api.team.io/blog/posts'



# (0) Ensure ping endpoint returns as expected
response = requests.get(endpoint_url_my_api_ping)

assert response.status_code == 200
assert response.json() == {'success': 'true'}



# (1) Ensure test is a required parameter
def check_test_arg(url_addition, good_or_bad):
	response = requests.get(endpoint_url_my_api_posts + '?' + f'{url_addition}' + '&' + 'sortBy=id')

	if good_or_bad == "bad":
		assert response.status_code == 400
		assert response.json() == {'error': 'Tags parameter is required'}
	else:
		assert response.status_code == 200
		assert response.json() != {'error': 'Tags parameter is required'}



test_arg_values = {'good': ['tags=science', 'tags=science,tech', 'tags=history'], 
				   'bad': ['', 'tags1=science', 'TAGS=tech', 'Tags=history']}

for k,v in test_arg_values.items():
	for test in v:
		check_test_arg(url_addition=test, good_or_bad=k)



# (2) Ensure that we have correct error handling for incorrectly specified optional arguments
incorrect_value = 'authorId'
response = requests.get(endpoint_url_my_api_posts + '?' + 'tags=science' + '&' + f'sortBy={incorrect_value}')

assert response.status_code == 400
assert response.json() == {'error': "sortBy parameter is invalid"}


incorrect_value = 'upwards'
response = requests.get(endpoint_url_my_api_posts + '?' + 'tags=science' + '&' + f'direction={incorrect_value}')

assert response.status_code == 400
assert response.json() == {'error': "direction parameter is invalid"}



# (3) Ensure that get requests to my API and the original API returns congruent results
def check_congruency(my_api_response, original_api_response, type):
	if type!="multi-tag":
		assert my_api_response.status_code == 200
		assert original_api_response.status_code == 200

		assert len(my_api_response.json()['posts']) == len(original_api_response.json()['posts'])
		assert my_api_response.json()['posts'] == original_api_response.json()['posts']

	if type=="multi-tag":
		assert(len(my_api_response) <= len(original_api_response)) # because we remove duplicates
		
		combined_unique_posts = list({v['id']:v for v in original_api_response}.values())
		assert my_api_response == combined_unique_posts


# (A) - single tag
my_api_response = requests.get(endpoint_url_my_api_posts + '?' + 'tags=science')
original_api_response = requests.get(endpoint_url_original + '?' + 'tag=science')

check_congruency(my_api_response, original_api_response, 'single')


# (B) - nonsensical tag
my_api_response = requests.get(endpoint_url_my_api_posts + '?' + 'tags=!science!')
original_api_response = requests.get(endpoint_url_original + '?' + 'tag=!science!')

check_congruency(my_api_response, original_api_response, 'nonsensical')


# (C) - multi-tag
my_api_response = requests.get(endpoint_url_my_api_posts + '?' + 'tags=science,history')
original_api_response1 = requests.get(endpoint_url_original + '?' + 'tag=science')
original_api_response2 = requests.get(endpoint_url_original + '?' + 'tag=history')

combined = list()
combined.extend(original_api_response1.json()['posts'])
combined.extend(original_api_response2.json()['posts'])

check_congruency(my_api_response.json()['posts'], combined, 'multi-tag')
