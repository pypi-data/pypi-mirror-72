from enum import Enum


class HookNames(Enum):
    before_start = 'before_start'
    after_stop = 'after_stop'


# class HookHandler(object):
#
#     def __init__(self, handler):
#         super().__init__()
#         self._handler = handler
#
#     def __call__(self, *args, **kwargs):
#         self._handler(self._driver, self._driver.context)
