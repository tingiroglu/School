from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *
from django.urls import reverse
from django.utils.html import format_html
from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.contrib import messages
from django.db import IntegrityError, DatabaseError
from itertools import chain


def linkify(field_name):
    """
    Converts a foreign key value into clickable links.

    If field_name is 'parent', link text will be str(obj.parent)
    Link will be admin url for the admin url for obj.parent.id:change
    """

    def _linkify(obj):
        linked_obj = getattr(obj, field_name)
        if linked_obj is None:
            return '-'
        app_label = linked_obj._meta.app_label
        model_name = linked_obj._meta.model_name
        view_name = f'admin:{app_label}_{model_name}_change'
        link_url = reverse(view_name, args=[linked_obj.pk])
        return format_html('<a href="{}">{}</a>', link_url, linked_obj)

    _linkify.short_description = field_name  # Sets column name
    return _linkify


# Register your models here.
@admin.register(User)
class Users(admin.ModelAdmin):
    list_display = ("user_type",)


@admin.register(School)
class Schools(admin.ModelAdmin):
    list_display = ("name",)


# class ClassInline(admin.TabularInline):
#     model = Teacher

@admin.register(Class)
class Classes(admin.ModelAdmin):
    # list_display = ("name",)
    model = Class
    model2 = SchoolManager

    def get_queryset(self, request):
        if request.user.is_superuser:
            # print("fdsfsa")
            queryset = Class.objects.all()
            # print(request.user.__class__())

            return queryset

        elif request.user.user_type == 1:

            manager_obj = SchoolManager.objects.filter(fullname=request.user.username)
            manager = manager_obj.get()

            queryset = self.model.objects.filter(school_id=manager.schl_manager.id)

            return queryset


@admin.register(Teacher)
class Teachers(admin.ModelAdmin):
    # list_display = ("name",)
    # list_display = [
    #     "name",
    #     linkify(field_name="school_ob"),
    #     linkify(field_name="class_obj"),
    # ]

    model = Teacher
    model2 = SchoolManager

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):

        if request.user.is_superuser:
            if db_field.name == "class_obj":
                query_set = Class.objects.all()
                kwargs["queryset"] = query_set
            elif db_field.name == "school_ob":
                query_set = School.objects.all()
                kwargs["queryset"] = query_set

            return super(Teachers, self).formfield_for_foreignkey(db_field, request, **kwargs)

        elif request.user.user_type == 1:

            if db_field.name == "class_obj":

                school_manager_obj = SchoolManager.objects.filter(fullname=request.user.username)
                school_manager = school_manager_obj.get()
                classes_obj = Class.objects.filter(school_id=school_manager.schl_manager.id)
                kwargs["queryset"] = classes_obj


            elif db_field.name == "school_ob":
                school_manager_obj = SchoolManager.objects.filter(fullname=request.user.username)
                school_manager = school_manager_obj.get()
                school_obj = School.objects.filter(id=school_manager.schl_manager.id)
                kwargs["queryset"] = school_obj

            elif db_field.name == 'users':
                kwargs['disabled'] = True
            return super(Teachers, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        if request.user.is_superuser:

            queryset = self.model.objects.all()
            return queryset

        elif request.user.user_type == 1:

            manager_obj = SchoolManager.objects.filter(fullname=request.user.username)
            manager = manager_obj.get()

            queryset = self.model.objects.filter(school_ob_id=manager.schl_manager.id)

            return queryset


@admin.register(SchoolManager)
class SchoolManagers(admin.ModelAdmin):
    list_display = ("fullname",)


@admin.register(Student)
class Students(admin.ModelAdmin):
    # list_display = ("fullname",)
    # list_display = [
    #     "fullname",
    #     linkify(field_name="classes"),
    #


    # model1 =Teacher
    model = Teacher
    model1 = Student
    model2 = SchoolManager
    model3 = Class

    def change_view(self, request, object_id, form_url='', extra_context=None):
        try:

            return super(Students, self).change_view(request, object_id, form_url, extra_context)
        except (IntegrityError, DatabaseError) as e:
            print("değişim hatası")
            request.method = 'GET'
            messages.add_message(request, messages.ERROR, "Bu kullanıcı Adı Kullanılıyor Lütfen Başka deneyin")
            # messages.error(request,e)
            return super(Students, self).change_view(request, object_id, form_url, extra_context)
    def save_model(self, request, obj, form, change):
        # print(obj.classes.id)
        # print(obj.schools.id)
        # std_user = User.objects.create_user(username=username, email=email, password=password,
        #                          user_type=int(role_types), is_staff=True)
        # std = Teacher.objects.create(name=username, class_obj=clss_obj, school_ob=schl_obj,users=teacher_user)

        try:
            user_filter = User.objects.filter(username=obj.fullname)

            if user_filter.exists() ==  False:
                std_user = User.objects.create_user(username=obj.fullname, password=obj.fullname, email=obj.fullname + "@gmail.com", is_staff=True, user_type=3)

                schl_obj = School.objects.filter(id = obj.schools.id)
                cls_obj = Class.objects.filter(id = obj.classes.id)
                schl = schl_obj.get()
                cls = cls_obj.get()

                std = Student.objects.create(fullname=obj.fullname, classes=cls, schools=schl,users=std_user)

                messages.add_message(request, messages.INFO, 'Kullanıcı Başarıyla Oluşturuldu Şifresi ve Username,' + obj.fullname)
            else:
                messages.add_message(request, messages.ERROR, "Bu kullanıcı Adı Kullanılıyor Lütfen Başka deneyin")


                return HttpResponseRedirect(request.path)

        except Exception as ex:
            print("işte geliyor hataaaa")
            # return HttpResponseRedirect(request.path)
            return  super(Students, self).save_model(request, obj, form,change)
        # finally:
        #     print("noo")
        #     return super(Students, self).save_model(request, obj, form, change)
        #     Student.delete(std)
        #     print("hataaaa")
        #     return redirect("index")
        # finally:
        #     return super(Students, self).save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if request.user.is_superuser:
            if db_field.name == "classes":
                query_set = Class.objects.all()
                kwargs["queryset"] = query_set
            elif db_field.name == "schools":
                query_set = School.objects.all()
                kwargs["queryset"] = query_set
            return super(Students, self).formfield_for_foreignkey(db_field, request, **kwargs)

        #ogretmen islemleri
        elif request.user.user_type == 2:
            if db_field.name == "classes":
                teacher_obj = Teacher.objects.filter(name=request.user.username)
                teacher = teacher_obj.get()
                classes_obj = Class.objects.filter(school_id=teacher.school_ob.id)
                kwargs["queryset"] = classes_obj

            elif db_field.name == "schools":
                teacher_obj = Teacher.objects.filter(name=request.user.username)
                teacher = teacher_obj.get()
                school_obj = School.objects.filter(id=teacher.school_ob.id)
                kwargs["queryset"] = school_obj
                # kwargs['disabled'] = True

            elif db_field.name == 'users':
                kwargs['disabled'] = True

            return super(Students, self).formfield_for_foreignkey(db_field, request, **kwargs)
        # Müdür İşlemleri
        elif request.user.user_type == 1:
            if db_field.name == "classes":
                school_managers = SchoolManager.objects.filter(fullname=request.user.username)
                school_mng = school_managers.get()
                classes_obj = Class.objects.filter(school_id=school_mng.schl_manager.id)
                kwargs["queryset"] = classes_obj

            elif db_field.name == "schools":
                school_managers = SchoolManager.objects.filter(fullname=request.user.username)
                school_mng = school_managers.get()
                school_obj = School.objects.filter(id=school_mng.schl_manager.id)
                kwargs["queryset"] = school_obj
            elif db_field.name == 'users':
                kwargs['disabled'] = True
            return super(Students, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):

        if request.user.is_superuser:
            queryset = Student.objects.all()
            # print(request.user.__class__())

            return queryset

        elif request.user.user_type == 2:

            teacher_obj = Teacher.objects.filter(name=request.user.username)

            teacher = teacher_obj.get()
            queryset = self.model1.objects.filter(classes=teacher.class_obj.id)

            ogr_name = queryset.values('fullname')
            readonly_fields = ('fullname',)

            return queryset

        elif request.user.user_type == 1:

            manager_obj = SchoolManager.objects.filter(fullname=request.user.username)
            manager = manager_obj.get()

            queryset = Student.objects.filter(schools_id=manager.schl_manager.id)
            return queryset
