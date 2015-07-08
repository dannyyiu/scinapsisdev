from django import forms
from django.core.mail import send_mail

class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        subject = self.cleaned_data['subject']
        message = self.cleaned_data['message']
        sender = self.cleaned_data['email']
        #cc_myself = form.cleaned_data['cc_myself']

        recipients = ['info@scinapsis.com']

        send_mail(subject, message, sender, recipients)