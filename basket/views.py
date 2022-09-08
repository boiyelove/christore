from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse

# Create your views here.
from products.models import Product#, Variation
from .models import Basket, BasketItem


def view(request):
	try:
		the_id = request.session['basket_id']
		basket = Basket.objects.get(id=the_id)
	except:
		the_id = None


	if the_id:
		new_total = 0.00
		for item in basket.basketitem_set.all():
			line_total = float(item.product.price) * item.quantity
			new_total += line_total
		request.session['items_total'] = basket.basketitem_set.count()
		basket.total = new_total
		basket.save()
		context = {"basket": basket,}
	else:
		empty_message = "Your Basket is Empty"
		context = {"empty": True, "empty_message": empty_message}
	template = "basket/view.html"
	return render(request, template, context)

def remove_from_basket(request, id):
	try:
		the_id = request.session["baskey_id"]
		basket = Basket.objects.get(id=the_id)
	except:
		return HttpResponseRedirect(reverse("basket"))

	basketitem = BasketItem.objects.get(id=id)
	#basketitem.delete()
	basketitem.basket = None
	basketitem.save()
	#send "send success message"
	return HttpResponseRedirect(reverse("basket"))



def add_to_basket(request, slug):
	request.session.set_expiry(120000)

	try:
		the_id =request.session["basket_id"]
	except:
		new_basket = Basket()
		new_basket.save()
		request.session["basket_id"]=new_basket.id
		the_id = new_basket.id
	basket = Basket.objects.get(id=the_id)

	try:
		product = Product.objects.get(slug=slug)
	except Product.DoesNotExist:
		pass
	except:
		pass
	product_var = [] #product variation
	if request.method == "POST":
		qty = request.POST['qty']
		for item in request.POST:
			key = item
			val = request.POST[key]
			try:
				v= Variation.objects.get(product = product, category__iexact=key, title__iexact=val)
				product_var.append(v)
			except:
				pass

		basketitem = BasketItem.objects.create(basket=basket, product=product)
		basket_item.quantity = qty
		basket_item.save()
		# message.success("Successful")
		return HttpResponseRedirect(reverse("basket"))
	# message.error("An error occured")
	return HttpResponseRedirect(reverse("basket"))



