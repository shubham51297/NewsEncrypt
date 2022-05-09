from email import message
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from .models import User, Source, NewsTip, Editor

def querydict_to_dict(query_dict):
    data = {}
    for key in query_dict.keys():
        v = query_dict.getlist(key)
        if len(v) == 1:
            v = v[0]
        data[key] = v
    return data

def index(request):
    if request.method == "POST":
        data = querydict_to_dict(request.POST)
        url = '/login'
        try:
            source=User.objects.get(username=data['username'])
        except User.DoesNotExist:
            source = None
        if source==None:
            resp_body = '<script>alert("The user doesn\'t exists.");\
            window.location="%s"</script>' % url
            return HttpResponse(resp_body)
        elif source.password!=data['password']:
                resp_body = '<script>alert("Password mismatch");\
                window.location="%s"</script>' % url
                return HttpResponse(resp_body)
        elif source.userType=='E':
            url='/editor/{}'.format(data['username'])
            return redirect(url)
        else:
            url='/addMessage/{}'.format(data['username'])
            return redirect(url)
        print(data)
        return render(request, 'mainApp/login.html')
    return render(request, 'mainApp/login.html')
    #return HttpResponse("Hello, world. You're at the polls index.")

def editor(request,username):
    return render(request, 'mainApp/editor.html', {'username': username })
def addSource(request,username):
    
    if request.method == "POST":
        data = querydict_to_dict(request.POST)
        #data={'username': 'TestUsername', 'password': 'Test123', 'name': 'Test'}
        
        user=User()
        user.username=data['username']
        user.password=data['password']
        user.userType='S'

        private_key = RSA.generate(1024)
        pubkey = private_key.publickey()
        privateKey = private_key.exportKey().decode("utf-8")
        publicKey = pubkey.exportKey().decode("utf-8")

        source=Source()
        source.username=data['username']
        source.name=data['name']
        source.publicKey=publicKey
        source.privateKey=privateKey
        
        user.save()
        source.save()
        print(user)
        print(source)
        url='/editor/{}'.format(username)
        return redirect(url)
    return render(request, 'mainApp/addSource.html', {'username':username})
    #return HttpResponse("Hello, world. You're at the polls index.")

def addMessage(request,username):
    if request.method == "POST":
        data = querydict_to_dict(request.POST)
        #data={'editor': 'shubham512', 'source': 'TestUsername', 'message': 'Test'}
        source=Source.objects.get(username=username)
        publicKey=source.publicKey
        
        key = RSA.import_key(publicKey)
        cipher = PKCS1_OAEP.new(key)
        message=bytes(data['message'], encoding='utf-8')
        ciphertext = cipher.encrypt(message)
        print(ciphertext)
        
        news=NewsTip()
        news.source=username
        news.editor=data['editor']
        news.message=ciphertext

        news.save()
    results=Editor.objects.all()
    results=results.values()
    print(results)
    return render(request, 'mainApp/tip.html',{'results': results})
    return HttpResponse("Hello, world. ViewMessage")

def allMessage(request,currenteditor):
    messages=NewsTip.objects.filter(editor=currenteditor)
    results=messages.values()
    return render(request, 'mainApp/allMessage.html',{'results': results})

def singleMessage(request,id):
    message=NewsTip.objects.filter(id=id)
    result=message.values()[0]
    #print(result['source'])
    source=Source.objects.filter(username=result['source'])
    source=source.values()[0]
    #print(source)
    privateKey=source['privateKey']
    key = RSA.import_key(privateKey)
    cipher = PKCS1_OAEP.new(key)
    curMessage=result['message']
    print(type(result['message']))
    plaintext = cipher.decrypt(curMessage)
    print (plaintext.decode("utf-8"))
    return render(request, 'mainApp/singleMessage.html',{'plaintext': plaintext.decode("utf-8")})
    return HttpResponse("Hello, world. allMessage")