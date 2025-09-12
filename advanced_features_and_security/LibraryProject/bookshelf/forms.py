from django import forms

class ExampleForm(forms.Form):
    title = forms.CharField(max_length=255, label="Book title")

class SearchForm(forms.Form):
    q = forms.CharField(max_length=100, required=False, label="Search")
