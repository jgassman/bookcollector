import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from gamecollection.forms import GameForm, SearchForm, SeriesForm, StudioForm, SystemForm
from gamecollection.models import Game, Genre, Series, Studio, System


@login_required
def index(request):
    context = {
        'game_count': Game.objects.count(),
        'studio_count': Studio.objects.count(),
        'series_count': Series.objects.count(),
        'system_count': System.objects.count(),
        'all_game_count': Game.objects.aggregate(Sum('copies')),
        'systemData': json.dumps({s.name: Game.objects.filter(system=s).count() for s in System.objects.all()}),
        'genreData': json.dumps({g.name: Game.objects.filter(genre=g).count() for g in Genre.objects.all()})
    }
    return render(request, 'gamecollection/index.html', context=context)


@login_required
def games(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_text = form.cleaned_data['search_text']
            games = Game.objects.filter(title__icontains=search_text)
    else:
        games = Game.objects.order_by('title')
    paginator = Paginator(games, 25)
    page = request.GET.get('page')
    search_form = SearchForm()
    try:
        all_games = paginator.page(page)
    except PageNotAnInteger:
        all_games = paginator.page(1)
    except EmptyPage:
        all_games = paginator.page(paginator.num_pages)
    return render(request, 'gamecollection/games.html', {'all_games': all_games, 'search_form': search_form})


@login_required
def genres(request):
    all_genres = Genre.objects.order_by('name')
    return render(request, 'gamecollection/genres.html', {'all_genres': all_genres})

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
    return render(request, 'gamecollection/series.html', {'all_series': all_series, 'search_form': search_form})


@login_required
def studios(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_text = form.cleaned_data['search_text']
            studios = Studio.objects.filter(name__icontains=search_text)
    else:
        studios = Studio.objects.order_by('name')
    paginator = Paginator(studios, 25)
    page = request.GET.get('page')
    search_form = SearchForm()
    try:
        all_studios = paginator.page(page)
    except PageNotAnInteger:
        all_studios = paginator.page(1)
    except EmptyPage:
        all_studios = paginator.page(paginator.num_pages)
    return render(request, 'gamecollection/studios.html', {'all_studios': all_studios, 'search_form': search_form})


@login_required
def systems(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_text = form.cleaned_data['search_text']
            systems = System.objects.filter(name__icontains=search_text)
    else:
        systems = System.objects.order_by('name')
    paginator = Paginator(systems, 25)
    page = request.GET.get('page')
    search_form = SearchForm()
    try:
        all_systems = paginator.page(page)
    except PageNotAnInteger:
        all_systems = paginator.page(1)
    except EmptyPage:
        all_systems = paginator.page(paginator.num_pages)
    return render(request, 'gamecollection/systems.html', {'all_systems': all_systems, 'search_form': search_form})


@login_required
def game_detail(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    return render(request, 'gamecollection/game_detail.html', {'game': game})


@login_required
def genre_detail(request, genre_id):
    genre = get_object_or_404(Genre, pk=genre_id)
    context = {
        'genre': genre,
        'game_count': Game.objects.filter(genre=genre).count(),
        'series': [s for s in Series.objects.all() if s.genre == genre],
        'series_count': sum([1 for s in Series.objects.all() if s.genre == genre]),
    }
    return render(request, 'gamecollection/genre_detail.html', context=context)


@login_required
def series_detail(request, series_id):
    series = get_object_or_404(Series, pk=series_id)
    context = {'series': series,
               'systemData': json.dumps({s.name: Game.objects.filter(system=s, series=series).count() for s in series.systems}),
               'genreData': json.dumps({g.name: Game.objects.filter(genre=g, series=series).count() for g in series.genres})}
    return render(request, 'gamecollection/series_detail.html', context=context)


@login_required
def studio_detail(request, studio_id):
    studio = get_object_or_404(Studio, pk=studio_id)
    context = {'studio': studio,
               'systemData': json.dumps({s.name: Game.objects.filter(system=s, studio=studio).count() for s in studio.systems}),
               'genreData': json.dumps({g.name: Game.objects.filter(genre=g, studio=studio).count() for g in studio.genres})}
    return render(request, 'gamecollection/studio_detail.html', context=context)


@login_required
def system_detail(request, system_id):
    system = get_object_or_404(System, pk=system_id)
    context = {'system': system,
               'studioData': json.dumps({s.name: Game.objects.filter(studio=s, system=system).count() for s in system.studios}),
               'genreData': json.dumps({g.name: Game.objects.filter(genre=g, system=system).count() for g in system.genres})}
    return render(request, 'gamecollection/system_detail.html', context=context)


@login_required
def new_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            form.save()
        if 'return' in request.POST:
            return redirect('/gamecollection/games')
    return render(request, 'gamecollection/new_game.html', {'form': GameForm()})


@login_required
def new_series(request):
    if request.method == 'POST':
        form = SeriesForm(request.POST)
        if form.is_valid():
            form.save()
        if 'return' in request.POST:
            return redirect('/gamecollection/series')
    return render(request, 'gamecollection/new_series.html', {'form': SeriesForm()})


@login_required
def new_studio(request):
    if request.method == 'POST':
        form = StudioForm(request.POST)
        if form.is_valid():
            form.save()
        if 'return' in request.POST:
            return redirect('/gamecollection/studios')
    return render(request, 'gamecollection/new_studio.html', {'form': StudioForm()})


@login_required
def new_system(request):
    if request.method == 'POST':
        form = SystemForm(request.POST)
        if form.is_valid():
            form.save()
        if 'return' in request.POST:
            return redirect('/gamecollection/systems')
    return render(request, 'gamecollection/new_system.html', {'form': SystemForm()})
