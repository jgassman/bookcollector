import json
import bookcollection.utils as utils

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .forms import SearchForm
from .models import Author, Book, Series, Genre, Subgenre, AGE_GROUP_CHOICES, Tag


@login_required
def index(request):
    read_books = Book.objects.filter(read=True, storage=False).count()
    unread_books = Book.objects.filter(read=False, storage=False).count()
    stored_books = Book.objects.filter(storage=True).count()
    unstored_books = Book.objects.filter(storage=False).count()
    context = {
        'book_count': Book.objects.filter(storage=False).count(),
        'author_count': Author.objects.filter(storage=False).count(),
        'series_count': Series.objects.filter(storage=False).count(),
        'genreData': json.dumps({g.name: Book.objects.filter(genre=g, storage=False).count() for g in Genre.objects.all()}),
        'ageData': json.dumps({age[1]: Book.objects.filter(age_group=age[0], storage=False).count() for age in AGE_GROUP_CHOICES}),
        'readData': json.dumps({
            'Read ({} books)'.format(read_books): read_books,
            'Unread ({} books)'.format(unread_books): unread_books,
        }),
        'storageData': json.dumps({
            'Stored ({} books)'.format(stored_books): stored_books,
            'Unstored ({} books)'.format(unstored_books): unstored_books,
        }),
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
    paginator = Paginator(authors, 50)
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
def genre_authors(request, genre_id):
    genre = get_object_or_404(Genre, pk=genre_id)
    authors = [a for a in Author.objects.all() if genre in a.genres]
    paginator = Paginator(authors, 50)
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
def age_authors(request, age_code):
    age = utils.get_age_group(age_code)
    authors = utils.get_age_group_authors(age)
    paginator = Paginator(authors, 50)
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
def books(request, age_code=None, *args, **kwargs):
    books = Book.objects.all()
    if age_code:
        books = books.filter(age_group=age_code)
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_text = form.cleaned_data['search_text']
            books = books.filter(title__icontains=search_text)
    books = sorted(books, key=lambda b: b.alphabetical_title)
    paginator = Paginator(books, 50)
    page = request.GET.get('page')
    search_form = SearchForm()
    try:
        all_books = paginator.page(page)
    except PageNotAnInteger:
        all_books = paginator.page(1)
    except EmptyPage:
        all_books = paginator.page(paginator.num_pages)
    return render(request, 'bookcollection/books.html', {'all_books': all_books, 'ages': AGE_GROUP_CHOICES,
        'age_code': age_code, 'search_form': search_form})


@login_required
def unread(request, age_code=None, *args, **kwargs):
    books = Book.objects.filter(read=False, storage=False)
    if age_code:
        books = books.filter(age_group=age_code)
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_text = form.cleaned_data['search_text']
            books = sorted(books.filter(title__icontains=search_text), key=lambda b: b.alphabetical_title)
    books = sorted(books, key=lambda b: b.alphabetical_title)
    paginator = Paginator(books, 50)
    page = request.GET.get('page')
    search_form = SearchForm()
    try:
        all_books = paginator.page(page)
    except PageNotAnInteger:
        all_books = paginator.page(1)
    except EmptyPage:
        all_books = paginator.page(paginator.num_pages)
    return render(request, 'bookcollection/unread.html', {'all_books': all_books,
        'ages': AGE_GROUP_CHOICES, 'age_code': age_code, 'search_form': search_form})


@login_required
def author_books(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    books = author.sorted_books
    paginator = Paginator(books, 50)
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
def genre_books(request, genre_id):
    genre = get_object_or_404(Genre, pk=genre_id)
    books = genre.sorted_books
    paginator = Paginator(books, 50)
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
def author_genres(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    all_genres = [g for g in Genre.objects.all() if g in author.genres]
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
    paginator = Paginator(series, 50)
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
def author_series(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    series = [s for s in Series.objects.all() if author in s.authors]
    paginator = Paginator(series, 50)
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
def genre_series(request, genre_id):
    genre = get_object_or_404(Genre, pk=genre_id)
    series = [s for s in Series.objects.all() if s.genre == genre]
    paginator = Paginator(series, 50)
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
def age_series(request, age_code):
    age = utils.get_age_group(age_code)
    series = sorted([book.series for book in utils.get_age_group_books(age) if book.series])
    paginator = Paginator(series, 50)
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
    if request.method == 'POST':
        if 'read' in request.POST:
            Book.objects.filter(pk=book_id).update(read=True)
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'bookcollection/book_detail.html', {'book': book})


@login_required
def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    context = {
        'author': author,
        'author_books': author.sorted_books,
        'genreData': json.dumps({g.name: Book.objects.filter(genre=g).count() for g in author.genres}),
        'ageData': json.dumps({age[1]: Book.objects.filter(authors=author, age_group=age[0]).count() for age in AGE_GROUP_CHOICES}),
        'readData': json.dumps({
            'Read': Book.objects.filter(authors=author, read=True).count(),
            'Unread': Book.objects.filter(authors=author, read=False).count()
            })
    }
    return render(request, 'bookcollection/author_detail.html', context=context)


@login_required
def genre_detail(request, genre_id):
    genre = get_object_or_404(Genre, pk=genre_id)
    books = genre.sorted_books
    context = {
        'genre': genre,
        'book_count': len(books),
        'books': books,
        'authors': [a for a in Author.objects.all() if genre in a.genres],
        'author_count': sum([1 for a in Author.objects.all() if genre in a.genres]),
        'series': [s for s in Series.objects.all() if s.genre == genre],
        'series_count': sum([1 for s in Series.objects.all() if s.genre == genre]),
        'genreData': json.dumps({g.name: Book.objects.filter(subgenre=g).count() for g in Subgenre.objects.filter(genre=genre)}),
        'ageData': json.dumps({age[1]: Book.objects.filter(genre=genre, age_group=age[0]).count() for age in AGE_GROUP_CHOICES}),
        'readData': json.dumps({
            'Read': Book.objects.filter(genre=genre, read=True).count(),
            'Unread': Book.objects.filter(genre=genre, read=False).count()
            })
    }
    if request.method == 'POST':
        if 'subgenre' in request.POST:
            context['show_subs'] = True
        elif 'age_groups' in request.POST:
            context['show_ages'] = True
            context['age_data'] = [(age[1], sorted(Book.objects.filter(genre=genre, age_group=age[0]),
                                    key=lambda b: b.alphabetical_title)) for age in AGE_GROUP_CHOICES]
    return render(request, 'bookcollection/genre_detail.html', context=context)


@login_required
def series_detail(request, series_id):
    series = get_object_or_404(Series, pk=series_id)
    series_books = series.book_set.all().order_by('series_number')
    return render(request, 'bookcollection/series_detail.html', {'series': series, 'series_books': series_books})


@login_required
def tags(request):
    tags = Tag.objects.all()
    return render(request, 'bookcollection/tags.html', {'tags': tags})


@login_required
def tag_detail(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    tag_books = sorted(tag.book_set.all(), key=lambda b: b.alphabetical_title)
    return render(request, 'bookcollection/tag_detail.html', {'tag': tag, 'tag_books': tag_books})


@login_required
def ages(request):
    ages = AGE_GROUP_CHOICES
    return render(request, 'bookcollection/ages.html', {'ages': ages})


@login_required
def age_detail(request, age_code):
    age = utils.get_age_group(age_code)
    age_books = sorted(Book.objects.filter(age_group=age_code), key=lambda b: b.alphabetical_title)
    series_count = len(set([book.series for book in age_books if book.series]))
    context = {}
    context['age'] = age
    context['age_books'] = age_books
    context['book_count'] = len(age_books)
    context['author_count'] = len(utils.get_age_group_authors(age))
    context['series_count'] = series_count
    context['genreData'] = json.dumps({g.name: Book.objects.filter(genre=g, age_group=age[0]).count()
                                       for g in Genre.objects.all()})
    context['genres'] = utils.get_age_group_books_by_genre(age)
    context['readData'] = json.dumps({'Read': Book.objects.filter(age_group=age[0], read=True).count(),
                                      'Unread': Book.objects.filter(age_group=age[0], read=False).count()})
    if request.method == 'POST':
        if 'genres' in request.POST:
            context['show_genres'] = True
    return render(request, 'bookcollection/age_detail.html', context=context)
