from rest_framework import serializers

# Gesture serializer
class GestureSerializer(serializers.Serializer):
    data = serializers.CharField()
    mapped_text = serializers.CharField()

class TranslateRequestSerializer(serializers.Serializer):
    data = serializers.CharField()

class ResetSerializer(serializers.Serializer):
    pass_key = serializers.CharField()