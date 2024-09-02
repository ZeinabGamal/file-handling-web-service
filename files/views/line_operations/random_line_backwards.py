import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_xml.renderers import XMLRenderer
from rest_framework.renderers import JSONRenderer, BaseRenderer
from ...models import UploadedFile

class PlainTextRenderer(BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'

    def render(self, data, media_type=None, renderer_context=None):
        return data.encode('utf-8')

class RandomLineBackwardsView(APIView):
    renderer_classes = [PlainTextRenderer, JSONRenderer, XMLRenderer]

    def get(self, request, *args, **kwargs):
        file_name = kwargs.get('file_name')
        
        # Ensure file name ends with .txt
        if not file_name.endswith('.txt'):
            file_name += '.txt'

        try:
            # Retrieve the file by its name
            uploaded_file = UploadedFile.objects.get(file__icontains=file_name)
            with open(uploaded_file.file.path, 'r') as f:
                lines = f.readlines()

            if not lines:
                return Response({"error": "The file is empty."}, status=status.HTTP_404_NOT_FOUND)

            # Filter out empty lines
            non_empty_lines = [line for line in lines if line.strip()]

            if not non_empty_lines:
                return Response({"error": "The file contains only empty lines."}, status=status.HTTP_404_NOT_FOUND)

            original_line = random.choice(non_empty_lines).strip()
            reversed_line = original_line[::-1]
            
            # Find the line number (1-based index)
            line_number = next((i + 1 for i, line in enumerate(non_empty_lines) if line.strip() == original_line), None)
            if line_number is None:
                return Response({"error": "The selected line was not found."}, status=status.HTTP_404_NOT_FOUND)

            # Find the most frequent letter ignoring spaces
            filtered_line = original_line.replace(' ', '')
            most_frequent_letter = max(set(filtered_line), key=filtered_line.count, default='')

            response_data = {
                'line': reversed_line,
                'line_number': line_number,
                'file_name': uploaded_file.file.name,
                'most_frequent_letter': most_frequent_letter
            }

            accept_header = request.headers.get('Accept', '')
            if 'application/json' in accept_header:
                return Response(response_data, status=status.HTTP_200_OK)
            elif 'application/xml' in accept_header:
                return Response(response_data, content_type='application/xml', status=status.HTTP_200_OK)
            else:  # Default to text/plain
                return Response(reversed_line, content_type='text/plain', status=status.HTTP_200_OK)

        except UploadedFile.DoesNotExist:
            return Response({"error": "File not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
