from django.db import models
from model_utils import Choices
from decimal import Decimal

# from .service import create_charge


class CallRecord(models.Model):
    class Meta:
        verbose_name = 'Call Record'
        verbose_name_plural = 'Call Records'

    RECORD_TYPE = Choices(
        ('start', 'start', 'Start Record'),
        ('end', 'end', 'End Record'),
    )

    record_type = models.CharField('Type', max_length=28, choices=RECORD_TYPE, default=RECORD_TYPE.start)
    record_timestamp = models.DateTimeField('Record Timestamp')
    source = models.CharField(max_length=9, null=True, blank=True)
    destination = models.CharField(max_length=9, null=True, blank=True)
    call_id = models.IntegerField()

    # def save(self, **kwargs):
    #     if self.call_id:
    #         start_record = CallRecord.objects.filter(call_id=self.call_id, record_type=CallRecord.RECORD_TYPE.start)
    #         if start_record and start_record.count() > 1:
    #             self.call_id = start_record.first().id
    #     super(CallRecord, self).save()


class TelephoneBill(models.Model):
    class Meta:
        verbose_name = 'Telephone Bill'
        verbose_name_plural = 'Telephone Bills'

    call_record = models.ForeignKey('CallRecord', null=True, on_delete=models.SET_NULL)
    duration = models.TimeField('Call Duration', null=True)
    price = models.DecimalField('Call Price', max_digits=8, decimal_places=2, default=Decimal())

    @property
    def call_price(self):
        return get_call_price(self)
