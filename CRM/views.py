from django.shortcuts import render
from models import Admin,Categories,User,Subscription
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.cache import cache_control
import fetchNews, mailgun
# @cache_control(no_cache=True,must_revalidate=True)

def index(request):
    return HttpResponse("Hello, world. You're at the CRM index.")

                        #Funvtion to display client home page
def home(request):
    return render(request, "CRM/home.html")

                        #Function to display subscribe form and accept user input
def subscribe(request):
    options = ""
    text = ""
    for catg in Categories.objects.all():                       #fetch all the categories from DB
        options += "<option value=\""+catg.category+"\">" + catg.category + "</option>"
    if options == "" :
        text = "No Categories in the list..Come back later"

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phnNo = request.POST['phnNo']
        category = request.POST['category']
        user = User(name=name, email=email, phnno=phnNo)
        user.save()                                             #save user details in the DB
        subscription = Subscription(user=User.objects.get(email=email), category=Categories.objects.get(category=category))
        subscription.save()                                      #save users subscription details in the DB
        mailgun.send_mail(email,category+" News","Congratulations You have been subscribed to"+category+"news\n\nThank you for subscribing to our news service")                #Send subscription mail to the client
        text = "Subscribed successfully"
    return render(request, "CRM/subscribe.html", {'options': options, 'message':text})

                        #function to display unsubcribe form
def unsubscribe(request):
    options = ""
    text = "If you want to opt-out, you'll be unsubscribed from all categories"

    if request.method == 'POST':
        email = request.POST['email']
        phnNo = request.POST['phnNo']
        user = User.objects.get(email=email)
        if user.email == email:
            if user.phnno == phnNo:
                user.delete()                       #delete user if phnNo and email match in the DB
                for client in Subscription.objects.all():
                    mail = client.user.email
                    if mail == email:
                        client.delete()                 #remove the subscription of the deleted user
                mailgun.send_mail(email,"Unsubscribed from News Service","You have been unsubscribed from all the categories of news\nYou won't receive any mail hereafter ")
                text = "Unsubscribed Successfully"
            else:
                text = "Phone No. didn't match our Database"
        else:
            text = "There's no subscription for the provided email"

    return render(request, "CRM/unsubscribe.html", {'message': text})

                        # function to display admin login page and to authenticate the admin access to the CRM system
def adminLogin(request):
    text = ""

    try:
        user=request.session['username']
        return HttpResponseRedirect("/CRM/adminHome")
    except :

        if request.method == 'POST':
            user = request.POST['username']
            password = request.POST['password']
            if Admin.objects.filter(username=user, password=password).exists():         #check login credentials
                request.session['username'] = user                                      #session establishment
                return HttpResponseRedirect('/CRM/adminHome')                           #open dashboard if credentials found correct
            else:
                text="Wrong username or password.. contact your DBA"
        return render(request, "CRM/Admin/adminLogin.html", {"message": text})

                        #function to display admin dashboard
def adminHome(request):
    # admin = Admin.objects.get(id=1)
    try:
        user=request.session['username']                            #session tracking
        return render(request, "CRM/Admin/home.html")
    except:
        return HttpResponseRedirect('/CRM/adminLogin')

                    # Function to display add category page
def addCategory(request):
    try:
        text=""
        user=request.session['username']                            #session tracking
        if request.method == 'POST':
            catg = request.POST['category']
            url = request.POST['url']
            if 'http://in.reuters.com/news/archive/' in url:
                data = Categories(category=catg ,link=url)
                data.save()                                         #save the category details if the link is of reuters archive type
                text = "Category added to the Mailing List"
            else:
                text = "Currently only 'http://in.reuters.com/news/archive/...' type of URL are allowed"

        return render(request, "CRM/Admin/addCategory.html",{'message':text})
    except:
        return HttpResponseRedirect('/CRM/adminLogin')

                    #function to display remove category page
def removeCategory(request):
    try:
        user = request.session['username']                          #session tracking
        options = ""
        text = ""

        if request.method == 'POST':
            catg=request.POST['category']

            Categories.objects.filter(category=catg).delete()               #delete the category from the DB
            for client in Subscription.objects.all():
                mail = client.user.email
                subscription = client.category.category
                if subscription == catg:
                    client.delete()                                         #delete the subscription of the category from the DB
                    break
            flag = 0
            for user in User.objects.all():
                for client in Subscription.objects.all():
                    mail = client.user.email
                    if mail == user.email:
                        flag = 1
                        break
                if flag == 0:
                    mailgun.send_mail(user.email,"Unsubscribed from "+catg+" News Service","You have been unsubscribed from the "+catg+" category of news as we are no longer providing the support for this category\nSorry for the inconvenience ")
                    user.delete()                                   #delete the user from the DB if he was subscribed to only that category which was removed

            text = "Category Removed from mailing list"

        for catg in Categories.objects.all():                                   #fetch all the categories from DB
            options += "<option value=\""+catg.category+"\">" + catg.category + "</option>"
        if options == "":
            text = "No Categories in the list"

        return render(request, "CRM/Admin/removeCategory.html", {'options': options, 'message': text})
    except:
        return HttpResponseRedirect('/CRM/adminLogin')

topics = []
link = []
news = []

                    #function to display send mail page and to perform actions of that page
def sendMail(request):
    try:
        user=request.session['username']
        text = ""
        if request.method == 'POST':
            if Subscription.objects.all().count()==0:
                text = "No need to perform any action as there are no users to send mail to"

            elif request.POST['action']=='fetch':                   #if admin clicks fetch news
                del topics[:]
                del link[:]
                del news[:]
                for catg in Categories.objects.all():
                    topics.append(catg.category)                        #fetch all catgories and the links for fetching news
                    link.append(catg.link)

                if len(topics)==0:
                    text = "No Categories in the list"
                else:
                    for i in range(len(link)):
                        news.append(fetchNews.fetch(link[i]))               #fetch mews from the reuters site
                        # print news[i]
                    text = "News for all the categories fetched"

            elif request.POST['action']=='mail':                    #if admin clicks send mail
                # return HttpResponse("sending mail")
                if len(link) == 0:
                    text = "Fetch news first"
                else:
                    flag = 0
                    for client in Subscription.objects.all():               #loop to send mail to all the subscribed user
                        user = client.user.email
                        subscription = client.category.category
                        mailgun.send_mail(user, subscription+" News", news[topics.index(subscription)])
                        flag = 1
                    if flag==0:
                        text="No Users subscribed to the news services"
                    del topics[:]
                    del link[:]
                    del news[:]
                    text = "Mails sent successfully to the users"
        return render(request, "CRM/Admin/sendMail.html", {'message': text})
    except:
        return HttpResponseRedirect('/CRM/adminLogin')

def logout(request):
    try:
        del request.session['username']                             #delete session
    except KeyError:
        pass
    return HttpResponseRedirect('/CRM/adminLogin')
