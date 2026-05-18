from rest_framework import generics
from .models import Course
from .serializers import CourseSerializer
from .mongo_models import ActivityLog


class CourseListAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get(self, request, *args, **kwargs):

        ActivityLog(
            action="GET Courses",
            endpoint="/api/courses/"
        ).save()

        return super().get(request, *args, **kwargs)


class CourseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer