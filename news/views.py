from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from newsapi import NewsApiClient
from django.views.decorators.http import require_GET
from django.conf import settings
import praw
# Create your views here.

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
            "id": article['source']['id'],
            "headline": article['title'],
            "link": article['url'],
            "source": "newsapi",
            'publishedAt': article['publishedAt']
        })

    for post in reddit_posts:
        newsList.append({
            "id": post.id,
            'headline': post.title,
            'link': post.url,
            'source': 'reddit',
            'publishedAt': post.created_utc
        })

    return JsonResponse({'news': newsList})
