from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import JsonResponse

from .models import Subscriptions

class SubscribeView(View):
    def post(self, *args, **kwargs):
        data = {}
        email = self.request.POST.get('email', None)
        success = True
        if email:
            subs = Subscriptions.objects.all()
            subs = subs.filter(
                email=email
            ).distinct()

            if subs:
                message = "You have already subscribed"
            else:
                sub = Subscriptions.objects.create(
                    email=email
                )
                sub.save()

                print("sub", sub)

                if sub:
                    message = "Thanks for subscribing, We will be in touch"
                else:
                    success = False
                    message = "Error creating your subscription, Try again Later"

            data['message'] = message
            data['success'] = success

        return JsonResponse(data)
