from django.db import models
from contact.models import *
from account.models import *
from document.models import *
import uuid

# Create your models here.

## Particular User contacts which is used for analysing the document
class Contact(DateTimeMixin):
    user_key = models.ForeignKey(
        User, related_name="user", null=True, blank=True, on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=240)
    email = models.EmailField(null=True, blank=True)
    company = models.TextField(null=True, blank=True)
    role = models.CharField(max_length=276, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.name)


## As contact user having the different comapny name
class Company(
    DateTimeMixin,
):
    name = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self) -> str:
        return self.name


## Use for the sharing of documents
class DocumentShare(DateTimeMixin):
    contact_user = models.ForeignKey(
        Contact,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="contact",
    )
    document = models.ForeignKey(
        Document,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="document",
    )
    rating = models.FloatField(null=True, blank=True, verbose_name="rating")
    url = models.UUIDField(
        default=uuid.uuid4,
        auto_created=True,
        blank=True,
        null=True,
        unique=True,
        editable=False,
        verbose_name="unique_url",
    )
    disabled = models.BooleanField(default=False)
    is_rated = models.BooleanField(default=False, verbose_name="Is Rated")

    def __str__(self) -> str:
        return str(self.contact_user.name)




class ContetRating(DateTimeMixin):
    document_share = models.ForeignKey(DocumentShare, on_delete=models.CASCADE,blank=True,null=True,verbose_name="Shared Doc", related_name="content_rating")
    content = models.ForeignKey(Content, on_delete=models.CASCADE,blank=True,null=True,verbose_name="Content")
    rating = models.FloatField(null=True, blank=True, verbose_name="Rating")

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return str(self.content.content_field.section)
    

class SubContentRating(DateTimeMixin):
    sub_content = models.ForeignKey(SubContent, on_delete=models.CASCADE,blank=True,null=True,verbose_name="Sub Content")
    content_rating = models.ForeignKey(ContetRating, on_delete=models.CASCADE, blank=True, null=True,verbose_name="Content Rating",related_name="subcontent_rating")
    rating = models.FloatField(null=True, blank=True, verbose_name="Rating")

    class Meta:
        ordering = ['created_at']
