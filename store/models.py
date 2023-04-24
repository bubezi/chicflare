from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# from allauth.account.signals import user_signed_up
# from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


MITAA = (
    ('select', 'SELECT'),
    ('Juja', "JUJA"),
    ('Thika', "THIKA"),
    ('Rongai', "RONGAI"),
)

GENDER = (
    ('select', 'SELECT'),
    ('male','MALE'),
    ('female', 'FEMALE'),
    ('prefer not to say', 'PREFER NOT TO SAY'),
)

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    phone = PhoneNumberField(null=True, blank=False, unique=True)
    points = models.BigIntegerField(default=0, blank=False, null=True)
    location = models.CharField(max_length=200, choices=MITAA, null=True, blank=False)
    gender = models.CharField(max_length=200, choices=GENDER, null=True, blank=False)
    balance = models.FloatField(default=0, null=False, blank=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField(null=False, blank=False, default=0)
    image = models.ImageField(null=True, blank=True)
    digital = models.BooleanField(default=False)
    details = models.TextField(default="Amazing product Just for you", max_length=2000)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        url = self.image.url
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if not i.product.digital:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.BigIntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


# class ShippingAddress(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
#     order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
#     address = models.CharField(max_length=200, null=False)
#     city = models.CharField(max_length=200, null=False)
#     location = models.CharField(max_length=200, null=False, choices=MITAA, default='select')
#     # zipcode = models.CharField(max_length=200, null=False)
#     date_added = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.address


@receiver(post_save, sender=User)
def create_or_save_user_profile(sender, created, **kwargs):
    if created:
        obj = sender.objects.last()

        Customer.objects.create(user=obj, name=obj.username, email=obj.email)
