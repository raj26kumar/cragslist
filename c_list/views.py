import requests
from django.shortcuts import render
from requests.compat import quote_plus
from . import models
from django.http import HttpResponse
from bs4 import BeautifulSoup

base_c_list_url = 'https://hyderabad.craigslist.org/search/hhh?query={}'
image_url = 'https://images.craigslist.org/{}_300x300.jpg'


# Create your views here.


def home(request):
    return render(request, "base.html")

def hello():
    return requests("hello")

def new_search(request):
    search = request.POST.get('search')
    # { starts
    models.Search.objects.create(search=search)
    final_url = base_c_list_url.format(quote_plus(search))
    # <! -- we are adding our search to the link -- >
    # print(quote_plus(search))
    # print(final_url)
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    # <! -- we are scraping data from the response which had final url which has our search name -- >

    # post_titles = soup.find_all('a', {'class': 'result-title'})
    # print(data)
    # print(post_titles[0].get('href'))
    post_listings = soup.find_all('li', {'class': 'result-row'})

    # <! -- we scraped all the date from 'class-result-row' within <li> link -- >

    # post_title = post_listings[0].find(class_='result-title').text      # <! --- this is only to understand how
    # post_url = post_listings[0].find('a').get('href')                   #     we are using in for loop to scrap
    # post_price = post_listings[0].find(class_='result-price').text      #     out required date --->
    # print(post_title)
    # print(post_url)
    # print(post_price)

    final_post = []
    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        # <! -- if price is not available --->
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = image_url.format(post_image_id)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'
        final_post.append((post_title, post_url, post_price, post_image_url))

    # } ends here <! -- this is completly one i.e., interlinked with each other -- >

    user_input_in_search = {
        'search': search,
        'final_post': final_post,
    }
    return render(request, "c_list/search.html", user_input_in_search)
