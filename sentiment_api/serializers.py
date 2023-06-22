from sentiment_api.models import Positive,Negative,Neutral
from rest_framework import serializers
#from myapp.serializers import ArticleSerializer

class PositiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Positive
        fields = '__all__'



class NegativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Negative
        fields = '__all__'

class NeutralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Neutral
        fields = '__all__'

        
