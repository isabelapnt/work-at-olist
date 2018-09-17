from django.db import models
from model_utils import Choices
from decimal import Decimal

from .service import get_call_price, get_duration_in_time


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
    source = models.CharField(max_length=11, null=True, blank=True)
    destination = models.CharField(max_length=11, null=True, blank=True)
    call_id = models.IntegerField()


class TelephoneBill(models.Model):
    class Meta:
        verbose_name = 'Telephone Bill'
        verbose_name_plural = 'Telephone Bills'

    destination = models.CharField(max_length=11)
    start_date = models.CharField(max_length=10)
    start_time = models.CharField(max_length=10)
    duration = models.CharField(max_length=10)
    price = models.DecimalField('Call Price', max_digits=8, decimal_places=2, default=Decimal())

    @classmethod
    def create_bill(cls, start_records, end_records, period):
        bill = []
        data = {}
        for start, end in zip(start_records, end_records):
            price = get_call_price(start, end)

            data['destination'] = start.destination
            data['start_date'] = start.record_timestamp.date().strftime('%Y-%m-%d')
            data['start_time'] = start.record_timestamp.time().strftime('%Hh%Mm%Ss')
            data['duration'] = get_duration_in_time(start, end)
            data['price'] = price

            instanse = cls.objects.create(**data)
            bill.append(instanse.id)

        return bill
