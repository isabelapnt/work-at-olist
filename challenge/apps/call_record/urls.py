from django.conf.urls import url, include
from rest_framework.routers import SimpleRouter
router = SimpleRouter()

urlpatterns = [
    url(r'^', include(router.urls))
]
