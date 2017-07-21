from django import forms

from .models import Author, Book, Series


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'


class SeriesForm(forms.ModelForm):
    class Meta:
        model = Series
        fields = '__all__'


class SearchForm(forms.Form):
    search_text = forms.CharField(label='Search', max_length=50)
