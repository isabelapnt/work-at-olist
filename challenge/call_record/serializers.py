from rest_framework import serializers

from .models import (
    CallRecord,
    TelephoneBill
)


class StartRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = CallRecord
        fields = (
            'id',
            'call_id',
            'source',
            'destination',
            'record_type',
            'record_timestamp'
        )
        read_only_fields = ('id', 'call_id')

    def create(self, validated_data):
        return CallRecord.objects.create(**validated_data)


class EndRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = CallRecord
        fields = (
            'id',
            'call_id',
            'record_type',
            'record_timestamp'
        )
        read_only_fields = ('id', )

    def validate_call_id(self, call_id):
        start_record = CallRecord.objects.filter(call_id=call_id, record_type=CallRecord.RECORD_TYPE.start)
        if not start_record or start_record.count() > 1:
            raise serializers.ValidationError({'call_id': 'invalid'})
        return call_id


class TelephoneBillSerializer(serializers.ModelSerializer):

    class Meta:
        model = TelephoneBill
        fields = (
            'id',
            'call_record',
            'duration',
            'price'
        )
        read_only_fields = ('id', )
