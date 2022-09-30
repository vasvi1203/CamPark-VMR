from django import forms
from .models import VideoUpload, QueryUpload

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = VideoUpload
        fields = ["videoFile"]
        labels = {
            'videoFile': ('<strong><i class="fas fa-video"></i> Video</strong>')
        }

class QueryUploadForm(forms.ModelForm):
    class Meta:
        model = QueryUpload
        fields = ["query"]
        labels = {
            'query': ('<strong><i class="fas fa-user-edit"></i> Enter your query</strong>')
        }