from django.db import models


class PaddlePaymentManager(models.Manager):

    def create_paddle_(self, title):
        book = self.create(title=title)
        # do something with the book
        return book
