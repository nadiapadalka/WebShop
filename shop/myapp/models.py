from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from transliterate import translit
from django.urls import reverse
from decimal import Decimal
from django.conf import settings

# Create your models here.

class Category(models.Model):

	name = models.CharField(max_length=100)
	slug = models.SlugField(blank=True)

	def __str__(self):
		return self.name

	def get_category_slug(self):
		return reverse('category_detail', kwargs={'category_slug': self.slug})


def pre_save_category_slug(sender, instance, *args, **kwargs):
	if not instance.slug:
		slug = slugify(translit(str(instance.name), reversed=True))
		instance.slug = slug;

pre_save.connect(pre_save_category_slug, sender=Category)

class Brand(models.Model):

	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

def image_folder(instance, filename):
	filename = instance.slug + '.' + filename.split('.')[1]
	return "{0}/{1}".format(instance.slug, filename)

class ProductManager(models.Manager):

	def all(self, *args, **kwargs):
		return super(ProductManager, self).get_queryset().filter(available=True)

class Product(models.Model):

	category = models.ForeignKey(Category, on_delete=models.PROTECT)
	brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
	title = models.CharField(max_length=100)
	slug = models.SlugField()
	description = models.TextField()
	image = models.ImageField(upload_to=image_folder)
	price = models.DecimalField(max_digits=9, decimal_places=2)
	available = models.BooleanField(default=True)
	objects = ProductManager()

	def __str__(self):
		return self.title

	def get_product_slug(self):
		return reverse('product_detail', kwargs={'product_slug': self.slug})


class CartItem(models.Model):

	product = models.ForeignKey(Product, on_delete=models.PROTECT)
	product_count = models.PositiveIntegerField(default=1)
	total_item = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

	def __str__(self):
		return "Car item for product {0}".format(self.product.title)


class Cart(models.Model):

	items = models.ManyToManyField(CartItem, blank=True)
	total_cart = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

	def __str__(self):
		return str(self.id)

	def add_cart_item_to_cart(self, product_slug):
		cart=self
		product = Product.objects.get(slug=product_slug)
		new_item, _ = CartItem.objects.get_or_create(product=product, total_item=product.price)
		if new_item not in cart.items.all():
			cart.items.add(new_item)
			cart.save()

	def remove_cart_item_from_cart(self, prod_slug):
		cart=self
		prod = Product.objects.get(slug=prod_slug)
		for cart_item in cart.items.all():
			if cart_item.product == prod:
				cart.items.remove(cart_item)
				cart.save()

	def change_count(self, count, item_id):
		cart = self
		cart_item = CartItem.objects.get(id=int(item_id))
		cart_item.product_count = int(count)
		cart_item.total_item = int(count) * Decimal(cart_item.product.price)
		cart_item.save()
		cart_total_price = 0.00
		for item in cart.items.all():
			cart_total_price += float(item.total_item)
		cart.total_cart = cart_total_price
		cart.save()

	def make_discount(self, coupon):
		cart = self
		if(coupon == '15percentdiscount'):
			cart.total_cart = cart.total_cart - ((15 * cart.total_cart) / 100)
		elif(coupon == '30percentdiscount'):
			cart.total_cart = cart.total_cart - ((30 * cart.total_cart) / 100)
		elif(coupon == '50percentdiscount'):
			cart.total_cart = cart.total_cart - ((50 * cart.total_cart) / 100)
		cart.save()

ORDER_STATUS_STATE = (
	("In process","In process"),
	("Performing","Performing"),
	("Paid for","Paid for")
)

class Order(models.Model):

	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
	items = models.ForeignKey(Cart, on_delete=models.PROTECT)
	total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	phone = models.CharField(max_length=10)
	address = models.CharField(max_length=120)
	buying_type = models.CharField(max_length=50, choices=[('By yourself', 'By yorself'), ('Delievery', 'Delievery')], default='By yourself')
	comments = models.TextField()
	status = models.CharField(max_length=120, choices=ORDER_STATUS_STATE, default=ORDER_STATUS_STATE[0][0])

	def __str__(self):
		return "Order №{0}".format(str(self.id))
