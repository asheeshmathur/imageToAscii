from threading import Thread

'''
Custom Thread Class, because we have to return a value from function.
Our solution has two part, GUI part and Processing Part.
GUI portion selects the file and all parameters and hand it over to processing ccode.
This  returns the actual contents, the ascii image

This class encapsulates the result

Reference
https://coderslegacy.com/python/get-return-value-from-thread/
'''
class CustomThread(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = []

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return

