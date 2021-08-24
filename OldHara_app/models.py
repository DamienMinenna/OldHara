import os, sys

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

STATUS = (
    (0,"Validated"),
    (1,"Missing DOI"),
    (2,"No DOI")
)

# TYPE = (
#     (0,"journal-article"),
#     (1,"proceedings-article"),
#     (2,"dissertation"),
#     (3,"book-chapter"),
#     (4,"book"),
#     (5,"report"),
#     (6,"dataset"),
#     (7,"component"),
#     (8,"reference-entry"),
#     (9,"monograph"),
#     (10,"peer-review"),
#     (11,"posted-content"),
#     (12,"standard"),
#     (13,"other"),
#     )

# TYPE_LIST = [ 
#     'journal-article', 
#     'proceedings-article',
#     'dissertation',
#     'book-chapter',
#     'book',
#     'report',
#     'dataset',
#     'component',
#     'reference-entry',
#     'monograph',
#     'peer-review',
#     'posted-content',
#     'standard',
#     'other',    
#     ]

class Path_Biblio(models.Model):
    path = models.CharField(max_length=1000, unique=True)

    def __str__(self):
        return self.path

class FileStore(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    folder = models.ForeignKey(Path_Biblio, on_delete=models.CASCADE)
    file = models.FileField(upload_to = 'toSort/',blank=True)

    def __str__(self):
        return self.created_on

class LabelHara(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Biblio(models.Model):
    # slug = models.SlugField(max_length=200, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices = STATUS, default=0)
    title = models.TextField()

    doi = models.TextField(blank = True)

    # To delete!
    #type = models.IntegerField(choices = TYPE, default=0)

    db_CrossRef = models.JSONField(null = True)        # Main database for the App

    db = models.JSONField(null = True)        # Main database for the App

    # to del
    #data = models.JSONField(null = True)        # Main database for the App


    db_text = models.TextField(blank = True)

    file = models.FileField(upload_to='toSort/',blank=True) 

    folder = models.ForeignKey(Path_Biblio, on_delete=models.CASCADE)

    note = models.TextField(blank = True)

    # label = models.ForeignKey(LabelHara, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
