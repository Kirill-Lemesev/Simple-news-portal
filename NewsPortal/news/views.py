from django.shortcuts import render, redirect
from django.conf import settings
from datetime import datetime
from random import randint
import json


def show_index(request):
    """ Function returns index page """
    return redirect('/news/')


def main_page(request):
    """ Function returns main page of the project """

    with open(settings.NEWS_JSON_PATH, 'r') as json_file:
        news = json.load(json_file)

    ordered_news = sorted(news, key=lambda x: datetime.strptime(x['created'], '%Y-%m-%d %H:%M:%S'), reverse=True)

    for news in ordered_news:
        new_date = news['created'].split()[0]
        news['created'] = new_date

    if request.GET.get('q'):

        sub = request.GET.get('q')

        query_list = []

        for news in ordered_news:
            if sub in news['title']:
                query_list.append(news)

        return render(request, 'news/main.html', {'news': query_list})

    return render(request, 'news/main.html', {'news': ordered_news})


def show_article(request, post_id):
    """ Function returns content by page id """
    content = dict

    with open(settings.NEWS_JSON_PATH, 'r') as json_file:
        news_feed = json.load(json_file)

    for news in news_feed:
        if news['link'] == post_id:
            content = news

    return render(request, 'news/article.html', content)


def add_article(request):
    """ Function returns page for add article and add new news"""
    if request.method == 'POST':

        created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        title = request.POST.get('title')
        text = request.POST.get('text')

        with open(settings.NEWS_JSON_PATH, 'r') as json_file:
            news = json.load(json_file)

        link_list = []
        for article in news:
            link_list.append(article['link'])

        link = randint(0, 9999999)

        while link in link_list:
            link = randint(0, 9999999)

        new_article = {'created': created, 'text': text, 'title': title, 'link': link}

        news.append(new_article)

        with open(settings.NEWS_JSON_PATH, "w") as json_file:
            json.dump(news, json_file)

        return redirect('/news')

    else:
        return render(request, 'news/create.html')
