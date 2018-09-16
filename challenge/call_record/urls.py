from django.conf.urls import url, include
from rest_framework.routers import SimpleRouter
from .api import (
    StartRecordViewSet,
    EndRecordViewSet,
    TelephoneBillViewSet
)

router = SimpleRouter()
router.register(r'start', StartRecordViewSet)
router.register(r'end', EndRecordViewSet)
router.register(r'billing', TelephoneBillViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
