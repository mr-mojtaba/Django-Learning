from django import forms
from .models import Comment, Post


class TicketForm(forms.Form):
    SUBJECT_CHOICES = (
        ('پیشنهاد', 'پیشنهاد'),
        ('انتقاد', 'انتقاد'),
        ('گزارش', 'گزارش'),
    )

    message = forms.CharField(widget=forms.Textarea, required=True)
    name = forms.CharField(max_length=250, required=True)
    email = forms.EmailField()
    phone = forms.CharField(max_length=11, required=True)
    subject = forms.CharField()

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            if not phone.isnumeric():
                raise forms.ValidationError("شماره تلفن عددی نیست!")
            else:
                return phone


class CommentForm(forms.ModelForm):
    def clean_name(self):
        name = self.cleaned_data['name']
        if name:
            if len(name) < 3:
                raise forms.ValidationError("نام کوتاه است!")
            else:
                return name

    class Meta:
        model = Comment
        fields = [
            'name',
            'body',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'نام و نام خانوادگی',
                'class': 'cm-name',
            }),
            'body': forms.TextInput(attrs={
                'placeholder': 'متن',
                'class': 'cm-body',
            }),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'description',
            'slug',
            'reading_time',
        ]

        widgets = {
            'author': forms.HiddenInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        censored_words = ['فحش', 'خراب', 'بدکاره']
        description = cleaned_data.get('description')
        if description:
            for word in censored_words:
                description = description.replace(word, "'سانسور'")
            cleaned_data['description'] = description
        return cleaned_data
