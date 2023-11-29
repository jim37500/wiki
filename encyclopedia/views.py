from django.shortcuts import render
from django import forms
from django.http import HttpResponse
from markdown2 import Markdown
from django.urls import reverse
from django.http import HttpResponseRedirect
import random


from . import util

class SearchForm(forms.Form):
    keyword = forms.CharField(label="",required= False,
    widget= forms.TextInput(attrs={'placeholder':'Search Encyclopedia'}))

form = SearchForm()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": form
    })

def pages(request, entry):
    if request.method == "GET":
        content = util.get_entry(entry)
        if content == None:
            return render(request, "encyclopedia/result.html", {
                "message":"Page not Found",
                "form": form
            })
        
        markdowner = Markdown()
        return render(request, "encyclopedia/pages.html", {
            "entry": entry,
            "content": markdowner.convert(content),
            "form": form
        })
    
    else:
        return HttpResponseRedirect("edit")

def search(request):
    if request.method == "GET":
        form = SearchForm(request.GET)
        if form.is_valid():
            keyword = form.cleaned_data["keyword"].lower()
            entries = util.list_entries()

            results = []
            for entry in entries:
                if keyword == entry.lower():
                    return pages(request, entry)
                if keyword in entry.lower():
                    results.append(entry)
            
            if results:
                return render(request, "encyclopedia/search.html", {
                "form": form,
                "results": results
                })
            else:
                return render(request, "encyclopedia/result.html", {
                    "message":"Result not Found",
                    "form": form
                })
    else:
        return index(request)


def add_newpage(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')

        entries = util.list_entries()
        for entry in entries:
            if title.lower() == entry.lower():
                return render(request, "encyclopedia/result.html", {
                    "form": form,
                    "message": "Error! The title of page has existed"
                })
        
        util.save_entry(title, content)
        return render(request, "encyclopedia/result.html", {
            "form": form,
            "message": "Success, the page has added"
        })
    else:
        return render(request, "encyclopedia/add.html")
    
def edit_page(request, entry):
    if request.method == "GET":
        content = util.get_entry(entry)
        return render(request, "encyclopedia/edit.html", {
            "form": form,
            "entry": entry,
            "content": content
        })
    
    else:
        title = entry
        content = request.POST.get('content')
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("pages", kwargs={'entry': entry}))

def random_page(request):
    entry = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("pages", kwargs={'entry': entry}))

    

    
        