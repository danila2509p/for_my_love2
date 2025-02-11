from django.shortcuts import render, redirect
import datetime
from .forms import ImageUploadForm
from .models import ImageModel


def main(request):
    auth = request.session.get('user', False)
    now = datetime.datetime.now()
    now += datetime.timedelta(hours=3)
    delta = datetime.datetime(2024, 6, 30)
    r = (now - delta).days
    context = {
        'now': r,
        'auth': auth,
    }
    return render(request, 'main.html', context)

def login(request):
    auth = True
    if request.method == 'POST':
        username = request.POST.get('user')
        password = request.POST.get('pass')
        if username == 'kira' and password == '3006':
            request.session['user'] = True
            auth = True
            return redirect('/')
        elif username == 'danya' and password == '3006':
            request.session['user'] = True
            auth = True
            return redirect('/')
        else:
            auth = False
    context = {
        'auth': auth,
    }
    return render(request, 'login.html', context)
def logout(request):
    request.session['user'] = False
    return redirect('/')

def image(request):
    auth = request.session.get('user', False)

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = ImageUploadForm()
    all_images = ImageModel.objects.all()
    context = {
        'auth': auth,
        'form': form,
        'all_images': all_images,
    }
    return render(request, 'image.html', context)