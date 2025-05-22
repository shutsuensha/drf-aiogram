from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="telegram_user_id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                required=True,
                description="Telegram User ID (обязательный)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        telegram_user_id = self.request.query_params.get("telegram_user_id")
        if not telegram_user_id:
            raise ValidationError({"telegram_user_id": "This query parameter is required."})

        queryset = self.queryset.filter(telegram_user_id=telegram_user_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        status_value = request.data.get("status", "done")
        if status_value not in ["done", "undone"]:
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        instance.status = status_value
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
