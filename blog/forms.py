# forms.py
from django import forms
from .models import Post, Comment,Tag
from .models import CommentReport

from .models import Post, PostImage, PostDocument, PostVideo

class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea)
    
    class Meta:
        model = Post
        fields = ['title', 'content','tags']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'tags': forms.CheckboxSelectMultiple()
        }

    def save(self, commit=True):
        post = super().save(commit=commit)
        if commit and self.files:
            # Handle images
            for image in self.files.getlist('images'):
                PostImage.objects.create(post=post, image=image)
            
            # Handle documents
            for document in self.files.getlist('documents'):
                PostDocument.objects.create(post=post, document=document)
            
            # Handle videos
            for video in self.files.getlist('videos'):
                PostVideo.objects.create(post=post, video=video)
        return post


class CommentForm(forms.ModelForm):
    body = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control custom-txt',
            'cols': '40',
            'rows': '3',
            'placeholder': 'Write your comment here...'
        }),
        label=''
    )
    
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control-file',
            'accept': 'image/*'
        })
    )
    
    video = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control-file',
            'accept': 'video/*'
        })
    )
    
    voice = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control-file',
            'accept': 'audio/*'
        })
    )

    class Meta:
        model = Comment
        fields = ['body', 'image', 'video', 'voice']

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        video = cleaned_data.get('video')
        voice = cleaned_data.get('voice')
        
        # Check file sizes
        if image and image.size > 5 * 1024 * 1024:  # 5MB limit
            raise forms.ValidationError("Image file is too large ( > 5MB )")
        
        if video and video.size > 50 * 1024 * 1024:  # 50MB limit
            raise forms.ValidationError("Video file is too large ( > 50MB )")
            
        if voice and voice.size > 10 * 1024 * 1024:  # 10MB limit
            raise forms.ValidationError("Audio file is too large ( > 10MB )")

        return cleaned_data
    
from django import forms

class CommentForm(forms.ModelForm):
    body = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control custom-txt',
            'cols': '40',
            'rows': '3',
            'placeholder': 'Write your comment here...'
        }),
        label=''
    )
    
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control-file',
            'accept': 'image/*'
        })
    )
    
    video = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control-file',
            'accept': 'video/*'
        })
    )
    
    voice = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control-file',
            'accept': 'audio/*'
        })
    )

    class Meta:
        model = Comment
        fields = ['body', 'image', 'video', 'voice']

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        video = cleaned_data.get('video')
        voice = cleaned_data.get('voice')
        
        if image and image.size > 5 * 1024 * 1024:  # 5MB limit
            raise forms.ValidationError("Image file is too large ( > 5MB )")
        
        if video and video.size > 50 * 1024 * 1024:  # 50MB limit
            raise forms.ValidationError("Video file is too large ( > 50MB )")
            
        if voice and voice.size > 10 * 1024 * 1024:  # 10MB limit
            raise forms.ValidationError("Audio file is too large ( > 10MB )")

        return cleaned_data

class CommentReportForm(forms.ModelForm):
    class Meta:
        model = CommentReport
        fields = ['reason', 'details']
        widgets = {
            'details': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'})}