import uuid
from datetime import date
from django.conf import settings
from django.db import models


class Product(models.Model):
    PRODUCT_TYPES = [
        ('H', 'Hardcover'),  # Wert und lesbare Form
        ('P', 'Paperback'),
        ('E', 'E-book'),
        ('A', 'Audio book'),
    ]

    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100,
                                blank=True)
    author = models.CharField(max_length=50)
    pages = models.IntegerField()  # Must call function to take effect
    date_published = models.DateField(blank=True,
                                      default=date.today,
                                      )
    type = models.CharField(max_length=1,
                            choices=PRODUCT_TYPES,
                            )
    userID = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='product_created_by',
                               related_query_name='product_created_by',
                               )

    class Meta:
        ordering = ['title', '-type']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def check_date_published(self):
        print('----- In Product.check_date_published():', self.date_published, 'vs.', date.today())

        if self.date_published > date.today():
            print('----- Warning: date_published is in the future')
            return False
        else:
            return True

    def get_full_title(self):
        return_string = self.title
        if self.subtitle:  # if subtitle is not empty
            return_string = self.title + ': ' + self.subtitle
        return return_string

    def get_helpful(self):
        helpful = Vote.objects.filter(isHelpful='Y',
                                      product=self)
        return helpful

    def get_helpful_count(self):
        return len(self.get_helpful())

    def get_notHelpful(self):
        notHelpful = Vote.objects.filter(isHelpful='N',
                                         product=self)
        return notHelpful

    def get_notHelpful_count(self):
        return len(self.get_notHelpful())

    def vote(self, userID, isHelpful):
        Y_or_N = 'Y'
        if isHelpful == 'NO':
            Y_or_N = 'N'
        Vote.objects.create(isHelpful=Y_or_N,
                            userID=userID,
                            product=self
                            )

    def __str__(self):
        return self.title + ' (' + self.author + ')'

    def __repr__(self):
        return self.get_full_title() + ' / ' + self.author + ' / ' + self.type


class Comment(models.Model):
    IS_HELPFUL = [
        ('Y', 'YES'),
        ('N', 'NO'),
    ]

    title = models.TextField(max_length=100)
    text = models.TextField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    userID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    productID = models.ForeignKey(Product, on_delete=models.CASCADE)
    isFlagged = models.BooleanField
    isHelpful = models.CharField(max_length=1, choices=IS_HELPFUL)

    class Meta:
        ordering = ['timestamp']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def get_comment_prefix(self):
        if len(self.text) > 50:
            return self.text[:50] + '...'
        else:
            return self.text

    def __str__(self):
        return self.get_comment_prefix() + ' (' + self.userID.username + ')'

    def __repr__(self):
        return self.get_comment_prefix() + ' (' + self.userID.username + ' / ' + str(self.timestamp) + ')'


class Vote(models.Model):
    VOTE_TYPES = [
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ]

    stars = models.CharField(max_length=1,
                             choices=VOTE_TYPES,
                             )
    userID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    productID = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.stars + ' on ' + self.product.title + ' by ' + self.userID.username

class Screenshot(models.Model):
    productID = models.ForeignKey(Product, on_delete=models.CASCADE)
    mediaURL = models.URLField(primary_key=True, default=uuid.uuid4, editable=False)


