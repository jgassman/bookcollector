import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from comiccollection.forms import ComicBookForm, IllustratorForm, PublisherForm, SearchForm, SeriesForm, WriterForm
from .models import ComicBook, Genre, Illustrator, Publisher, Series, Writer


@login_required
def index(request):
    context = {
        'comic_count': ComicBook.objects.count(),
        'writer_count': Writer.objects.count(),
        'illustrator_count': Illustrator.objects.count(),
        'series_count': Series.objects.count(),
        'publisher_count': Publisher.objects.count(),
        'genreData': json.dumps({g.name: ComicBook.objects.filter(genre=g).count() for g in Genre.objects.all()}),
        'publisherData': json.dumps({p.name: ComicBook.objects.filter(publisher=p).count() for p in Publisher.objects.all()}),
    }
    return render(request, 'comiccollection/index.html', context=context)


@login_required
def comics(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_text = form.cleaned_data['search_text']
            comics = ComicBook.objects.filter(title__icontains=search_text)
    else:
        comics = ComicBook.objects.order_by('title')
    paginator = Paginator(comics, 25)
    page = request.GET.get('page')
    search_form = SearchForm()
    try:
        all_comics = paginator.page(page)
    except PageNotAnInteger:
        all_comics = paginator.page(1)
    except EmptyPage:
        all_comics = paginator.page(paginator.num_pages)
    return render(request, 'comiccollection/comics.html', {'all_comics': all_comics, 'search_form': search_form})


@login_required
def series(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_text = form.cleaned_data['search_text']
            series = Series.objects.filter(name__icontains=search_text)
    else:
        series = Series.objects.order_by('name')
    paginator = Paginator(series, 25)
    page = request.GET.get('page')
    search_form = SearchForm()
    try:
        all_series = paginator.page(page)
    except PageNotAnInteger:
        all_series = paginator.page(1)
    except EmptyPage:
        all_series = paginator.page(paginator.num_pages)
    return render(request, 'comiccollection/series.html', {'all_series': all_series, 'search_form': search_form})


@login_required
def series(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_text = form.cleaned_data['search_text']
            series = Series.objects.filter(name__icontains=search_text)
    else:
        series = Series.objects.order_by('name')
    paginator = Paginator(series, 25)
    page = request.GET.get('page')
    search_form = SearchForm()
    try:
        all_series = paginator.page(page)
    except PageNotAnInteger:
        all_series = paginator.page(1)
    except EmptyPage:
        all_series = paginator.page(paginator.num_pages)
    return render(request, 'comiccollection/series.html', {'all_series': all_series, 'search_form': search_form})


@login_required
def illustrators(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_text = form.cleaned_data['search_text']
            illustrators = Illustrator.objects.filter(Q(first_name__icontains=search_text) |
                                                      Q(last_name__icontains=search_text))
            illustrators = []
    else:
        illustrators = Illustrator.objects.all()
    print(illustrators)
    paginator = Paginator(illustrators, 25)
    page = request.GET.get('page')
    search_form = SearchForm()
    try:
        all_illustrators = paginator.page(page)
    except PageNotAnInteger:
        all_illustrators = paginator.page(1)
    except EmptyPage:
        all_illustrators = paginator.page(paginator.num_pages)
    return render(request, 'comiccollection/illustrators.html',
                  {'all_illustrators': all_illustrators, 'search_form': search_form})


@login_required
def publishers(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_text = form.cleaned_data['search_text']
            publishers = Publisher.objects.filter(name__icontains=search_text)
    else:
        publishers = Publisher.objects.order_by('name')
    paginator = Paginator(publishers, 25)
    page = request.GET.get('page')
    search_form = SearchForm()
    try:
        all_publishers = paginator.page(page)
    except PageNotAnInteger:
        all_publishers = paginator.page(1)
    except EmptyPage:
        all_publishers = paginator.page(paginator.num_pages)
    return render(request, 'comiccollection/publishers.html',
                  {'all_publishers': all_publishers, 'search_form': search_form})


@login_required
def writers(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_text = form.cleaned_data['search_text']
            writers = Writer.objects.filter(Q(first_name__icontains=search_text) | Q(last_name__icontains=search_text))
    else:
        writers = Writer.objects.order_by('last_name')
    paginator = Paginator(writers, 25)
    page = request.GET.get('page')
    search_form = SearchForm()
    try:
        all_writers = paginator.page(page)
    except PageNotAnInteger:
        all_writers = paginator.page(1)
    except EmptyPage:
        all_writers = paginator.page(paginator.num_pages)
    return render(request, 'comiccollection/writers.html', {'all_writers': all_writers, 'search_form': search_form})


@login_required
def comic_detail(request, comic_id):
    comic = get_object_or_404(ComicBook, pk=comic_id)
    return render(request, 'comiccollection/comic_detail.html', {'comic': comic})


@login_required
def illustrator_detail(request, illustrator_id):
    illustrator = get_object_or_404(Illustrator, pk=illustrator_id)
    context = {
        'illustrator': illustrator,
        'illustrator_comics': illustrator.comicbook_set.all(),
        'illustrator_series': illustrator.series,
        'genreData': json.dumps({g.name: ComicBook.objects.filter(genre=g, illustrators=illustrator).count() for g in Genre.objects.all()}),
    }
    return render(request, 'comiccollection/illustrator_detail.html', context=context)


@login_required
def publisher_detail(request, publisher_id):
    publisher = get_object_or_404(Publisher, pk=publisher_id)
    context = {
        'publisher': publisher,
        'publisher_comics': publisher.comicbook_set.all(),
        'publisher_series': publisher.series,
        'genreData': json.dumps({g.name: ComicBook.objects.filter(genre=g, publisher=publisher).count() for g in Genre.objects.all()}),
    }
    return render(request, 'comiccollection/publisher_detail.html', context=context)


@login_required
def writer_detail(request, writer_id):
    writer = get_object_or_404(Writer, pk=writer_id)
    context = {
        'writer': writer,
        'writer_comics': writer.comicbook_set.all(),
        'writer_series': writer.series,
        'genreData': json.dumps({g.name: ComicBook.objects.filter(genre=g, writers=writer).count() for g in Genre.objects.all()}),
    }
    return render(request, 'comiccollection/writer_detail.html', context=context)


@login_required
def series_detail(request, series_id):
    series = get_object_or_404(Series, pk=series_id)
    series_comics = series.comicbook_set.all()
    return render(request, 'comiccollection/series_detail.html', {'series': series, 'series_comics': series_comics})


@login_required
def comic_create(request):
    if request.method == 'POST':
        form = ComicBookForm(request.POST)
        if form.is_valid():
            form.save()
        if 'return' in request.POST:
            return redirect('/comiccollection/comics')
    return render(request, 'comiccollection/new_comic.html', {'form': ComicBookForm()})


@login_required
def illustrator_create(request):
    if request.method == 'POST':
        form = IllustratorForm(request.POST)
        if form.is_valid():
            form.save()
        if 'return' in request.POST:
            return redirect('/comiccollection/illustrators')
    return render(request, 'comiccollection/new_illustrator.html', {'form': IllustratorForm()})


@login_required
def publisher_create(request):
    if request.method == 'POST':
        form = PublisherForm(request.POST)
        if form.is_valid():
            form.save()
        if 'return' in request.POST:
            return redirect('/comiccollection/publishers')
    return render(request, 'comiccollection/new_publisher.html', {'form': PublisherForm()})


@login_required
def writer_create(request):
    if request.method == 'POST':
        form = WriterForm(request.POST)
        if form.is_valid():
            form.save()
        if 'return' in request.POST:
            return redirect('/comiccollection/writers')
    return render(request, 'comiccollection/new_writer.html', {'form': WriterForm()})


@login_required
def series_create(request):
    if request.method == 'POST':
        form = SeriesForm(request.POST)
        if form.is_valid():
            form.save()
        if 'return' in request.POST:
            return redirect('/comiccollection/series')
    return render(request, 'comiccollection/new_series.html', {'form': SeriesForm()})
