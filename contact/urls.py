# from rest_framework.routers import DefaultRouter
# from django.urls import path
# from .views import DocumentShareViewset


# router = DefaultRouter()
# router.register('document', DocumentShareViewset, basename='document')

# urlpatterns = router.urls


from django.urls import path
from .views import *

urlpatterns = [
    # Need to pass shred document id in this url
    path("documents-rating/<str:id>/", DocumentRatingView.as_view(), name="documents-rating"),
    
]

