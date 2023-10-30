from django.forms import ModelForm
from common import utils
from . import models


class ArticleAdminForm(ModelForm):
    @utils.wysiwyg('Meta')
    class Meta:
        model = models.Article
        exclude = ['created_at', 'changed_at']

    @utils.wysiwyg('Media')
    class Media:
        pass
