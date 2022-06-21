from django.shortcuts import render, redirect
from main.models import PhotoGraphy, Category
from django.contrib import messages
from main.model_form import PhotoCreationForm
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DeleteView


# continue from here dude
def categoryListView(request, *args, **kwargs):
    category = PhotoCreationForm()
    # category_random = Category.objects.filter("?")
    # print(category_random)
    # category_

    # for c in category:
    #     print(c.)
    # category_image = Category.objects.get('?')
    context = {
        'form': category
    }
    return render(request, 'main/index.html', context)


class DeletePhotogreaphyView(DeleteView):
    model = PhotoGraphy



class PhotographyListView(ListView):
    model = PhotoGraphy
    template_name = 'list_view.html'
    paginate_by = 40


def create_photography(request, *args, **kwargs):
    create_form = PhotoCreationForm()
    categories = Category.objects.all()
    if request.method == "POST":
        create_form = PhotoCreationForm(request.POST)
        if create_form.is_valid():
            project = create_form.save(commit=False)
            title = create_form.cleaned_data.get("title")
            category_name = create_form.cleaned_data.get('category')
            category, created = Category.objects.get_or_create(category_of_photo=category_name)
            project.category = category
            project.user = request.user
            project.save()

            message = f"{title} created as successful"
            messages.success(request, message)
            return redirect('profile', username=request.user.username)
    context = {
        'categories': categories,
        'form': create_form
    }
    return render(request, 'main/create_form.html', context)


def update_photography(request, title):
    form = PhotoCreationForm(instance=request.user)
    photography = PhotoGraphy.objects.get(title=title)
    categories = Category.objects.all()

    if request.user != photography.user:
        return PermissionDenied

    if request.method == "POST":
        form = PhotoCreationForm(request.POST, instance=photography)
        if form.is_valid():
            category_title = request.POST.get('category')
            category, created = Category.objects.get_or_create(category_of_photo=category_title)
            update = form.save(commit=False)
            update.category = category
            update.save()
            return redirect("detail-view")
    context = {
        'form': form,
        'category': categories
    }
    return render(request, 'main/update_form.html', context)
