from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Request(models.Model):

    STATUS_CHOICES = [
        ('new', 'Новая заявка' ),
        ('in_progress', 'Выполняется'),
        ('completed', 'Услуга оказана'),
        ('cancelled', 'Услуга отменена'),
    ]
    SERVICE_CHOICES = [
        ('common_clean','Общий клининг'),
        ('full_clean','Генеральная уборка'),
        ('post_cons_cleaning','Послестроительная уборка'),
        ('dry_cleaning','Химчистка')
    ]
    PAYMENT_CHOICES = [
        ('cash','Оплата наличными'),
        ('card','Оплата банковской картой')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Имя пользователя')
    address = models.CharField(max_length=100, verbose_name='Адресс для оказание услуг')
    phone_number = models.CharField(max_length=100, verbose_name='Номер телефона')
    desired_date = models.DateTimeField(null=True, verbose_name='Дата и время'  )
    payment_type = models.CharField(max_length=100,choices=PAYMENT_CHOICES, default='cash',verbose_name='Способ оплаты')
    service = models.CharField(max_length=100, choices=SERVICE_CHOICES, verbose_name='Услуги')
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='new', verbose_name='Статус заявки')

    def __str__(self):
        return f"{self.user.username} - {self.service}"









