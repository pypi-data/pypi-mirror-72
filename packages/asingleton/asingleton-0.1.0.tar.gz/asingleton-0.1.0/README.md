# asingleton

```python3
>>> from asingleton import singleton

>>> print(singleton.__doc__)

    singleton(cls, 
                attr_name='instance', 
                disable_name_mangling=False, 
                not_just_this_class=False) -> cls
    
    singleton(attr_name='instance', 
                disable_name_mangling=False, 
                not_just_this_class=False)(cls) -> cls
    
    >>> @singleton
    ... class Service:
    ...     pass
    ... 
    >>> Service() is Service.instance
    True
    >>> Service()  # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
        ...
    AssertionError: There is already an instance of type <class '...Service'>;
    it can be accessed through the class attribute 'Service.instance'.
    
    >>> @singleton('__instance')
    ... class Service:
    ...     @classmethod
    ...     def get_instance(cls):
    ...         return cls.__instance
    ... 
    >>> Service() is Service.get_instance()
    True
    >>> Service.__instance
    Traceback (most recent call last):
        ...
    AttributeError: type object 'Service' has no attribute '__instance'
    
    >>> @singleton(not_just_this_class=True)
    ... class Service:
    ...     pass
    ... 
    >>> class Apache(Service):
    ...     pass
    ... 
    >>> Apache() is Apache.instance
    True
    >>> Apache()  # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
        ...
    AssertionError: There is already an instance of type <class '...Apache'>;
    it can be accessed through the class attribute 'Apache.instance'.
    
    >>> class Service:
    ...     def __new__(cls, *args, **kwargs):
    ...         """My custom __new__"""
    ...         return super().__new__(cls, *args, **kwargs)
    ...     original_new = __new__
    ... 
    >>> singleton(Service) is Service
    True
    >>> Service.__new__ is Service.original_new
    False
    >>> Service.__new__.__wrapped__ is Service.original_new
    True
    >>> Service.__new__.__doc__
    'My custom __new__'
    
```
