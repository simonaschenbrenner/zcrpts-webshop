import uuid
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg, Max, Min
from django.http import HttpResponse
from django.template.defaultfilters import slugify


def get_image_filename(instance, filename):
    title = instance.product.title
    slug = slugify(title)
    return "product_pictures/%s-%s" % (slug, filename)


class Product(models.Model):
    title = models.CharField(max_length=50)
    version = models.CharField(max_length=100)
    price = models.FloatField(default=0)
    short_description = models.CharField(max_length=200)
    long_description = models.TextField(max_length=1000, blank=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    pdf = models.FileField(upload_to='product_pdfs/', blank=True, null=True)
    myuser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['title', 'version']
        unique_together = ['title', 'version']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def get_long_description(self):
        if self.long_description:  # long_description is not empty
            return self.long_description
        else:
            return self.short_description

    def get_full_title(self):
        return self.title + '(' + self.version + ')'

    def image_url(self):
        if self.image.url:
            return self.image.url
        else:
            url = ''
            return url

    def get_average_rating(self):
        ratings = Comment.objects.filter(product=self).aggregate(Avg('rate'))
        return ratings['rate__avg']

    def get_max_rating(self):
        ratings = Comment.objects.filter(product=self).aggregate(Max('rate'))
        return ratings['rate__max']

    def get_max_rating(self):
        ratings = Comment.objects.filter(product=self).aggregate(Min('rate'))
        return ratings['rate__min']

    # Todo
    def rate(self, myuser, stars):
        pass
        # Rating.objects.create(product=self, myuser=myuser, stars=stars)

    def __str__(self):
        return self.title + ' (' + self.version + ')'

    def __repr__(self):
        return self.get_full_title() + ' / ' + self.version + ' / ' + self.type


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    myuser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_flagged = models.BooleanField(default=False)
    rate = models.IntegerField(validators=[
        MaxValueValidator(5),
        MinValueValidator(1)
    ])

    class Meta:
        ordering = ['product', 'timestamp']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        unique_together = ['product', 'myuser']

    # def vote_helpful(self, myuser, up_or_down):
    #     if up_or_down == 'down':
    #         U_or_O = 'D'
    #     else:
    #         U_or_O = 'U'
    #     if Vote.objects.filter(comment=self, myuser=myuser).exists():
    #         return Vote.objects.filter(comment=self, myuser=myuser).update(up_or_down = U_or_O)
    #     vote = Vote.objects.create(comment=self, myuser=myuser, up_or_down=U_or_O)
    #     return vote

    def vote_helpful(self, myuser, up_or_down):
        if up_or_down == 'down':
            U_or_O = 'D'
        else:
            U_or_O = 'U'
        vote = Vote.objects.filter(comment=self, myuser=myuser)
        if vote.exists():
            for v in vote:
                if str(v) == U_or_O:
                    return vote.delete()
                else:
                    return vote.update(up_or_down = U_or_O)
        new_vote = Vote.objects.create(comment=self, myuser=myuser, up_or_down=U_or_O)
        return new_vote

    def get_upvotes(self):
        upvotes = Vote.objects.filter(up_or_down='U', comment=self)
        return upvotes

    def get_downvotes(self):
        downvotes = Vote.objects.filter(up_or_down='D', comment=self)
        return downvotes

    def get_upvotes_count(self):
        return len(self.get_upvotes())

    def get_downvotes_count(self):
        return len(self.get_downvotes())

    def get_text_prefix(self):
        if len(self.title) > 50:
            return self.title[:50] + '...'
        else:
            return self.title

    # report inappropriate review

    def set_flag(self, myuser):
        print(self.is_flagged)
        if not self.is_flagged:
            self.is_flagged = True
            self.save()
            # flag = Flag.objects.create(comment=self, myuser=myuser, is_flagged=self.is_flagged)
            # return flag

    def __str__(self):
        return self.myuser.username + ' commented on ' + self.product.title + ': "' + self.title + '"'

    def __repr__(self):
        return 'Product Comment: "' + self.title + '"' + ' on ' + self.product.title + ' by ' + self.myuser.username \
               + ' at ' + str(self.timestamp)


# class Flag(models.Model):
#     comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
#     myuser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     is_flagged = models.BooleanField(default=False)
#
#     class Meta:
#         ordering = ['comment', 'myuser']
#         # unique_together = ['is_flagged', 'myuser']
#         verbose_name = 'Comment Flag'
#         verbose_name_plural = 'Comment Flags'
#
#     def delete_flag(self):
#         not_flagged = Comment.objects.filter(is_flagged='0')
#         Flag.objects.filter(comment=not_flagged).delete()

class Vote(models.Model):
    VOTE_TYPES = [
        ('U', 'up'),
        ('D', 'down'),
    ]
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    myuser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    up_or_down = models.CharField(max_length=1, default=0, choices=VOTE_TYPES)

    class Meta:
        ordering = ['comment', 'myuser']
        unique_together = ['up_or_down', 'comment']
        verbose_name = 'Comment Voting'
        verbose_name_plural = 'Comment Votings'

    def __str__(self):
        return self.up_or_down

    def __repr__(self):
        return 'Comment Rating: ' + self.up_or_down + ' on ' + self.comment.title + ' by ' + self.myuser.username


class Picture(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    pictures = models.FileField(upload_to=get_image_filename)

    class Meta:
        ordering = ['product']
        unique_together = ['product']
        verbose_name = 'Product Picture'
        verbose_name_plural = 'Product Pictures'

    def __str__(self):
        return 'Picture ' + self.product.version + ' of ' + self.product.title

    def __repr__(self):
        return 'Product Picture ' + self.product.version + ' of ' + self.product.title + '(' + self.picture.url + ')'


class Screenshot(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    mediaURL = models.URLField(primary_key=True, default=uuid.uuid4, editable=False)


class LicenseKey(models.Model):
    productID = models.ForeignKey(Product, on_delete=models.CASCADE)
    # TODO LicenseKey muss gehashed werden
    licenseKey = models.CharField(max_length=200)
