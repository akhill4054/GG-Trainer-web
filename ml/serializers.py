from rest_framework import serializers

# Gesture serializer
class GestureSerializer(serializers.Serializer):
    data = serializers.CharField()
    mapped_text = serializers.CharField()
    rd = serializers.IntegerField(default=0)

class TranslateRequestSerializer(serializers.Serializer):
    data = serializers.CharField()

class ResetSerializer(serializers.Serializer):
    pass_key = serializers.CharField()

class RemoveSyncedGestureSerializer(serializers.Serializer):
    mapped_text = serializers.CharField()