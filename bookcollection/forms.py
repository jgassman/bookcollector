from django import forms

from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

    def clean(self):
        if self.cleaned_data.get('subgenre').genre != self.cleaned_data.get('genre'):
            raise forms.ValidationError("Genre for subgenre must match book genre")
        return self.cleaned_data


class SearchForm(forms.Form):
    search_text = forms.CharField(label='Search', max_length=50)
