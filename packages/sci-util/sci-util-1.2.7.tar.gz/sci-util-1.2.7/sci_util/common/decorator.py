#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: violinsolo
# Created on 2019-07-16


# ======
# print fn
# ======
def fn_temporary_not_use(func):
    # print(func.__name__)
    def _wrapper(*args, **kwargs):
        print(f'[Warning] fn:"{func.__name__}" is only temporary, ** TRY NOT TO INVOKE IT! **')
        fn_res = func(*args, **kwargs)
        return fn_res

    return _wrapper


if __name__ == '__main__':

    @fn_temporary_not_use
    def _fn_no_use(a, b):
        return a+b

    print(_fn_no_use(1, 3))
