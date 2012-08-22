import contextlib


@contextlib.contextmanager
def AOP(func):
    class AOPClass(object):
        def __init__(self):
            self.before_hooks = []
            self.after_hooks = []

        def add_before_hook(self, before_hook):
            self.before_hooks.append(before_hook)

        def add_after_hook(self, after_hook):
            self.after_hooks.append(after_hook)

        def call_hooks(self, hooks, *args, **kwargs):
            for hook in hooks:
                hook(*args, **kwargs)

        def replacement_func(self, *args, **kwargs):
            self.call_hooks(self.before_hooks, *args, **kwargs)

            try:
                ret = self.orig_func(*args, **kwargs)
            finally:
                self.call_hooks(self.after_hooks, *args, **kwargs)

            return ret

    aop_obj = AOPClass()

    if hasattr(func, '__call__'):
        func = func.__name__

    aop_obj.orig_func = __builtins__[func]
    __builtins__[func] = aop_obj.replacement_func
    yield aop_obj
    __builtins__[func] = aop_obj.orig_func
