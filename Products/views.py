from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.forms import modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, ListView
from .forms import ProductForm, CommentForm, PictureForm, EditReviewForm
from .models import Product, Comment, Picture, LicenseKey


class ProductListView(ListView):
    model = Product
    context_object_name = 'all_the_products'  # Default: object_list
    template_name = 'product-list.html'  # Default: product_list.html


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'that_one_product'  # Default: product
    template_name = 'product-detail.html'  # Default: product_detail.html


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product-create.html'  # Default: product_form.html
    success_url = reverse_lazy('product-list')

    def form_valid(self, form):
        form.instance.myuser = self.request.user
        return super().form_valid(form)


def product_create(request):

    if request.method == 'POST':
        print("in Post")
        form = ProductForm(request.POST, request.FILES)
        form.instance.myuser = request.user
        if form.is_valid():
            form.save()
            print("Saved a new product")
        else:
            print(form.errors)

        return redirect('product-list')
    else:
        form = ProductForm
        context = {'form': form}
        return render(request, 'product-create.html', context)


def product_list(request):
    context = {'all_the_products': Product.objects.all(),
               'all_the_pics': Picture.objects.all()}
    return render(request, 'product-list.html', context)


def product_detail(request, **kwargs):
    product_id = kwargs['pk']
    product = Product.objects.get(id=product_id)
    # Add comment
    if request.method == 'POST':
        form = CommentForm(request.POST)
        form.instance.myuser = request.user
        form.instance.product = product
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Review has been submitted. Thank you")
            except IntegrityError:
                return HttpResponse("Already submitted a review")
        else:
            print(form.errors)
            return HttpResponse("Some error")
    # Comments
    comments = Comment.objects.filter(product=product)

    context = {'that_one_product': product,
               'description': product.get_long_description(),
               'comments_for_that_one_product': comments,
               'comment_form': CommentForm,
               'logged_in_user': request.user,
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


def flag(request, pk: int, commentid: int):
    comment = Comment.objects.get(id=int(commentid))
    myuser = request.user
    try:
        comment.set_flag(myuser)
    except ObjectDoesNotExist:
        print("already flagged")
        return HttpResponse("You already flagged")

    return redirect('product-detail', pk=pk)


def update_review(request, pk: int, commentid: int):
    instance = get_object_or_404(Comment, id=int(commentid))
    if request.method == 'POST':
        reviewForm = EditReviewForm(request.POST, instance=instance)
        reviewForm.instance.user = request.user
        if reviewForm.is_valid():
            reviewForm.save()
        else:
            pass
            print(reviewForm.errors)
        return redirect('product-detail', pk=pk)
    else:
        reviewForm = EditReviewForm(instance=instance)
        context = {'form': reviewForm}
        return render(request, 'review-update.html', context)


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


def comment_delete(request, **kwargs):
    comment_id = kwargs['commentid']
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return redirect('product-detail', pk=kwargs['pk'])
    # if request.method == 'POST':
    #     print('deleted the comment')
    #     comment.delete()
    #     return redirect('product-detail', pk=kwargs['pk'])



# class CommentEditView(EditReviewForm):
#     model = Comment
#     form_class = EditReviewForm
#     template_name = 'review-update.html'  # Default: product_form.html
#     success_url = reverse_lazy('product-detail')
