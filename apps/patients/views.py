from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Patient
from .serializers import PatientSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

class PatientListView(generics.ListAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def get_queryset(self):
        return super().get_queryset().order_by('full_name')

class PatientDetailView(View):
    def get(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk)
        serializer = PatientSerializer(patient)
        return Response(serializer.data)

class CreatePatientView(generics.CreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class UpdatePatientView(generics.UpdateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class DeletePatientView(generics.DestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer