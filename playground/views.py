from urllib import response
from django.core.mail import EmailMessage, BadHeaderError
from django.shortcuts import render
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from templated_mail.mail import BaseEmailMessage
from .tasks import notify_customers
from rest_framework.views import APIView
import requests
import logging

logger = logging.getLogger(__name__)

class HelloView(APIView):
    @method_decorator(cache_page(5 * 60))
    def get(self, request):
        try:
            logger.info('Calling httpbin')
            response = requests.get('https://httpbin.org/delay/2')
            logger.info('Received the response')
            data = response.json()
        except requests.ConnectionError:
                logger.critical('httpbin is offline')
        return render(request, 'hello.html', {'name': 'Nick'})




# @cache_page(5 * 60)
# def say_hello(request):
#     response = requests.get('https://httpbin.org/delay/2')
#     data = response.json()
#     return render(request, 'hello.html', {'name': data})





    # notify_customers.delay('Hello')
    # try:
    #     message = BaseEmailMessage(
    #         template_name='emails/hello.html',
    #         context={'name': "Nick"}
    #     )
    #     message.send(['korg1000@yandex.ru'])

        # message = EmailMessage('subject', 'message', 'arhipon@list.ru', ['korg1000@yandex.ru'])
        # message.attach_file('playground/static/images/scull_3.jpg')
        # message.send()
    # except BadHeaderError:
    #     pass
    # requests.get('https://httpbin.org/delay/2')

    # key = 'httpbin_result'
    # if cache.get(key) is None:
    #     response = requests.get('https://httpbin.org/delay/3')
    #     data = response.json()
    #     cache.set(key, data)


    # return render(request, 'hello.html', {'name': cache.get(key)})
