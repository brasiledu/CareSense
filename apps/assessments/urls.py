from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AssessmentViewSet, meem_test_view, clock_drawing_test_view

# Router para as ViewSets
router = DefaultRouter()
router.register(r'assessments', AssessmentViewSet)

app_name = 'assessments'

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    
    # Views de testes
    path('<int:assessment_id>/meem/', meem_test_view, name='meem_test'),
    path('<int:assessment_id>/clock-drawing/', clock_drawing_test_view, name='clock_drawing_test'),
]
