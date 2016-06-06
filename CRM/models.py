from __future__ import unicode_literals

from django.db import models

'''
this file contains all the django models i.e the sqlite DB tables and their fields.
'''

class Admin(models.Model):
    username = models.CharField(max_length=80)
    password = models.CharField(max_length=30)
    class Meta:
        db_table = 'Admin'

class User(models.Model):
    name = models.CharField(max_length=80)
    email = models.CharField(primary_key=True, max_length=50)
    phnno = models.CharField(db_column='phnNo', max_length=10)  # Field name made lowercase.

    class Meta:
        db_table = 'User'

class Categories(models.Model):
    category = models.CharField(primary_key=True,max_length=40,default='Top News')
    link = models.CharField(max_length=140,null=False)

    class Meta:
        db_table = 'Categories'

class Subscription(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Subscription'
