from django.db import models
"""
Contains OldHara models
"""
MONTH_WORD = [('0', ''), 
            ('1', 'January'),
            ('2', 'February'), 
            ('3', 'March'),
            ('4', 'April'), 
            ('5', 'May'),
            ('6', 'June'), 
            ('7', 'August'),
            ('8', 'July'), 
            ('9', 'September'),
            ('10', 'October'), 
            ('11', 'November'), 
            ('12', 'December')]


TYPE_REF = [('0', "book-section"),
            ('1', "monograph"),
            ('2', "report"),
            ('3', "peer-review"),
            ('4', "book-track"),
            ('5', "journal-article"),
            ('6', "book-part"),
            ('7', "other"),
            ('8', "book"),
            ('9', "journal-volume"),
            ('10', "book-set"),
            ('11', "reference-entry"),
            ('12', "proceedings-article"),
            ('13', "journal"),
            ('14', "component"),
            ('15', "book-chapter"),
            ('16', "proceedings-series"),
            ('17', "report-series"),
            ('18', "proceedings"),
            ('19', "standard"),
            ('20', "reference-book"),
            ('21', "posted-content"),
            ('22', "journal-issue"),
            ('23', "dissertation"),
            ('24', "grant"),
            ('25', "dataset"),
            ('26', "book-series"),
            ('27', "edited-book"),
            ('28', "standard-series")]


# ["book-section",
#             "monograph",
#             "report",
#             "peer-review",
#             "book-track",
#             "journal-article",
#             "book-part",
#             "other",
#             "book",
#             "journal-volume",
#             "book-set",
#             "reference-entry",
#             "proceedings-article",
#             "journal",
#             "component",
#             "book-chapter",
#             "proceedings-series",
#             "report-series",
#             "proceedings",
#             "standard",
#             "reference-book",
#             "posted-content",
#             "journal-issue",
#             "dissertation",
#             "grant",
#             "dataset",
#             "book-series",
#             "edited-book",
#             "standard-series"]

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

    file = models.FileField(upload_to='unsorted/',blank=True) # File

    folder = models.ForeignKey(Folder_Refs, on_delete=models.CASCADE) # File location

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title