# django-safe-fields

Save field value encrypted to database.

## Install

```shell
pip install django-safe-fields
```

## Shipped Fields

**Mixins**

- SafeFieldMixinBase
- SafeStringFieldMixin
- SafeIntegerFieldMixin

**Fields**

- SafeCharField
- SafeTextField
- SafeEmailField
- SafeURLField
- SafeGenericIPAddressField
- SafeIntegerField

## Note

1. Default cipher is aes-128-ecb. It keeps the same with mysql's aes_encrypt and aes_decrypt when server variable block_encryption_mode=aes-128-ecb.
1. Default password is settings.SECRET_KEY, but we STRONGLY suggest you use different password for every different field.

## Usage

**pro/settings.py**

```
INSTALLED_APPS = [
    ...
    'django_safe_fields',
    ...
]
```

1. Insert `django_safe_fields` into INSTALLED_APPS.

**app/models.py**

```
from django.db import models
from django.conf import settings
from django_safe_fields.fields import SafeCharField
from django_safe_fields.fields import SafeGenericIPAddressField
from django_safe_fields.fields import SafeIntegerField
from fastutils.cipherutils import S12Cipher
from fastutils.cipherutils import HexlifyEncoder

class Account(models.Model):
    username = SafeCharField(max_length=64)
    name = SafeCharField(max_length=64, cipher_class=S12Cipher)
    email = SafeCharField(max_length=128, null=True, blank=True, cipher=S12Cipher(password=settings.SECRET_KEY, encoder=HexlifyEncoder(), force_text=True))
    last_login_ip = SafeGenericIPAddressField(max_length=256, null=True, blank=True, password="THIS FIELD PASSWORD")
    level = SafeIntegerField(null=True, blank=True)

    def __str__(self):
        return self.username

```

1. All fields will be stored with encryption.
1. AesCipher is a strong cipher.
1. With aes encryption, you can NOT search partly, only the `exact` search rule will be accepted.
1. With aes encryption, you can NOT sort.
1. S12Cipher is a week cipher that let you search the field partly and also let you sort with the field.
1. IvCihper is a week cipher for integer field that let you sort with the field.

## Releases

### v0.1.1 2020-06-23

- Fix problem in objects.get that double encrypt the raw data.

### v0.1.0 2020-06-20

- First release.
