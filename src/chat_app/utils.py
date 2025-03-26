import os
from django.utils.text import slugify

def unique_slugify(instance, slug):
    """
    This function takes an instance and a slug and returns a unique slug by adding a 
    random string at the end of the slug if the slug already exists in the database.
    """
    model = instance.__class__
    unique_slug = slug
    counter = 1
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f'{slug}-{counter}'
        counter += 1
    return unique_slug


def get_image_upload_path(instance, filename):
    """
    This function takes an instance and a filename and returns the path where the image
    should be saved.
    """
    model_name = instance.__class__.__name__.lower()
    return f"/uploads/{model_name}/{slugify(filename)}"
    