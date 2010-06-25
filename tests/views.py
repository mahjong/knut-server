from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.core.files.storage import default_storage
from django.core.servers.basehttp import FileWrapper
from models import User, Test, Category, Result, TestUser
from django.template import RequestContext
import os
import string
import random

def test_upload(request):
    if request.method == "GET":
        return HttpResponse("GET")
    elif request.method == "POST":
        nLogin = request.POST.get('login', '')
        nPassword = request.POST.get('password', '')
        #print nLogin, nPassword
        user = User.objects.filter(login=nLogin, password=nPassword)
        if user:
            #print user
#            print request.POST
            nTitle = request.POST.get("title")
            test_old = user[0].test_set.filter(title=nTitle)
            if test_old:
                # nie usuwam, uwaga promotora
#                if test_old[0].version < int(request.POST.get("version")):
#                    default_storage.delete("test_files/%s/questions.tar.bz2"%test_old[0].id)
#                    default_storage.delete("test_files/%s/answers.xml"%test_old[0].id)
#                    os.rmdir("test_files/%s"%test_old[0].id)
#                    test_old[0].delete()
                # we have this test already, no need to update
                if test_old[0].version == int(request.POST.get("version")):
                    return HttpResponse("OK")
            
            nInstructions = request.POST.get("instructions")
            nPassword = request.POST.get("test-password")
            nCategory = request.POST.get("test-category")
            nVersion = int(request.POST.get("version"))
            category, created = Category.objects.get_or_create(name=nCategory)
            test_id = ''.join(random.sample(string.digits, 3)) + ''.join(random.sample(string.lowercase, 3))
            test_new = user[0].test_set.create(title=nTitle, instructions=nInstructions, password=nPassword, category=category,  version=nVersion, id_unq = test_id)
            tarfile = request.FILES["tarfile"]
            default_storage.save("test_files/%s/%s"%(test_new.id,tarfile.name), tarfile)
            answers_xml = request.FILES["answers_xml"]
            default_storage.save("test_files/%s/%s"%(test_new.id,answers_xml.name), answers_xml)
            return HttpResponse("OK")
        else:
            #print "ERROR:User does not exist"
            return HttpResponse("ERROR:User does not exist")
        
def results_upload(request):
    try:
        if request.method == "POST":
            login = request.POST.get('login', '')
            test_id = request.POST.get('test-id', '')
            points = request.POST.get('points', '')
            points_percentage = request.POST.get('points-percentage', '')
            test = get_object_or_404(Test, id_unq=test_id)
            if test.password:
                # results with test with password can be submited only once
                try:
                    Result.objects.get(user_id_unq=login, test_id_unq=test_id)
                    return HttpResponse("ERROR:Test already submited")
                except Result.DoesNotExist:
                    pass
                  
            result = Result(user_id_unq=login, test_id_unq=test_id, points=points, points_percentage=points_percentage)
            result.save()
            try:
                testuser = TestUser.objects.get(user_id_unq=login, test_id_unq=test_id)
                testuser.test_returned()
            except TestUser.DoesNotExist:
                pass
            results_xml = request.FILES["results_xml"]
            default_storage.save("results_files/%s/%s"%(result.id, results_xml.name), results_xml)
            return HttpResponse("OK")
        else:
            return HttpResponse("ERROR:Use POST")
    except:
#        print 'exception'
#        print sys.exc_info()
#        raise
        return HttpResponse("ERROR: Unhandled exception, contact administrator")

def test_list(request):
    if request.method == "GET":
        return HttpResponse("GET")
    elif request.method == "POST":
        user = User.objects.filter(login=request.POST.get("login"), password=request.POST.get("password"))
        if user:
            tests = user[0].test_set.all()
            return render_to_response('tests_list.html', {
                'tests': tests,
                })
        else:
            return HttpResponse("ERROR:User does not exist")
        
def test_list_public(request):
    tests = Test.objects.filter(password='')
    return render_to_response('tests_list.html', {'tests': tests})

def test_list_all(request):
    search_term = request.GET.get('search', '')
    category_name = request.GET.get('cat', '')
    category, created = Category.objects.get_or_create(name=category_name)
    if created:
        tests = []
    else:
        if search_term:
            tests = Test.objects.filter(category=category, title__icontains=search_term)
        else:
            tests = Test.objects.filter(category=category)
    return render_to_response('tests_list_all.html', {'tests': tests})

def test_delete(request, test_id):
    if request.method == "GET":
        return HttpResponse("GET")
    elif request.method == "POST":
        user = User.objects.filter(login=request.POST.get("login"), password=request.POST.get("password"))
        if user:
            test = user[0].test_set.filter(id_unq=test_id)
            if test:
                default_storage.delete("test_files/%s/questions.tar.bz2"%test[0].id)
                default_storage.delete("test_files/%s/answers.xml"%test[0].id)
                os.rmdir("test_files/%s"%test[0].id)
                test[0].delete()
                return HttpResponse("OK")
            else:
                return HttpResponse("ERROR:Test does not exist")
        else:
            return HttpResponse("ERROR:User does not exist")

    return HttpResponse("ERROR")

def questions_download(request):
    send = False

    if request.method != "POST":
        return HttpResponse("ERROR")

    test_id = request.POST.get("test-id")
    test = get_object_or_404(Test, id_unq=test_id)
    if not test:
#        print 'ERROR: Test does not exist'
        return HttpResponse("ERROR: Test does not exist")
        

    if test.password != '':
        user_login = request.POST.get("login", '')
        if user_login:# knut editor, test owner
            user_pass = request.POST.get("password", '')
            user = User.objects.filter(login=user_login, password=user_pass)
            if len(user)>0 and user[0].id == test.user.id:
                send = True
            else:
#                print user[0].id
#                print test.user.id
#                print 'ERROR: User does not exist'
                return HttpResponse("ERROR: User does not exist")
        else:# olpc app, test with password
            test_pass = request.POST.get("test-password", '')
            if test.password == test_pass:
                user_name = request.POST.get("user-name", '')
                testuser, created = TestUser.objects.get_or_create(user_id_unq=user_name, test_id_unq=test_id)
                if not created:
#                    print 'Test requested again'
                    return HttpResponse("ERROR")
                send = True
            else:
#                print 'ERROR: Wrong test password'
                return HttpResponse("ERROR")
    else:
        send = True

    if send:
        questions_file_name = "test_files/%s/questions.tar.bz2"%test.id
        wrapper = FileWrapper(file(questions_file_name))
        response = HttpResponse(wrapper, content_type="aplication/x-gtar")
        response["Content-Length"] = os.path.getsize(questions_file_name)
        return response
    
def results_list(request):
    send = False

    if request.method != "POST":
        return HttpResponse("ERROR")

    test_id = request.POST.get("test-id")
    user_login = request.POST.get("login", '')
    user_pass = request.POST.get("password", '')
    if not test_id or not user_login or not user_pass:
#        print 'ERROR: login, test-id and password required'
        return HttpResponse("ERROR: login, test-id and password required")
    
    test = Test.objects.filter(id_unq=test_id)
    if not test:
#        print 'ERROR: Test does not exist'
        return HttpResponse("ERROR: Test does not exist")

    test = test[0]
    user = User.objects.filter(login=user_login, password=user_pass)
    if len(user) > 0 and user[0].id == test.user.id:
        send = True
    else:
#        print 'ERROR: User does not exist'
        return HttpResponse("ERROR: User does not exist")
    
    if send:
        results = Result.objects.filter(test_id_unq=test_id)
        return render_to_response('results_list.html', {'results': results})
    else:
#        print 'ERROR: Couldnt find test results'
        return HttpResponse("ERROR: No test results")
    
def user_answers_download(request):
    try:
        if request.method != "POST":
            return HttpResponse("ERROR")
    
        test_id = request.POST.get("test-id")
        user_id = request.POST.get("user-id")
        user_login = request.POST.get("login", '')
        user_pass = request.POST.get("password", '')
        results_id = request.POST.get("result-id", '')
        if not test_id or not user_login or not user_pass or not user_id:
#            print 'ERROR: login, test-id and password required'
            return HttpResponse("ERROR: login, test-id and password required")
        
        user = User.objects.filter(login=user_login, password=user_pass)
        if len(user) != 1:
#            print 'ERROR: User does not exist'
            return HttpResponse("ERROR: User does not exist")
        user = user[0]
        
        result = Result.objects.get(user_id_unq=user_id, test_id_unq=test_id, pk=results_id)

        results_filename = "results_files/%s/results.xml" % result.id
        wrapper = FileWrapper(file(results_filename))
        response = HttpResponse(wrapper, content_type="aplication/xml")
        response["Content-Length"] = os.path.getsize(results_filename)
        return response
    except:
#        raise
#        print 'ERROR: Couldnt find test answers'
        return HttpResponse("ERROR: No test answers")


def answers_download(request):
    send = False

    if request.method != "POST":
        return HttpResponse("ERROR")

    test_id = request.POST.get("test-id")
    test = Test.objects.filter(id_unq=test_id)
    if not test:
#        print 'ERROR: Test does not exist'
        return HttpResponse("ERROR: Test does not exist")
    test = test[0]
        
    if test.password != '':
        user_login = request.POST.get("login", '')
        if user_login:# knut editor, test owner
            user_pass = request.POST.get("password", '')
            user = User.objects.filter(login=user_login, password=user_pass)
            if len(user)>0 and user[0].id == test.user.id:
                send = True
            else:
#                print 'ERROR: User does not exist'
                return HttpResponse("ERROR: User does not exist")
        else:
            test_pass = request.POST.get("test-password", '')
            if test.password == test_pass:
                send = True
            else:
#                print 'ERROR: Wrong test password'
                return HttpResponse("ERROR")
    else:
        send = True

    if send:
        questions_file_name = "test_files/%s/answers.xml"%test.id
        wrapper = FileWrapper(file(questions_file_name))
        response = HttpResponse(wrapper, content_type="aplication/xml")
        response["Content-Length"] = os.path.getsize(questions_file_name)
        return response 
    
def categories(request):
    categories = Category.objects.all()
    return render_to_response('categories.html', {'categories': categories,},
                              context_instance=RequestContext(request))
    
def category(request, category_id):
    cat = get_object_or_404(Category, pk=category_id)
    tests = Test.objects.filter(category=cat, password='')
    return render_to_response('category.html', {'tests': tests,},
                              context_instance=RequestContext(request))

