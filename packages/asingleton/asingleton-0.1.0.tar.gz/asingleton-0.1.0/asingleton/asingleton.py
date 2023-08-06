from functools import wraps


def singleton(*args, **kwargs):
    """
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
    ...         \"""My custom __new__\"""
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
    """
    default_attr_name = 'instance'
    default_disable_name_mangling = False
    default_not_just_this_class = False
    
    def decorator(cls):
        original_cls = cls
        original_new = cls.__new__
        
        def __new__(cls, *args, **kwargs):
            if not_just_this_class or cls is original_cls:
                if not disable_name_mangling and attr_name.startswith('__') \
                        and not attr_name.endswith('__'):
                    effective_attr_name = f'_{cls.__name__}{attr_name}'
                else:
                    effective_attr_name = attr_name
                
                assert effective_attr_name not in cls.__dict__ or \
                        type(getattr(cls, effective_attr_name)) is not cls, \
                        f"There is already an instance of type {cls}; " \
                        "it can be accessed through the class attribute " \
                        f"'{cls.__name__}.{attr_name}'."
                
                setattr(cls, effective_attr_name, 
                        original_new(cls, *args, **kwargs))
                return getattr(cls, effective_attr_name)
            else:
                return original_new(cls, *args, **kwargs)
        
        __new__.__wrapped__ = cls.__new__
        
        # Only mimic {cls.__new__} if it belong to {cls}.
        if '__new__' in cls.__dict__:
            wraps(cls.__new__)(__new__)
        
        cls.__new__ = __new__
        return cls
    
    if args and isinstance(args[0], type) or 'cls' in kwargs:
        def singleton(cls, attr_name=default_attr_name, 
                    disable_name_mangling=default_disable_name_mangling,
                    not_just_this_class=default_not_just_this_class):
            return (cls, attr_name, disable_name_mangling, not_just_this_class)
        
        (cls, 
        attr_name, 
        disable_name_mangling, 
        not_just_this_class) = singleton(*args, **kwargs)
        return decorator(cls)
    else:
        def singleton(attr_name=default_attr_name, 
                    disable_name_mangling=default_disable_name_mangling,
                    not_just_this_class=default_not_just_this_class):
            return (attr_name, disable_name_mangling, not_just_this_class)
        
        (attr_name, 
        disable_name_mangling, 
        not_just_this_class) = singleton(*args, **kwargs)
        return decorator
