from datetime import date

from django import forms
from django.core.exceptions import ValidationError

from .models import Video


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = [
            'title',
            'description',
            'quality',
            'publish_date',
            'video_file',
            'thumbnail',
        ]
        labels = {
            'title': '',
            'description': '',
            'quality': '',
            'publish_date': '',
            'video_file': '',
            'thumbnail': '',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Video Title',
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Description (Optional)',
                'rows': 6,
            }),
            'quality': forms.Select(attrs={
                'aria-label': 'Video Quality',
            }),
            'publish_date': forms.TextInput(attrs={
                'placeholder': 'Date of Publishing',
                'onfocus': "this.type='date'",
                'onblur': "if (!this.value) this.type='text'",
                'aria-label': 'Date of Publishing',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].required = False
        self.fields['thumbnail'].required = False
        # Correct way to set a placeholder for a ChoiceField
        choices = list(self.fields['quality'].choices)
        choices[0] = ('', 'Video Quality')
        self.fields['quality'].choices = choices
        self.fields['video_file'].widget.attrs.update({
            'class': 'upload-input',
            'accept': 'video/mp4,video/avi,video/quicktime,.mp4,.avi,.mov',
        })
        self.fields['thumbnail'].widget.attrs.update({
            'class': 'upload-input',
            'accept': 'image/*',
        })

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title and not isinstance(title, str):
            raise ValidationError("Title must be a string.")
        return title

    def clean_publish_date(self):
        publish_date = self.cleaned_data.get('publish_date')
        if publish_date and publish_date > date.today():
            raise ValidationError("Publish date cannot be in the future.")
        return publish_date

    def clean_video_file(self):
        video_file = self.cleaned_data.get('video_file')
        if video_file:
            filename = video_file.name.lower()
            if not filename.endswith(('.mp4', '.avi', '.mov')):
                raise ValidationError("Upload a valid video file: .mp4, .avi, or .mov.")
        return video_file

    def clean_thumbnail(self):
        thumbnail = self.cleaned_data.get('thumbnail')
        if thumbnail:
            filename = thumbnail.name.lower()
            if not filename.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                raise ValidationError("Upload a valid thumbnail image: .jpg, .jpeg, .png, or .webp.")
        return thumbnail

    def clean(self):
        cleaned_data = super().clean()
        video_file = cleaned_data.get('video_file')
        quality = cleaned_data.get('quality')

        if video_file and quality and quality not in ['360p', '720p', '1080p']:
            raise ValidationError("Choose a valid video quality.")

        return cleaned_data
