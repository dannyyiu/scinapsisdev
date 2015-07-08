from django import forms
from search.models import PubTechProdResult, PubProductInfo

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def login_action(self):
        login = self.cleaned_data['username']
        passw = self.cleaned_data['password']

class SearchFilterForm(forms.Form):
    #COMPANIES=[('novus','Novus'),('abgent','Abgent')]
    #company = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=COMPANIES)

    target_human = forms.BooleanField(label="human", widget=forms.CheckboxInput(attrs={'onclick': 'this.form.submit();'}))
    target_mouse = forms.BooleanField(label="mouse", widget=forms.CheckboxInput(attrs={'onclick': 'this.form.submit();'}))
    t = forms.CharField(widget=forms.HiddenInput())
    q = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, queryset, *args, **kwargs):
        super(SearchFilterForm, self).__init__(*args, **kwargs)
        suppliers = PubTechProdResult.objects.all().values('supplier').distinct()
        com = [(s['supplier'],s['supplier']) for s in suppliers]
        self.fields['company'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={'onclick': 'this.form.submit();'}), choices=com)

        #hosts = PubProductInfo.objects.all().values('host').annotate().order_by('host')
        hosts = PubTechProdResult.objects.all().values('prod__host').distinct()
        ho = [(h['prod__host'],h['prod__host']) for h in hosts]
        self.fields['host'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={'onclick': 'this.form.submit();'}), choices=ho)

