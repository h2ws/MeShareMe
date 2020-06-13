from django.http import HttpResponse
from django.shortcuts import render
import socket
import os

def getlocalwifi_essid():
    return os.popen('''iwconfig `ip route | grep default  | cut -f 5 -d ' '  `   |  cut -d '"' -f 2 | head -n 1''').read()[:-1]

def getlocalip_f():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((os.popen("ip route | grep default  | cut -f 3 -d ' '").read()[:-1], 0))
        ip = s.getsockname()[0]

    finally:
        s.close()
    return ip

cnt = {"text": "", "filename": "N/A", "localip": getlocalip_f(), 'localwifi_essid': getlocalwifi_essid()} 


def getlocalip(request):
    return HttpResponse(getlocalip_f())
 
def hello(request):
    return HttpResponse("Hello world ! ")


def share(request):
    context = {}
    context['hi'] = "I am data, hi"
    return render(request, 'share.html', context)


def submit(request):
    cnt['localip'] =  getlocalip_f()
    cnt['localwifi_essid'] =  getlocalwifi_essid()
    return render(request, 'submit.html', cnt)

def submit_upload_file(request):
    cnt["filename"] = request.POST["filename"]
    print(request.POST)
    with open('/tmp/hw.file','wb') as file:
        for chunk in request.FILES.get('file', None):
            file.write(chunk)
    return HttpResponse("OK")

def submit_download_file(request):
    file=open('/tmp/hw.file','rb')
    response =HttpResponse(file)
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']='attachment;filename="%s"'%(cnt['filename'])
    return response


def submit_upload_text(request):
    cnt["text"] = request.POST["text"]
    return HttpResponse(cnt["text"])

