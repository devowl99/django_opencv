from django.shortcuts import render#, redirect
from .forms import SimpleUploadForm, ImageUploadForm
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .cv_functions import cv_detect_face 

# Create your views here.
def first_view(request):
    return render(request, 'opencv_webapp/first_view.html', {})


def simple_upload(request):

    if request.method == 'POST':
        
        form = SimpleUploadForm(request.POST, request.FILES) 

        if form.is_valid():
            myfile = request.FILES['image']

            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)            
            uploaded_file_url = fs.url(filename)

            context = {'form': form, 'uploaded_file_url': uploaded_file_url}

            return render(request, 'opencv_webapp/simple_upload.html', context)

    else:
        form = SimpleUploadForm()
        context = {'form': form}
        return render(request, 'opencv_webapp/simple_upload.html', context)


# Detect face with OpenCV
def detect_face(request):

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False) 	    
            post.save() # DB record 추가 & 이미지 파일 저장 종료

            # document : ImageUploadModel Class에 선언되어 있는 “document”에 해당
            imageURL = settings.MEDIA_URL + form.instance.document.name

            # == form.instance.document.url
            # == post.document.url
            # == '/media/images/2021/10/29/ses_XQAftn4.jpg'
            # print(form.instance, form.instance.document.name, form.instance.document.url)

            cv_detect_face(settings.MEDIA_ROOT_URL + imageURL)

            return render(request, 'opencv_webapp/detect_face.html', {'form':form, 'post':post})

    else:
         form = ImageUploadForm()
         return render(request, 'opencv_webapp/detect_face.html', {'form':form})