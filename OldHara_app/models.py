from django.db import models
"""
Contains OldHara models
"""

TYPE_REF = ["book-section",
            "monograph",
            "report",
            "peer-review",
            "book-track",
            "journal-article",
            "book-part",
            "other",
            "book",
            "journal-volume",
            "book-set",
            "reference-entry",
            "proceedings-article",
            "journal",
            "component",
            "book-chapter",
            "proceedings-series",
            "report-series",
            "proceedings",
            "standard",
            "reference-book",
            "posted-content",
            "journal-issue",
            "dissertation",
            "grant",
            "dataset",
            "book-series",
            "edited-book",
            "standard-series"]


STATUS_REF = (
    (0,"Validated"),
    (1,"Action needed")
)

class Folder_Refs(models.Model):
    """
    Model for the folders
    """
    path = models.CharField(max_length=5000, unique=True)

    def __str__(self):
        return self.path


class Ref(models.Model):
    """
    Main database model of the refs
    """
    created_on = models.DateTimeField(auto_now_add=True) # Creation date

    status = models.IntegerField(choices = STATUS_REF, default=0) # Status

    title = models.TextField() # Title

    doi = models.TextField(blank = True) # DOI

    data = models.JSONField(null = True) # Main data of the ref used and modified by the App

    data_text = models.TextField(blank = True) # Text version of the data for JS.

    file = models.FileField(upload_to='toSort/',blank=True) # File

    folder = models.ForeignKey(Folder_Refs, on_delete=models.CASCADE) # File location

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title