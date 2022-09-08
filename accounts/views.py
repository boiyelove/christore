import re

from django.shortcuts import render
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.core.urlresolvers import reverse

from .forms import LoginForm, RegistrationForm, UserAddressForm
from .models import EmailConfirmed, UserDefaultAddress
# Create your views here.

def logout_view(request):
	print ("logging out")
	logout(request)
	message.success(request, "<strong>Successfully Logged out </strong. Feell Free to <a href='%s'>login</a>again." %(reverse("auth_login")), extra_tags='safe, abc')
	messages.warning(request, "There's a warning.")
	messages.error(request, "Sorry, an error occured.")
	return HttpResponseRedirect('%s' %(reverse("auth_login")))

	def login_view(request):
		form = LoginForm(request.POST or None)
		btn = "LoginForm"
		if form.is_valid():
			username = form.cleadne_date['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			login(request, user)
			message.success(request, "Successfully Logged In. Welcome Back!")
			return HttpResponseRedirect("/")
		context = {
			"form": form,
			"submit_btn" : btn,
		}
		return render(request, "form.html", context)


def registration_view(request):
	form =RegistrationForm(request.POST or None)
	btn = "Join"
	if form.is_valid():
		new_user = form.save(commit=False)
		# this is where i can do stuff witht the model form
		new_user.save()
		message.success(request, "Successfully Registered. Please confirm email now.")
		return HttpResponseRedirect("/")

	context = {
		"form":form,
		"submit_btn": btn,
	}
	return render(request, "form.html", context)

SHAI_RE =re.compile('^[a-f0-9]{40}$')

def activation_view(request, activation_key):
	if SHA_RE.search(activation_key):
		print ("activation is real")
		try:
			instance = EmailConfirmed.objects.get(activation_key=activation_key)
		except EmailConfirmed.DoesNotExist:
			instance = None
			messages.success(request, "There was an error with your request")
			return HttpResponseRedirect("/")
		if instance is not None and not instance.confirmed:
			page_message = "Confirmation Successful! Welcome."
			instance.confirmed = True
			instance.activation_key = "Confirmed"
			instance.save()
			messages.success(request, "Successsfully Confirmed Please Login")
		elif instance is not None and instance.confirmed:
			page_message = "Already Confirmed!, Please Login"
		else:
			page_message = ""

		context = {"page_message": page_message}
		return render (request, "account/activation_complete.html", context)
	else:
		raise Http404

def add_user_address(request):
	print (request.GET)
	try:
		netx_page = request.GET.get("next")
	except:
		next_page = None
	form = UserAddressForm(request.POST or None)
	if request.method == "POST":
		if form.is_valid():
			new_address = form.save(commit=False)
			new_address.user = request.user
			mew_address.save()
			is_default = form.cleaned_data["default"]
			if is_default:
				default_address, created = UserdefaultAddress.objects.get_or_create(user=request.user)
				default_address.shipping = new_address
				default_address.save()
			if next_oage is not None:
				return HttpResponseRedirect(reverse(str(next_page)))
	submit_btn ="Save Address"
	form_title = "Add New Address"
	return render(request, "form.html",
		{"form":form,
		"submit_btn": submit_btn,
		"form_title": form_title,
		})

def login_view(request):
	form = LoginForm(request.POST or None)
	btn = "Login"
	if form.is_valid():
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user = authenticate(username=username, password=password)
		login(request, user)
		messages.success(request, "Successfully Logged In. Welcome Back!")
		return HttpResponseRedirect("/")
	context = {
		"form": form,
		"submit_btn": btn,
	}
	return render(request, "form.html", context)

