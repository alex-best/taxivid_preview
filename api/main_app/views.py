from rest_framework.generics import CreateAPIView
from django.views import View
from django.http import HttpResponseRedirect
from furl import furl

from .models import TelegramUser
from .serializers import TelegramUserSerializer


class TelegramUserCreate(CreateAPIView):
    queryset = TelegramUser
    serializer_class = TelegramUserSerializer


class AppHttpResponseRedirect(HttpResponseRedirect):
    allowed_schemes = ['https', 'citymobil-st', 'maximzakaz']


class CitymobilRedirectView(View):

    def get(self, *args, **kwargs):
        url = furl('citymobil-st://ride?from=59.942717,30.261496&from_str=Малый Васильевского острова&to=59.913185,30.322128&to_str=Дойников переулок&oid=63126368&id_calculation=cd97ffcc4cdb7eefc0bde19c985511fa&tariff=2')
        url.args['from'] = ','.join((self.request.GET['start-lat'], self.request.GET['start-lon']))
        url.args['to'] = ','.join((self.request.GET['end-lat'], self.request.GET['end-lon']))
        return AppHttpResponseRedirect(url.url)


class MaximRedirectView(View):

    def get(self, *args, **kwargs):
        url = furl('maximzakaz://order?refOrgId=SRAVNITAXI&refOrderId=63126372&startAddressName=Малый Васильевского острова, 52&startLatitude=59.942717&startLongitude=30.261496&endAddressName=Дойников переулок&endLatitude=59.913185&endLongitude=30.322128')
        url.args['startLatitude'] = self.request.GET['start-lat']
        url.args['startLongitude'] = self.request.GET['start-lon']
        url.args['endLatitude'] = self.request.GET['end-lat']
        url.args['endLongitude'] = self.request.GET['end-lon']
        return AppHttpResponseRedirect(url.url)
