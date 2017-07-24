import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AuthorForm, BookForm, SeriesForm, SearchForm
from .models import Author, Book, Series, Genre, Subgenre, AGE_GROUP_CHOICES


@login_required
def index(request):
    context = {
        'book_count': Book.objects.count(),
        'author_count': Author.objects.count(),
        'series_count': Series.objects.count(),
        'genreData': json.dumps({g.name: Book.objects.filter(genre=g).count() for g in Genre.objects.all()}),
        'ageData': json.dumps({age[0]: Book.objects.filter(age_group=age[0]).count() for age in AGE_GROUP_CHOICES})
    }
    return render(request, 'bookcollection/index.html', context=context)


@login_required
def authors(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_text = form.cleaned_data['search_text']
            authors = Author.objects.filter(Q(first_name__icontains=search_text) | Q(last_name__icontains=search_text))
    else:
        authors = Author.objects.order_by('last_name')
    paginator = Paginator(authors, 25)
    page = request.GET.get('page')
    search_form = SearchForm()
    try:
        all_authors = paginator.page(page)
    except PageNotAnInteger:
        all_authors = paginator.page(1)
    except EmptyPage:
        all_authors = paginator.page(paginator.num_pages)
    return render(request, 'bookcollection/authors.html', {'all_authors': all_authors, 'search_form': search_form})


@login_required
def books(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_text = form.cleaned_data['search_text']
            books = Book.objects.filter(title__icontains=search_text)
    else:
        books = Book.objects.order_by('title')
    paginator = Paginator(books, 25)
    page = request.GET.get('page')
    search_form = SearchForm()
    try:
        all_books = paginator.page(page)
    except PageNotAnInteger:
        all_books = paginator.page(1)
    except EmptyPage:
        all_books = paginator.page(paginator.num_pages)
    return render(request, 'bookcollection/books.html', {'all_books': all_books, 'search_form': search_form})


@login_required
def genres(request):
    all_genres = Genre.objects.order_by('name')
    return render(request, 'bookcollection/genres.html', {'all_genres': all_genres})


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
    return render(request, 'bookcollection/series.html', {'all_series': all_series, 'search_form': search_form})


@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'bookcollection/book_detail.html', {'book': book})


@login_required
def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    author_books = author.book_set.all()
    context = {
        'author': author,
        'author_books': author_books,
        'genreData': json.dumps({g.name: Book.objects.filter(genre=g).count() for g in author.genres}),
        'ageData': json.dumps({age[0]: Book.objects.filter(authors=author, age_group=age[0]).count() for age in AGE_GROUP_CHOICES})
    }
    return render(request, 'bookcollection/author_detail.html', context=context)


@login_required
def genre_detail(request, genre_id):
    genre = get_object_or_404(Genre, pk=genre_id)
    context = {
        'genre': genre,
        'book_count': Book.objects.filter(genre=genre).count(),
        'authors': [a for a in Author.objects.all() if genre in a.genres],
        'author_count': sum([1 for a in Author.objects.all() if genre in a.genres]),
        'series': [s for s in Series.objects.all() if s.genre == genre],
        'series_count': sum([1 for s in Series.objects.all() if s.genre == genre]),
        'genreData': json.dumps({g.name: Book.objects.filter(subgenre=g).count() for g in Subgenre.objects.filter(genre=genre)}),
        'ageData': json.dumps({age[0]: Book.objects.filter(genre=genre, age_group=age[0]).count() for age in AGE_GROUP_CHOICES})
    }
    return render(request, 'bookcollection/genre_detail.html', context=context)


@login_required
def series_detail(request, series_id):
    series = get_object_or_404(Series, pk=series_id)
    series_books = series.book_set.all()
    return render(request, 'bookcollection/series_detail.html', {'series': series, 'series_books': series_books})


@login_required
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
        if 'return' in request.POST:
            return redirect('/bookcollection/books')
    return render(request, 'bookcollection/new_book.html', {'form': BookForm()})


@login_required
def author_create(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
        if 'return' in request.POST:
            return redirect('/bookcollection/authors')
    return render(request, 'bookcollection/new_author.html', {'form': AuthorForm()})


@login_required
def series_create(request):
    if request.method == 'POST':
        form = SeriesForm(request.POST)
        if form.is_valid():
            form.save()
        if 'return' in request.POST:
            return redirect('/bookcollection/series')
    return render(request, 'bookcollection/new_series.html', {'form': SeriesForm()})
