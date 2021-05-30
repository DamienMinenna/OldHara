import os, sys

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

STATUS = (
    (0,"Need revision"),
    (1,"Validated")
)

TYPE = (
    (0,"journal-article"),
    (1,"proceedings-article"),
    (2,"dissertation"),
    (3,"book-chapter"),
    (4,"book"),
    (5,"report"),
    (6,"dataset"),
    (7,"component"),
    (8,"reference-entry"),
    (9,"monograph"),
    (10,"peer-review"),
    (11,"posted-content"),
    (12,"standard"),
    (13,"other"),
    )

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
    type = models.IntegerField(choices = TYPE, default=0)

    db = models.JSONField(null = True)        # Main database for the App
    file = models.FileField(upload_to='toSort/',blank=True) 

    data = models.JSONField(null=True)
    title = models.TextField()
    json_payload = models.TextField(blank = True)

    folder = models.ForeignKey(Path_Biblio, on_delete=models.CASCADE)

    note = models.TextField(blank = True)

    # label = models.ForeignKey(LabelHara, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def getAuthors_list(self):

        if 'message' in self.data:
            if 'author' in  self.data['message']:

                authors = ''
                nb = 0
                for author_i in self.data['message']['author']:
                    authors = authors + str(author_i['family']) + ', ' + str(author_i['given']) + '; '
                    nb = nb + 1

                if nb > 0:
                    return authors[:-2]
                else:
                    return ''

            else:
                return ''
        else:
            return ''

    def getAuthors(self):

        if 'message' in self.data:
            if 'author' in  self.data['message']:

                authors = ''
                nb = 0
                for author_i in self.data['message']['author']:
                    authors = authors + str(author_i['given']) + ' ' + str(author_i['family']) + ', '
                    nb = nb + 1

                if nb > 0:
                    return authors[:-2]
                else:
                    return ''

            else:
                return ''
        else:
            return ''

    def getTitle(self):
        if 'message' in self.data:
            if 'title' in  self.data['message']:
                return str(self.data['message']['title'][0])
            else:
                return ''
        else:
            return ''

    def getDate(self):
        if 'message' in self.data:
            if 'issued' in  self.data['message']:
                if 'date-parts' in  self.data['message']['issued']:
                    return str(self.data['message']['issued']['date-parts'][0][0])
                else:
                    return ''
            else:
                return ''
        else:
            return ''

    def getJournal(self):
        if 'message' in self.data:
            if 'container-title' in  self.data['message']:
                return str(self.data['message']['container-title'][0])
            else:
                return ''
        else:
            return ''

    def getVolume(self):
        if 'message' in self.data:
            if 'volume' in  self.data['message']:
                return str(self.data['message']['volume'])
            else:
                return ''
        else:
            return ''

    def getPage(self):
        if 'message' in self.data:
            if 'page' in  self.data['message']:
                return str(self.data['message']['page'])
            else:
                return ''
        else:
            return ''

    def getArticleNumber(self):
        if 'message' in self.data:
            if 'article-number' in  self.data['message']:
                return str(self.data['message']['article-number'])
            else:
                return ''
        else:
            return ''

    def getIssue(self):
        if 'message' in self.data:
            if 'issue' in  self.data['message']:
                return str(self.data['message']['issue'])
            else:
                return ''
        else:
            return ''

    def getDOI(self):
        if 'message' in self.data:
            if 'DOI' in  self.data['message']:
                return str(self.data['message']['DOI'].lower())
            else:
                return ''
        else:
            return ''

    def getType(self):
        if 'message' in self.data:
            if 'type' in  self.data['message']:
                return str(self.data['message']['type'])
            else:
                return ''
        else:
            return ''
