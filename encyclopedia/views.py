from django.shortcuts import render, redirect
from django.http import Http404

from . import util
import random



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_page(request, title):
    content = util.get_entry(title)

    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "Page Not Found"
        })

    converted_content = util.convert_Markdowm_to_Html(content)

    return render(request, "encyclopedia/entry_page.html", {
        "title": title.upper(),
        "content": converted_content
    })

def search(request):
    if request.method == "POST":
        search_query = request.POST["q"]
        content = util.get_entry(search_query) 
        if content:
            return render(request, "encyclopedia/entry_page.html", {
                "title": search_query,
                "content": content
            })
        else:
            entries = util.list_entries()
            suggest = []

            for entry in entries:
                if search_query.lower() in entry.lower():
                    suggest.append(entry)
                    return render(request, "encyclopedia/recommend.html", {
                        "suggest": suggest
                    })
            
    return render(request, "encyclopedia/error.html", {
        "message": "Page Not Found"
    })


def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html")
    else:
        title = request.POST['title']
        content = request.POST['content']

        existing_title = util.get_entry(title)

        if existing_title:
            return render(request, "encyclopedia/error.html", {
                "message": "Entry already exists"
            })
        else:
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry_page.html", {
                "title": title.upper(),
                "content": content
            })
    
def edit(request, title):
    if request.method == "GET":
        content = util.get_entry(title)

        if content is None:
            return render(request, "encyclopedia/error.html", {
                "message": "Page Not Found" },
                status=404
                )
        else:
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "content": content  
            })
    else:
        if request.method == "POST":
            updated_content = request.POST["content"]
            updated_title = request.POST["title"]

            util.save_entry(updated_title, updated_content)

            return render(request, "encyclopedia/entry_page.html", {
                "title": updated_title,
                "content": updated_content
            })
    

def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    content = util.get_entry(random_entry)
    return render(request, "encyclopedia/entry_page.html", {
        "title": random_entry,
        "content": content
    })




      

       