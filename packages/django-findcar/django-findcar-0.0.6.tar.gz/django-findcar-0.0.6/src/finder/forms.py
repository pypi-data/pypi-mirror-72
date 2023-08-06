from django import forms
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
4

class ImageUploadForm(forms.Form):
    fname = forms.CharField(max_length=100, label='Name')
    lname = forms.CharField(max_length=100, label='Name')
    email = forms.EmailField(required=False, label='Email address')
    image = forms.ImageField()


def upload(request):
    submitted = False
    if request.method == 'POST':
        form = ImageUploadForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # assert False
            return HttpResponseRedirect('/upload?submitted=True')
    else:
        form = ImageUploadForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'upload.html', {'form': form, 'submitted': submitted})
