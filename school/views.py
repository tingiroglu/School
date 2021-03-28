from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.core import serializers
import json
from django.contrib.auth.models import Permission
from django.contrib import messages
from django.contrib.auth.models import Group
# messages.add_message(request, messages.INFO, 'Hello world.')
from django.contrib.auth.decorators import permission_required
from django.db import IntegrityError
import datetime
from django.contrib import auth


def student_permission():
    try:
        grup = Group.objects.create(name="Student")
    except:
        pass


def teacher_permission():
    try:
        grup = Group.objects.create(name="Teachers")

    except:
        grup = Group.objects.get(name="Teachers")
        p1 = Permission.objects.get(codename='add_student')
        p2 = Permission.objects.get(codename='view_student')
        p3 = Permission.objects.get(codename='delete_student')
        p4 = Permission.objects.get(codename='change_student')
        grup.permissions.add(p1, p2, p3, p4)
        grup.save()


def manager_permission():
    try:
        grup = Group.objects.create(name="Manager")
    except:
        pass
    grup = Group.objects.get(name="Manager")
    p1 = Permission.objects.get(codename='add_student')
    p2 = Permission.objects.get(codename='view_student')
    p3 = Permission.objects.get(codename='delete_student')
    p4 = Permission.objects.get(codename='change_student')
    # p5 = Permission.objects.get(codename='add_teacher')
    # p6 = Permission.objects.get(codename='delete_teacher')
    p7 = Permission.objects.get(codename='view_teacher')
    # p8 = Permission.objects.get(codename='change_teacher')
    # p9 = Permission.objects.get(codename='add_class')
    p10 = Permission.objects.get(codename='view_class')
    # p11 = Permission.objects.get(codename='change_class')
    # p12 = Permission.objects.get(codename='delete_class')
    grup.permissions.add(p1, p2, p3, p4, p7, p10,)

    grup.save()


try:
    student_permission()
    teacher_permission()
    manager_permission()
except:
    pass


def index(request):
    print("ever burayı görmek için izni var")
    return render(request, "index.html")


def register(request):
    # User.objects.create_superuser(username="fatih",email="fatih.tingir97@gmail.com", password="fatih", user_type=4)
    # print(a)
    schools = School.objects.all()
    classess = Class.objects.filter(school=1)
    # data = serializers.serialize('json', classess)
    context = {
        "schools": schools,
        'classess': classess,
    }

    if request.POST:
        err = None
        # role_type 0 == manager
        username = request.POST['username']
        password = request.POST['password']
        role_types = int(request.POST.get('roles'))
        email = request.POST['email']
        school = request.POST['schoolslct']
        cls = request.POST['classSelect']
        if school == '4':
            messages.add_message(request, messages.ERROR, "Lütfen Okul Seçin")
            return redirect("register")

        if int(role_types) == 1:
            schl = School.objects.filter(name=school)
            print(schl)
            print(schl.get())
            try:
                school_manager_user = User.objects.create_user(username=username, email=email, password=password,
                                                               user_type=int(role_types), is_staff=True)
                print(school_manager_user)
                print(school_manager_user.id)
                schl_obj = schl.get()

                school_manager = SchoolManager.objects.create(fullname=username, schl_manager=schl_obj,
                                                              users=school_manager_user)
                # print(school_manager)
                # school_manager.users.add(school_manager_user)
                messages.add_message(request, messages.SUCCESS, "Tebrikler Okulun Müdür Artık Sizsiniz")

                my_group = Group.objects.get(name='Manager')
                my_group.user_set.add(school_manager_user)

                return redirect("index")
            except IntegrityError as ex:
                err = 2
                messages.add_message(request, messages.ERROR, "Zaten Bu Okulun Müdür var Lütfen Başka Okula Deneyin")
                return redirect("register")
            except Exception as Ex:
                print(Ex)
                err = 1
                User.delete(school_manager_user)
                School.delete(school_manager)
                messages.add_message(request, messages.ERROR, "Kayıt oluşturulamadı Kontrol Edip Tekrar Deneyiniz")
                return redirect("register")
            finally:
                if err == 2:
                    return redirect("register")
                if err is not None:
                    print("evet a var")
                    messages.add_message(request, messages.ERROR,
                                         "Kullanıcı Adı kullanılıyor Lütfen Başka deneyin")
                    return redirect("register")
                else:
                    return redirect("index")

        if int(role_types) == 2:
            schl = School.objects.filter(name=school)
            clss = Class.objects.filter(name=cls)

            try:
                teacher_user = User.objects.create_user(username=username, email=email, password=password,
                                                        user_type=int(role_types), is_staff=True)

                schl_obj = schl.get()
                clss_obj = clss.get()

                # teacher_user = User.objects.create(username=username, password=password,user_type=2)

                teacher = Teacher.objects.create(name=username, class_obj=clss_obj, school_ob=schl_obj,
                                                 users=teacher_user)
                my_group = Group.objects.get(name='Teachers')
                my_group.user_set.add(teacher_user)
                messages.add_message(request, messages.SUCCESS, "Tebrikler Seçtiğiniz Sınıfın Artık Öğretmeni Sizsiniz")

                return redirect("index")
            except IntegrityError as ex:
                messages.add_message(request, messages.ERROR, "Lütfen Okul Seciniz")
                return redirect("register")
            except Exception as Ex:
                err = 0
                print(Ex)
                print(teacher)
                if teacher is not None:
                    User.delete(teacher_user)
                    Teacher.delete(teacher)
                messages.add_message(request, messages.ERROR,
                                     "Bu Okuldaki Sınıfın Bir Öğretmeni Var Lütfen Başka Sınıf Deneyin")
                return redirect("register")
            # finally:
            #     if err is not None:
            #         print("evet a var")
            #         messages.add_message(request, messages.ERROR,
            #                              "Kullanıcı Adı kullanılıyor Lütfen Başka deneyin")
            #         return redirect("register")
            #     else:
            #         return redirect("index")

        if int(role_types) == 3:
            schl = School.objects.filter(name=school)
            clss = Class.objects.filter(name=cls)

            try:
                student_user = User.objects.create_user(username=username, email=email, password=password,
                                                        user_type=int(role_types), is_staff=True)

                schl_obj = schl.get()
                clss_obj = clss.get()

                student = Student.objects.create(fullname=username, classes=clss_obj, schools=schl_obj,
                                                 users=student_user)
                my_group = Group.objects.get(name='Student')
                my_group.user_set.add(student_user)
                messages.add_message(request, messages.SUCCESS, "Tebrikler Artık Seçtiğiniz Sınıfın Öğrencisisiniz.")

                return redirect("index")

            except IntegrityError as ex:
                messages.add_message(request, messages.ERROR, "Kullanıcı Adı Kullanılıyor")
                return redirect("register")
            except Exception as Ex:
                err = 0
                print(Ex)
                User.delete(student_user)
                Student.delete(student)
                messages.add_message(request, messages.ERROR,
                                     "Bu Sınıfta Böyle Bir öğrenci zaten var")
                return redirect("register")

    return render(request, 'schoolPage/register.html', context)


def getdetails(request):
    SchlName = request.GET['cnt']
    result_set = []
    answer = str(SchlName[1:-1])
    selected_class = School.objects.get(name=answer)
    all_class = selected_class.class_set.all()
    for classes in all_class:
        result_set.append({'name': classes.name})
    return HttpResponse(json.dumps(result_set), content_type='application/json')


def login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.add_message(request, messages.SUCCESS, message="Başarıyla Girş Yaptınız")
            return redirect('index')
        else:
            messages.add_message(request, messages.ERROR, message="Hatalı Username ya da Password")

            return redirect('login')
    else:
        return render(request, 'schoolPage/login.html')


def logout(request):
    try:
        request.session.delete()
    except:
        return redirect('login')
    return redirect('login')
