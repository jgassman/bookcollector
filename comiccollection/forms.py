from django import forms

from .models import ComicBook, Illustrator, Publisher, Series, Writer


class ComicBookForm(forms.ModelForm):
    class Meta:
        model = ComicBook
        fields = '__all__'


class IllustratorForm(forms.ModelForm):
    class Meta:
        model = Illustrator
        fields = '__all__'


class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = '__all__'


class SeriesForm(forms.ModelForm):
    class Meta:
        model = Series
        fields = '__all__'


class WriterForm(forms.ModelForm):
    class Meta:
        model = Writer
        fields = '__all__'


class SearchForm(forms.Form):
    search_text = forms.CharField(label='Search', max_length=50)
