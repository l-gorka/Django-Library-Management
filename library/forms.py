from django import forms
from .models import Author, Book, Genre

class BookForm(forms.ModelForm):
    authors_str = forms.CharField(label='Authors', widget=forms.Textarea, required=True)
    genres_str = forms.CharField(label='Genres', widget=forms.Textarea, required=True)

    class Meta:
        model = Book
        exclude = ['authors', 'genre']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get("instance")
        if instance:
            self.fields['authors_str'].initial = ", ".join(x.name for x in instance.authors.all())
            self.fields['genres_str'].initial = ", ".join(x.genre_name for x in instance.genre.all())

    
    def save(self, commit=True, *args, **kwargs):
        instance = super().save(commit=False, *args, **kwargs)
        authors_str = self.cleaned_data.get('authors_str')
        genres_str = self.cleaned_data.get('genres_str')
        if commit:
            authors_qs = Author.objects.comma_to_qs(authors_str)
            genres_qs = Genre.objects.comma_to_qs(genres_str)
            if not instance.id:
                '''
                This is a new instance.
                '''
                instance.save()
            instance.authors.clear()
            instance.genre.clear()
            instance.authors.add(*authors_qs)
            instance.genre.add(*genres_qs)
            instance.save()
        return instance