from django.shortcuts import render
#----custom start here-----
#from django.http import HttpResponse
from generator import generate, resolve
from django.shortcuts import render
from pstring.models import Links #for database query
from pstring.forms import LinksForm #for form display
from django.http import HttpResponseRedirect #for completion of form function (django tutorial)
from django.http import HttpRequest
import urllib2
import os #for heroku environment variables access

def index(request):
    all_data = Links.objects.all()
    long_urls = []
    for i in all_data:
        long_urls.append(i.long_url)
    context = {"long_urls" : long_urls}
    #return render(request, "pstring/index.html", context)
    from ipware.ip import get_real_ip
    ip = get_real_ip(request)
    if ip is None:
        ip = "0.0.0.0"
    if request.method == "POST":
        form = LinksForm(request.POST)
        def check_url_status(any_url):
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
        def recaptcha_verify():
            import json
            try:
                user_response = request.POST["g-recaptcha-response"]
            except:
                return False
            if user_response == "":
                return False
            secret_key = os.environ.get('RECAPTCHA_SECRET', '')
            try:
                response = urllib2.urlopen("https://www.google.com/recaptcha/api/siteverify?secret="+secret_key+"&response="+user_response)
            except:
                return False
            result = json.load(response)
            if result["success"]:
                return True
            else:
                return False
        #validated = fix_url_and_check()
        if form.is_valid() and fix_url_and_check()[0] and recaptcha_verify():
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
            #---start email notification
            from django.core.mail import send_mail
            message = "URL : " + str(lurl) + "\nShort: " + str(short_url)
            send_mail("New Short added", message, "webmaster@pul.io", [os.environ.get('MY_EMAIL')], fail_silently=False)
            #---end email notification
            redirect_to_url = row_add.short
            return HttpResponseRedirect('../' + str(redirect_to_url))
    else:
        form = LinksForm()
    context = {"form": form}
    return render(request, "pstring/index.html", context)
def resolve_landing(request, short):
    response = "This would result in index value: "
    iv = resolve(short)
    def get_data():
        try:
            row = Links.objects.get(pk=iv)
        except Exception as e:
            return [False, e]
        lurl = row.long_url
        return [True, lurl]
    result = get_data()
    if result[0]:
        final = "This will be a page with information on " + result[1]
        url = result[1]
        context = {"iv" : iv, "final" : final, "url": url}
        return render(request, "pstring/resolve_landing.html", context)
    else:
        final = "There was an error:\n" + str(result[1])
        context = {"iv" : iv, "final" : final}
        return render(request, "pstring/index.html", context)
    
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
            #---start email notification
            from django.core.mail import send_mail
            message = "URL : " + str(lurl) + "\nShort: " + str(short_url)
            send_mail("New Short added", message, "webmaster@pul.io", [os.environ.get('MY_EMAIL')], fail_silently=False)
            #---end email notification
            redirect_to_url = row_add.short
            return HttpResponseRedirect('../' + str(redirect_to_url))
    else:
        form = LinksForm()
    context = {"form": form}
    return render(request, "pstring/show_form.html", context)
