from django.urls import reverse
from django.db import models
from common import utils


class Article(utils.InformationMixin):
    type_choices = [
        ('document', 'Документ'),
        ('other', 'Інше'),

        ('about', 'Про заклад'),
        ('education', 'Освітній процес'),
        ('public_information', 'Публічна інформація'),
        ('teacher_certification', 'Атестація педагогічних працівників'),
        ('budget', 'Кошторис'),
        ('finance_report', 'Звіт про надходження та використання коштів'),
        ('annual_report', 'Річний звіт про діяльність Палацу'),
        ('bullying', 'СТОП булінг'),
    ]

    type = models.CharField(
        verbose_name='Тип',
        max_length=50,
        choices=type_choices
    )

    name = models.CharField(
        verbose_name='Назва',
        help_text='Має вищий пріорітет над заголовком в навігації',
        max_length=100
    )
    title = models.CharField(
        verbose_name='Заголовок',
        help_text='Має вищий пріорітет над назвою в статті',
        max_length=100,
        blank=True
    )

    is_published = models.BooleanField(
        verbose_name='Опубліковано',
        default=False
    )

    order_number = models.IntegerField(
        verbose_name='Число сортування',
        help_text=(
            'Число, яке використовується для того, щоб '
            'визначити порядок відображення елементів. '
            'Чим більше, тии вище пріорітет відображення.'
        ),
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['-order_number', '-changed_at', '-created_at']
        verbose_name = 'Стаття'
        verbose_name_plural = 'Статті'

    def __str__(self):
        return self.title or self.name

    def get_absolute_url(self):
        return reverse('article', kwargs={'pk': self.pk})


class ArticleFile(models.Model):
    name = models.CharField('Назва', max_length=50, blank=True, null=True)
    file = models.FileField(
        verbose_name='Файл',
        upload_to='documents',
        help_text=(
            'Ім\'я файлу має складатися ЛИШЕ з літер англійського '
            'алфавіту, цифр та символа підкреслення'
        ),
        max_length=500
    )
    article = models.ForeignKey(
        'general.Article',
        verbose_name='Стаття',
        help_text='Стаття, до котрої буде відноситись файл',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файли'

    @property
    def file_name(self) -> str:
        return self.file.name.split('/')[-1]


class Banner(utils.DatesMinix):
    title = models.CharField(
        verbose_name='Заголовок',
        max_length=150,
    )
    link = models.CharField(
        verbose_name='Посилання',
        help_text=(
            'Якщо вказати посилання, в банері з\'явиться '
            'кнопка "Детальніше", яка буде вести на це посилання.'
        ),
        max_length=500,
        blank=True
    )
    background = models.ImageField(
        verbose_name='Зображення',
        upload_to='background/',
        blank=True
    )

    is_published = models.BooleanField(
        verbose_name='Показувати баннер',
        default=False
    )

    order_number = models.IntegerField(
        verbose_name='Число сортування',
        help_text=(
            'Число, яке використовується для того, щоб '
            'визначити порядок відображення елементів. '
            'Чим більше, тии вище пріорітет відображення.'
        ),
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['-order_number', '-changed_at', '-created_at']
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннери'

    def __str__(self) -> str:
        return 'Баннер' + self.title
