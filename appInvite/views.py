# -*- coding: utf-8 -*-
from appInvite import forms
from django.shortcuts import render_to_response
from invite.settings import DEBUG
from django.core.context_processors import csrf
from django.core.mail import send_mail
import logging
from appInvite.models import waitingInviteUser, InvitedUser
import hashlib, hmac

logger = logging.getLogger('appInvite.views')
logger.addHandler(logging.StreamHandler())
if DEBUG:
    logger.setLevel(logging.DEBUG)


def writeInvite(request):
    context = {'form': forms.writeInvite()}
    return render_to_response('index.html', context)


def sendInvite(request):
    form = forms.writeInvite(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        name = data['name']
        email = data['email']
        pswd = generatePassword(email)
        waitInvUser = waitingInviteUser(name=name,
                                        email=email,
                                        pswd=pswd
                                        )
        waitInvUser.save()
        msg = u"""ссылка для %s:\n
        http://127.0.0.1:8000/activate/%s """ % (name, pswd)
        send_mail('invite',
                  msg,
                  'invite@invite.com',
                  [email])
        logger.debug('sending invite to %s for %s' % (request.POST['email'], request.POST['name']))
        return render_to_response('sendedInvite.html', request.POST)
    else:
        return render_to_response('index.html', {'form': form})


def generatePassword(msg):
    # можно было бы добавить еще криптографической соли в виде msg = сегодняшняя дата и ссылка действовала только в день
    # посылки инвайта
    return hmac.new(key="testInvite", msg=msg, digestmod=hashlib.sha1).hexdigest()


def activateInvite(request, userpswd):
    wtuser = waitingInviteUser.objects.filter(pswd=userpswd)
    if wtuser:
        invUser = InvitedUser(name=wtuser[0].name,
                              email=wtuser[0].email,
                              pswd=userpswd)
        invUser.save()
        wtuser.delete()
        logger.debug(InvitedUser.objects.all())
        if waitingInviteUser.objects.filter(pswd=userpswd):
            raise Exception('exist')
        form = forms.changePswd({'name': invUser.name,
                                 'email': invUser.email,
                                'newpswd': 'pswd'})

        return render_to_response('activated.html', {'form': form, 'name': invUser.name, 'email': invUser.email})
    errmsg = 'Не правильная ссылка для инвайта.'
    return render_to_response('errormsg.html', {'msg': errmsg})


def newPswd(request):
    invUser = InvitedUser.objects.filter(email=request.POST['email'])[0]
    invUser.pswd = generatePassword(request.POST['newpswd'])  # Вместо пароля сохраняем Хеш-пароля
    invUser.save()
    return render_to_response('chgPass.html',{'name':invUser.name})

def showDebugInfo(request):
    return render_to_response('debug.html',
        {'tables': (waitingInviteUser.objects.all(),
         InvitedUser.objects.all())
        })
