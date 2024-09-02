from django.urls import path
from .views.file_management.file_upload import FileUploadView
from .views.line_operations.random_line import RandomLineView
from .views.line_operations.random_line_backwards import RandomLineBackwardsView
from .views.line_operations.longest_lines import LongestLinesView
from .views.line_operations.longest_lines_in_file import LongestLinesInFileView

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('random-line/<str:file_name>/', RandomLineView.as_view(), name='random-line'),
    path('random-line-backwards/<str:file_name>/', RandomLineBackwardsView.as_view(), name='random-line-backwards'),
    path('100-longest-lines/', LongestLinesView.as_view(), name='longest-lines'),
    path('20-longest-lines-in-file/<str:file_name>/', LongestLinesInFileView.as_view(), name='longest-lines-in-file'),
]
