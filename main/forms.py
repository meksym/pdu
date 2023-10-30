from django.forms import ModelForm, Textarea, HiddenInput, ValidationError
from .models import Section, News, Article


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


class SectionAdminForm(ModelForm):
    @wysiwyg('Meta')
    class Meta:
        model = Section
        exclude = ['date_of_last_change']
        widgets = {'preview_text': Textarea(attrs={'cols': 80, 'rows': 10})}

    @wysiwyg('Media')
    class Media:
        pass

    def clean(self) -> None:
        if not self.cleaned_data.get('min_age') or not self.cleaned_data.get('max_age'):
            raise ValidationError(
                'Необхідно ввести мінімальний та максимальний вік'
            )
        elif self.cleaned_data['min_age'] > self.cleaned_data['max_age']:
            raise ValidationError(
                'Мінімальний вік не може бути більшим за максимальний'
            )


class NewsAdminForm(ModelForm):
    @wysiwyg('Meta')
    class Meta:
        model = News
        exclude = ['date_of_last_change', 'date_of_published']

    @wysiwyg('Media')
    class Media:
        pass


class ArticleAdminForm(ModelForm):
    @wysiwyg('Meta')
    class Meta:
        model = Article
        exclude = ['date_of_last_change']

    @wysiwyg('Media')
    class Media:
        pass
