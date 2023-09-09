from rest_framework import serializers
from myconf.conf import get_model
from myconf import conf

class FinanceSerializer(serializers.ModelSerializer):
    class Meta:
        model=get_model(conf.FINANCE)
        fields="__all__"

class Student_PaySerializer(serializers.ModelSerializer):
    class Meta:
        model=get_model(conf.STUDENT_PAY)
        fields="__all__"

class DaySerializer(serializers.Serializer):
    name = serializers.CharField(source='date__day')
    kirim = serializers.IntegerField(source='amount', required=False)
    chiqim = serializers.IntegerField(source='amount', required=False)

class MonthSerializer(serializers.Serializer):
    name = serializers.SerializerMethodField()
    kirim = serializers.SerializerMethodField()
    chiqim = serializers.SerializerMethodField()
    days = DaySerializer(many=True, read_only=True)

    def get_name(self, obj):
        return obj['date'].strftime("%B").lower()

    def get_kirim(self, obj):
        kirim_total = sum(day['kirim'] for day in obj['days'])
        return kirim_total

    def get_chiqim(self, obj):
        chiqim_total = sum(day['chiqim'] for day in obj['days'])
        return chiqim_total

class YearSerializer(serializers.Serializer):
    # name = serializers.CharField(source='date__year')
    name = serializers.CharField(source='date.year')
    kirim = serializers.SerializerMethodField()
    chiqim = serializers.SerializerMethodField()
    months = MonthSerializer(many=True, read_only=True)

    def get_kirim(self, obj):
        kirim_total = sum(month['kirim'] for month in obj['months'])
        return kirim_total

    def get_chiqim(self, obj):
        chiqim_total = sum(month['chiqim'] for month in obj['months'])
        return chiqim_total
