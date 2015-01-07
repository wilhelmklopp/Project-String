from django.shortcuts import render
#----custom start here-----
#from django.http import HttpResponse
from generator import generate, resolve
from django.shortcuts import render
from pstring.models import Links #for database query
from pstring.forms import LinksForm #for form display
from django.http import HttpResponseRedirect #for completion of form function (django tutorial)
from django.http import HttpRequest

def index(request):
    hello_world = "Hello world woooot"
    all_data = Links.objects.all()
    long_urls = []
    for i in all_data:
        long_urls.append(i.long_url)
    context = {"hello_world" : hello_world, "long_urls": long_urls}
    return render(request, "pstring/index.html", context)
def resolve_landing(request, short):
    response = "This would result in index value: "
    iv = resolve(short)
    result = response + str(iv)
    context = {"iv" : iv, "result" : result}
    return render(request, "pstring/resolve_landing.html", context)
def show_form(request):
    from ipware.ip import get_real_ip
    ip = get_real_ip(request)
    if ip is None:
        ip = "0.0.0.0"
    if request.method == "POST":
        form = LinksForm(request.POST)
        def check_url_status(any_url):
            import urllib2
            try:
                req = urllib2.urlopen(str(any_url))
                http_status = str(req.getcode())
                req.close()
                if http_status[0] == "2":
                    return True
                else:
                    return False #Server responded with something other than Status Code Complete.
            except:
                return False # Server did not respond.
        def fix_url_and_check():
            lurl = str(form.cleaned_data["long_url"])
            for i in range(0, len(lurl)):
                correct = False
                if lurl[i] != ":":
                    pass
                else:
                    if lurl[i+1] + lurl[i+2] == "//":
                        correct = True
                        if check_url_status(lurl):
                            return [True, lurl]
            if correct != True:
                new_lurl = "http://" + lurl
                if check_url_status(new_lurl):
                    return [True, new_lurl]
                else:
                    new_lurl = "https://" + lurl
                    if check_url_status(new_lurl):
                        return [True, new_lurl]
                    else:
                        return [False, new_lurl]
        #validated = fix_url_and_check()
        if form.is_valid() and fix_url_and_check()[0]:
            #add processing of data here
            import uuid
            from django.utils import timezone
            lurl = fix_url_and_check()[1] # previously validated.     ----------now comes old code------:  str(form.cleaned_data["long_url"])
            all_data = Links.objects.all()
            #iv = len(all_data)+1
            row_add = Links(long_url = lurl, unique_uuid = uuid.uuid4(), last_changed = timezone.now(), user_ip=ip, pageviews=0)
            row_add.save()
            iv = row_add.auto_id
            short_url = generate(iv)
            row_add.short = short_url
            row_add.save()
            return HttpResponseRedirect('/')
    else:
        form = LinksForm()
    context = {"form": form}
    return render(request, "pstring/show_form.html", context)
