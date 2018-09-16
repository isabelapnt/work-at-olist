from rest_framework import viewsets

from .models import (
    CallRecord,
    TelephoneBill
)
from .serializers import (
    StartRecordSerializer,
    EndRecordSerializer,
    TelephoneBillSerializer
)


class StartRecordViewSet(viewsets.ModelViewSet):
    queryset = CallRecord.objects.filter(record_type=CallRecord.RECORD_TYPE.start)
    serializer_class = StartRecordSerializer


class EndRecordViewSet(viewsets.ModelViewSet):
    queryset = CallRecord.objects.filter(record_type=CallRecord.RECORD_TYPE.end)
    serializer_class = EndRecordSerializer


class TelephoneBillViewSet(viewsets.ModelViewSet):
    queryset = TelephoneBill.objects.all()
    serializer_class = TelephoneBillSerializer
