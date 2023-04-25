from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from newsapi import NewsApiClient
from django.views.decorators.http import require_GET
from django.conf import settings
import praw
import datetime
from getnews.models import News
from django.shortcuts import get_object_or_404
import json

reddit = praw.Reddit(client_id=settings.REDDIT_CLIENT_ID,
                     client_secret=settings.REDDIT_CLIENT_SECRET,
                     user_agent=settings.REDDIT_USER_AGENT)

newsapi = NewsApiClient(api_key=settings.NEWS_API_KEY)


@require_GET
def listNews(request):

    query = request.GET.get('query')

    news_headlines = newsapi.get_top_headlines(
        language='en', q=query, page_size=5)

    if query:
        reddit_posts = reddit.subreddit('news').search(query, limit=10)
    else:
        reddit_posts = reddit.subreddit('news').hot(limit=10)

    newsList = []
    for article in news_headlines['articles']:
        newsList.append({
            "news_id": article['source']['id'],
            "headline": article['title'],
            "link": article['url'],
            "source": "newsapi",
            'published_at': article['publishedAt']
        })

    for post in reddit_posts:
        newsList.append({
            "news_id": post.id,
            'headline': post.title,
            'link': post.url,
            'source': 'reddit',
            'published_at': post.created_utc
        })

    return JsonResponse({'news': newsList})


@require_GET
def get_news(request):
    # get search query from request parameters
    search_query = request.GET.get('query')
    if not search_query:
        search_query = ''
    # set expiry limit to 5 minutes ago
    expiry_limit = datetime.datetime.utcnow() - datetime.timedelta(minutes=5)

    # check if we have a news item in the database for this search query

    news_item = News.objects.filter(
        headline__icontains=search_query)

    # if we have a news item and it was updated within the expiry limit, return it
    response_data = []
    if len(news_item):
        print(news_item)
        for i in news_item:
            response_data.append({
                'news_id': i.news_id,
                'headline': i.headline,
                'link': i.link,
                'favorite': False,
                'source': i.source,
                'published_at': i.published_at,
                'updated_at': i.updated_at
            })
    # # otherwise, make a fresh API call, update the news item in the database, and return it
    else:
        # get news data from APIs
        query = request.GET.get('query')
        news_headlines = newsapi.get_top_headlines(
            language='en', q=query, page_size=5)

        if query:
            reddit_posts = reddit.subreddit('news').search(query, limit=10)
        else:
            reddit_posts = reddit.subreddit('news').hot(limit=10)

        merged_data = []
        for article in news_headlines['articles']:
            if article['source']['id']:
                merged_data.append({
                    "news_id": article['source']['id'],
                    "headline": article['title'],
                    "link": article['url'],
                    "source": "newsapi",
                    'published_at': article['publishedAt']
                })

        for post in reddit_posts:
            if post.id:
                merged_data.append({
                    "news_id": post.id,
                    'headline': post.title,
                    'link': post.url,
                    'source': 'reddit',
                    'published_at': post.created_utc
                })

        response_data = []
        for obj in merged_data:
            news_item = News.objects.create(
                user=str(settings.USER_NAME),
                news_id=obj['news_id'],
                headline=obj['headline'],
                link=obj['link'],
                source=obj['source'],
                favorite=False,
                published_at=obj['published_at'],
                updated_at=datetime.datetime.utcnow(),
            )
            news_item.save()
            response_data.append(news_item)

    # return response data as JSON
    return JsonResponse({'res': response_data})


def toggle_favorite(request):
    # Get the id and user from the query parameters
    news_id = request.GET.get('id')
    user = request.GET.get('user')

    # Find the News object with the given news_id and user
    obj = get_object_or_404(News, id=news_id, user=user)

    # Toggle the favorite field
    obj.favorite = not obj.favorite
    obj.save()

    # Return a JSON response with the updated favorite status
    return JsonResponse({'res': obj})
