from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email or len(email) <= 0:
            raise ValueError('Email field is required !')
        if not password:
            raise ValueError('Password is must !')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser):
    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'

    class Types(models.TextChoices):
        CLIENT = "CLIENT", 'client'
        EMPLOYEE = "EMPLOYEE", 'employee'

    type = models.CharField(
                max_length=8,
                choices=Types.choices,
                default=Types.CLIENT
    )
    email = models.EmailField(
                max_length=100,
                unique=True
    )
    is_active = models.BooleanField(
                default=True
    )
    is_admin = models.BooleanField(
                default=False
    )
    is_staff = models.BooleanField(
                default=False)
    is_superuser = models.BooleanField(
                default=False
    )
    is_client = models.BooleanField(
                default=False
    )
    is_employee = models.BooleanField(
                default=False
    )

    USERNAME_FIELD = 'email'

    objects = UserAccountManager()

    def __str__(self):
        return str(self.email)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        if not self.type or self.type == None:
            self.type = UserAccount.Types.CLIENT
        return super().save(*args, **kwargs)


class ClientManager(models.Manager):
    def create_user(self, email, password=None):
        if not email or len(email) <= 0:
            raise ValueError('Email field is required !')
        if not password:
            raise ValueError('Password is must !')
        email = email.lower()
        user = self.model(
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(type=UserAccount.Types.CLIENT)
        return queryset


class Client(UserAccount):
    class Meta:
        proxy = True
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    objects = ClientManager()

    def save(self, *args, **kwargs):
        self.type = UserAccount.Types.CLIENT
        self.is_client = True
        return super().save(*args, **kwargs)


class EmployeeManager(models.Manager):
    def create_user(self, email, password=None):
        if not email or len(email) <= 0:
            raise ValueError('Email field is required !')
        if not password:
            raise ValueError('Password is must !')

        email = email.lower()
        user = self.model(
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(type=UserAccount.Types.EMPLOYEE)
        return queryset


class Employee(UserAccount):
    class Meta:
        proxy = True
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    objects = EmployeeManager()

    def save(self, *args, **kwargs):
        self.type = UserAccount.Types.EMPLOYEE
        self.is_employee = True
        return super().save(*args, **kwargs)


class MinResolutionErrorException(Exception):
    pass


class MaxResolutionErrorException(Exception):
    pass


class ProfileEmployee(models.Model):
    class Meta:
        verbose_name = 'Профиль Сотрудника'
        verbose_name_plural = 'Профиль Сотрудника'

    MAX_RESOLUTION = (800, 800)
    MIN_RESOLUTION = (400, 400)
    MAX_IMAGE_SIZE = 3145728

    name = models.CharField(
                max_length=100,
                verbose_name='Имя'
    )
    user = models.OneToOneField(
                Employee,
                on_delete=models.CASCADE,
                verbose_name='Сотрудник'
    )
    description = models.TextField(
                verbose_name='Описание'
    )
    image = models.ImageField(
                verbose_name='Ваша фотография с собакой'
    )
    content = models.TextField(
                verbose_name='Опишите себя'
    )
    achievements = models.TextField(
                verbose_name='Ваши достижения|необязательно'
    )

    def __str__(self):
        return f"Сотрудник {self.user}"


class Schedule(models.Model):

    SCHEDULE_DEFAULT = ("Понедельник", "Понедельник")
    SCHEDULE = (
        ("Понедельник", "Понедельник"),
        ("Вторник", 'Вторник'),
        ("Среда", 'Среда'),
        ("четверг", "Четверг"),
        ("Пятница", "Пятница"),
        ("Суббота", "Суббота"),
        ("Воскресенье", "Воскресенье")
    )
    TIME_DEFAULT = (1, "с 07:00 утра до 22:00")
    TIME = (
        ("с 07:00 утра до 22:00", "с 07:00 утра до 22:00"),
        ("с 09:00 утра до 21:00", "с 09:00 утра до 21:00"),
        ("с 12:00 до 21:00", "с 12:00 до 21:00")
    )

    profileemployee = models.ForeignKey(
                ProfileEmployee,
                on_delete=models.CASCADE,
                verbose_name='Профиль Сотрудника',
                related_name='profile_schedule'
    )
    choice_schedule = models.CharField(
                choices=SCHEDULE,
                max_length=100,
                verbose_name='График недели',
                default=SCHEDULE_DEFAULT,
                unique=True
    )
    time = models.CharField(
                choices=TIME,
                max_length=100,
                verbose_name='Время',
                default=TIME_DEFAULT
    )

    def __str__(self):
        return f"{self.choice_schedule} {self.time}"


class Skills(models.Model):

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'

    DEFAULT = 'Выберите'
    LIST_SKILLS = (
        ("Ответственный", "Ответственный"),
        ("Пунктуальный", "Пунктуальный"),
        ("Стрессоустойчивый", "Стрессоустойчивый"),
        ("Внимательный", "Внимательный"),
        ("Терпеливый", "Терпеливый"),
        ("Доброта", "Доброта"),
        ("Честность", "Честность"),
        ("Отзывчивость", "Отзывчивость"),
    )

    profileemployee = models.ForeignKey(
                ProfileEmployee,
                on_delete=models.CASCADE,
                verbose_name='Профиль Сотрудника',
                blank=True,
                null=True,
                related_name='profile_skills'
    )
    skills = models.CharField(
                max_length=17,
                verbose_name='Навыки',
                default=DEFAULT,
                choices=LIST_SKILLS
    )

    def __str__(self):
        return f"{self.skills}"


class ProfileClient(models.Model):
    user = models.OneToOneField(
                Client,
                on_delete=models.CASCADE,
                verbose_name='Клиент'
    )
    name = models.CharField(
                verbose_name='Имя',
                max_length=100
    )
    title = models.CharField(
                verbose_name='Порода',
                max_length=100
    )
    content = models.TextField(
                verbose_name='Опишите вашу собаку'
    )
    name_dog = models.CharField(
                verbose_name='Имя собаки',
                max_length=100,
    )
    image = models.ImageField(
                verbose_name='Ваша фотография',
    )
    image_dog = models.ImageField(
                verbose_name='Фотография вашей собаки'
    )

    def __str__(self):
        return f"{self.name}"

    def validate_unique(self, exclude=None):
        super(ProfileClient, self).validate_unique(exclude=exclude)

