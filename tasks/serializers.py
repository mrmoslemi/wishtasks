from rest_framework import serializers

from tasks.models import Task


class TaskCreateSerializer(serializers.Serializer):
    callback = serializers.URLField(required=True)
    scheduled = serializers.DateTimeField(required=True)


class TaskDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['code', 'callback', 'state', 'scheduled', 'execution', 'creation']
