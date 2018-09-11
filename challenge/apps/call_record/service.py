from datetime import datetime
from decimal import Decimal


def parse_time(s):
    ''' Parse 12-hours format '''
    return datetime.strptime(s, '%I:%M %p').time()


def get_duration_in_minutes(self):
    start = self.start_record.record_timestamp
    end = self.start_record.end_record.record_timestamp
    interval = start - end

    duration = interval.total_seconds()
    minutes = divmod(duration, 60)[0]
    return int(minutes)


def get_call_price(self):
    start_time = parse_time('6:00 AM')
    end_time = parse_time('10:00 PM')
    start_record_timestamp = self.start_record.record_timestamp.time()

    fixed_charge = Decimal(0.36)
    price = Decimal(0.0)

    has_rate = start_record_timestamp >= start_time and start_record_timestamp <= end_time
    if has_rate:
        rate = Decimal(0.09)
        duration = get_duration_in_minutes(self)
        price = duration * rate

    return fixed_charge + price
