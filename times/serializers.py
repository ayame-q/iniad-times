from rest_framework import serializers
from .models import Image, RevisionMessage, PreArticle, Staff


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'title', 'image')


class RevisionMessageSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(write_only=True)
    staff = serializers.SlugRelatedField(read_only=True, slug_field='name')
    class Meta:
        model = RevisionMessage
        fields = ('comment', "uuid", "staff", "created_at")
        extra_kwargs = {'created_at': {'read_only': True}}

    def create(self, validated_data):
        pre_article = PreArticle.objects.get(uuid=validated_data["uuid"])
        validated_data.pop("uuid")
        result = super(RevisionMessageSerializer, self).create(validated_data)
        result.pre_articles.add(pre_article)
        return result