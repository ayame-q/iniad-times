from django import forms
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.template.defaultfilters import safe
from datetime import timedelta
from .models import User, Article, Staff
from django_boost.forms.mixins import FormUserKwargsMixin
from allauth.socialaccount.models import SocialAccount


class ImageSelect(forms.RadioSelect):
    template_name = "times/widgets/image_choice.html"
    option_template_name = "times/widgets/image_choice_option.html"


class BaseForm(forms.ModelForm):
    def __init__(self, label_suffix="", *args, **kwargs):
        kwargs["label_suffix"] = label_suffix
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label


class AdminArticleForm(FormUserKwargsMixin, BaseForm):
    class Meta:
        model = Article
        fields = ("title", "text", "eyecatch", "article_writers", "article_editors", "category", "published_at", "is_posted", "is_public")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text"].widget.attrs["class"] = "text-input"
        self.fields["is_posted"].label = "公開"
        self.fields["is_public"].label = "学外者の閲覧を許可する"


class StaffProfileForm(FormUserKwargsMixin, BaseForm):
    class Meta:
        model = Staff
        fields = ("name", "comment")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["comment"].widget.attrs["class"] = "text-input"
