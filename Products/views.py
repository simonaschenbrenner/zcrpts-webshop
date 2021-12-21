from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from .forms import ProductForm, CommentForm
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
    context = {'all_the_products': Product.objects.all()}
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
            form.save()
        else:
            print(form.errors)

    # Comments
    comments = Comment.objects.filter(product=product)

    # Pictures
    pictures = Picture.objects.filter(product=product)

    context = {'that_one_product': product,
               'description': product.get_long_description(),
               'comments_for_that_one_product': comments,
               'rating': product.get_average_rating(),
               'comment_form': CommentForm}
    return render(request, 'product-detail.html', context)


def rate(request, pk: str, stars: int):
    product = Product.objects.get(id=int(pk))
    myuser = request.user
    product.rate(myuser, stars)
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






