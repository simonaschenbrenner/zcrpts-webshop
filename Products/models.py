from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg, Max, Min
from django.template.defaultfilters import slugify


class Product(models.Model):
    title = models.CharField(max_length=50)
    version = models.CharField(max_length=10)
    price = models.FloatField(default=0)
    short_description = models.CharField(max_length=200)
    long_description = models.TextField(max_length=1000, blank=True)
    logo = models.ImageField(upload_to='product_logos/', blank=False)
    screenshot = models.ImageField(upload_to='product_screenshots/',
                                   blank=False)
    pdf = models.FileField(upload_to='product_pdfs/', blank=False)
    featured = models.BooleanField(default=False)
    operating_system = models.CharField(max_length=20)
    language = models.CharField(max_length=20)
    tested_with = models.CharField(max_length=100)
    script = models.FileField(upload_to='product_scripts/', blank=False)
    average_rating = models.PositiveSmallIntegerField(
        default=0,
        validators=[MaxValueValidator(5)])
    myuser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)

    class Meta:
        ordering = ['title', 'version']
        unique_together = ['title', 'version']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def get_long_description(self):
        if self.long_description:
            return self.long_description
        else:
            return self.short_description

    def get_full_title(self):
        return self.title + ' (' + self.version + ')'

    def rate(self):
        self.average_rating = Comment.objects.filter(product=self) \
            .aggregate(average_rating=Avg('rating'))['average_rating']
        self.save()

    def __str__(self):
        return self.get_full_title()

    # TODO
    def __repr__(self):
        return self.get_full_title() + ' / ' + self.version + ' / '


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    myuser = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    is_flagged = models.BooleanField(default=False)
    rating = models.IntegerField(validators=[
        MaxValueValidator(5),
        MinValueValidator(1)
    ])

    class Meta:
        ordering = ['product', 'timestamp']
        unique_together = ['product', 'myuser']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def vote_helpful(self, myuser, up_or_down):
        if up_or_down == 'down':
            u_or_d = 'D'
        else:
            u_or_d = 'U'
        vote = Vote.objects.filter(comment=self, myuser=myuser)
        if vote.exists():
            for v in vote:
                if str(v) == u_or_d:
                    return vote.delete()
                else:
                    return vote.update(up_or_down=u_or_d)
        new_vote = Vote.objects.create(
            comment=self,
            myuser=myuser,
            up_or_down=u_or_d)
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

    def flag(self):
        if not self.is_flagged:
            self.is_flagged = True
            self.save()

    def unflag(self):
        if self.is_flagged:
            self.is_flagged = False
            self.save()

    def __str__(self):
        return self.myuser.username + ' commented on ' + self.product.title \
               + ': "' + self.title + '"'

    def __repr__(self):
        return 'Product Comment: "' + self.title + '"' + ' on ' \
               + self.product.title + ' by ' + self.myuser.username + ' at ' \
               + str(self.timestamp) + ' with ' + str(self.rating) + ' stars'


class Vote(models.Model):
    VOTE_TYPES = [
        ('U', 'up'),
        ('D', 'down'),
    ]
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    myuser = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    up_or_down = models.CharField(max_length=1, default=0, choices=VOTE_TYPES)

    class Meta:
        ordering = ['comment', 'myuser']
        unique_together = ['up_or_down', 'comment']
        verbose_name = 'Comment Voting'
        verbose_name_plural = 'Comment Votings'

    def __str__(self):
        return self.up_or_down

    def __repr__(self):
        return 'Comment Rating: ' + self.up_or_down + ' on '\
               + self.comment.title + ' by ' + self.myuser.username


class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    myuser = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    stars = models.PositiveSmallIntegerField(default=0,
                                             validators=[MaxValueValidator(5)])

    class Meta:
        ordering = ['product', 'myuser']
        unique_together = ['product', 'myuser']
        verbose_name = 'Product Rating'
        verbose_name_plural = 'Product Ratings'

    def __str__(self):
        return self.myuser.username + ' gave ' + self.product.title + ' '\
               + self.stars + ' stars'

    def __repr__(self):
        return 'Product Rating: ' + self.stars + ' on ' + self.product.title\
               + ' by ' + self.myuser.username


def get_image_filename(instance, filename):
    title = instance.product.title
    slug = slugify(title)
    return "product_pictures/%s-%s" % (slug, filename)


class LicenseKey(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # TODO LicenseKey muss gehashed werden
    license_key = models.CharField(max_length=24)
