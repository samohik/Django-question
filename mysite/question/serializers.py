from rest_framework import serializers

from answers.serializers import AnswerSerializer
from question.models import Question


class QuestionSerializer(serializers.ModelSerializer):
    text = serializers.CharField(required=True)
    created_at = serializers.DateTimeField(
        format="%Y-%m-%d",
        read_only=True,
    )
    created_by = serializers.StringRelatedField(
        many=False,
        read_only=False,
    )


    class Meta:
        model = Question
        fields = [
            "id",
            "created_by",
            "text",
            "created_at",
        ]

class QuestionDetailSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(
        format="%Y-%m-%d",
        read_only=True,
    )
    answer_questions = AnswerSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Question
        fields = [
            "id",
            "created_by",
            "text",
            "created_at",
            "answer_questions",
        ]
