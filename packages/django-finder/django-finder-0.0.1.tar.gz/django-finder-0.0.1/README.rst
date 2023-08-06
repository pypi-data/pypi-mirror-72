=====
Django Finder
=====

Finder is a Django app to conduct a search for a car from only a picture. 


Quick start
-----------

1. Add "finder" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'finder.apps.FinderConfig',
    ]

2. Include the finder URLconf in your project urls.py like this::

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Index.as_view(), name='index'),
    path('upload/', forms.upload, name='upload'),
    path('upload/predictImage', index.predict_image, name="predictImage"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


3. Run ``python manage.py runserver`` 
4. 

5. Visit http://127.0.0.1:8000 to participate.