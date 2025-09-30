from rest_framework import serializers
from answers.models import Answer


class AnswerSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(
        format="%Y-%m-%d",
        read_only=True,
    )
    text = serializers.CharField(required=True)
    question_id = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=True,
    )
    user_id = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=True,
    )

    class Meta:
        model = Answer
        fields = [
            "id",
            "question_id",
            "user_id",
            "text",
            "created_at",
        ]




