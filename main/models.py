from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin, Group
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.hashers import make_password
from django.templatetags.static import static
from django.conf import settings
from django.urls import reverse
from urllib.request import urlopen
from datetime import datetime
from bs4 import BeautifulSoup
from django.db import models
import os
import mimetypes


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class PageTextMixin(models.Model):
    json_text = models.JSONField(verbose_name='Текст сторінкт у JSON форматі')
    html_text = models.TextField(verbose_name='Текст сторінкт у HTML форматі')

    def clear_page(self) -> None:
        '''Clears page from data uri (url)'''

        root = settings.MEDIA_ROOT / 'image'
        url = settings.MEDIA_URL + 'image/'

        assert type(self.json_text) is dict and self.json_text.get(
            'ops'), 'Value error'
        for action in self.json_text['ops']:
            insert = action.get('insert')

            if type(insert) is dict and insert.get('image') and insert['image'].startswith('data:'):
                data_uri = insert['image']
                files = os.listdir(root)

                if files:
                    files.sort(key=lambda f: int(f.split('.')[0]))
                    num_file = str(int(files[-1].split('.')[0]) + 1)
                else:
                    num_file = '1'

                extension = mimetypes.guess_extension(data_uri.split(';')[0][5:])
                file_name = num_file + extension
                response = urlopen(data_uri)

                with open(root / file_name, 'wb') as f:
                    f.write(response.file.read())
                insert['image'] = url + file_name

                for act in self.json_text['ops']:
                    insert = act.get('insert')
                    if type(insert) is dict and insert.get('image') and insert['image'] == data_uri:
                        insert['image'] = url + file_name

                self.html_text = self.html_text.replace(data_uri, url + file_name)

    class Meta:
        abstract = True


class User(AbstractBaseUser, PermissionsMixin):
    gender_choices = [('man', 'Чоловік'), ('woman', 'Жінка')]

    email = models.EmailField(verbose_name='Email', unique=True)
    first_name = models.CharField(verbose_name='Ім’я', max_length=100)
    last_name = models.CharField(verbose_name='Фамілія', max_length=100)
    gender = models.CharField(verbose_name='Стать', max_length=50, choices=gender_choices, default='man')
    is_active = models.BooleanField(verbose_name='Активний користувач', default=True)
    is_staff = models.BooleanField(verbose_name='Персонал', default=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    objects = CustomUserManager()

    class Meta:
        ordering = ['-last_login']
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        try:
            staff_group = Group.objects.get(name='Персонал (перегляд даних)')
            if not self.is_superuser and self.is_staff and staff_group not in self.groups.all():
                self.groups.add(staff_group)
        except Group.DoesNotExist:
            pass
        except Group.MultipleObjectsReturned:
            pass

    def __str__(self) -> str:
        return f'Користувач {self.first_name} {self.last_name} ({self.email})'


class Section(PageTextMixin, models.Model):
    type_choices = [
        ('science', 'Науково-технічний'),
        ('humanitarian', 'Гуманітарний'),
        ('touristic', 'Туристсько-краєзнавчий'),
        ('sport', 'Фізкультурно-спортивний'),
        ('artistic', 'Художньо-естетичний'),
        ('patriotic', 'Військово-патріотичний'),
        ('social', 'Соціально-реабілітаційний'),
    ]
    department_choices = [
        ('it', 'Відділ інформаційно-методичного супроводу'),
        ('decor', 'Відділ декоративно-прикладної творчості'),
        ('sport', 'Відділ туризму, спорту та фізичного розвитку'),
        ('art', 'Відділ художньо-естетичного виховання'),
        ('mass', 'Організаційно-масовий відділ'),
    ]

    name = models.CharField(verbose_name='Назва гуртка', max_length=100, unique=True)
    preview_text = models.CharField(verbose_name='Коротки опис', max_length=600)
    record_link = models.CharField(verbose_name='Посилання на запис', max_length=500, blank=True)
    banner = models.ImageField(verbose_name='Зображення', upload_to='section/', blank=True)
    type = models.CharField(verbose_name='Тип', max_length=50, choices=type_choices, default='science')
    department = models.CharField(verbose_name='Відділ', max_length=50, choices=department_choices, default='decor')
    direction = models.ManyToManyField('main.Direction', verbose_name='Напрямок', blank=True)
    min_age = models.IntegerField(verbose_name='Мінімальний вік', validators=[MinValueValidator(1)], default=1)
    max_age = models.IntegerField(verbose_name='Максимальний вік', validators=[MaxValueValidator(99)], default=18)
    is_published = models.BooleanField(verbose_name='Опубліковано', default=False)
    is_active_record = models.BooleanField(verbose_name='Запис на гурток', default=False)
    date_of_last_change = models.DateTimeField(verbose_name='Час останньої зміни', auto_now=True)

    schedule_for_monday = models.CharField('Розклад на понеділок', max_length=250, blank=True)
    schedule_for_tuesday = models.CharField('Розклад на вівторок', max_length=250, blank=True)
    schedule_for_wednesday = models.CharField('Розклад на середу', max_length=250, blank=True)
    schedule_for_thursday = models.CharField('Розклад на четвер', max_length=250, blank=True)
    schedule_for_friday = models.CharField('Розклад на пʼятницю', max_length=250, blank=True)
    schedule_for_saturday = models.CharField('Розклад на суботу', max_length=250, blank=True)
    schedule_for_sunday = models.CharField('Розклад на неділю', max_length=250, blank=True)

    class Meta:
        ordering = ['-date_of_last_change']
        verbose_name = 'Гурток'
        verbose_name_plural = 'Гуртки'

    def __str__(self) -> str:
        return f'Гурток {self.name}'

    def save(self, *args, **kwargs):
        self.clear_page()
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse('section', kwargs={'pk': self.pk})


class News(PageTextMixin, models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=150)
    is_published = models.BooleanField(verbose_name='Опубліковано', default=False)
    date_of_published = models.DateTimeField(verbose_name='Час публікації', blank=True, null=True)
    date_of_last_change = models.DateTimeField(verbose_name='Час останньої зміни', auto_now=True)

    class Meta:
        ordering = ['-date_of_published']
        verbose_name = 'Новина'
        verbose_name_plural = 'Новини'

    def __str__(self) -> str:
        return f'Новина - {self.title}'

    def save(self, *args, _disable_check: bool = False, **kwargs):
        self.clear_page()

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
            if element.name is None:
                continue
            elif element.name != 'p':
                result += f'<p>{element}</p>'
            else:
                result += str(element)
            i += 1
        return result

    @property
    def preview_image(self) -> str:
        soup = BeautifulSoup(self.html_text, 'html.parser')
        img = soup.find('img')
        return img['src'] if img else static('image/ognews.jpg')


class Article(PageTextMixin, models.Model):
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

    name = models.CharField(verbose_name='Назва', help_text='Має вищий пріорітет над заголовком в навігації', max_length=100)
    title = models.CharField(verbose_name='Заголовок', help_text='Має вищий пріорітет над назвою в статті', max_length=100, blank=True)
    type = models.CharField(verbose_name='Тип', max_length=50, choices=type_choices)
    document = models.FileField(verbose_name='Документ', upload_to='documents', blank=True)
    is_published = models.BooleanField(verbose_name='Опубліковано', default=False)
    date_of_last_change = models.DateTimeField(verbose_name='Час останньої зміни', auto_now=True)

    class Meta:
        ordering = ['-date_of_last_change']
        verbose_name = 'Стаття'
        verbose_name_plural = 'Статті'

    def __str__(self) -> str:
        return f'Стаття (тип: {self.get_type_display()}) {self.title}'

    def save(self, *args, **kwargs):
        self.clear_page()
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse('article', kwargs={'pk': self.pk})


class Banner(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=150, unique=True)
    link = models.CharField(verbose_name='Посилання', help_text='Посилання для кнопки "Детальніше"', max_length=500, blank=True)
    background = models.ImageField(verbose_name='Зображення', upload_to='background/', blank=True)
    show_link = models.BooleanField(verbose_name='Показати посилання', default=False)
    is_published = models.BooleanField(verbose_name='Показати баннер (опублікувати)', default=False)
    created_at = models.DateTimeField(verbose_name='Дата створення', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннери'

    def __str__(self) -> str:
        return f'Баннер {self.title}'


class Direction(models.Model):
    name = models.CharField(verbose_name='Назва напрямку', max_length=30, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Напрямок'
        verbose_name_plural = 'Напрямки'

    def __str__(self) -> str:
        return f'Напрямок {self.name}'
