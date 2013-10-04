"""
    Appswell SimpleLog Model and ModelForm Examples

    Note:
    Per docs, you must import google.appengine.webapp.template before importing
    any Django modules

    References:
    http://code.google.com/appengine/articles/djangoforms.html
"""

# must import google.appengine.ext.webapp.template for django newforms
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from google.appengine.ext import db
from google.appengine.ext.db import djangoforms

AppswellSimpleLogTypes = [
    'system',
    'error',
    'warning',
    'info',
    'debug'
]

class AppswellSimpleLog(db.Model):

    # Model Fields
    type        = db.StringProperty(default='debug',
                    choices=AppswellSimpleLogTypes)
    keyword     = db.StringProperty(multiline=False)
    message     = db.StringProperty(multiline=False)
    created     = db.DateTimeProperty(auto_now_add=True)

    # log
    def log(self, keyword, message, type='debug'):
        self.keyword = keyword
        self.message = message
        self.type = type
        return self.put()

    # alias for save/put
    def autosave(self):
        return self.put()

    @staticmethod
    def find_last_n(n=5):
        RecordList = []
        Query = AppswellSimpleLog.gql('ORDER BY created DESC LIMIT %s' % (n))
        for r in Query:
            r.key = r.key()
            RecordList.append((r.key, str(r.created), r.url, r.note))
        return RecordList


class AppswellSimpleLogModelForm(djangoforms.ModelForm):
    """
        ModelForm for AppswellSimpleLog above.  Notice how the constructor
        is overridden to change the widget (html output) for the note field
    """
    class Meta:
        model = AppswellSimpleLog
        fields = ('type', 'keyword', 'message')

    def __init__(self, *args, **kwargs):
        """
            Use constructor to override widget details, like form type or
            label.  Examples:

            self.fields['message'].widget = forms.Textarea(
                attrs={ 'class':'appswell_textarea', 'rows':4, 'cols':40 } )
        """
        super(AppswellSimpleModelForm, self).__init__(*args, **kwargs)

        # override labels
        self.fields['message'].label = 'log message'
