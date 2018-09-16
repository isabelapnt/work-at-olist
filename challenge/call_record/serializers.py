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
        validated_data['call_id'] = CallRecord.objects.count()
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
        records = CallRecord.objects.filter(call_id=call_id)
        if not records or records.count() > 1:
            raise serializers.ValidationError('invalid')
        return call_id

    def validate_record_type(self, record_type):
        if record_type != CallRecord.RECORD_TYPE.end:
            raise serializers.ValidationError('invalid')
        return record_type


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
