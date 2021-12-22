from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib import messages , auth
from django.contrib.auth.models import User
from .models import UserProfile
import re 
from products.models import Product
# Create your views here.

def sign_in(request):
    if request.method == "POST" and 'btnlogin' in request.POST:
        username= request.POST['user']
        password=request.POST['pass']
        user = auth.authenticate(username=username , password=password)
        ##Chek for user if exist
        if user is not None:
            if "rememberme" not in request.POST:
                request.session.set_expiry(0)
            auth.login(request , user)
            #messages.success(request , 'You are now logged in')
        else:
            messages.error(request , 'username or password invalid')
        return redirect("signin")
    else:
        return render(request , 'accounts/signin.html')

###########################  Devider ######################################################################
def logout(request):
    if request.user.is_authenticated :
        auth.logout(request)
    return redirect('index')
   
###########################  Devider ######################################################################
def signup(request):
    if request.method == "POST" and 'btnsignup' in request.POST:
        #variables for Fields
        fname = None
        lname= None
        address =None
        address2 =None
        city = None
        state= None
        zip_number =None
        email = None
        username = None
        password = None
        terms =None
        is_added = None
        
        #Get values from  the form 
        if 'fname' in request.POST: fname= request.POST['fname']
        else: messages.error(request , 'error in first name')

        if 'lname' in request.POST: lname= request.POST['lname']
        else: messages.error(request , 'error in last name')

        if 'address' in request.POST: address= request.POST['address']
        else: messages.error(request , 'error in address')

        if 'address2' in request.POST: address2= request.POST['address2']
        else: messages.error(request , 'error in address2')

        if 'city' in request.POST: city= request.POST['city']
        else: messages.error(request , 'error in city field')

        if 'state' in request.POST: state= request.POST['state']
        else: messages.error(request , 'error in state field')

        if 'zip' in request.POST: zip_number= request.POST['zip']
        else: messages.error(request , 'error in zip field')

        if 'email' in request.POST: email= request.POST['email']
        else: messages.error(request , 'error in email')

        if 'user' in request.POST: username= request.POST['user']
        else: messages.error(request , 'error in username')

        if 'pass' in request.POST: password= request.POST['pass']
        else: messages.error(request , 'error in password')

        if 'termes' in request.POST: terms= request.POST['termes']

        #Chek the values empty
        if fname and lname and address and address2 and city and state and zip_number and email and username and password :
            # Chech if terms acceptable
            if terms =='on':
                #Checkif username is taken 
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'This username is taken')
                else:
                    #Check if email used 
                    if User.objects.filter(email=email).exists():
                        messages.error(request, 'This email is taken')
                    else:
                        patt = "^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"
                        if re.match(patt , email):
                            #Add user
                            user = User.objects.create_user(first_name = fname ,last_name= lname , email=email , username=username , password=password)
                            user.save()
                            #Add user profile
                            userprofile = UserProfile(user=user , address=address , address2=address2 , city=city , state=state , zip_number=zip_number)
                            userprofile.save()
                            #Clear fields 
                            fname = '',
                            lname= '',
                            address='',
                            address2='',
                            city='',
                            state='',
                            zip_number='',
                            email='',
                            username='',
                            password='',
                            terms= None
                            #Success Message 
                            messages.success(request, 'You account is created successfuly')
                            is_added = True
                        else:
                            messages.error(request, 'Enter a valid email')
            else:
                messages.error(request, 'You must agree to the terms' )
        else:
            messages.error(request, 'Check empty fields')
        return render(request , 'accounts/signup.html' , {
            'fname':fname,
            'lname':lname,
            'address': address,
            'address2':address2,
            'city':city,
            'state':state,
            'zip':zip_number,
            'email':email,
            'user':username,
            'pass':password,
            'is_added':is_added
        })
    else:    
        return render(request , 'accounts/signup.html')

###########################  Devider ######################################################################
def profile(request):
    if request.method == "POST" and 'btnsave' in request.POST:

        ## Update data for user profile
        if request.user is not None and request.user.id != None:
            userprofile = UserProfile.objects.get(user=request.user)
            if request.POST['fname'] and request.POST['lname'] and request.POST['address'] and request.POST['address2'] and request.POST['city'] and request.POST['state'] and request.POST['zip'] and request.POST['email'] and request.POST['user'] and request.POST['pass'] :
               request.user.first_name = request.POST['fname'] 
               request.user.last_name = request.POST['lname'] 
               userprofile.address = request.POST['address']
               userprofile.address2 = request.POST['address2']
               userprofile.city =request.POST['city']
               userprofile.state =request.POST['state']
               userprofile.zip_number =request.POST['zip']
              # request.user.email = request.POST['email']
               #request.user.username = request.POST['user']
               if not request.POST['pass'].startswith('pbkdf2_sha256'):
                   request.user.set_password(request.POST['pass'])
               request.user.save()
               userprofile.save()
               auth.login(request, request.user)
               messages.success(request , "Your data has been saved")
            else:
                messages.error(request, 'Check your values and elements')
        return redirect('profile')
    else:
        if request.user is not None:
            context = None
            #if request.user.id != None:
            if not request.user.is_anonymous:
                userprofile = UserProfile.objects.get(user=request.user)
                context={
                    'fname': request.user.first_name,
                    'lname': request.user.last_name,
                    'address': userprofile.address,
                    'address2': userprofile.address2,
                    'city':userprofile.city,
                    'state': userprofile.state,
                    'zip': userprofile.zip_number,
                    'email': request.user.email,
                    'user': request.user.username,
                    'pass': request.user.password
                }
            return render(request , 'accounts/profile.html',context)
        else: redirect('profile')
    
###########################  Devider ######################################################################
def product_favorite(request , pro_id):
    if request.user.is_authenticated and not request.user.is_anonymous:
        pro_fav = Product.objects.get(pk=pro_id)
        if UserProfile.objects.filter(user = request.user , product_favorites=pro_fav):
            messages.info(request, 'Already product in the favorite list')

        else:
            userprofile = UserProfile.objects.get(user = request.user)
            userprofile.product_favorites.add(pro_fav)
            messages.success(request , "Proudct added in your favorite list")

        return redirect('/products/' + str(pro_id))
    else:
        messages.error(request ,'You must be logged in')
        return redirect('/products/' + str(pro_id))
  
###########################  Devider ######################################################################
def show_product_favorite(request):
    context=None
    if request.user.is_authenticated and not request.user.is_anonymous:
        userInfo= UserProfile.objects.get(user=request.user)
        pro = userInfo.product_favorites.all()
        context= {'products':pro}
    return render(request, 'products/products.html', context)