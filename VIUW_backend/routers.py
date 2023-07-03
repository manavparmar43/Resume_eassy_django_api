from django.urls import path
from rest_framework.routers import DefaultRouter
from document.views import *
from contact.views import *

router = DefaultRouter()
router.register("document-type", DocumentTypeViewSet, basename="document-type")
router.register("document-field", DocumentFieldViewSet, basename="document-field")
# router.register("document-content", DocumentContentViewSet, basename="document-content")
router.register("document", DocumentViewSet, basename="document")
router.register("document-field-choice", DocumentFieldChoiceViewset, basename="document-field-choice")
router.register('document-preview', DocumentShareViewset, basename='document-preview')
router.register("contact", ContactViewset, basename="contact")
