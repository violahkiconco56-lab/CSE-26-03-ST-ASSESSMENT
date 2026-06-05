from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Video
from .forms import VideoForm


def index(request):
    return render(request, 'index.html')


def video_list(request):
    videos = Video.objects.all().order_by('-id')

    return render(
        request,
        'video_list.html',
        {'videos': videos}
    )


def upload_video(request):

    if request.method == 'POST':

        form = VideoForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            form.save()

            return redirect('video_list')

    else:
        form = VideoForm()

    return render(
        request,
        'upload_video.html',
        {'form': form}
    )


def video_detail(request, pk):

    video = get_object_or_404(
        Video,
        id=pk
    )

    video.views += 1
    video.save()

    return render(
        request,
        'video_detail.html',
        {'video': video}
    )
def delete_video(request, pk):

    video = get_object_or_404(
        Video,
        id=pk
    )

    video.delete()

    return redirect('video_list')

