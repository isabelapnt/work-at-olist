from django.contrib import admin
from .models import (
    CallRecord,
    TelephoneBill
)


class StartRecord(CallRecord):
    class Meta:
        proxy = True


class StartRecordAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'call_id',
        'source',
        'destination',
        'record_type',
        'record_timestamp'
    )
    fields = ('source', 'destination', 'record_type', 'record_timestamp')

    def get_queryset(self, request):
        return CallRecord.objects.filter(record_type=CallRecord.RECORD_TYPE.start)


class EndRecord(CallRecord):
    class Meta:
        proxy = True


class EndRecordAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'call_id',
        'record_type',
        'record_timestamp'
    )
    fields = ('call_id', 'record_type', 'record_timestamp')

    def get_queryset(self, request):
        return CallRecord.objects.filter(record_type=CallRecord.RECORD_TYPE.end)


class TelephoneBillAdmin(admin.ModelAdmin):

    list_display = ('id', 'call_record', 'duration', 'price')
    fields = ('call_record', 'duration', 'price')


admin.site.register(StartRecord, StartRecordAdmin)
admin.site.register(EndRecord, EndRecordAdmin)
admin.site.register(TelephoneBill, TelephoneBillAdmin)
