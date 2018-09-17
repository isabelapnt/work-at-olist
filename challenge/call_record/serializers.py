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

    def validate_source(self, source):
        if not source.isdigit():
            raise serializers.ValidationError('invalid')
        return source

    def validate_destination(self, destination):
        if not destination.isdigit():
            raise serializers.ValidationError('invalid')
        return destination

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


class GetTelephoneBillSerializer(serializers.Serializer):

    subscriber_telephone = serializers.CharField(max_length=11)
    period = serializers.IntegerField(required=False)

    def validate_subscriber_telephone(self, subscriber_telephone):
        if not subscriber_telephone.isdigit():
            raise serializers.ValidationError('invalid')

        has_source = CallRecord.objects.filter(source=subscriber_telephone).exists()
        if not has_source:
            raise serializers.ValidationError('not_found')

        return subscriber_telephone


class TelephoneBillSerializer(serializers.ModelSerializer):

    class Meta:
        model = TelephoneBill
        fields = (
            'id',
            'destination',
            'start_date',
            'start_time',
            'duration',
            'price'
        )
        read_only_fields = ('id', )
