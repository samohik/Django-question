from rest_framework import serializers
from answers.models import Answer


class AnswerSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(
        format="%Y-%m-%d",
        read_only=True,
    )
    text = serializers.CharField(required=True)

    class Meta:
        model = Answer
        fields = [
            "question_id",
            "user_id",
            "text",
            "created_at",
        ]


