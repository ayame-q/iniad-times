from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta, date
from django.db.models import Count, Sum
from times.models import Article, PreArticle, PreArticleWriterRelation


class Command(BaseCommand):
    def print(self, *args):
        print(f"[{timezone.localtime().strftime('%Y/%m/%d %H:%M:%S')}]", *args)

    def handle(self, *args, **options):
        self.print("Make PreArticle instances from Article without parent")
        articles = Article.objects.filter(parents=None)
        for article in articles:
            writers = article.article_writers.all()
            editors = article.article_editors.all()
            prearticle = PreArticle.objects.create(
                slug=article.slug,
                title=article.title,
                text=article.text,
                last_staff=article.last_staff,
                category=article.category,
                eyecatch=article.eyecatch,
                publish_at=article.publish_at,
                sns_publish_text=article.sns_publish_text,
                is_public=article.is_public,
                is_draft=False,
                is_final=True,
                revise_count=2,
                article=article
            )
            for writer in writers:
                PreArticleWriterRelation.objects.create(prearticle=prearticle, staff=writer, writer_check=True)
            for editor in editors:
                prearticle.article_editors.add(editor)
        self.print("Finished.")