from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from bookmarks.models import Bookmark
import requests
from bs4 import BeautifulSoup


def correct_url(url):
    try:
        requests.get(url)
        return True
    except:
        return False


def parse_meta(url):
    """
    Parses url for meta data
    Supported protocols: opengraph, schema.org
    :returns: dictionary
    """
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" +
               " AppleWebKit/537.36 (KHTML, like Gecko)" +
               " Chrome/74.0.3729.169 Safari/537.36"}
    source_code = requests.get(url, headers=headers).text
    soup = BeautifulSoup(source_code, "html.parser")
    # Title
    title = soup.title
    if title:
        title = title.string.strip()
    else:
        # OpenGraph
        title = soup.find("meta", {"property": "og:title"})
        if title:
            title = title["content"].strip()
        else:
            # Schema.org
            title = soup.find("a", {"itemprop": "url"})
            if title:
                title = title["title"].strip()
            else:
                title = None

    # Description
    description = soup.find("meta", {"name": "description"})
    if description:
        description = description["content"].strip()
    else:
        # OpenGraph
        description = soup.find("meta", {"property": "og:description"})
        if description:
            description = description["content"].strip()
        else:
            description = ""

    # Icons
    icon = soup.find("link", rel="icon")
    if icon:
        icon = icon["href"]
    else:
        # OpenGraph
        icon = soup.find("meta", {"property": "og:image"})
        if icon:
            icon = icon["content"].strip()
        else:
            # Schema.org
            icon = soup.find("meta", {"itemprop": "image"})
            if icon:
                icon = icon["content"].strip()
            else:
                icon = None
    # Url correction
    if icon:
        url = url.split("/")
        if icon.startswith("//"):
            icon = url[0] + icon
        if icon.startswith("/"):
            icon = url[0] + "//" + url[2] + icon
    else:
        icon = ""

    return {"title": title, "description": description, "favicon": icon}


def index(request):
    if request.user.is_authenticated:
        logout(request)
    return render(request, "bookmarks/index.html")


def register(request):
    exist = False
    no_name = False
    if request.POST:
        name = request.POST["name"]
        email = request.POST["email"]
        password = request.POST["password"]
        # Check if field "name" is not empty
        if name:
            if not User.objects.filter(username=name).exists():
                user = User.objects.create_user(name, email, password)
                user.save()
                return HttpResponse('User has been created<p>\
                                    <a href="/bookmarks">Index page</a>')
            else:
                exist = True
        else:
            no_name = True
    context = {"exist": exist, "no_name": no_name}
    return render(request, "bookmarks/register.html", context)


def user_login(request):
    wrong = False
    if request.GET:
        name = request.GET["name"]
        password = request.GET["password"]
        user = authenticate(request, username=name, password=password)
        if user is not None:
            login(request, user)
            return redirect(show_bookmarks)
        else:
            wrong = True
    context = {"wrong": wrong}
    return render(request, "bookmarks/login.html", context)


def show_bookmarks(request):
    if request.user.is_authenticated:
        bookmarks = Bookmark.objects.filter(username=request.user.username)
        context = {"username": request.user.username, "bookmarks": bookmarks}
        return render(request, "bookmarks/show_bookmarks.html", context)
    else:
        return HttpResponse('You need to log in or register first\
                            <p><a href="/bookmarks">Index page</a>')


def add_bookmark(request):
    incorrect_url = False
    added = False
    in_db = False
    if request.POST:
        url = request.POST["url"]
        if not url.startswith("http://www."):
            if not url.startswith("www."):
                url = "http://www." + url
            else:
                url = "http://" + url
        if correct_url(url):
            username = request.user.username
            if Bookmark.objects.filter(username=username, url=url).count():
                in_db = True
            else:
                metadata = parse_meta(url)
                bookmark = Bookmark(username=username,
                                    url=url, title=metadata["title"],
                                    favicon=metadata["favicon"],
                                    description=metadata["description"])
                bookmark.save()
                added = True
        else:
            incorrect_url = not correct_url(url)
    context = {"incorrect_url": incorrect_url, "added": added, "in_db": in_db}
    return render(request, "bookmarks/add_bookmark.html", context)


def delete(request, id):
    bookmark = Bookmark.objects.get(username=request.user.username, id=id)
    bookmark.delete()
    return redirect('/bookmarks/show')
