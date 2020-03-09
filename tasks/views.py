from django.http import HttpResponseBadRequest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from tasks.models import Task
from tasks.serializers import TaskCreateSerializer, TaskDetailsSerializer
from django.utils import timezone


class Schedule(APIView):
    def post(self, request):
        serializer = TaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            callback = serializer.validated_data['callback']
            scheduled = serializer.validated_data['scheduled']
            task = Task.objects.create(callback=callback, scheduled=scheduled)
            task.schedule()
            serializer = TaskDetailsSerializer(task)
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        else:
            return HttpResponseBadRequest()


class Details(APIView):
    def get(self, request, code):
        if Task.objects.filter(code=code).exists():
            task = Task.objects.get(code=code)
            serializer = TaskDetailsSerializer(task)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        else:
            return HttpResponseBadRequest()


class ResetDetails(APIView):
    def get(self, request):
        missed_tasks = Task.objects.filter(scheduled__lt=timezone.now()).exclude(state=Task.EXECUTED)
        serializer = TaskDetailsSerializer(missed_tasks, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class Reset(APIView):
    def get(self, request):
        missed_tasks = Task.objects.filter(scheduled__lt=timezone.now()).exclude(state=Task.EXECUTED)
        for missed_task in missed_tasks:
            missed_task.force_run()
        return Response(status=status.HTTP_200_OK)
