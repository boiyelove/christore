from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import models
from django.template.loader import render_to_string

# Create your models here.

class UserDefaultAddress(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	shipping = models.ForeignKey("UserAddress", null=True, blank = True, related_name="user_address_shipping_default")
	billing = models.ForeignKey("UserAddress", null = True, blank = True, related_name="user_address_billin_default")

	def __str__(self):
		return str(self.user.username)

class UserAddressManager(models.Manager):
	def get_billing_addresses(self, user):
		return  super(UserAddressManager, self).filter(billing=True).filter(user=user)

class UserAddress(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	address = models.CharField(max_length=120)
	address2 = models.CharField(max_length=120, null=True, blank=True)
	city = models.CharField(max_length=120)
	state = models.CharField(max_length=120)
	country = models.CharField(max_length=120)
	zipcode = models.PositiveSmallIntegerField()
	phone = models.PositiveIntegerField()
	shipping = models.BooleanField(default=True)
	billing = models.BooleanField(default = False)
	timestamp = models.DateTimeField(auto_now_add = False, auto_now= True)
	updated = models.DateTimeField(auto_now_add = True, auto_now= False)

	def __str__(self):
		return self.get_address()

	def get_address(self):
		return "%s, %s, %s, %s, %s" %(self.address, self.city, self.state, self, country, self.zipcode)

	objects = UserAddressManager()

	class Meta:
		ordering = ['-updated', 'timestamp']

class UserStripe(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	stripe_id = models.CharField(max_length=120, null=True, blank=True)

	def __str__ (self):
		return str(self.stripe_id)

class EmailConfirmed(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	activation_key = models.CharField(max_length=200)
	confirmed = models.BooleanField(default=False)

	def __str__(self):
		return str(self.confirmed)

	def activate_user_email(self):
		activation_url = "%s%s" %(settings.SITEURL, reverse("activation_view", ards=[self.activation_key]))
		context = {
			"activation_key" : self.activation_key,
			"activation_url" : activation_url,
			"user": self.user.username,
		}
		message = render_to_string("accounts/activation_message.txt", context)
		subject = "Activate your Email"
		self.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)

	def email_user(self, subject, message, from_email=None, **kwargs):
		send_mail(subject, message, from_email, [self.user.email], kwargs)






class EmailMarketingSignUp(models.Model):
	email =models.EmailField()
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=True, auto_now=False)
	#confirmed = models.BooleanField(default=False)

	def __str__(self):
		return str(self.email)

class Person(models.Model):
	name = models.CharField(max_length=50)

class Group(models.Model):
	name = models. CharField(max_length=128)
	members = models.ManyToManyField("Person", through=' Membership' , through_fields=(' group' , ' person' ))

class Membership(models.Model):
	group = models.ForeignKey(Group)






