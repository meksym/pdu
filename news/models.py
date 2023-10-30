from django.templatetags.static import static
from django.urls import reverse
from datetime import datetime
from bs4 import BeautifulSoup
from django.db import models
from common import utils


class News(utils.InformationMixin):
    title = models.CharField(
        verbose_name='Заголовок',
        max_length=150
    )

    date_of_published = models.DateTimeField(
        verbose_name='Дата публікації',
        null=True
    )
    is_published = models.BooleanField(
        verbose_name='Опубліковано',
        default=False
    )

    class Meta:
        ordering = ['-changed_at', '-created_at']
        verbose_name = 'Новина'
        verbose_name_plural = 'Новини'

    def __str__(self) -> str:
        return 'Новина' + self.title

    def save(self, *args, _disable_check: bool = False, **kwargs):
        if not _disable_check:
            if self.is_published and not self.date_of_published:
                self.date_of_published = datetime.now()
            elif not self.is_published and self.date_of_published:
                self.date_of_published = None

        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse('one_news', kwargs={'pk': self.pk})

    @property
    def preview_html(self) -> str:
        soup = BeautifulSoup(self.html_text, 'html.parser')
        result = ''
        i = 0

        for element in soup.contents:
            if i == 2:
                break
            if element.name is None:  # type: ignore
                continue
            elif element.name != 'p':  # type: ignore
                result += f'<p>{element}</p>'
            else:
                result += str(element)
            i += 1

        return result

    @property
    def preview_image(self):
        default = 'image/ognews.jpg'
        soup = BeautifulSoup(self.html_text, 'html.parser')
        img = soup.find('img')

        return img['src'] if img else static(default)  # type: ignore
