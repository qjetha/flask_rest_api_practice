# Description

Writes a simple REST API in Flask to provide users with a listing of all the blog posts that have at least one tag specified in the tags parameter. The API has 2 endpoints:

1. The ping endpoint allows the GET method and simply returns a JSON object with 'success' == true.
2. The posts endpoint allows the GET method and three query parameters:
    * tags -> for the user to specify a comma separated list of blog post tags (required parameter)
    * sortBy -> allows the user to specify a field to sort the posts by (optional)
    * direction -> specifies the direction for sorting (optional)



# How it Works

As this is simply a practice project, the Flask API gets the blog post data by issuing a GET request to another API (yes, this is silly!). The request_blog.py file makes the request to the API, which must be done separately for each tag. So for each tag the user specified in the tags query parameter, we must call the Posts class in the request_blog.py file. To speed this up, we use threading to issue requests in parallel. The unique listing of posts that is returned from these API calls is returned as a JSON object.



