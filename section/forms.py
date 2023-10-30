from django import forms
from common import utils
from . import models


class SectionAdminForm(forms.ModelForm):
    @utils.wysiwyg('Meta')
    class Meta:
        model = models.Section
        exclude = ['changed_at', 'created_at']
        widgets = {
            'preview_text': forms.Textarea(attrs={'cols': 80, 'rows': 10})
        }

    @utils.wysiwyg('Media')
    class Media:
        pass

    def clean(self) -> None:
        if (
            not self.cleaned_data.get('min_age') or
            not self.cleaned_data.get('max_age')
        ):
            raise forms.ValidationError(
                'Необхідно ввести мінімальний та максимальний вік'
            )
        elif self.cleaned_data['min_age'] > self.cleaned_data['max_age']:
            raise forms.ValidationError(
                'Мінімальний вік не може бути більшим за максимальний'
            )
