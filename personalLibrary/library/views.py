from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Book, Connections
from bs4 import BeautifulSoup
import requests


@login_required(login_url="/users/login_user")
def index(req):
    conns = Connections.objects.filter(User=req.user).order_by().values('Book').distinct()
    books = Book.objects.filter(ISBN__in=conns)
    return render(req, "library/index.html", {"user":req.user,"books":books,"addBookURL":"/library/add_book"})


@login_required(login_url="/users/login_user")
def add_book(req):
    if req.method != "POST":
        return render(req, "library/add_book.html", {})
    
    if (ISBN:=req.POST.get("isbn")) != None:
        context = {"status":"fuckin' searching :D"} 
        context.update(getBook(ISBN.strip()))
        return render(req, "library/add_book.html", context)

    if req.POST["ISBN"] == "" or len(req.POST["ISBN"])> 30:
        return render(req, "library/add_book.html", {"status":"failed to add"})
    if len(req.POST["Title"]) > 60:
        return render(req, "library/add_book.html", {"status":"failed to add"})
    if len(req.POST["Author"]) > 60:
        return render(req, "library/add_book.html", {"status":"failed to add"})
    if len(req.POST["Genre"]) > 120:
        return render(req, "library/add_book.html", {"status":"failed to add"})
    try:
        numOfPages = int(req.POST["NumOfPages"])
        if numOfPages < 1 or 32766 < numOfPages:
            return render(req, "library/add_book.html", {"status":"failed to add"})
    except:
        return render(req, "library/add_book.html", {"status":"failed to add"})
        
    if len(Connections.objects.filter(User=req.user, Book=req.POST["ISBN"].strip())) != 0:
        return render(req, "library/add_book.html", {"status":"book already in db"})
    newConn = Connections(User=req.user, Book=req.POST["ISBN"].strip())
    newConn.save()

    if len(Book.objects.filter(ISBN=req.POST["ISBN"].strip())) != 0:
        return redirect("/library")

    newBook = Book(ISBN=req.POST["ISBN"].strip(), Title=req.POST["Title"], Author=req.POST["Author"], NumOfPages=req.POST["NumOfPages"], Genre=req.POST["Genre"])
    newBook.save()
    return redirect("/library")

def getBook(ISBN):
    context = {} 
    urlStart = "https://aleph.nkp.cz/F/"
    urlEnd = "?func=find-b&find_code=ISN&x=0&y=0&request="
    response = requests.get(urlStart)
    soup = BeautifulSoup(response.content, 'html.parser')
    urlTemp = soup.find('b', text='NKC')
    urlMid = urlTemp.parent["href"][23:79]
    realUrl = urlStart + urlMid + urlEnd + ISBN.strip()
    response = requests.get(realUrl)
    soup = BeautifulSoup(response.content, 'html.parser')
    for td in soup.find_all('td', class_="td1"):
        if td.text == "Název":
            td = td.find_next('td', class_="td1")
            info = td.text.split("/")
            context["title"] = info[0].strip()
            context["author"] = info[1].split(";")[0].strip()
        elif td.text == "Popis (rozsah)":
            td = td.find_next('td', class_="td1")
            context["pages"] = td.text.split("s")[0][:-1]
        elif td.text == "Forma, žánr":
            td = td.find_next('td', class_="td1")
            context["genre"] = td.text
    
    context["ISBN"] = ISBN.strip()
    return context


@login_required(login_url="/users/login_user")
def delete_book(req, ISBN):
    Connections.objects.filter(User=req.user, Book=ISBN).delete()
    if len(Connections.objects.filter(Book=ISBN)) == 0:
        Book.objects.filter(ISBN=ISBN).delete()
    return redirect("/library")

@login_required(login_url="/users/login_user")
def delete_users_data(req):
    conns = Connections.objects.filter(User=req.user).order_by().values('Book').distinct()
    for ISBN in conns:
        Book.objects.filter(ISBN=ISBN["Book"]).delete()
    conns = Connections.objects.filter(User=req.user) 
    for conn in conns:
        conn.delete()
    return redirect("/users/delete_user")
