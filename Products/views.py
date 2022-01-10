from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.shortcuts import redirect, render
from .forms import ProductForm, CommentForm, PictureForm, SearchForm
from .models import Product, Comment, Picture, LicenseKey


def product_search(request, search_term: str, min_stars: int):

    if request.method == 'POST':
        print("in product_search() POST")
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            if min_stars is None:
                min_stars = 0
            if search_term is None:
                search_results = Product.objects.all()
            else:
                search_results = Product.objects.filter(
                    Q(rating__gte=min_stars) & (
                        Q(title__icontains=search_term) |
                        Q(short_description__icontains=search_term) |
                        Q(long_description__icontains=search_term)
                    )
                )
        else:
            print(search_form.errors)

        context = {
            'search_form': search_form,
            'all_the_products': search_results
        }
        return render(request, 'product-list.html', context)


def product_list(request):

    if request.method == 'POST':
        print("in product_list() POST")
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            min_stars = search_form.cleaned_data['min_stars']
            search_term = search_form.cleaned_data['search_term']
            print("FORM CONTENTS:", min_stars, search_term)
            if not len(min_stars) > 0:
                min_stars = 0
            if not len(search_term) > 0:
                search_results = Product.objects.all().filter(average_rating__gte=min_stars)
            else:
                search_results = Product.objects.filter(
                    Q(title__icontains=search_term) |
                    Q(short_description__icontains=search_term) |
                    Q(long_description__icontains=search_term)
                ).filter(average_rating__gte=min_stars)
        else:
            print(search_form.errors)

        context = {
            'search_form': search_form,
            'all_the_products': search_results
        }

    else:
        context = {
            'search_form': SearchForm,
            'all_the_products': Product.objects.all(),
            'all_the_pics': Picture.objects.all()
        }

    return render(request, 'product-list.html', context)


@staff_member_required(login_url='/useradmin/login/')
def product_create(request):

    if request.method == 'POST':
        print("in Post")
        form = ProductForm(request.POST, request.FILES)

        picForm = PictureForm(request.POST, request.FILES)
        print(picForm)

        form.instance.myuser = request.user
        if form.is_valid() and picForm.is_valid():
            form.save()
            print("Saved a new product")
            picForm.instance.product = form
            picture = Picture(product=form, picture=picForm['pictures'])
            # picture.save()

        else:
            print(form.errors)

        return redirect('product-list')
    else:
        form = ProductForm
        picForm = PictureForm
        context = {'form': form,
                   'pictureForm': picForm}
        return render(request, 'product-create.html', context)


def product_detail(request, **kwargs):

    product_id = kwargs['pk']
    product = Product.objects.get(id=product_id)
    # Add comment
    if request.method == 'POST':
        form = CommentForm(request.POST)
        form.instance.myuser = request.user
        form.instance.product = product
        if form.is_valid():
            form.save()
            messages.success(request, "Review has been sent. Thank you")
        else:
            print(form.errors)

    # Comments
    comments = Comment.objects.filter(product=product)

    context = {'that_one_product': product,
               'description': product.get_long_description(),
               'comments_for_that_one_product': comments,
               'comment_form': CommentForm,
               }
    return render(request, 'product-detail.html', context)


def rate(request, pk: str, stars: int):
    product = Product.objects.get(id=int(pk))
    myuser = request.user
    product.rate(myuser, stars)
    return redirect('product-detail', pk=pk)


def vote(request, pk: int, commentid: int, is_helpful: str):
    comment = Comment.objects.get(id=int(commentid))
    myuser = request.user
    comment.vote_helpful(myuser, is_helpful)
    return redirect('product-detail', pk=pk)


def download_license(request, pk: int):
    product = Product.objects.get(id=pk)
    license_keys = LicenseKey.objects.filter(productID=product.id)
    context = {'that_one_product': product,
               'license_key': license_keys[0]}
    if request.method == 'POST':
        #TODO pdf download
        return render(request, 'download-page.html', context)
    else:
        return render(request, 'download-page.html', context)


# TODO Filter flagged
@staff_member_required(login_url='/useradmin/login/')
def comment_list(request, **kwargs):
    context = {'all_comments': Comment.objects.all()}
    return render(request, 'comment-list.html', context)