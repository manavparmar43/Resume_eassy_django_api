from rest_framework import serializers
from rest_framework.validators import ValidationError
from account.serializers import DynamicFieldsModelSerializer
from django.conf import settings
from rest_framework import exceptions
from .models import *
from contact.models import DocumentShare, Contact


class DocumentTypeSerializer(DynamicFieldsModelSerializer):
    icon = serializers.SerializerMethodField()

    class Meta:
        model = DocumentType
        fields = (
            "id",
            "name",
            "icon",
        )
        read_only_fields = ("id", "icon")

    def get_icon(self, obj):
        try:
            return str(obj.icon.url)
        except:
            return None


class DocumentFieldSerializer(DynamicFieldsModelSerializer):
    type = serializers.PrimaryKeyRelatedField(
        queryset=DocumentType.objects.all(), required=False
    )

    class Meta:
        model = DocumentField
        fields = ("id", "type", "section", "count")
        read_only_fields = ("id",)


class DocumentChoiceFieldListSerializer(DynamicFieldsModelSerializer):
    type = serializers.PrimaryKeyRelatedField(
        queryset=DocumentType.objects.all(), required=False
    )
    # document_field_key=DocumentFieldSerializer(many=True,read_only=True)


    class Meta:
        model = DocumentChoiceFied
        depth=2
        fields = ("id", "type", "document_field_key", "title", "selected")
        read_only_fields = ("id",)

# class DocumentContentListSerializer(DynamicFieldsModelSerializer):


#     class Meta:
#         model = DocumentContent
#         depth = 1
#         fields = (
#             "id",
#             "document_field",
#             "content",
#             "count",
#             "uniquecode"
#         )
#         read_only_fields = ("id",)

    

class DocumentChoiceFieldSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = DocumentChoiceFied
        fields = ("id", "user","document_field_key","title","selected")
        read_only_fields = ("id",)

# class DocumentContentSerializer(DynamicFieldsModelSerializer):
#     document_field = serializers.PrimaryKeyRelatedField(
#         queryset=DocumentChoiceFied.objects.all()
#     )
#     field = serializers.SerializerMethodField(required=False)
#     class Meta:
#         model = DocumentContent
#         fields = (
#             "id",
#             "document_field",
#             "field",
#             "content",
#             "count",
#             "uniquecode"
#         )
#         read_only_fields = ("id",)

#     def get_field(self, obj):
#         try:
#             return str(obj.document_field.section)
#         except:
#             return None

class SubContentSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = SubContent
        fields = ("id", "sub_content", "sub_content_count")
        read_only_fields = ("id",)


class ContentSerializer(DynamicFieldsModelSerializer):
   
    content_field = DocumentFieldSerializer(fields=("section",))
    doc_content = SubContentSerializer(many=True, read_only=True)

    class Meta:
        model = Content
        fields = ("id","content_field", "rating", "doc_content")
        read_only_fields = ("id",)

    
    

class DocumentSerializer(DynamicFieldsModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False
    )
    document_key = serializers.PrimaryKeyRelatedField(
        queryset=DocumentType.objects.all(), required=False
    )
    document = ContentSerializer(many=True, read_only=True)
    class Meta:
        model = Document
        fields = ("id","title", "user", "document_key","rating", "document")
        read_only_fields = (
            "id",
            "user",
            "rating",
            "document_key",
        )

   

    def validate(self, attrs):
        return super().validate(attrs)


from django.db.models import Avg


class DocumentDashboardSerializer(serializers.ModelSerializer):
    document_key = DocumentTypeSerializer()
    rating = serializers.SerializerMethodField()
    my_reviews = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ("id", "title", "document_key", "rating", "my_reviews")

    def get_rating(self, obj):
        try:
            data = DocumentShare.objects.filter(document=obj.id).aggregate(
                rating=Avg("rating")
            )
            return data["rating"]
        except ZeroDivisionError:
            return 0

    def get_my_reviews(self, obj):
        try:
            rating_data = DocumentShare.objects.filter(document=obj.id).values()
            rating_user = [
                {
                    "created_at": rating["created_at"].date(),
                    "rating": rating["rating"],
                    "contact_user": Contact.objects.get(
                        id=rating["contact_user_id"]
                    ).name,
                    "company": Contact.objects.get(
                        id=rating["contact_user_id"]
                    ).company,
                    "title": Document.objects.get(id=rating["document_id"]).title,
                }
                for rating in rating_data
                if rating["rating"] is not None
            ]

            return rating_user
        except Exception as e:
            return str(e)



