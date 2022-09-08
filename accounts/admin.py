from django.contrib import admin

# Register your models here.
from .models import UserStripe, EmailConfirmed, EmailMarketingSignUp, UserAddress, UserDefaultAddress, Membership, Group, Person


class UserAddressAdmin(admin.ModelAdmin):
	class Meta:
		model = UserAddress 

admin.site.register(UserAddress, UserAddressAdmin)
admin.site.register(UserDefaultAddress)
admin.site.register(UserStripe)
admin.site.register(EmailConfirmed)

class EmailMarketingSignUpAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'timestamp']
	class Meta:
		model =EmailMarketingSignUp

admin.site.register(EmailMarketingSignUp, EmailMarketingSignUpAdmin)
admin.site.register(Person)
admin.site.register(Group)
admin.site.register(Membership)
