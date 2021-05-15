from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

# Create your models here.

courses = [
    ("none", "なし"),
    ("engineering", "エンジニアリングコース"),
    ("design", "デザインコース"),
    ("business", "ビジネスコース"),
    ("civil-system", "シビルシステムコース"),
]


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), related_name="profile", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="ユーザー")
    email = models.EmailField(verbose_name="メールアドレス", unique=True, db_index=True)
    family_name = models.CharField(max_length=20, default="", null=True, blank=True, verbose_name="姓")
    given_name = models.CharField(max_length=20, default="", null=True, blank=True, verbose_name="名")
    family_name_ruby = models.CharField(max_length=20, default="", null=True, blank=True, verbose_name="姓フリガナ")
    given_name_ruby = models.CharField(max_length=20, default="", null=True, blank=True, verbose_name="名フリガナ")
    comment = models.TextField(null=True, blank=True, verbose_name="自己紹介")
    course = models.CharField(max_length=12, choices=courses, default="none", verbose_name="コース")
    interested_in = models.JSONField(null=True, blank=True, verbose_name="興味")
    questionnaire = models.JSONField(null=True, blank=True, verbose_name="アンケート")
    created_at = models.DateTimeField(default=timezone.localtime, verbose_name="登録日")

    def get_full_name(self):
        return self.family_name + " " + self.given_name

    def get_full_name_ruby(self):
        return self.family_name_ruby + " " + self.given_name_ruby

    def save(self, *args, **kwargs):
        if self.email:
            print("Add Staff:", self.email)
            User = get_user_model()
            try:
                user = User.objects.get(email=self.email)
                self.user = user
            except User.DoesNotExist:
                pass
        return super(Profile, self).save(*args, **kwargs)


class News(models.Model):
    title = models.CharField(max_length=30, verbose_name="タイトル")
    date = models.DateField(default=timezone.localdate, verbose_name="日付")
    created_at = models.DateTimeField(default=timezone.localtime, verbose_name="登録日")

    class Meta:
        ordering = ["-date"]