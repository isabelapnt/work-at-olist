from django.db import models
from model_utils import Choices


class CallRecord(models.Model):
    class Meta:
        verbose_name = 'Call Record'
        verbose_name_plural = 'Call Records'

    RECORD_TYPE = Choices(
        ('start', 'start', 'Call Start Record'),
        ('end', 'end', 'Call Start Record'),
    )

    record_type = models.CharField('Type', max_length=28, choices=RECORD_TYPE, default=RECORD_TYPE.start)
    record_timestamp = models.DateTimeField('Record Timestamp', auto_now_add=True)


class StartRecord(CallRecord):
    class Meta:
        verbose_name = 'Call Start Record'
        verbose_name_plural = 'Call Start Records'

    source = models.CharField(max_length=9, null=True, blank=True)
    destination = models.CharField(max_length=9, null=True, blank=True)


class EndRecord(CallRecord):
    class Meta:
        verbose_name = 'Call End Record'
        verbose_name_plural = 'Call End Records'

    start_record = models.OneToOneField('StartRecord', on_delete=models.CASCADE)
