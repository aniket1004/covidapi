from rest_framework import serializers

class CovidCountryDetails(serializers.ModelSerializer):

    country = serializers.CharField()
    continent = serializers.CharField()
    class Meta:
        fields = ['country','continent']