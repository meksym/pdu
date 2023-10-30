from mimetypes import guess_extension
from django.forms import HiddenInput
from urllib.request import urlopen
from django.conf import settings
from django.db import models
import os


class DatesMinix(models.Model):
    changed_at = models.DateTimeField(
        verbose_name='Час останньої зміни',
        auto_now=True
    )
    created_at = models.DateTimeField(
        verbose_name='Час створення',
        auto_now_add=True
    )

    class Meta:
        abstract = True


class InformationMixin(DatesMinix):
    json_text = models.JSONField(verbose_name='Текст сторінки у JSON форматі')
    html_text = models.TextField(verbose_name='Текст сторінки у HTML форматі')

    def clear_page(self) -> None:
        '''Clears page from data uri (url)'''

        root = settings.MEDIA_ROOT / 'image'
        url = settings.MEDIA_URL + 'image/'

        for action in self.json_text['ops']:
            insert = action.get('insert')

            if (
                type(insert) is dict and
                insert.get('image') and
                insert['image'].startswith('data:')
            ):
                data_uri = insert['image']
                files = os.listdir(root)

                if files:
                    files.sort(key=lambda f: int(f.split('.')[0]))
                    num_file = str(int(files[-1].split('.')[0]) + 1)
                else:
                    num_file = '1'

                extension = guess_extension(data_uri.split(';')[0][5:]) or ''
                file_name = num_file + extension
                response = urlopen(data_uri)

                with open(root / file_name, 'wb') as f:
                    f.write(response.file.read())
                insert['image'] = url + file_name

                for act in self.json_text['ops']:
                    insert = act.get('insert')

                    if (
                        type(insert) is dict and
                        insert.get('image') and
                        insert['image'] == data_uri
                    ):
                        insert['image'] = url + file_name

                self.html_text = self.html_text.replace(
                    data_uri,
                    url + file_name
                )

    def save(self, *args, **kwargs):
        self.clear_page()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


def wysiwyg(cls_name: str):
    '''Add data for WYSIWYG (Rich page text editor)'''

    def decorator(cls):
        wysiwyg_widgets = {
            'json_text': HiddenInput(),
            'html_text': HiddenInput(),
        }
        wysiwyg_js = [
            'js/quill.min.js',
            'js/wysiwyg.js'
        ]
        wysiwyg_css = [
            'css/quill.core.css',
            'css/quill.snow.css',
            'css/quill.bubble.css',
        ]

        class Result(cls):
            if cls_name == 'Meta':
                widgets = getattr(cls, 'widgets', {})
                widgets.update(wysiwyg_widgets)
            elif cls_name == 'Media':
                js = getattr(cls, 'js', [])
                js = list(js) + wysiwyg_js
                css = getattr(cls, 'css', {})
                css['all'] = list(css.get('all', [])) + wysiwyg_css
            else:
                raise ValueError

        return Result

    return decorator
