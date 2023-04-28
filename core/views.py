from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from .models import Movie, MovieImage

def upload_images(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    ImageFormSet = inlineformset_factory(Movie, MovieImage, fields=('movie_img',), extra=5, can_delete=True)

    if request.method == 'POST':
        formset = ImageFormSet(request.POST, request.FILES, instance=movie)
        if formset.is_valid():
            formset.save()
            return redirect('movie_detail', movie_id=movie_id)
    else:
        formset = ImageFormSet(instance=movie)

    return render(request, 'upload_images.html', {'formset': formset})
