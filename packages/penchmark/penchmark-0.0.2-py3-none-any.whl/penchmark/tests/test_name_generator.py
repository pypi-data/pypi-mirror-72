import functools

from penchmark import NameGenerator


def _fn0():
    pass


class _Cls0:
    def simple_method(self):
        pass

    @classmethod
    def class_method(cls):
        pass

    @staticmethod
    def static_method():
        pass

    def __call__(self):
        pass


def test_name_generator():
    name_generator = NameGenerator()

    partial_fn = functools.partial(max, 1)
    assert name_generator(partial_fn) == 'functools.partial'

    prefix = 'penchmark.tests.test_name_generator.'
    assert name_generator(lambda x: x) == prefix + 'lambda'
    assert name_generator(lambda x: x) == prefix + 'lambda-2'

    def local_fn1():
        pass

    class LocalCls1:
        def simple_method(self):
            pass

        @classmethod
        def class_method(cls):
            pass

        @staticmethod
        def static_method():
            pass

        def __call__(self):
            pass

    assert name_generator(local_fn1) == prefix + 'local_fn1'
    assert name_generator(LocalCls1()) == prefix + 'LocalCls1'
    assert name_generator(LocalCls1.simple_method) == prefix + 'LocalCls1.simple_method'
    assert name_generator(LocalCls1.class_method) == prefix + 'LocalCls1.class_method'
    assert name_generator(LocalCls1.static_method) == prefix + 'LocalCls1.static_method'

    assert name_generator(_fn0) == prefix + '_fn0'
    assert name_generator(_Cls0()) == prefix + '_Cls0'
    assert name_generator(_Cls0.simple_method) == prefix + '_Cls0.simple_method'
    assert name_generator(_Cls0.class_method) == prefix + '_Cls0.class_method'
    assert name_generator(_Cls0.static_method) == prefix + '_Cls0.static_method'
