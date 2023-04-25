from django.http import JsonResponse
from newsapi import NewsApiClient
from django.views.decorators.http import require_GET
from django.conf import settings
import praw
import datetime
from getnews.models import News
from django.shortcuts import get_object_or_404
from django.utils import timezone

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


def toggle_favorite(request):
    # Get the id and user from the query parameters
    news_id = request.GET.get('id')
    user = request.GET.get('user')

    # Find the News object with the given news_id and user
    if news_id:
        obj = get_object_or_404(News, id=news_id, user=user)
        obj.favorite = not obj.favorite
        obj.save()
        res = {
            "user": obj.user,
            "favorite": obj.favorite,
            "id": obj.id,
            "headline": obj.headline,
            "link": obj.link,
            "source": obj.source
        }
        return JsonResponse({'Response': res})

    else:
        favorite_news = News.objects.filter(favorite=True, user=user)
        res = []
        for obj in favorite_news:
            res.append({
                "id": obj.id,
                "headline": obj.headline,
                "link": obj.link,
                "source": obj.source
            })
        return JsonResponse({'Response': res})


def thirdPartyAPICalls():
    news_headlines = newsapi.get_top_headlines(
        language='en', page_size=10)

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
    return merged_data


def storeDataInDB(request):

    news_headlines = newsapi.get_top_headlines(
        language='en', page_size=10)

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
        newsExist = News.objects.filter(news_id=obj['news_id'])
        if len(newsExist):
            continue
        else:
            news_item = News(
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
            response_data.append({
                "user": news_item.user,
                "favorite": news_item.favorite,
                "id": news_item.id,
                "headline": news_item.headline,
                "link": news_item.link,
                "source": news_item.source,
                'favorite': False,
                'published_at': news_item.published_at,
                'updated_at': news_item.updated_at,
            })
    return response_data


def collectNews(request):
    five_minutes_ago = timezone.now() - timezone.timedelta(minutes=5)
    newsExist = News.objects.filter(updated_at__gt=five_minutes_ago)
    response = []
    if len(newsExist):
        print('insideee')
        for news_item in newsExist:
            response.append({
                "user": news_item.user,
                "favorite": news_item.favorite,
                "id": news_item.id,
                "headline": news_item.headline,
                "link": news_item.link,
                "source": news_item.source,
                'favorite': False,
                'published_at': news_item.published_at,
                'updated_at': news_item.updated_at,
            })
        return JsonResponse({'res': response})

    else:
        print('outtttt')
        data = storeDataInDB(request=None)
        return JsonResponse({'res': data})
