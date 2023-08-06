import os
from django.db.models import CharField
from django.utils.http import urlsafe_base64_encode as b64encode


def generate_random_field():
    return b64encode(os.urandom(20))


class RandomCharField(CharField):
    description = "A random field meant for URL-safe identifiers"

    def __init__(self, **kwargs):
        kwargs['max_length'] = 27

        super().__init__(**kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_length"]

        return name, path, args, kwargs

    def pre_save(self, model_instance, add):
        """
        This is used to ensure that we auto-set values if required.
        See CharField.pre_save
        """
        value = super().pre_save(model_instance, add)
        if not value:
            value = generate_random_field()
            setattr(model_instance, self.attname, value)
        return value
