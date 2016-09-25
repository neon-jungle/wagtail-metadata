from django.conf import settings


def get_image_model_string():
    try:
        image_model = settings.WAGTAILIMAGES_IMAGE_MODEL
    except AttributeError:
        image_model = 'wagtailimages.Image'
    return image_model
