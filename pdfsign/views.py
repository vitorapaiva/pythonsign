from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

#Dependencias da assinatura
import sys
import datetime
from cryptography.hazmat import backends
from cryptography.hazmat.primitives.serialization import pkcs12
from endesive.pdf import cms
from urllib.request import urlopen
#fim dependencias da assinatura

# Create your views here.
def index(request):
    return render(request, 'index.html')
def receita(request):
    return render(request, 'receita.html')
def sign(request):
    date = datetime.datetime.utcnow() - datetime.timedelta(hours=12)
    date = date.strftime("D:%Y%m%d%H%M%S+00'00'")
    dct = {
        "aligned": 0,
        "sigflags": 3,
        "sigflagsft": 132,
        "sigpage": 0,
        "sigbutton": True,
        "sigfield": "Signature1",
        "sigandcertify": True,
        "signaturebox": (470, 840, 570, 640),
        "signature": "Teste de Assinatura Python",
#        "signature_img": "signature_test.png",
        "contact": "mak@trisoft.com.pl",
        "location": "Szczecin",
        "signingdate": date,
        "reason": "Porque quero assinar com python",
        "password": "1234",
    }
    with urlopen("http://www.portalxibe.com.br/certificado.pfx") as fp:
        p12 = pkcs12.load_key_and_certificates(
            fp.read(), b"oFnvgdP1234!", backends.default_backend()
        )
    fname="http://www.portalxibe.com.br/prescricao.pdf"
    datau = urlopen(fname).read()
    datas = cms.sign(datau, dct, p12[0], p12[1], p12[2], "sha256")
    fname="/var/www/html/pythonsigned/prescricao-signed.pdf"
    with open(fname, "wb") as fp:
        fp.write(datau)
        fp.write(datas)
    return JsonResponse(dct)