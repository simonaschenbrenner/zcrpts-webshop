from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from Carts.models import Cart
from .forms import CommentForm, EditReviewForm, ProductForm, SearchForm
from .models import Comment, Product, LicenseKey


def product_list(request):

    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            min_stars = search_form.cleaned_data['min_stars']
            search_term = search_form.cleaned_data['search_term']
            if not len(min_stars) > 0:  # String is empty
                min_stars = 0
            if not len(search_term) > 0:  # String is empty
                search_results = Product.objects.all() \
                    .filter(average_rating__gte=min_stars)
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

    else:  # request.method == 'GET'
        context = {
            'search_form': SearchForm,
            'all_the_products': Product.objects.all(),
        }

    return render(request, 'product-list.html', context)


@staff_member_required(login_url='/useradmin/login/')
def product_create(request, **kwargs):

    if 'pid' in kwargs:  # Edit an existing product
        product = Product.objects.get(id=kwargs['product_id'])
    else:
        product = None

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        form.instance.product = product
        form.instance.myuser = request.user
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        return redirect('product-list')

    else:  # request.method == 'GET'
        form = ProductForm(instance=product)
        context = {'form': form}
        return render(request, 'product-create.html', context)


def product_detail(request, **kwargs):

    product = Product.objects.get(id=kwargs['pid'])

    if request.method == 'POST':
        if 'addToCart' in request.POST:
            Cart.add_item(request.user, product)
            context = {'that_one_product': product}
            return render(request, 'product-detail.html', context)

        elif 'addComment' in request.POST:
            form = CommentForm(request.POST)
            form.instance.myuser = request.user
            form.instance.product = product
            if form.is_valid():
                try:
                    form.save()
                    product.rate()
                except IntegrityError as e:
                    print(e)
                    messages.error(request,
                                   'You already submitted a review. \
                                   Please edit your past review')
            else:
                print(form.errors)
                messages.error(request,
                               'Review could not be saved')

    comments = Comment.objects.filter(product=product)
    context = {'product': product,
               'description': product.get_long_description(),
               'comments': comments,
               'comment_form': CommentForm,
               'logged_in_user': request.user}
    return render(request, 'product-detail.html', context)


def comment_vote(request, pid: int, cid: int, up_or_down: str):
    comment = Comment.objects.get(id=int(cid))
    myuser = request.user
    comment.vote_helpful(myuser, up_or_down)
    return redirect('product-detail', pid=pid)


def comment_flag(request, pid: int, cid: int):
    comment = Comment.objects.get(id=int(cid))
    comment.flag()
    return redirect('product-detail', pid=pid)


@staff_member_required(login_url='/useradmin/login/')
def comment_unflag(request, cid: int):
    comment = Comment.objects.get(id=int(cid))
    comment.unflag()
    return redirect('comment-list-all')


def comment_edit(request, pid: int, cid: int):
    # instance = get_object_or_404(Comment, id=int(commentid))  # TODO delete
    comment = Comment.objects.get(id=cid)

    if request.method == 'POST':
        form = EditReviewForm(request.POST, instance=comment)
        form.instance.user = request.user
        if form.is_valid():
            form.save()
            form.instance.product.rate()
        else:
            print(form.errors)
            messages.error(request,
                           'Review could not be saved')
        return redirect('product-detail', id=pid)
    else:
        form = EditReviewForm(instance=comment)
        context = {'form': form}
        return render(request, 'comment-edit.html', context)


# def download_license(request, pk: int):
#     product = Product.objects.get(id=pk)
#     license_keys = LicenseKey.objects.filter(productID=product.id)
#     context = {'that_one_product': product,
#                'license_key': license_keys[0]}
#     if request.method == 'POST':
#         # TODO pdf download
#         return render(request, 'download-page.html', context)
#     else:
#         return render(request, 'download-page.html', context)


@staff_member_required(login_url='/useradmin/login/')
def comment_list_all(request, **kwargs):
    context = {'all_comments': Comment.objects.all(), 'only_flagged': False}
    return render(request, 'comment-list.html', context)


@staff_member_required(login_url='/useradmin/login/')
def comment_list_flagged(request, **kwargs):
    comments = Comment.objects.filter(is_flagged=True)
    context = { 'all_comments': comments, 'only_flagged': True}
    return render(request, 'comment-list.html', context)


def comment_delete(request, **kwargs):
    comment_id = kwargs['commentid']
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    if 'productid' in kwargs:
        return redirect('product-detail', pk=kwargs['productid'])
    else:
        return redirect('comment-list')