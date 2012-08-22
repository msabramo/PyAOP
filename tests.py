from StringIO import StringIO
import sys
import unittest

from pyaop import AOP


class PyAOPTests(unittest.TestCase):

    def setUp(self):
        self.stringio = StringIO()

    def before_open_func(self, f, *args, **kwargs):
        self.stringio.write("before_open_func: f = %r, args = %r, kwargs = %r\n" % (f, args, kwargs))

    def after_open_func(self, f, *args, **kwargs):
        self.stringio.write("after_open_func: f = %r, args = %r, kwargs = %r\n" % (f, args, kwargs))

    def test_one_before_hook(self):
        with AOP(open) as open_aop:
            open_aop.add_before_hook(self.before_open_func)

            try:
                f = open("foo.txt")
            except IOError:
                pass

            self.assertEqual(self.stringio.getvalue(), "before_open_func: f = 'foo.txt', args = (), kwargs = {}\n")

    def test_one_after_hook(self):
        with AOP(open) as open_aop:
            open_aop.add_after_hook(self.after_open_func)

            try:
                f = open("foo.txt")
            except IOError:
                pass

            self.assertEqual(self.stringio.getvalue(), "after_open_func: f = 'foo.txt', args = (), kwargs = {}\n")

    def test_lots_of_hooks(self):
        with AOP(open) as open_aop, AOP(chr) as chr_aop, AOP(ord) as ord_aop:
            open_aop.add_before_hook(lambda f, *args, **kwargs: self.stringio.write("before open 1\n"))
            open_aop.add_before_hook(lambda f, *args, **kwargs: self.stringio.write("before open 2\n"))
            open_aop.add_after_hook(lambda f, *args, **kwargs: self.stringio.write("after open 1\n"))
            open_aop.add_after_hook(lambda f, *args, **kwargs: self.stringio.write("after open 2\n"))
            chr_aop.add_before_hook(lambda f, *args, **kwargs: self.stringio.write("before chr 1\n"))
            chr_aop.add_before_hook(lambda f, *args, **kwargs: self.stringio.write("before chr 2\n"))
            ord_aop.add_before_hook(lambda f, *args, **kwargs: self.stringio.write("before ord\n"))

            try:
                ord('A')
                chr(65)
                f = open("foo.txt")
            except IOError:
                pass

            self.assertEqual(
                self.stringio.getvalue(),
                "before ord\nbefore chr 1\nbefore chr 2\nbefore open 1\nbefore open 2\nafter open 1\nafter open 2\n")

