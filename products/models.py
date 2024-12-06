from django.db import models


class AbstractModel(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Category(AbstractModel):
    parent = models.ForeignKey('self', on_delete=models.CASCADE,
                               null=True, blank=True)


class Tag(AbstractModel):
    pass


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 null=True, blank=True, related_name='product_categories')  # category_id
    tags = models.ManyToManyField(Tag, blank=True)
    title = models.CharField(max_length=255)
    text = models.TextField(null=True, blank=True)
    price = models.FloatField()
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def tag_names(self):
        return [tag.name for tag in self.tags.all()]


STARS = (
    (i, '* ' * i) for i in range(1, 6)
)


class Review(models.Model):
    text = models.TextField()
    stars = models.IntegerField(choices=STARS, default=5)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='reviews')

    def __str__(self):
        return self.text
