# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.shortcuts import render, HttpResponse,redirect
from django.contrib import messages
from models import *
from time import gmtime, strftime
from datetime import datetime, timedelta
import bcrypt

def index(request):
    if 'id' not in request.session:
        return render(request,'appointment/index.html') 
    else:
        return redirect('/user')
def user(request):
    user = User.objects.get(id=request.session['id'])
    today = strftime("%Y-%m-%d", gmtime())
    tomorrow = datetime.today() + timedelta(days=1)
    context = { "date": strftime("%B %d, %Y", gmtime()),
                "today" : today,
                "time" : strftime("%H:%M", gmtime()),
                "appointments" : user.appointments.filter(date=today).order_by('time'),
                "other_appointment" : user.appointments.filter(date__gte=tomorrow),
                "name" : user.name
  }
    return render(request, 'appointment/appointment.html', context)  
def register(request):
    if request.method == 'POST':
        errors = User.objects.regis_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
        else:
            psw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(name=request.POST['name'], email=request.POST['email'],password = psw,dob=request.POST['dob'])
            request.session['id'] = user.id
        return redirect('/user')
def login(request):
    if request.method == 'POST':
        try:
            User.objects.get(email = request.POST['user']) 
        except:
            messages.warning(request, 'Username or password you entered is incorrect.') 
            return redirect ('/')
        user = User.objects.get(email= request.POST['user'])
        if bcrypt.checkpw(request.POST['psw'].encode(), user.password.encode()):
            request.session['id'] = user.id
            return redirect('/user')
        else:
            messages.warning(request, 'Username or password you entered is incorrect.')
    return redirect('/')
def add(request):
    if len(request.POST['task']) <=0:
        messages.warning(request, "Task cannot be blank")
    if request.POST['date'] < strftime("%Y-%m-%d", gmtime()):
        messages.warning(request, "Please choose today or future date")
    if len(request.POST['time']) <=0:
        messages.warning(request, "Please choose appointment time.")
    else:
        user = User.objects.get(id=request.session['id']) 
        Appointment.objects.create(user=user,task=request.POST['task'],date=request.POST['date'],time=request.POST['time'],status=request.POST['status'])
    return redirect('/user')
def edit(request,id):
    context = { "appointment" : Appointment.objects.get(id=id),
                "date" : strftime("%Y-%m-%d", gmtime()),
                "time" : strftime("%H:%M", gmtime())
    }
    return render(request, "appointment/edit.html", context)
def update(request,id):
    if len(request.POST['task']) <=0:
        messages.warning(request, "Task cannot be blank.")
    if request.POST['date'] < strftime("%Y-%m-%d", gmtime()):
        messages.warning(request, "Please choose today or future date.")
    if len(request.POST['time']) <=0:
        messages.warning(request, "Please choose appointment time.")
    else:
        edit_appointment = Appointment.objects.get(id=id)
        edit_appointment.task = request.POST['task']
        edit_appointment.status = request.POST['status']
        edit_appointment.date = request.POST['date']
        edit_appointment.time = request.POST['time']
        edit_appointment.save()
    return redirect('/edit/'+id)
def logout(request):
    del request.session['id']
    return redirect('/')
def delete(request,id):
    Appointment.objects.get(id=id).delete()
    return redirect('/user')