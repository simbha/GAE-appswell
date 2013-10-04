"""
    Model and ModelForm Examples
"""
#
# IMPORTS
#
from google.appengine.ext import db
from google.appengine.ext.db import djangoforms
from django import forms



#
# CLASSES
#
class AppswellSimpleForm(db.Model):

    # Model Fields
    url = db.LinkProperty(required=True)
    note = db.StringProperty(multiline=True)
    created = db.DateTimeProperty(auto_now_add=True)

    # alias for save/put
    def autosave(self):
        self.put()

    @staticmethod
    def find_last_n(n=5):
        RecordList = []
        Query = AppswellSimpleForm.gql('ORDER BY created DESC LIMIT %s' % (n))
        for r in Query:
            r.key = r.key()
            RecordList.append((r.key, str(r.created), r.url, r.note))
        return RecordList


class AppswellSimpleModelForm(djangoforms.ModelForm):
    """
        ModelForm for AppswellSimpleForm above.  Notice how the constructor
        is overridden to change the widget (html output) for the note field

        For usage, see http://goo.gl/tergq.
    """
    class Meta:
        model = AppswellSimpleForm
        fields = ('url', 'note')

    def __init__(self, *args, **kwargs):
        """We reset the widget for the note field to add a class attribute
        to the tag."""
        super(AppswellSimpleModelForm, self).__init__(*args, **kwargs)
        self.fields['note'].widget = forms.Textarea(
            attrs={ 'class':'appswell_textarea', 'rows':4, 'cols':40 } )

        # override labels
        self.fields['note'].label = 'why you like it (optional)'
        self.fields['url'].label = 'link (include http://)'


__all__ = [ AppswellSimpleForm, AppswellSimpleModelForm ]
