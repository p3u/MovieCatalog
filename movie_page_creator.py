
from urllib import urlopen
import json
import fresh_tomatoes
import media
import random

#
n_movies = 6
api_key = "48c37abd49c54acd1204d6d19fb990d7"


def get_youtube_url(movie_data):
    # Gets the first youtube returned link from themoviedb if exists
    if "videos" in movie_data:
        for video in movie_data["videos"]["results"]:
            if video["site"] == "YouTube":
                return "https://www.youtube.com/watch?v=" + video["key"]
    # Fallback video
    return "https://www.youtube.com/watch?v=7rVt2b80L-A"


def get_movie_poster(movie_data):
    poster_img = "http://image.tmdb.org/t/p/w185//"
    poster_img += str(movie_data.get("poster_path", "None"))
    if (poster_img == "http://image.tmdb.org/t/p/w185//None"):
        poster_img = "https://i.imgur.com/Z2MYNbj.png/large_movie_poster.png"  # NOQA
    return poster_img


def create_random_movie():
    # Connects to the database to get a random movie (from the first 1000)
    # Proccesses the data and returns a Movie object
    connection = urlopen("https://api.themoviedb.org/3/movie/" +
                         str(random.randrange(1, 1000)) +
                         "?api_key=" + api_key + "&append_to_response=videos")
    movie_json = connection.read()
    movie_data = json.loads(movie_json)
    if movie_data.get("status_code") == 34:  # If movie not found, try again
        return create_random_movie()
    else:
        return media.Movie(movie_data.get("title", "-").encode("utf-8"),
                           movie_data.get("overview", "-").encode("utf-8"),
                           get_movie_poster(movie_data),
                           get_youtube_url(movie_data))


# Create a list of n random movies, and display them on a page
movie_list = []
for i in range(n_movies):
    print str(i + 1) + "/" + str(n_movies)
    movie_list.append(create_random_movie())
fresh_tomatoes.open_movies_page(movie_list)
