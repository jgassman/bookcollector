import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum
from django.shortcuts import get_object_or_404, render

from gamecollection.forms import SearchForm
from gamecollection.models import Game, Genre, Series, Developer, System, AGE_RATING_CHOICES


@login_required
def index(request):
    context = {
        'game_count': Game.objects.count(),
        'developer_count': Developer.objects.count(),
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
def developers(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_text = form.cleaned_data['search_text']
            developers = Developer.objects.filter(name__icontains=search_text)
    else:
        developers = Developer.objects.order_by('name')
    paginator = Paginator(developers, 25)
    page = request.GET.get('page')
    search_form = SearchForm()
    try:
        all_developers = paginator.page(page)
    except PageNotAnInteger:
        all_developers = paginator.page(1)
    except EmptyPage:
        all_developers = paginator.page(paginator.num_pages)
    return render(request, 'gamecollection/developers.html', {'all_developers': all_developers, 'search_form': search_form})


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
    if request.method == 'POST':
        if 'case' in request.POST:
            Game.objects.filter(pk=game_id).update(needs_case=False)
        elif 'booklet' in request.POST:
            Game.objects.filter(pk=game_id).update(needs_booklet=False)
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
def developer_detail(request, developer_id):
    developer = get_object_or_404(Developer, pk=developer_id)
    context = {'developer': developer,
               'systemData': json.dumps({s.name: Game.objects.filter(system=s, developers=developer).count() for s in developer.systems}),
               'genreData': json.dumps({g.name: Game.objects.filter(genre=g, developers=developer).count() for g in developer.genres})}
    return render(request, 'gamecollection/developer_detail.html', context=context)


@login_required
def system_detail(request, system_id):
    system = get_object_or_404(System, pk=system_id)
    context = {'system': system,
               'ageData': json.dumps({age[1]: Game.objects.filter(age_rating=age[0]).count() for age in AGE_RATING_CHOICES}),
               'genreData': json.dumps({g.name: Game.objects.filter(genre=g, system=system).count() for g in system.genres})}
    return render(request, 'gamecollection/system_detail.html', context=context)
