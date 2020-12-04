from django import forms
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.template.defaultfilters import safe
from datetime import timedelta
from .models import User, Article, PreArticle, Staff
from django_boost.forms.mixins import FormUserKwargsMixin
from allauth.socialaccount.models import SocialAccount


class BaseForm(forms.ModelForm):
    def __init__(self, label_suffix="", *args, **kwargs):
        kwargs["label_suffix"] = label_suffix
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label


class PreArticleForm(BaseForm):
    class Meta:
        model = PreArticle
        fields = ("title", "slug", "text", "eyecatch", "sns_publish_text", "category", "publish_at",
                  "is_public", "parent", "is_draft")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["slug"].widget.attrs["placeholder"] = "ページのURLで \"https://iniad-wm.com/年/月/\" 以降の部分です。英数字と-が使用できます。"
        self.fields["parent"].disabled = True
        self.fields["parent"].label = ""
        self.fields["parent"].widget = forms.HiddenInput()
        self.fields["is_public"].label = "学外者の閲覧を許可する"

    def clean_sns_publish_text(self):
        data = self.cleaned_data["sns_publish_text"]
        if 115 < len(data) + len(self.cleaned_data["title"]):
            raise forms.ValidationError("長すぎます")
        return data

    def clean(self):
        data = super(PreArticleForm, self).clean()
        if not data["is_draft"] and not data["slug"]:
            raise forms.ValidationError("Page URLを指定してください")
        return data


class AdminArticleForm(BaseForm):
    class Meta:
        model = Article
        fields = ("title", "text", "eyecatch", "sns_publish_text", "article_writers", "article_editors", "category", "publish_at",
                  "is_publishable", "is_public")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text"].widget.attrs["class"] = "text-input"
        self.fields["is_publishable"].label = "公開"
        self.fields["is_public"].label = "学外者の閲覧を許可する"

    def clean_sns_publish_text(self):
        data = self.cleaned_data["sns_publish_text"]
        if 115 < len(data) + len(self.cleaned_data["title"]):
            raise forms.ValidationError("長すぎます")
        return data


class StaffProfileForm(BaseForm):
    class Meta:
        model = Staff
        fields = ("name", "comment")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["comment"].widget.attrs["class"] = "text-input"
