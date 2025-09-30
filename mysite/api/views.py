import jwt
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.template.context_processors import request
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import (
    ViewSet,
    GenericViewSet,
)

from answers.models import Answer
from answers.serializers import AnswerSerializer
from api.utils import create_jwt, decode_jwt
from question.models import Question
from question.serializers import QuestionSerializer, QuestionDetailSerializer
from users.models import Profile
from users.serializers import RegistrationSerializer, LoginSerializer, ProfileSerializer


class UserRegistrationViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request: Request, *args, **kwargs) -> Response:
        """Register new User."""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():

            user = serializer.create(serializer.validated_data)

            # Create profile for the user
            profile_serializer = ProfileSerializer(data={"username": user.username})

            if profile_serializer.is_valid():
                profile_serializer.save(user=user)
            return Response({"message": f"New User was created"}, status=status.HTTP_201_CREATED)

        else:
            return Response({"message": "Not valid data"}, status=status.HTTP_400_BAD_REQUEST)


class LoginViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        token = create_jwt(user)

        response = Response(status=status.HTTP_200_OK)
        response.set_cookie(key="jwt", value=token, httponly=True)
        response.data = {
            "message": "Login was success",
            "jwt": token,
        }

        return response


class TokenAuthenticateViewSet(ViewSet):
    permission_classes = [AllowAny, ]

    def list(self, request):
        token = request.COOKIES.get("jwt")
        try:
            data = decode_jwt(token)

            user = User.objects.get(id=data["id"])
            login(request, user)

            return Response({"message": f"User {user.username} authorize"})

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("JWT token has expired.")

        except jwt.InvalidTokenError:
            raise AuthenticationFailed(f"Invalid JWT token.Token {token}")

        except Exception as e:
            raise AuthenticationFailed(f"{e}")

    class ProfileViewSet(
        ViewSet,
    ):
        serializer_class = ProfileSerializer
        queryset = Profile.objects.all()
        lookup_field = 'username'

        def get_object(self):
            lookup_value = self.kwargs[self.lookup_field]
            return self.queryset.get(**{self.lookup_field: lookup_value})

        def list(self, request, *args, **kwargs):
            try:
                user = self.queryset.get(id=request.user.id)
            except Exception as e:
                raise AuthenticationFailed("Unauthenticated")

            return Response(
                self.serializer_class(user).data,
                status=status.HTTP_200_OK
            )

        @action(detail=False, methods=['put'])
        def update_user(self, request, *args, **kwargs):
            try:
                user = self.queryset.get(id=request.user.id)
            except Exception as e:
                raise AuthenticationFailed("Unauthenticated")

            serializer = self.serializer_class(
                user,
                data=request.data,
                partial=True,
            )
            if serializer.is_valid():
                serializer.save()

                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK
                )

            return Response(
                {"message": "Data incorrect"},
                status=status.HTTP_400_BAD_REQUEST
            )


class ProfileViewSet(
    ViewSet,
):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    lookup_field = 'username'

    def get_object(self):
        lookup_value = self.kwargs[self.lookup_field]
        return self.queryset.get(**{self.lookup_field: lookup_value})

    def list(self, request, *args, **kwargs):
        try:
            user = self.queryset.get(id=request.user.id)
        except Exception as e:
            raise AuthenticationFailed("Unauthenticated")

        return Response(
            self.serializer_class(user).data,
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['put'])
    def update_user(self, request, *args, **kwargs):
        try:
            user = self.queryset.get(id=request.user.id)
        except Exception as e:
            raise AuthenticationFailed("Unauthenticated")

        serializer = self.serializer_class(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            {"message": "Data incorrect"},
            status=status.HTTP_400_BAD_REQUEST
        )

class LogoutViewSet(ViewSet):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

    def list(self, request, *args, **kwargs):
        logout(request)
        response = Response()
        response.data = {"message": "User logout"}
        response.status_code = status.HTTP_200_OK
        response.delete_cookie(key="jwt")

        return response


class QuestionViewSet(GenericViewSet):
    queryset = Question.objects.select_related(
        "created_by",
    ).prefetch_related(
        "answer_questions",
    ).all()
    serializer_class = QuestionSerializer

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            self.queryset,
            many=True,
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def retrieve(self, request: Request, pk):
        try:
            serializer = QuestionDetailSerializer(
                self.queryset.get(id=pk),
                many=False,
            )
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        except Question.DoesNotExist:
            return Response(
                {"message": f"Question {pk} dont exist "},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(methods=["post"], detail=True,
            url_name="answers", url_path="answers")
    def answers(self, request: Request, pk):
        try:
            question = self.queryset.get(id=pk)
            serializer = AnswerSerializer(data=request.data)

            if serializer.is_valid():
                serializer.validated_data["question_id"] = question
                serializer.validated_data["user_id"] = Profile.objects.get(
                    id=self.request.user.id,
                )

                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED,
                )

        except Question.DoesNotExist:
            return  Response(
                status=status.HTTP_400_BAD_REQUEST,
            )


    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
        )
        if serializer.is_valid():
            serializer.validated_data["created_by"] = Profile.objects.get(
                id=self.request.user.id)
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
                status=status.HTTP_400_BAD_REQUEST,
            )

    def destroy(self, request: Request, pk):
        try:
            data = self.queryset.get(id=pk)
            if str(request.user) == str(data.created_by):
                data.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)

        except Question.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AnswerViewSet(GenericViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def retrieve(self, request: Request, pk):
        try:
            serializer = self.serializer_class(
            self.queryset.get(id=pk))
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        except Answer.DoesNotExist:
            return Response(
                {"message": f"Answer {pk} dont exist "},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def destroy(self, request: Request, pk):
        try:
            data = self.queryset.get(id=pk)
            if str(request.user) == str(data.user_id):
                data.delete()
                return Response(
                    status=status.HTTP_204_NO_CONTENT,
                )
            else:
                return Response(
                    status=status.HTTP_403_FORBIDDEN,
                )
        except Answer.DoesNotExist:
            return Response(
                {"message": f"Answer {pk} dont exist "},
                status=status.HTTP_400_BAD_REQUEST,
            )
