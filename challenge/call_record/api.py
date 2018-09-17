from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route

from .service import get_start_end_records_in_period
from .models import (
    CallRecord,
    TelephoneBill
)
from .serializers import (
    StartRecordSerializer,
    EndRecordSerializer,
    GetTelephoneBillSerializer,
    TelephoneBillSerializer
)


class StartRecordViewSet(viewsets.ModelViewSet):
    queryset = CallRecord.objects.filter(record_type=CallRecord.RECORD_TYPE.start)
    serializer_class = StartRecordSerializer


class EndRecordViewSet(viewsets.ModelViewSet):
    queryset = CallRecord.objects.filter(record_type=CallRecord.RECORD_TYPE.end)
    serializer_class = EndRecordSerializer


class TelephoneBillViewSet(viewsets.ViewSet):

    @list_route(methods=['POST'])
    def history(self, request):
        import pdb; pdb.set_trace()
        serializer = GetTelephoneBillSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            source = serializer.data.get('subscriber_telephone')
            period = serializer.data.get('period')

            start_records, end_records = get_start_end_records_in_period(source, period)
            bill_ids = TelephoneBill.create_bill(start_records, end_records, period)
            bill = TelephoneBill.objects.filter(id__in=bill_ids)
            bill_serializer = TelephoneBillSerializer(bill, many=True)

            return Response(bill_serializer.data)

    def list(self, request):
        queryset = TelephoneBill.objects.all()
        serializer = TelephoneBillSerializer(queryset, many=True)
        return Response(serializer.data)
