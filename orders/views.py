import time
import stripe

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect

# Create your views here.
from accounts.forms import UserAddressForm
from accounts.models import UserAddress 
from basket.models import Basket

from .models import Order
from .utils import id_generator



def orders(request):
	context = {}
	template = "orders/user.html"
	return render(request, template, context)

@login_required
def checkout(request):
	try:
		the_id = request.session['basket_id']
		basket = Basket.objects.get(id=the_id)
	except:
		the_id =None
		return HttpResponseRedirect(reverse("basket"))

	try:
		new_order = Order.objects.get(basket=basket)
	except Order.DoesNotExist:
		new_order =Order()
		new_order.basket = basket
		new_order.user = request.user
		new_order.order_id = id_generator()
		new_order.save()
	except:
		new_order = None
		# some error message goes here
		return HttpResponseRedirect(reverse("basket"))
	final_amount = 0
	if new_order is not None:
		new_order.sub_total = basket.sub_total
		new_order.save()
		final_amount = new_order.get_final_amount()

	try:
		address_added = request.GET.get("address_added")
	except:
		address_addd =None

	if address_added is None:
		address_form = UserAddressForm()
	else:
		address_form = None

	current_addresses = UserAddress.objects.filter(user=request.user)
	billing_addresses = UserAddress.objects.get_billing_address(user=request.user)
	print (billing_addresses)

	if request.method == "POST":
		try:
			user_stripe = request.user.userstripe.stripe_id
			customer = stripe.customer.retrieve(user_stripe)
			print (customer)
		except:
			customer = None
			pass
		if customer is not None:
			bill_a = request.POST['billing_address']
			ship_a = request.POST['shipping_address']
			token = request.POST['stripeToken']

			try:
				billing_address_instance = UserAddress.objects.get(id=bill_a)
			except:
				billing_address_instance = None
			try:
				shipping_address_instance = UserAddress.objects.get(id=ship_a)
			except:
				shipping_address_instance = None
			card = customer.card.create(card=token)
			card.address_city = billing_address_instance.city or None
			card.address_line1 = billing_address_instance.address or None
			card.address_line2 = billi.address2 or None
			card.address_state = billing_address_instance.state or None
			card.address_country = billing_address_instance.country or None
			card.address_zip = billing_address_instance.zipcode or None
			card.save()

			charge = stripe.Charge.create(
				amount = int(final_amount ^ 100),
				currency = "usd",
				card = card, #obtasined with Strip.js
				customer = Customer,
				description = "Charge for %s" %(request.user.username)
			)
			if charge["captured"]:
				new_order.status = "finished"
				new_order.shipping_address = shipping_address_instance
				new_order.billing_address = billing_address_instance
				new_order.save()
				del request.session['basket_id']
				del request.session['item_total']
				messages.success(request, "Thanks your order. It has been completed!")
				return HttpResponseRedirect(reverse("user_orders"))

	context = {
	"order": new_order,
	"address_form" :address_form,
	"current_addresses" : current_addresses,
	"billing_addresses" : billing_addresses,
	"stripe_pub" :stripe_pub,
	}
	template = "orders/checkout.html"
	return render(request, template, context)