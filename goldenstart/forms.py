from django import forms
from goldenstart.models import User, Document, Tracking

class EmailLoginForm(forms.Form):
    email = forms.EmailField()
    access_code = forms.CharField()
    
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('document', )