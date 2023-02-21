"""toxit_main URL Configuration

    The `urlpatterns` list routes URLs to views https://docs.djangoproject.com/en/4.1/topics/http/urls/

    namespace is needed to have multiple urls link to the langing page,
    if no namepsace is provided in the include() portion of path then the warning

        WARNINGS:
        ?: (urls.W005) URL namespace 'toxit' isn't unique. You may not be able to reverse all URLs in this namespace

    gets raised and can cause side effects later in development 
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('toxit.urls', namespace='toxit_no_url')), # no url redirect instead of /toxit/
    path('toxit/', include('toxit.urls', namespace='toxit')),  # namespace necessary to keep each unique and prevent W005 error
    path('admin/', admin.site.urls),
    path('toxit/', include('toxit.urls')),
]