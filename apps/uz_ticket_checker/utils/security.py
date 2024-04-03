from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


def encode_uid(pk):
    return force_str(urlsafe_base64_encode(force_bytes(pk)))


def decode_uid(pk):
    return force_str(urlsafe_base64_decode(pk))
