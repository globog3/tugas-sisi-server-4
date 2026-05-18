from rest_framework import generics
from rest_framework.response import Response
from django.core.cache import cache

from .models import Course
from .serializers import CourseSerializer
from .mongo_models import ActivityLog


class CourseListAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get(self, request, *args, **kwargs):
        cache_key = "course_list"

        cached_data = cache.get(cache_key)

        if cached_data:
            print("DATA FROM REDIS CACHE")
            return Response(cached_data)

        queryset = Course.objects.all()
        serializer = CourseSerializer(queryset, many=True)

        cache.set(cache_key, serializer.data, timeout=60)

        ActivityLog(
            action="GET_COURSE_LIST",
            endpoint="/api/courses/"
        ).save()

        print("DATA FROM DATABASE")

        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save()

        cache.delete("course_list")

        ActivityLog(
            action="CREATE_COURSE",
            endpoint="/api/courses/"
        ).save()


class CourseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_object(self):
        course_id = self.kwargs["pk"]

        cache_key = f"course_detail_{course_id}"

        cached_course = cache.get(cache_key)

        if cached_course:
            print("DETAIL FROM REDIS CACHE")
            return Course.objects.get(pk=course_id)

        course = Course.objects.get(pk=course_id)

        cache.set(cache_key, {
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "instructor": course.instructor,
            "price": str(course.price)
        }, timeout=60)

        ActivityLog(
            action="GET_COURSE_DETAIL",
            endpoint=f"/api/courses/{course_id}/"
        ).save()

        print("DETAIL FROM DATABASE")

        return course

    def perform_update(self, serializer):
        course = serializer.save()

        cache.delete("course_list")
        cache.delete(f"course_detail_{course.id}")

        ActivityLog(
            action="UPDATE_COURSE",
            endpoint=f"/api/courses/{course.id}/"
        ).save()

    def perform_destroy(self, instance):
        course_id = instance.id

        instance.delete()

        cache.delete("course_list")
        cache.delete(f"course_detail_{course_id}")

        ActivityLog(
            action="DELETE_COURSE",
            endpoint=f"/api/courses/{course_id}/"
        ).save()