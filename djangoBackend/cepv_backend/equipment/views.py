from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import FileResponse
from django.utils import timezone

import pandas as pd

from .models import Dataset
from .serializers import DatasetSerializer, SignUpSerializer
from reports.pdf import generate_dataset_pdf


class uploadCSVAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        file = request.FILES.get('file')
        name = request.data.get("name")

        if not file or not name :
            return Response(
                {"error":"CSV file and name is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            df = pd.read_csv(file)
        except Exception:
            return Response(
                {"error":"INVALID CSV FILE"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        required_columns = {
            "Equipment Name",
            "Type",
            "Flowrate",
            "Pressure",
            "Temperature",
        }

        if not required_columns.issubset(df.columns):
            return Response(
                {"error":"CSV Structure is invalid"},
                status = status.HTTP_400_BAD_REQUEST
            )


        summary = {

            "total_equipment":len(df),
            "average_flowrate":df["Flowrate"].mean(),
            "average_pressure":df["Pressure"].mean(),
            "average_temperature":df["Temperature"].mean(),
            "type_distribution":df["Type"].value_counts().to_dict(),
        }

        preview_rows = df.head(10).to_dict(orient="records")
        chart_data = {
                "flowrate": df["Flowrate"].tolist(),
                "pressure": df["Pressure"].tolist(),
                "temperature": df["Temperature"].tolist(),
        }
        dataset = Dataset.objects.create(
            name=name,
            filename=file.name,
            summary=summary,
            preview=preview_rows,
            charts=chart_data,
            uploaded_at=timezone.now()
            
        )

        return Response({
            "dataset_id":dataset.id,
            "filename":dataset.filename,
             "dataset_name": dataset.name,
            "summary":summary,
            "preview":preview_rows,
            "charts": chart_data,
        },status=status.HTTP_201_CREATED)
    
class DatasetHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        datasets = Dataset.objects.order_by('-uploaded_at')[:5]
        serializer = DatasetSerializer(datasets,many=True)
        return Response(serializer.data)

class DatasetPDFReportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,dataset_id):
        print(f"DEBUG: DatasetPDFReportAPIView called for ID: {dataset_id}")
        try:
            dataset = Dataset.objects.get(id=dataset_id)
        except Dataset.DoesNotExist:
            print(f"DEBUG: Dataset {dataset_id} not found")
            return Response(
                {"error":"Dataset does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        pdf_buffer = generate_dataset_pdf(dataset)

        return FileResponse(
            pdf_buffer,
            as_attachment=True,
            filename=f"dataset_report_{dataset_id}.pdf"    
        )

class SignupAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User created successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DatasetAnalyzeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, dataset_id):
        print(f"DEBUG: DatasetAnalyzeAPIView called for ID: {dataset_id}")
        try:
            dataset = Dataset.objects.get(id=dataset_id)
        except Dataset.DoesNotExist:
            print(f"DEBUG: Dataset {dataset_id} not found in Analyze view")
            return Response(
                {"error": "Dataset not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response({
            "dataset_id": dataset.id,
            "filename": dataset.filename,
            "dataset_name": dataset.name,
            "summary": dataset.summary,
            "preview": dataset.preview,
            "charts": dataset.charts,
        })
