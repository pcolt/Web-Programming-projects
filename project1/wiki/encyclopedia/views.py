from django import forms
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from markdown2 import markdown, markdown_path
import os.path
import random
from . import util

class NewEntryForm(forms.Form):
	title = forms.CharField(label="New entrie's title")
	content = forms.CharField(label="New entrie's content", widget=forms.Textarea)

class ModifyEntryForm(forms.Form):
	title = forms.CharField(label="Entrie's title", widget=forms.TextInput(attrs={"readonly": "readonly"}))
	content = forms.CharField(label="Modify entrie's content", widget=forms.Textarea)

class SearchForm(forms.Form):
	search = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Search Encyclopedia"}))


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries(), "searchForm":SearchForm()})

def titles(request, title):
	if request.method == "POST":
		searchForm = SearchForm(request.POST)
		if searchForm.is_valid():
			searchTitle = searchForm.cleaned_data["search"]
			if searchTitle in util.list_entries():
				return render(request, "encyclopedia/title.html", {"searchForm":SearchForm(), "title":searchTitle, "content":markdown(util.get_entry(searchTitle))})			
			else:
				subsList = [i for i in util.list_entries() if searchTitle in i]
				return render(request, "encyclopedia/index.html", {
        "entries": subsList, "searchForm":SearchForm()
    })				

	try:
		return render(request, "encyclopedia/title.html", {"title":title, "content":markdown(util.get_entry(title)), "searchForm":SearchForm()})
	except TypeError:
		return HttpResponseNotFound("Page not found")

def randomPage(request):
	title = random.choice(util.list_entries())
	return titles(request, title)

def new(request):
	if request.method == "POST":
		form = NewEntryForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data["title"]
			content = form.cleaned_data["content"]
			fileName = "entries/" + title + ".md"
			if os.path.isfile(fileName):
				return HttpResponse(f"a '{title}' page already exists")
			else:
				f = open(fileName, "w")
				f.write(content)
				f.close()
				return titles(request, title)
		else:
			return render(request, "encyclopedia/new.html", {"newEntryForm":form, "searchForm":SearchForm()})
	return render(request, "encyclopedia/new.html", {"newEntryForm":NewEntryForm(), "searchForm":SearchForm()})

def edit(request, name):
	if request.method == "POST":
		form = ModifyEntryForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data["title"]
			content = form.cleaned_data["content"]
			fileName = "entries/" + title + ".md"
			f = open(fileName, "w")
			f.write(content)
			f.close()
			return titles(request, title)
		else:
			return render(request, "encyclopedia/edit.html", {"modifyEntryForm":form, "searchForm":SearchForm()})
	return render(request, "encyclopedia/edit.html", {"modifyEntryForm":ModifyEntryForm({"title":name, "content":util.get_entry(name)}), "searchForm":SearchForm()})
