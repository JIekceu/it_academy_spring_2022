from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import ListView

from . import forms
from . import models


# Create your views here.

class MaterialListView(LoginRequiredMixin, ListView):
    queryset = models.Material.objects.all()
    context_object_name = 'materials'
    template_name = "materials/all_materials.html"


# def all_materials(request):
#    materials = models.Material.objects.all()
#    return render(request, "materials/all_materials.html",
#                 {"materials": materials})


@login_required
def detailed_material(request, yy, mm, dd, slug):
    material = get_object_or_404(models.Material,
                                 publish__year=yy,
                                 publish__month=mm,
                                 publish__day=dd,
                                 slug=slug)

    if request.method == 'POST':
        comment_form = forms.CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.material = material
            new_comment.save()
        return redirect(material)   # POST redirect GET
    else:
        comment_form = forms.CommentForm()
    return render(request, "materials/detailed_material.html",
                  {"material": material,
                   "form": comment_form})


def share_material(request, material_id):
    material = get_object_or_404(models.Material, id=material_id)
    if request.method == 'POST':
        form = forms.EmailMaterialForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            material_uri = request.build_absolute_uri(
                material.get_absolute_url()
            )
            subject = 'Someone shared with your material ' + material.title
            body_template = ('On our resource someone shares material with '
                             'you. \n\nlink to material: {link}\n\ncomment: '
                             '{comment}')
            body = body_template.format(link=material_uri,
                                        comment=cd['comment'])
            send_mail(subject, body, 'admin@my.com', (cd['to_email'],))
    else:
        form = forms.EmailMaterialForm()
    return render(request,
                  'materials/share.html',
                  {'material': material, 'form': form})


def create_material(request):
    if request.method == 'POST':
        material_form = forms.MaterialForm(request.POST)
        if material_form.is_valid():
            new_material = material_form.save(commit=False)
            new_material.author = User.objects.first()
            new_material.slug = new_material.title.replace(' ', '-')
            new_material.save()
            return render(request,
                          "materials/detailed_material.html",
                          {"material": new_material})
    else:
        material_form = forms.MaterialForm()
    return render(request,
                  'materials/create.html',
                  {'form': material_form})


def custom_login(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                username=cd['username'],
                password=cd['password']
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('User was logged in')
                else:
                    return HttpResponse('User account is not activated')
            else:
                return HttpResponse('Incorrect User/Password')
    else:
        form = forms.LoginForm()
        return render(request, 'login.html', {'form': form})

def view_profile(request):
    return render(request, 'profile.html')


def register(request):
    if request.method == "POST":
        user_form = forms.RegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            models.Profile.objects.create(user=new_user, photo="unknown.jpg")
            return render(request, 'registration/registration_complete.html',
                          {'new_user': new_user})
        else:
            return HttpResponse('bad credentials')
    else:
        user_form = forms.RegistrationForm(request.POST)
        return render(request, 'registration/register_user.html', {"form": user_form})


def _get_forms(request, post_method):
    user_form = forms.UserEditForm(request.POST, instance=request.user)

    kw = {'instance': request.user.profile}
    if post_method: kw = kw.update({'files': request.FILES})

    profile_form = forms.ProfileEditForm(request.POST, **kw)
    return user_form, profile_form


def edit_profile(request):
    post_method = request.method == "POST"
    user_form, profile_form = _get_forms(request, post_method)

    if post_method:
        if profile_form.is_valid():
            if user_form.is_valid():
                if not profile_form.cleaned_data['photo']:
                    profile_form.cleaned_data['photo'] = request.user.profile.photo
                profile_form.save()
                user_form.save()
                return render(request, 'profile.html')
    else:
        return render(request, 'edit_profile.html',
                      {'user_form': user_form, 'profile_form': profile_form})













