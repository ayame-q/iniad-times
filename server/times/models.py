import io
import sys

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.shortcuts import resolve_url
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from datetime import timedelta
from uuid import uuid4
from stdimage import StdImageField
from .get_diff import get_diff

# Create your models here.


publish = None


courses = [
    ("none", "なし"),
    ("engineering", "エンジニアリングコース"),
    ("design", "デザインコース"),
    ("business", "ビジネスコース"),
    ("civil-system", "シビルシステムコース"),
]


class Staff(models.Model):
    email = models.EmailField(verbose_name="メールアドレス", unique=True, db_index=True)
    slug = models.SlugField(max_length=20, default="", null=True, blank=True, db_index=True, verbose_name="スクリーンネーム")
    name = models.CharField(max_length=20, default="", null=True, blank=True, verbose_name="ペンネーム")
    comment = models.TextField(null=True, blank=True, verbose_name="コメント")

    def __str__(self):
        try:
            if not self.name:
                return f"ペンネームなし ({self.user.name})"
            return f"{self.name} ({self.user.name})"
        except User.DoesNotExist:
            if not self.name:
                return self.email
            return f"{self.name} [{self.email}]"

    def save(self, *args, **kwargs):
        result = super(Staff, self).save(*args, **kwargs)
        if self.email:
            try:
                user = User.objects.get(email=self.email)
                user.staff = self
                user.save()
            except User.DoesNotExist:
                pass
        return result


class User(AbstractUser):
    uuid = models.UUIDField(default=uuid4, unique=True, db_index=True, editable=False, verbose_name="UUID")
    student_id = models.CharField(max_length=10, default="", null=True, blank=True, verbose_name="学籍番号")
    name = models.CharField(max_length=40, default="", null=True, blank=True, verbose_name="氏名")
    display_name = models.CharField(max_length=20, default="No name", verbose_name="公開名")
    entry_year = models.IntegerField(null=True, blank=True, verbose_name="入学年度")
    email = models.EmailField(verbose_name="メールアドレス", unique=True, db_index=True)
    staff = models.OneToOneField(Staff, related_name="user", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="スタッフID")
    created_at = models.DateTimeField(default=timezone.localtime, verbose_name="作成日")
    is_student = models.BooleanField(default=False, verbose_name="学生か")

    def __str__(self):
        return f"{self.username} ({self.name})"

    def get_class(self):
        if self.is_student:
            return self.entry_year - 2016
        else:
            return None


class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=24, verbose_name="カテゴリ名")
    display_name = models.CharField(max_length=40, verbose_name="表示名")

    def __str__(self):
        return self.display_name


class Tag(models.Model):
    name = models.CharField(max_length=24, verbose_name="タグ名")


class Image(models.Model):
    staff = models.ForeignKey(Staff, related_name="images", on_delete=models.SET_NULL, null=True, verbose_name="アップロードスタッフ")
    image = StdImageField(upload_to="upload_images", variations={'large': {'width': 2048, 'height': 1536}, 'medium': {'width': 1024, 'height': 768}, 'small': {'width': 512, 'height': 384}})
    title = models.CharField(max_length=50, null=True, blank=True, verbose_name="タイトル")
    is_default = models.BooleanField(default=False, verbose_name="デフォルト表示画像")

    def url(self):
        return self.image.medium.url

    def __str__(self):
        return self.title if self.title else "Image(No." + str(self.pk) + " uploaded by " + self.staff.name + ")"


class Post(models.Model):
    uuid = models.UUIDField(default=uuid4, unique=True, db_index=True, editable=False, verbose_name="UUID")
    slug = models.SlugField(max_length=50, db_index=True, unique=True, null=True, blank=True, verbose_name="Page URL")
    title = models.CharField(max_length=50, verbose_name="タイトル")
    text = models.TextField(verbose_name="本文")
    last_staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, verbose_name="最終更新者")
    article_writers = models.ManyToManyField(Staff, related_name="wrote_%(class)s", blank=True, verbose_name="執筆者")
    article_editors = models.ManyToManyField(Staff, related_name="edited_%(class)s", blank=True, verbose_name="編集者")
    category = models.ForeignKey(Category, related_name="%(class)s", null=True, on_delete=models.SET_NULL ,verbose_name="カテゴリー")
    tags = models.ManyToManyField(Tag, related_name="%(class)s", blank=True, verbose_name="タグ")
    lecture = models.ForeignKey("Lecture", related_name="%(class)s", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="授業")
    eyecatch = models.ForeignKey(Image, related_name="used_%(class)s", null=True, on_delete=models.SET_NULL, verbose_name="アイキャッチ画像")
    created_at = models.DateTimeField(default=timezone.localtime, verbose_name="作成日")
    publish_at = models.DateTimeField(default=timezone.localtime, null=True, blank=True, verbose_name="公開日")
    sns_publish_text = models.TextField(default="", null=True, blank=True, verbose_name="SNS告知文")
    is_public = models.BooleanField(default=False, verbose_name="INIAD関係者以外の閲覧を許可する")

    class Meta:
        abstract = True

    def __str__(self):
        if not self.title:
            return super(Post, self).__str__()
        return self.title

    def type(self):
        return "Post"

    def get_url(self, page, keys):
        for key in keys:
            if key == "slug" and self.slug:
                return resolve_url(page, self.publish_at.year, self.publish_at.month, self.slug)
            if key == "uuid":
                return resolve_url(page, self.uuid)
            if key == "id":
                return resolve_url(page, self.id)
        if self.type() == "Article":
            if self.slug:
                return resolve_url(page, self.publish_at.year, self.publish_at.month, self.slug)
            else:
                return resolve_url(page, self.id)
        return resolve_url(page, self.uuid)


class Lecture(models.Model):
    course = models.CharField(max_length=12, choices=courses, default="none", verbose_name="コース")
    name = models.CharField(max_length=40, default="none", verbose_name="名前")
    school_year = models.IntegerField(verbose_name="学年")


writer_check_choice = [
    (0, "未確認"),
    (1, "承認"),
    (-1, "拒否")
]


class PreArticleWriterRelation(models.Model):
    staff = models.ForeignKey(Staff, related_name="wrote_prearticle_relations", on_delete=models.CASCADE)
    prearticle = models.ForeignKey("PreArticle", related_name="writer_relations", on_delete=models.CASCADE)
    writer_check = models.IntegerField(choices=writer_check_choice, default=0, verbose_name="筆者確認済み")


class RevisionMessage(models.Model):
    uuid = models.UUIDField(default=uuid4, unique=True, db_index=True, editable=False, verbose_name="UUID")
    staff = models.ForeignKey(Staff, related_name="revision_messages", on_delete=models.CASCADE, verbose_name="スタッフ")
    created_at = models.DateTimeField(default=timezone.localtime, verbose_name="作成日")
    comment = models.TextField(verbose_name="コメント")


class Article(Post):
    updated_at = models.DateTimeField(default=timezone.localtime, verbose_name="更新日")
    is_publishable = models.BooleanField(default=False, verbose_name="公開準備済")
    is_published = models.BooleanField(default=False, verbose_name="公開済み")

    def type(self):
        return "Article"

    def time(self):
        return max(self.created_at, self.updated_at, self.publish_at)

    def is_new(self):
        return self.time() > timezone.localtime() - timedelta(weeks=1)


class PreArticle(Post):
    slug = models.SlugField(max_length=50, db_index=True, unique=False, null=True, blank=True, verbose_name="Page URL")
    parent = models.ForeignKey("self", related_name="children", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="親記事")
    article = models.ForeignKey(Article, related_name="parents", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="完成記事")
    article_writers = models.ManyToManyField(Staff, related_name="wrote_%(class)s", blank=True, through=PreArticleWriterRelation, verbose_name="執筆者")
    is_draft = models.BooleanField(default=True, verbose_name="下書きか")
    is_revision = models.BooleanField(default=False, verbose_name="校閲か")
    is_revision_checked = models.BooleanField(default=False, verbose_name="校閲チェック完了")
    is_revision_rejected = models.BooleanField(default=False, verbose_name="校閲リジェクト")
    is_final = models.BooleanField(default=False, verbose_name="公開直前版か")
    revision_messages = models.ManyToManyField(RevisionMessage, related_name="pre_articles", blank=True, verbose_name="メッセージ")
    revise_count = models.IntegerField(default=0, verbose_name="校閲完了数")

    def type(self):
        return "PreArticle"

    def time(self):
        return self.created_at

    def is_writer_check_completed(self):
        for writer_relation in self.writer_relations.all():
            if writer_relation.writer_check <= 0:
                return False
        return True

    def get_diff_for_parent(self):
        return get_diff(self.parent.text, self.text)

    def get_parents_id_list(self, include_self=False):
        list = []
        if include_self:
            list.append(self.id)
        p = self.parent
        while p:
            list.append(p.id)
            p = p.parent
        return list

    def is_slug_unique(self, slug):
        parents_id = self.get_parents_id_list(True)
        if PreArticle.objects.exclude(id__in=parents_id).filter(slug=slug, children=None):
            return False
        if Article.objects.filter(slug=slug):
            return False
        return True

    def get_revision_messages(self):
        return self.revision_messages.order_by("-created_at")

    def publish(self):
        writers = self.article_writers.all()
        editors = self.article_editors.all()
        old_article_published = False
        if self.article:
            old_article_published = self.article.is_published
        article = Article(
            id=self.article_id,
            slug=self.slug,
            title=self.title,
            text=self.text,
            last_staff=self.last_staff,
            category=self.category,
            eyecatch=self.eyecatch,
            publish_at=self.publish_at,
            updated_at=timezone.localtime(),
            sns_publish_text=self.sns_publish_text,
            is_public=self.is_public,
            is_publishable=True,
            is_published=old_article_published
        )
        article.save()
        for writer in writers:
            article.article_writers.add(writer)
        for editor in editors:
            article.article_editors.add(editor)
        self.article = article
        self.is_final = True
        self.save()
        publish.publish(article)
        return article

    @classmethod
    def is_slug_unique_in_class(cls, slug):
        if cls.objects.filter(slug=slug, children=None):
            return False
        if Article.objects.filter(slug=slug):
            return False
        return True


class BrowsingHistory(models.Model):
    article = models.ForeignKey(Article, related_name="browsed_histories", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="閲覧履歴")
    user = models.ForeignKey(User, related_name="browsed_histories", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="ユーザー")
    ip = models.GenericIPAddressField(null=True, verbose_name="IPアドレス")
    user_agent = models.CharField(max_length=512, null=True, verbose_name="UserAgent")
    referer = models.TextField(null=True, blank=True, verbose_name="リファラ")
    time = models.DateTimeField(default=timezone.localtime, verbose_name="時刻")
