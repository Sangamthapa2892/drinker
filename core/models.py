from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Subscriber(models.Model):
    email=models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.email

class Contact(models.Model):
    name=models.CharField(max_length=100)
    phone = PhoneNumberField(region='NP') 
    email=models.EmailField(unique=True)
    message=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Testimonial(models.Model):
    name=models.CharField(max_length=100)
    image=models.ImageField(upload_to='testimonials/',null=True,blank=True)
    text=models.TextField()
    rating=models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1),MaxValueValidator(5)],
        help_text="Rating from 1 (worst) to 5 (best)",
        verbose_name="User Rating",
        )
    role=models.CharField(max_length=100,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=False)
    def __str__(self):
        return self.name

class LiquorCategory(models.Model):
    name=models.CharField(max_length=100)
    image=models.ImageField(upload_to='category/',blank=True)
    description=models.TextField()
    text = models.TextField(default='', blank=True, null=True)
    def __str__(self):
        return self.name
    
class Liquor(models.Model):
    name=models.CharField(max_length=100)
    category=models.ForeignKey(LiquorCategory,on_delete=models.CASCADE, related_name='wines')
    image=models.ImageField(upload_to='liquors/',blank=True)
    region = models.CharField(max_length=100, blank=True)
    vintage = models.PositiveIntegerField(null=True, blank=True)
    alcohol_content = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    producer = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.name} ({self.vintage})"

class Order(models.Model):
    PAYMENT_METHODS = [
        ('cash_on_delivery', 'Cash on Delivery'),
        ('online_payment', 'Online Payment'),
    ]
    
    ORDER_STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    order_id = models.CharField(max_length=50, unique=True)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    delivery_address = models.TextField()
    delivery_instructions = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash_on_delivery')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order_id} - {self.customer_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    item_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product_name} - {self.quantity}"

    def save(self, *args, **kwargs):
        self.item_total = self.price * self.quantity
        super().save(*args, **kwargs)