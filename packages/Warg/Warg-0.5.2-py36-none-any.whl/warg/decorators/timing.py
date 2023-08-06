#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 14/11/2019
           """

__all__ = ["timeit"]

import contextlib
import functools
import time
from functools import wraps

import typing


def timeit(f: callable):
    """

    :param f:
    :type f:
    :return:
    :rtype:
    """

    @wraps(f)
    def wrapper(*args, **kwds):
        """

        :param args:
        :type args:
        :param kwds:
        :type kwds:
        :return:
        :rtype:
        """
        start_time = time.time()
        result = f(*args, **kwds)
        elapsed_time = time.time() - start_time
        print(f"{f} took {elapsed_time:.3f} seconds to compute")
        return elapsed_time, result

    return wrapper


def singleton(cls):
    """ Use class as singleton. """

    cls.__new_original__ = cls.__new__

    @functools.wraps(cls.__new__)
    def singleton_new(cls, *args, **kw):
        """

        @param cls:
        @type cls:
        @param args:
        @type args:
        @param kw:
        @type kw:
        @return:
        @rtype:
        """
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it

        cls.__it__ = it = cls.__new_original__(cls, *args, **kw)
        it.__init_original__(*args, **kw)
        return it

    cls.__new__ = singleton_new
    cls.__init_original__ = cls.__init__
    cls.__init__ = object.__init__

    return cls



class Timer( contextlib.AbstractContextManager):
  r"""**Measure execution time of function.**

  Can be used as context manager or function decorator, perform checkpoints
  or display absolute time from measurements beginning.

  **Used as context manager**::

      with Timer() as timer:
          ... # your operations
          print(timer) # __str__ calls timer.time() internally
          timer.checkpoint() # register checkpoint
          ... # more operations
          print(timer.checkpoint()) # time since last timer.checkpoint() call

      ... # even more operations
      print(timer) # time taken for the block, will not be updated outside of it

  When execution leaves the block, timer will be blocked. Last checkpoint and time taken
  to execute whole block will be returned by `checkpoint()` and `time()` methods respectively.

  **Used as function decorator**::

      @Timer()
      def foo():
          return 42

      value, time = foo()

  Parameters
  ----------
  function : Callable, optional
          No argument function used to measure time. Default: time.perf_counter

  """

  def __init__(self, function: typing.Callable = time.perf_counter):
    self.function = function

    self.start = self.function()
    self.last = self.start
    self.last_checkpoint = self.start

    self._exited: bool = False

  def time(self):
    """**Time taken since the object creation (measurements beginning).**

    Returns
    -------
    time-like
            Whatever `self.function() - self.function()` returns,
            usually fraction of seconds
    """
    if not self._exited:
      return self.function() - self.start
    return self.last - self.start

  def checkpoint(self):
    """**Time taken since last checkpoint call.**

    If wasn't called before, it is the same as as Timer creation time (first call returns
    the same thing as `time()`)

    Returns
    -------
    time-like
            Whatever `self.function() - self.function()` returns,
            usually fraction of seconds
    """
    if not self._exited:
      self.last_checkpoint = self.last
      self.last = self.function()
    return self.last - self.last_checkpoint

  def __call__(self, function):
    @functools.wraps(function)
    def decorated(*args, **kwargs):
      self.start = self.function()
      values = function(*args, **kwargs)
      self.__exit__()
      return values, self.time()

    return decorated

  def __exit__(self, *_, **__) -> None:
    self.last = self.function()
    self._exited: bool = True
    return False

  def __str__(self) -> str:
    return str(self.time())

if __name__ == '__main__':
  with Timer() as timer:
    print(timer) # __str__ calls timer.time() internally
    timer.checkpoint() # register checkpoint
    print(timer.checkpoint()) # time since last timer.checkpoint() call

  print(timer) # time taken for the block, will not be updated outside of it
  print()
  print(timer) # time taken for the block, will not be updated outside of it
  print()
  print(timer) # time taken for the block, will not be updated outside of it
  print()
  print()

  @Timer()
  def foo():
    return 42

  value, time = foo()
  print(time)
