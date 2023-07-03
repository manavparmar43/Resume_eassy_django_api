from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(DocumentType)
admin.site.register(DocumentField)
admin.site.register(DocumentContent)

admin.site.register(Document)
admin.site.register(DocumentChoiceFied)
admin.site.register(Content)
admin.site.register(SubContent)

