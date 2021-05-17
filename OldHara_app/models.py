import os, sys

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

STATUS = (
    (0,"Need revision"),
    (1,"Validated")
)

TYPE = (
    (0,"Book"),
    (1,"Book Section"),
    (2,"Conference Proceedings"),
    (3,"Journal Article"),
    (4,"Magazine Article"),
    (5,"Newspaper Article"),
    (6,"Report"),
    (7,"Thesis"),
    (8,"Web page"),
    (9,"Other"),
)


class Path_Biblio(models.Model):
    path = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.path

class Biblio(models.Model):
    # slug = models.SlugField(max_length=200, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    type = models.IntegerField(choices=TYPE, default=0)

    data = models.JSONField(null=True)
    title = models.TextField()
    json_payload = models.TextField(blank=True)

    folder = models.ForeignKey(Path_Biblio, on_delete=models.CASCADE)


    # authors = models.TextField(blank=True) # A modifier
    # journal = models.TextField(blank=True)
    # journalAbbr = models.TextField(blank=True)
    # volume = models.TextField(blank=True)
    # pages = models.TextField(blank=True)
    # date = models.TextField(blank=True)
    doi = models.TextField(blank=True)
    url = models.URLField(blank=True)

    # language = models.TextField(blank=True)
    keyword = models.TextField(blank=True)
    abstract = models.TextField(blank=True)

    mainFile = models.FileField(upload_to='toSort/',blank=True)

    # os.rename(model.mainFile.path, new_path)
    # model.mainFile.name = new_name
    # model.save()



    # mainFilename = models.CharField(max_length=1000,blank=True)

    note = models.TextField(blank=True)

    label = models.TextField(blank=True) # A modifier

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
