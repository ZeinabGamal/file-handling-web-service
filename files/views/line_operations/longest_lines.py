import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer, BaseRenderer
from rest_framework_xml.renderers import XMLRenderer
from ...models import UploadedFile

class PlainTextRenderer(BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'

    def render(self, data, media_type=None, renderer_context=None):
        if isinstance(data, str):
            return data.encode('utf-8')
        raise TypeError("PlainTextRenderer only supports strings.")

class LongestLinesView(APIView):
    renderer_classes = [PlainTextRenderer, JSONRenderer, XMLRenderer]

    def get(self, request, *args, **kwargs):
        lines = []
        for uploaded_file in UploadedFile.objects.all():
            file_path = uploaded_file.file.path

            if not os.path.exists(file_path):
                # Log a warning or error here if needed
                continue  # Skip files that do not exist

            try:
                with open(file_path, 'r') as f:
                    lines.extend(f.readlines())
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not lines:
            return Response({"error": "No lines found in any files."}, status=status.HTTP_404_NOT_FOUND)

        longest_lines = sorted(lines, key=len, reverse=True)[:100]

        accept_header = request.headers.get('Accept', '')

        if 'application/json' in accept_header:
            return Response({'lines': longest_lines}, status=status.HTTP_200_OK)
        elif 'application/xml' in accept_header:
            xml_data = {'lines': longest_lines}
            return Response(xml_data, content_type='application/xml', status=status.HTTP_200_OK)
        else:  # Default to text/plain
            lines_str = ''.join(longest_lines)
            return Response(lines_str, content_type='text/plain', status=status.HTTP_200_OK)
