from rest_framework.test import APITransactionTestCase
from datetime import datetime
from unittest.mock import patch

from ..service import(
    search_bill,
    get_start_end_records_in_period,
    get_period_date,
    get_call_price,
    get_duration_in_minutes,
    get_duration_in_time,
    parse_time
)
from ..models import CallRecord, TelephoneBill
 

class ServiceMethodsTest(APITransactionTestCase):

    def setUp(self):
        print("oioii")
        self.start_record = CallRecord.objects.create(
            record_type=CallRecord.RECORD_TYPE.start,
            record_timestamp=datetime(2017, 12, 12, 12, 0),
            source='99988526423',
            destination='9993468278',
        )

        self.end_record = CallRecord.objects.create(
            record_type=CallRecord.RECORD_TYPE.end,
            record_timestamp=datetime(2017, 12, 12, 14, 0),
            call_id=0
        )

    @patch('django.utils.timezone.now', return_value=datetime(2017, 12, 12))
    def get_period_date_test(self, now_mock):
        date_1 = get_period_date(12)
        date_2 = get_period_date(2018)
        date_3 = get_period_date()

        self.assertEqual(date_1, datetime(2017, 12, 12))
        self.assertEqual(date_2, datetime(2018, 12, 12))
        self.assertEqual(date_3, datetime(2017, 12, 12))
