from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AssessmentViewSet

# Router para as ViewSets
router = DefaultRouter()
router.register(r'assessments', AssessmentViewSet)

app_name = 'assessments'

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
]
