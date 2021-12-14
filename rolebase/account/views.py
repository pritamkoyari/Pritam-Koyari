from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from .decorator import *
from django.core.exceptions import PermissionDenied
from datetime import datetime
from datetime import date
global filternews
def filternews(queryfilter):
    try:
        newsdetails = News.objects.filter(dept=queryfilter).order_by('postedtime')
    except News.DoesNotExist:
        newsdetails = None
    filterednews = []
    if newsdetails is not None:
        for ND in newsdetails:
            if ND.status:
                filterednews.append({
                "id": ND.id,
                "headlines": ND.headlines,
                "details": ND.details,
                'dept': ND.dept,
                'owner': ND.owner,
                'img':ND.img,
                "postedtime": ND.postedtime
            })
            else:
                filterednews
    else:
        filterednews
        
    return filterednews



# Create your views here.
def index(request):
    return render(request,'home/index.html')


def home(request):
    ec=News.objects.filter(dept='Electronics&Communication').order_by('postedtime')[0]
    context={'ec':ec}
    return render(request, 'home/index.html',context)

def about(request):
    return render(request, 'home/about.html')



def achievement(request):
    return render(request, 'home/achievement.html')

def sports(request):
    return render(request, 'home/sports.html')
def event(request):
    return render(request, 'home/event.html')
def cdc(request):
    return render(request, 'home/cdc.html')

def ece(request):
    #ece=News.objects.filter(dept='Electronics&Communication').order_by('postedtime')
    ece=filternews('Electronics&Communication')
                
                
    context={'ece':ece}
    return render(request, 'home/ece.html',context)
    
def cse(request):
    cse=filternews('ComputerScience')
                
                
    context={'cse':cse}
    return render(request, 'home/cse.html',context)
def ee(request):
    ee=filternews('Electrical')
                
                
    context={'ee':ee}
    return render(request, 'home/ee.html',context)
def ce(request):
    ce=filternews('Civil')
                
                
    context={'ce':ce}
    
    return render(request, 'home/ce.html',context)
def me(request):
    me=filternews('Mechanical')
                
                
    context={'me':me}
    return render(request, 'home/me.html',context)
def annualfest(request):
    return render(request, 'home/annualfest.html')
def blood(request):
    return render(request, 'home/blood.html')
def dkb(request):
    return render(request, 'home/dkb.html')
def guest(request):
    return render(request, 'home/guest.html')

def leader(request):
    return render(request, 'home/leader.html')
def times(request):
    return render(request, 'home/times.html')
def tree(request):
    return render(request, 'home/tree.html')



@OnlyAuth
def signin(request):
    LM = LoginForm(request.POST or None)
    if request.method == 'POST':
        if LM.is_valid():
            UserName = request.POST.get('username')
            PassWord = request.POST.get('password')
            user = authenticate(request, username=UserName, password=PassWord)

            if user is not None and user.is_cdc:
                login(request, user)
                return redirect('cdc')
            elif user is not None and user.is_teacher:
                login(request, user)
                return redirect('teacher')
            elif user is not None and user.is_student:
                login(request, user)
                return redirect('student')
            else:
                messages.error(request, 'Username or Password is incorrect')
        else:
            messages.error(request, LM.errors)
    else:
        LM = LoginForm()
    context = {'form': LM}
    return render(request, 'common/signin.html', context)


@OnlyAuth
def signup(request):
    if request.method == 'POST':
        SF = SignupForm(request.POST)
        if SF.is_valid():
            isStudent = True
            isTeacher = False
            if isStudent:
                SignUpUser = SF.save(commit=False)
                SignUpUser.is_student = True
                SignUpUser.status = True
                SignUpUser.save()
            elif isTeacher:
                SignUpUser = SF.save(commit=False)
                SignUpUser.is_teacher = True
                SignUpUser.status = False
                SignUpUser.save()
            else:
                messages.warning(request, 'Please Select Your user Type')
                return redirect('signin')
            user = SF.cleaned_data.get('username')
            messages.success(request, 'Account Created for ' + user)
            return redirect('signin')
        else:
            messages.error(request, SF.errors)
    else:
        SF = SignupForm()
    context = {'form': SF}
    return render(request, 'common/signup.html', context)




@login_required(login_url='signin')
def signout(request):
    logout(request)
    return redirect('/signin')

# @login_required(login_url='signin')
# def cdc(request):
#     if not request.user.is_cdc:
#         raise PermissionDenied
#     return render(request, 'admin/CdcProfile.html')


@login_required(login_url='signin')
def student(request):
    if not request.user.is_student:
        raise PermissionDenied
    if not request.user.status:
        return render(request, 'common/notActive.html')

    userdata = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        UserProfileForm = SignupForm(
            request.POST, request.FILES, instance=userdata)

        if UserProfileForm.is_valid():
            student = UserProfileForm.save(commit=False)
            student.is_student = True
            student.status = True
            UserProfileForm.save()
            messages.success(
                request, 'Profile is Updated. please login again to craete a new Session')
            return redirect('signout')
        else:
            messages.warning(request, UserProfileForm.errors)
    else:
        UserProfileForm = SignupForm(instance=userdata)
    context = {'StudentData': userdata, 'UserProfileForm': UserProfileForm}
    return render(request, 'student/StudentProfile.html', context)




# @login_required(login_url='signin')
# def cdc(request):
#     if not request.user.is_cdc:
#         raise PermissionDenied
#     return render(request, 'admin/CdcProfile.html')





@login_required(login_url='signin')
def addnews(request):
    if not request.user.status:
        return render(request, 'common/notActive.html')

    userdata = User.objects.get(pk=request.user.id)

    try:
        newsdetails = News.objects.filter(owner=request.user.id)
    except News.DoesNotExist:
        newsdetails = None

    AllNews = []
    if newsdetails is not None:
        for ND in newsdetails:
            user = User.objects.get(pk=ND.owner)
            if user is not None:
                author = user.first_name + ' ' + user.last_name
                img = user.profilepic.url
            else:
                author = ""

            AllNews.append({
                "id": ND.id,
                "headlines": ND.headlines,
                "details": ND.details,
                'dept': ND.dept,
                'owner': ND.owner,
                'ownername': author,
                'ownerimg': img,
                "postedtime": ND.postedtime,
            })

    if request.method == 'POST':
        NewsForm = NewsManagement(request.POST, request.FILES)
        if NewsForm.is_valid():
            news = NewsForm.save(commit=False)
            # image = Image.open(news.img) 
            # new_image = image.resize((800, 800))
            # news.img=new_image
            news.status = False
            news.owner = request.user.id
            news.postedtime = date.today()
            news.save()
            messages.success(
                request, 'Your News Details is submited and wait for CDC process')
            return redirect('allnews')
        else:
            messages.warning(request, NewsForm.errors)

    else:
        NewsForm = NewsManagement()

    context = {'StudentData': userdata, 'NewsData': newsdetails,
               'NewsForm': NewsForm}
    return render(request, 'news/addnews.html', context)


@login_required(login_url='signin')
def allnews(request):
    if not request.user.status:
        return render(request, 'common/notActive.html')

    userdata = User.objects.get(pk=request.user.id)
    try:
        newsdetails = News.objects.filter(owner=request.user.id)
    except News.DoesNotExist:
        newsdetails = None

    AllNews = []
    if newsdetails is not None:
        for ND in newsdetails:
            user = User.objects.get(pk=ND.owner)
            if user is not None:
                author = user.first_name + ' ' + user.last_name
                img = user.profilepic.url
            else:
                author = ""
              
            print(author)
              
            AllNews.append({
                "id": ND.id,
                "headlines": ND.headlines,
                "details": ND.details,
                'dept': ND.dept,
                'owner': ND.owner,
                'ownername': author,
                'ownerimg': img,
                "postedtime": ND.postedtime
            })
    context = {'StudentData': userdata, 'NewsData': AllNews}
    return render(request, 'news/Allnews.html', context)


@login_required(login_url='signin')
def editnews(request, pk):
    if not request.user.status:
        return render(request, 'common/notActive.html')

    userdata = User.objects.get(pk=request.user.id)
    newsdetails = News.objects.get(pk=pk)

    if request.method == 'POST':
        NewsForm = NewsManagement(
            request.POST, request.FILES, instance=newsdetails)
        if NewsForm.is_valid():
            news = NewsForm.save(commit=False)
            news.status = False
            news.owner = request.user.id
            news.postedtime = date.today()
            news.save()
            messages.success(
                request, 'Your News Details is submited')
            return redirect('allnews')
        else:
            messages.warning(request, NewsForm.errors)
    else:
        NewsForm = NewsManagement(instance=newsdetails)

    context = {'StudentData': userdata, 'NewsForm': NewsForm,'newsdetails':newsdetails}
    return render(request, 'news/editnews.html', context)


@login_required(login_url='signin')
def deletenews(request, pk):
    if not request.user.status:
        return render(request, 'common/notActive.html')
    if request.method == 'POST':
        target_data = News.objects.get(pk=pk)
        target_data.delete()
        messages.success(request, 'This News deleted')
        return redirect('allnews')


def newsdetails(request,pk):
    if not request.user.status:
        return render(request, 'common/notActive.html')

    userdata = User.objects.get(pk=request.user.id)
    try:
        newsdetails = News.objects.get(pk=pk)
    except News.DoesNotExist:
        newsdetails = None
     
    newsowner= User.objects.get(pk=newsdetails.owner)  
        

    
    context = {'StudentData': userdata, 'NewsData': newsdetails,'newsowner':newsowner}
    return render(request, 'news/newsdetails.html', context)
    

@login_required(login_url='signin')
def teacher(request):
    if not request.user.is_teacher:
        raise PermissionDenied
    if not request.user.status:
        return render(request, 'common/notActive.html')
    userdata = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        UserProfileForm = SignupForm(
            request.POST, request.FILES, instance=userdata)

        if UserProfileForm.is_valid():
            student = UserProfileForm.save(commit=False)
            student.is_teacher = True
            student.status = True
            UserProfileForm.save()
            messages.success(
                request, 'Profile is Updated. please login again to craete a new Session')
            return redirect('signout')
        else:
            messages.warning(request, UserProfileForm.errors)
    else:
        UserProfileForm = SignupForm(instance=userdata)
    context = {'StudentData': userdata, 'UserProfileForm': UserProfileForm}
    return render(request, 'teacher/TeacherProfile.html', context)