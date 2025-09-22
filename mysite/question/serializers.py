from rest_framework import serializers
from question.models import Question


class QuestionSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(read_only=True)
    text = serializers.CharField(required=True)
    created_at = serializers.DateTimeField(
        format="%Y-%m-%d",
        read_only=True,
    )

    class Meta:
        model = Question
        fields = [
            "created_by",
            "text",
            "created_at",
        ]
