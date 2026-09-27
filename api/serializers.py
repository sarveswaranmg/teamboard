from rest_framework import serializers

from .models import KBEntry


class KBEntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = KBEntry

        fields = [
            "id",
            "question",
            "answer",
            "category",
        ]