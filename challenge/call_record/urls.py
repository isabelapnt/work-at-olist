from django.conf.urls import url, include
from rest_framework.routers import SimpleRouter
from .api import (
    StartRecordViewSet,
    EndRecordViewSet,
    TelephoneBillViewSet
)

router = SimpleRouter()
router.register(r'billing', TelephoneBillViewSet, base_name='billing')
router.register(r'start', StartRecordViewSet)
router.register(r'end', EndRecordViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
