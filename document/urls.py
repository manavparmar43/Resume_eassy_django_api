# from django.urls import path, include
# from .views import (
#     BookViewSet,
#     DocumentViewSet,
#     EssayViewSet,
#     BlogViewSet,
#     ProposalViewSet,
# )
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register("book", BookViewSet, basename="book")
# router.register("document", DocumentViewSet, basename="document")
# router.register("essay", EssayViewSet, basename="essay")
# router.register("blog", BlogViewSet, basename="blog")
# router.register("proposal", ProposalViewSet, basename="proposal")

# urlpatterns = router.urls


from django.urls import path
from .views import *

urlpatterns = [
    path("documents/", DocumentView.as_view(), name="documents"),
    path("my-doc-review/<str:id>/", MyDocumentReview.as_view(), name="my-doc-review")
    
]