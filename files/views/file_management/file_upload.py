from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from ...models import UploadedFile
from ...serializers import UploadedFileSerializer

class FileUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        if file_obj:
            if not file_obj.name.endswith('.txt'):
                return Response({"error": "Only .txt files are allowed."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if a file with the same name already exists
            if UploadedFile.objects.filter(file__icontains=file_obj.name).exists():
                return Response({"error": "A file with this name already exists. Please rename your file and try again."},
                                status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UploadedFileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
