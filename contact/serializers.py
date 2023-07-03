from rest_framework import serializers
from account.serializers import (
    UserSerializer,
    DynamicFieldsModelSerializer,
    RoleSerializer,
)
from .models import *
from document.serializers import DocumentSerializer, SubContentSerializer, ContentSerializer
from django.db.models import Avg

# from account.models import User
# from rest_framework import exceptions


# class CompanySerializer(DynamicFieldsModelSerializer):
#     class Meta:
#         model = Company
#         fields = ("id", "name")


class ContactSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Contact
        fields = (
            "id",
            "name",
            "company",
            "email",
            "role",
        )
        read_only_fields = ("id",)


class DocumentShareSaveSerializer(DynamicFieldsModelSerializer):
    contact = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(), source="contact_user"
    )

    document = serializers.PrimaryKeyRelatedField(queryset=Document.objects.all())

    class Meta:
        model = DocumentShare
        fields = (
            "id",
            "contact",
            "document",
            "rating",
            "disabled",
        )
        read_only_fields = (
            "id",
            "rating",
        )


class DocumentShareShowSerializer(DynamicFieldsModelSerializer):
    contact = ContactSerializer(
        fields=("id", "name", "company", "role"), source="contact_user"
    )

    document = serializers.PrimaryKeyRelatedField(
        queryset=Document.objects.all(), required=False
    )

    unique_url = serializers.SerializerMethodField()

    class Meta:
        model = DocumentShare
        fields = (
            "id",
            "contact",
            "document",
            "unique_url",
        )

    def get_unique_url(self, obj):
        url = settings.SITE_URL + "/api/document-preview/" + str(obj.id) + "/preview/"
        # url =  "http://127.0.0.1:8000/api/document-preview/" + str(obj.id) + "/preview/"
        return url


class SubContentRatingSerializer(DynamicFieldsModelSerializer):
    sub_content = SubContentSerializer(fields = ("sub_content",))
    class Meta:
        model = SubContentRating
        fields = ("id", "sub_content", "rating")
    

class ContentRatingSerializer(DynamicFieldsModelSerializer):
    subcontent_rating = SubContentRatingSerializer(many=True, read_only=True)
    content = ContentSerializer(fields=("content_field",))
    class Meta:
        model = ContetRating
        fields = ("id", "content", "rating", "subcontent_rating")


class DocumentRatingSerializer(DynamicFieldsModelSerializer):
    content_rating = ContentRatingSerializer(many=True, read_only=True)
    contact_user = ContactSerializer(fields=("id", "name", "company", "role"))
    document = DocumentSerializer(fields = ("id","title"))

    class Meta:
        model = DocumentShare
        fields = ("id","contact_user","document", "rating", "is_rated", "content_rating")

