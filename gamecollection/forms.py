from django import forms

from gamecollection.models import Game, Series, Developer, System


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = '__all__'


class SeriesForm(forms.ModelForm):
    class Meta:
        model = Series
        fields = '__all__'


class DeveloperForm(forms.ModelForm):
    class Meta:
        model = Developer
        fields = '__all__'


class SystemForm(forms.ModelForm):
    class Meta:
        model = System
        fields = '__all__'


class SearchForm(forms.Form):
    search_text = forms.CharField(label='Search', max_length=50)
