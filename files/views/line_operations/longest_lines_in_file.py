import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework_xml.renderers import XMLRenderer
from rest_framework.renderers import BaseRenderer
from ...models import UploadedFile

# Custom Renderer for Plain Text
class PlainTextRenderer(BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'

    def render(self, data, media_type=None, renderer_context=None):
        return '\n'.join(data).encode('utf-8')

class LongestLinesInFileView(APIView):
    renderer_classes = [PlainTextRenderer, JSONRenderer, XMLRenderer]

    def get(self, request, *args, **kwargs):
        file_name = kwargs.get('file_name', '').strip()
        if not file_name.endswith('.txt'):
            file_name += '.txt'

        try:
            uploaded_file = UploadedFile.objects.get(file__icontains=file_name)
            file_path = uploaded_file.file.path

            if not os.path.isfile(file_path):
                return Response({"error": "File does not exist."}, status=status.HTTP_404_NOT_FOUND)

            with open(file_path, 'r') as f:
                lines = f.readlines()

            # Get the 20 longest lines
            longest_lines = sorted(lines, key=len, reverse=True)[:20]
            longest_lines = [line.strip() for line in longest_lines]  # Remove newline characters

            accept_header = request.headers.get('Accept', '')

            # Handle response format based on the Accept header
            if 'application/json' in accept_header:
                response_data = {'longest_lines': longest_lines}
                return Response(response_data, status=status.HTTP_200_OK)
            elif 'application/xml' in accept_header:
                response_data = {'longest_lines': longest_lines}
                return Response(response_data, content_type='application/xml', status=status.HTTP_200_OK)
            else:  # Default to text/plain
                return Response(longest_lines, content_type='text/plain', status=status.HTTP_200_OK)

        except UploadedFile.DoesNotExist:
            return Response({"error": "File not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)