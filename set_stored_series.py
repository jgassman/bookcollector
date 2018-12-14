from bookcollection.models import Series

for series in Series.objects.all():
    if series.book_count == 0:
        series.storage = True
        series.save()
