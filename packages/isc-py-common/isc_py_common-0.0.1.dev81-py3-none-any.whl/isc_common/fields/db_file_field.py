from django.db.models import FileField


class DbFileField(FileField):
    def __init__(self, verbose_name=None, name=None, upload_to='', storage=None, **kwargs):
        kwargs.setdefault('max_length', 500)
        kwargs.setdefault('null', True)
        kwargs.setdefault('blank', True)
        def_str = '/blob/filename/mimetype'
        super().__init__(verbose_name=verbose_name, name=name, upload_to=f"{upload_to}{def_str}" if upload_to.find(def_str) == -1 else upload_to, storage=storage, **kwargs)
