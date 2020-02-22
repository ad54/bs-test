from django.shortcuts import render, redirect
from core.forms import ImageUploadForm, ImageSearchForm
from core.models import Image
from unsplash.api import Api
from unsplash.auth import Auth
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# Create your views here.

client_id = "QLazdAGWwfE9bnIPE-IoWdlo3O994IKGXSEMdtrUAnM"
client_secret = "5GfLe8hbONXXglK0egK8fmevJ579lRQJNK5ecBl406E"
redirect_uri = "urn:ietf:wg:oauth:2.0:oob"
code = "3039_1SG9AAlzAKxJftf6sIo2h3t4RrKufrXEO4RHv4"

def upload_img(request):
    """To upload image form local machine"""
    if request.method == 'GET':
        form = ImageUploadForm()
        context = {'form':form}
        return render(request, 'core/img_upload.html', context=context)
    elif request.method == 'POST':
        form = ImageUploadForm(request.POST or None,request.FILES or None)
        if form.is_valid():
            form.save()
            return redirect('list_images')
        context = {'form': form}
        return render(request, 'core/img_upload.html', context=context)


def list_images(request):
    """List all the images with pagination"""
    images = Image.objects.all()
    paginator = Paginator(images, 3)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)
    context = {'images': paginated_queryset,'page_request_var':page_request_var}
    return render(request,'core/list_img.html', context=context)
    pass


def search_images(request):
    """search images with tag from local machine"""
    if request.method == 'GET':
        form = ImageSearchForm()
        return render(request,'core/search_img.html',{'form':form} )
    if request.method == 'POST':
        tag = request.POST['tags']
        images = Image.objects.filter(tags=tag)
        context = {'images': images}
        return render(request, 'core/list_img.html', context=context)


def search_images_unsplash(request):
    """Search image from unsplash"""
    if request.method == 'GET':
        form = ImageSearchForm()
        return render(request,'core/search_img.html',{'form':form} )
    if request.method == 'POST':
        tag = request.POST['tags']
        auth = Auth(client_id, client_secret, redirect_uri, code=code)
        api = Api(auth)
        images = api.search.photos(tag)
        results = images.get('results')

        paginator = Paginator(results, 3)
        page_request_var = 'page'
        page = request.GET.get(page_request_var)
        try:
            paginated_queryset = paginator.page(page)
        except PageNotAnInteger:
            paginated_queryset = paginator.page(1)
        except EmptyPage:
            paginated_queryset = paginator.page(paginator.num_pages)

        context = {'images': paginated_queryset,'page_request_var':page_request_var}
        return render(request, 'core/list_img_unsplash.html', context=context)
