from django.shortcuts import resolve_url
from django.conf import settings
from django.utils import timezone
from django.contrib.sitemaps import ping_google as base_ping_google
from twitter import Twitter
from twitter import OAuth as TwitterOAuth
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from apscheduler.jobstores.base import JobLookupError
from .models import Article


class Publish:
    twitter_consumer_key = settings.TWITTER_CONSUMER_KEY
    twitter_consumer_secret = settings.TWITTER_CONSUMER_SECRET
    twitter_token = settings.TWITTER_ACCOUNT_TOKEN
    twitter_token_secret = settings.TWITTER_ACCOUNT_TOKEN_SECRET
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        future_articles = Article.objects.filter(publish_at__gt=timezone.localtime(), is_publishable=True)
        for article in future_articles:
            self.add_publish_job(article)

    def tweet(self, text):
        if self.twitter_consumer_key and self.twitter_consumer_secret:
            twitter = Twitter(auth=TwitterOAuth(consumer_key=self.twitter_consumer_key, consumer_secret=self.twitter_consumer_secret, token=self.twitter_token, token_secret=self.twitter_token_secret))
            twitter.statuses.update(status=text)
        else:
            print("[Bash Tweet Debug]")
            print(text)

    def ping_google(self):
        if not settings.DEBUG:
            try:
                base_ping_google()
            except Exception:
                pass
        else:
            print("[Google ping Debug]")

    def do_publish(self, article_id):
        self.ping_google()
        article = Article.objects.get(id=article_id)
        tweet_text = f"""{article.sns_publish_text}

「{article.title}」を公開しました

https://iniad-wm.com{article.get_url("article", ["slug", "id"])}"""
        self.tweet(tweet_text)
        article.is_published = True
        article.save()

    def add_publish_job(self, article):
        self.scheduler.add_job(self.do_publish, trigger=DateTrigger(run_date=article.publish_at, timezone=timezone.get_default_timezone()), id=str(article.id), kwargs={"article_id": article.id})
        print(f"Added publish job: Article {article.id}({article.title})")

    def remove_publish_job(self, article):
        self.scheduler.remove_job(job_id=str(article.id))
        print(f"Remove publish job: Article {article.id}({article.title})")

    def add_or_update_publish_job(self, article):
        try:
            self.remove_publish_job(article)
        except JobLookupError:
            pass
        self.add_publish_job(article)

    def publish(self, article):
        if article.is_publishable:
            if not article.is_published:
                if article.publish_at > timezone.localtime():
                    self.add_or_update_publish_job(article)
                else:
                    self.do_publish(article.id)
            else:
                self.ping_google()
