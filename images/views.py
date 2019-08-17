from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ImageCreateForm
from django.contrib.auth.decorators import login_required
from .models import Image
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse
from common.decorators import ajax_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            new_image.user = request.user  # user in the current session.
            new_image.save()
            messages.success(request, 'Image added successfully.')
            return redirect(new_image.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)

    return render(request,
                    'images/image/create.html',
                    {'form':form,
                    'section':'images'})

@login_required
def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request,
            'images/image/detail.html',
            {'image':image,
            "section":'images'})

@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')  # id of image will be submitted through ajax post
    action = request.POST.get('action')  # action to be performed
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)   
                # add the current user in the session to image users_like list.
            else:
                image.users_like.remove(request.user)
                # remove current user from the people that like's the image.
            return JsonResponse({'status':'ok'})
        except:
            pass
        return JsonResponse({'status':'amatuer'})

@login_required
def image_list(request):
    object_list = Image.objects.all()  # get all images
    paginator = Paginator(object_list, 8)  # 8 images per page
    page = request.GET.get('page')  # get the page number requested

    try:
        images = paginator.page(page)  # retrieve images of the requested page
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        images = paginator.page(1)
    # through ajax request
    if request.is_ajax():
        return render(request,
                    'images/image/list_ajax.html',
                    {'images':images,
                    'section':'images'})
    # normal http request
    return render(request,
                    'images/image/list.html',
                    {'images':images,
                    'section':'images'})


