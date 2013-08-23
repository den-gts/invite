# -*-coding: utf-8 -*-
from django.db import models


class waitingInviteUser(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    pswd = models.CharField(max_length=40)


class InvitedUser(models.Model):  # наследование почему то привело к тому,
                                  # что действия над одной таблицей осуществлялись и в другой:(
    name = models.CharField(max_length=20)
    email = models.EmailField()
    pswd = models.CharField(max_length=40)

