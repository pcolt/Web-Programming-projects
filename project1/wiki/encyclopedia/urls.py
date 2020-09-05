from django.urls import include, path, re_path

from . import views

urlpatterns = [
	path("", views.index, name="index"),
	path('new', views.new, name="new"),
	path('random', views.randomPage, name="randomPage"),
	path('edit<str:name>', views.edit, name="edit"),
	path('<title>', views.titles, name="title"),
	]
