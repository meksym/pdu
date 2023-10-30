from django import forms
from common import utils
from . import models


class NewsAdminForm(forms.ModelForm):
    @utils.wysiwyg('Meta')
    class Meta:
        model = models.News
        exclude = ['created_at', 'changed_at', 'date_of_published']

    @utils.wysiwyg('Media')
    class Media:
        pass
