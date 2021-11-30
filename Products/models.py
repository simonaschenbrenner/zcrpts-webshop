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
    myuser = models.ForeignKey(settings.AUTH_USER_MODEL,
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

    def get_upvotes(self):
        upvotes = Vote.objects.filter(up_or_down='U',
                                      product=self)
        return upvotes

    def get_upvotes_count(self):
        return len(self.get_upvotes())

    def get_downvotes(self):
        downvotes = Vote.objects.filter(up_or_down='D',
                                        product=self)
        return downvotes

    def get_downvotes_count(self):
        return len(self.get_downvotes())

    def vote(self, myuser, up_or_down):
        U_or_D = 'U'
        if up_or_down == 'down':
            U_or_D = 'D'
        vote = Vote.objects.create(up_or_down=U_or_D,
                                   myuser=myuser,
                                   product=self
                                   )

    def __str__(self):
        return self.title + ' (' + self.author + ')'

    def __repr__(self):
        return self.get_full_title() + ' / ' + self.author + ' / ' + self.type


class Comment(models.Model):
    text = models.TextField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    myuser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

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
        return self.get_comment_prefix() + ' (' + self.myuser.username + ')'

    def __repr__(self):
        return self.get_comment_prefix() + ' (' + self.myuser.username + ' / ' + str(self.timestamp) + ')'


class Vote(models.Model):
    VOTE_TYPES = [
        ('U', 'up'),
        ('D', 'down'),
    ]

    up_or_down = models.CharField(max_length=1,
                                  choices=VOTE_TYPES,
                                 )
    timestamp = models.DateTimeField(auto_now_add=True)
    myuser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.up_or_down + ' on ' + self.product.title + ' by ' + self.myuser.username
