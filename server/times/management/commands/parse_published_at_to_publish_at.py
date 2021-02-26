from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta, date
from django.db.models import Count, Sum
from times.models import Article


class Command(BaseCommand):
    def print(self, *args):
        print(f"[{timezone.localtime().strftime('%Y/%m/%d %H:%M:%S')}]", *args)

    def handle(self, *args, **options):
        self.print("Parse published_at to publish_at for Articles Start.")
        articles = Article.objects.all()
        for article in articles:
            if article.published_at != article.publish_at:
                article.publish_at = article.published_at
                article.save()
                print(f"Article {article.id}({article.title}).publish_at was updated to {article.publish_at}")
        self.print("Parse Finished.")