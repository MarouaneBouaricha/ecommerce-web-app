from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200)

	def __str__(self):
		return self.name

class Category(models.Model):
	name = models.CharField(max_length=50, null=False)
	image = models.ImageField(null=True, blank=True)
	
	def __str__(self):
		return self.name
	
	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url


class Subcategory(models.Model):
	name = models.CharField(max_length=50, null=False)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

	def __str__(self):
		return self.name

class Product(models.Model):
	name = models.CharField(max_length=200)
	price = models.FloatField()
	digital = models.BooleanField(default=False,null=True, blank=True)
	image = models.ImageField(null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	category = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True, blank=True)

	def __str__(self):
		return self.name

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url

class ProductImage(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    images = models.ImageField()

    def __str__(self):
        return self.product.name
	

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)
		
	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
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

	@property
	def get_items(self):
		orderitems = self.orderitem_set.all()
		return orderitems


class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
	order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total
	
	def __str__(self):
		return str(self.product.name)

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
	order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	country = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.city

class ContactMessage(models.Model):
	name = models.CharField(max_length=200, null=False)
	email = models.CharField(max_length=200, null=False)
	topic = models.CharField(max_length=200, null=False)
	message = models.TextField()

	def __str__(self):
		return self.name