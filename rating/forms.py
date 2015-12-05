from django import forms

from .models import Rating, CHOICES_VOTING


class RatingForm(forms.ModelForm):
    rate = forms.ChoiceField(choices=CHOICES_VOTING, widget=forms.RadioSelect(attrs={'class': 'star'}))

    class Meta:
        model = Rating
        fields = ('rate',)

    #def save(self, usuario=None):
    #    self.instance.state = 1
    #    super(RatingForm,self).save()
