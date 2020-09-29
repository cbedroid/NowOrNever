from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ContactUs

# @receiver(post_save, sender=ContactUs)
# def save_IP(sender, instance, **kwargs):
#     client_ip, is_routable = get_client_ip(request,)
#     if client_ip is None:
#         print('IP Address not available')
#     else:
#         print('Client IP', client_ip,)
#         c_form.ip_address = client_ip
#     instance.save()
