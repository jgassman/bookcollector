from django import forms

from gamecollection.models import Game, Series, Studio, System


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = '__all__'


class SeriesForm(forms.ModelForm):
    class Meta:
        model = Series
        fields = '__all__'


class StudioForm(forms.ModelForm):
    class Meta:
        model = Studio
        fields = '__all__'


class SystemForm(forms.ModelForm):
    class Meta:
        model = System
        fields = '__all__'


class SearchForm(forms.Form):
    search_text = forms.CharField(label='Search', max_length=50)
