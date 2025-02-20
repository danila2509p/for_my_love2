import base64
from io import BytesIO
from PIL import Image
from django.shortcuts import render, redirect
import datetime
from .models import ImageModel
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile


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


def encode_image_to_base64(image_field):
    img = Image.open(image_field)
    if img.mode in ('RGBA', 'LA'):
        img = img.convert('RGB')
    buffer = BytesIO()
    img.save(buffer, format="JPEG")
    encoded_image = base64.b64encode(buffer.getvalue())  # Возвращаем байты, а не строку
    return encoded_image


from django.core.files.base import ContentFile


def decode_base64_to_image(encoded_image):
    # Декодируем base64 строку
    decoded_image = base64.b64decode(encoded_image)

    # Создаем объект ContentFile
    image_file = ContentFile(decoded_image, name='image.jpg')

    return image_file
def image(request):
    auth = request.session.get('user', False)

    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
            # Кодируем изображение в base64 (возвращает байты)
            encoded_image = encode_image_to_base64(image)
            # Сохраняем в базу данных
            new_image = ImageModel(image=encoded_image)
            new_image.save()

    # Извлекаем все изображения из базы данных
    code_image = ImageModel.objects.all()
    all_images = [bytes(img.image).decode('utf-8') for img in code_image]

    context = {
        'auth': auth,
        'all_images': all_images,
    }
    return render(request, 'image.html', context)