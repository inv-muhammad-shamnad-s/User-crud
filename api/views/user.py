from ..models.user_model import User
from ..serializers.user_serializers import (
    UserListSerializer,
    UserManagementSerializer,
    UserCreateSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from ..messages.error_messages import USER_ERROR_MESSAGES
from ..messages.success_messages import USER_SUCCESS_MESSAGES


class UserCreateView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(
            {"message": USER_SUCCESS_MESSAGES["user_created"]},
            status=status.HTTP_201_CREATED,
        )


class UserListView(APIView):

    def get(self, request):
        user = User.objects.all()
        serializer = UserListSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserView(APIView):

    def get(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            raise NotFound({f"{pk}": USER_ERROR_MESSAGES["user_not_found"]})

        serializer = UserListSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            raise NotFound({f"{pk}": USER_ERROR_MESSAGES["user_not_found"]})

        serializer = UserManagementSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": USER_SUCCESS_MESSAGES["user_updated"]},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            raise NotFound({f"{pk}": USER_ERROR_MESSAGES["user_not_found"]})

        try:
            user.delete()
            return Response(
                {"message": USER_SUCCESS_MESSAGES["user_deleted"]},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception:
            return Response(
                {"error": USER_ERROR_MESSAGES["user_deleted"]},
                status=status.HTTP_400_BAD_REQUEST,
            )
