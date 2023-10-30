from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.db import models
from common import utils


class Section(utils.InformationMixin):
    type_choices = (
        ('science', 'Науково-технічний'),
        ('humanitarian', 'Гуманітарний'),
        ('touristic', 'Туристсько-краєзнавчий'),
        ('sport', 'Фізкультурно-спортивний'),
        ('artistic', 'Художньо-естетичний'),
        ('patriotic', 'Військово-патріотичний'),
        ('social', 'Соціально-реабілітаційний')
    )
    department_choices = (
        ('it', 'Відділ інформаційно-методичного супроводу'),
        ('decor', 'Відділ декоративно-прикладної творчості'),
        ('sport', 'Відділ туризму, спорту та фізичного розвитку'),
        ('art', 'Відділ художньо-естетичного виховання'),
        ('mass', 'Організаційно-масовий відділ'),
    )

    name = models.CharField(
        verbose_name='Назва гуртка',
        max_length=100,
        unique=True
    )
    preview_text = models.CharField(
        verbose_name='Коротки опис',
        max_length=600
    )

    banner = models.ImageField(
        verbose_name='Зображення',
        upload_to='section/',
        blank=True
    )

    type = models.CharField(
        verbose_name='Тип',
        max_length=250,
        choices=type_choices,
        default='science'
    )
    department = models.CharField(
        verbose_name='Відділ',
        max_length=250,
        choices=department_choices,
        default='decor'
    )

    direction = models.ManyToManyField(
        'section.Direction',
        verbose_name='Напрямок',
        blank=True
    )

    min_age = models.IntegerField(
        verbose_name='Мінімальний вік',
        validators=[MinValueValidator(1)],
        default=1
    )
    max_age = models.IntegerField(
        verbose_name='Максимальний вік',
        validators=[MaxValueValidator(99)],
        default=18
    )

    record_link = models.CharField(
        verbose_name='Посилання на запис',
        max_length=2000,
        blank=True,
        null=True
    )
    is_active_record = models.BooleanField(
        verbose_name='Запис на гурток',
        help_text='',
        default=False
    )

    is_published = models.BooleanField(
        verbose_name='Опубліковано',
        help_text='',
        default=False
    )

    schedule_for_monday = models.TextField('Розклад на понеділок', blank=True)
    schedule_for_tuesday = models.TextField('Розклад на вівторок', blank=True)
    schedule_for_wednesday = models.TextField('Розклад на середу', blank=True)
    schedule_for_thursday = models.TextField('Розклад на четвер', blank=True)
    schedule_for_friday = models.TextField('Розклад на пʼятницю', blank=True)
    schedule_for_saturday = models.TextField('Розклад на суботу', blank=True)
    schedule_for_sunday = models.TextField('Розклад на неділю', blank=True)

    class Meta:
        ordering = ['-changed_at', '-created_at']
        verbose_name = 'Гурток'
        verbose_name_plural = 'Гуртки'

    def __str__(self):
        return 'Гурток ' + self.name

    def get_absolute_url(self):
        return reverse('section', kwargs={'pk': self.pk})


class Direction(models.Model):
    name = models.CharField(
        verbose_name='Назва напрямку',
        help_text='Використовуеться на сторінці з фільтром гуртків',
        max_length=30,
        unique=True
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Напрямок'
        verbose_name_plural = 'Напрямки'

    def __str__(self) -> str:
        return 'Напрямок' + self.name
