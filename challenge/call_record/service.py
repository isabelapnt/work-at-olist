from datetime import datetime
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from decimal import Decimal



def parse_time(s):
    ''' Parse 12-hours format '''
    return datetime.strptime(s, '%I:%M %p').time()


def get_duration_in_time(start_record, end_record):
    start_time = start_record.record_timestamp
    end_record = end_record.record_timestamp
    interval = abs((start_time - end_record))
    interval_time = (datetime.min + interval).time()
    return interval_time.strftime('%Hh%Mm%Ss')


def get_duration_in_minutes(start_record, end_record):
    start = start_record.record_timestamp
    end = end_record.record_timestamp
    interval = start - end

    duration = abs(interval.total_seconds())
    minutes = divmod(duration, 60)[0]
    return int(minutes)


def get_call_price(start_record, end_record):
    start_time = parse_time('6:00 AM')
    end_time = parse_time('10:00 PM')
    start_record_timestamp = start_record.record_timestamp.time()

    fixed_charge = Decimal(0.36)
    price = Decimal(0.0)

    has_rate = start_record_timestamp >= start_time and start_record_timestamp <= end_time
    if has_rate:
        rate = Decimal(0.09)
        duration = get_duration_in_minutes(start_record, end_record)
        price = duration * rate

    return fixed_charge + price


def get_period_date(period):
    now = timezone.now()
    if not period:
        date = now + relativedelta(months=-1)
    elif period > 0 and period <= 12:
        date = timezone.datetime(now.year, period, now.day)
    else:
        date = timezone.datetime(period, now.month, now.day)

    return date


def get_start_end_records_in_period(source, period):
    from .models import CallRecord

    date = get_period_date(period)

    start_records = CallRecord.objects.filter(source=source, record_timestamp__lte=date)
    start_call_ids = start_records.values_list('call_id', flat=True)

    end_records = CallRecord.objects.filter(
        call_id__in=list(start_call_ids),
        record_type=CallRecord.RECORD_TYPE.end
    )

    end_call_ids = end_records.values_list('call_id', flat=True)
    valid_call_ids = list(set(start_call_ids).intersection(end_call_ids))

    start = start_records.filter(call_id__in=valid_call_ids)
    end = end_records.filter(call_id__in=valid_call_ids)

    return start, end


def search_bill(source, period):
    from .models import TelephoneBill

    date = get_period_date(period)
    bill = TelephoneBill.objects.filter(source=source, start_date__lte=date)

    if bill:
        return True, bill
    return False, None
