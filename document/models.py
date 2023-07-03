from django.db import models
from account.models import DateTimeMixin, User
import uuid

# from ckeditor.fields import RichTextField


# Create your models here.


## Use for creating type of documents, For Instance CV, Book,etc.
class DocumentType(DateTimeMixin):
    name = models.CharField(max_length=250)
    icon = models.FileField(upload_to="icons", blank=True, null=True)

    def __str__(self):
        return self.name


## Create a fields for document, For Instance hobbies, cover-pages, etc.
class DocumentField(DateTimeMixin):
    type = models.ForeignKey(
        DocumentType, on_delete=models.SET_NULL, null=True, blank=True
    )
    section = models.CharField(max_length=250, null=True, blank=True)
    count = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.section


class DocumentChoiceFied(DateTimeMixin):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    document_field_key = models.ForeignKey(
        DocumentField, on_delete=models.SET_NULL, null=True, blank=True
    )
    selected = models.BooleanField(default=False)
   
    
    title = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.title



## Create a content according to field, For instance, hobbies = "cricket and swimming", etc.
class DocumentContent(DateTimeMixin):
    document_field = models.ForeignKey(
        DocumentChoiceFied, on_delete=models.SET_NULL, null=True, blank=True
    )
    count = models.IntegerField(null=True, blank=True, default=0)
    content = models.TextField(null=True, blank=True)
    uniquecode=models.CharField(max_length=100,null=True, blank=True)
    def __str__(self) -> str:
        return str(self.document_field)


## Particular User document like "rahul created a CV"
class Document(DateTimeMixin):
    title = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    document_key = models.ForeignKey(
        DocumentType, on_delete=models.CASCADE, blank=True, null=True
    )
    # document_fields = models.ManyToManyField(DocumentContent, blank=True)
    rating = models.FloatField(null=True, blank=True)

    def __str__(self) -> str:
        return str(self.title)


class Content(DateTimeMixin):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, blank=True, null=True, related_name="document")
    content_field = models.ForeignKey(DocumentField, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    content_count = models.IntegerField(null=True, blank=True, default=0)
    rating = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['created_at', 'pk']

    def __str__(self):
        return str(self.content_field)
    

class SubContent(DateTimeMixin):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, null=True, blank=True, related_name="doc_content")
    sub_content = models.TextField(null=True, blank=True)
    sub_content_count = models.IntegerField(null=True, blank=True, default=0)
    rating = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['created_at', 'pk']

    def __str__(self):
        return str(self.content.content_field.section)