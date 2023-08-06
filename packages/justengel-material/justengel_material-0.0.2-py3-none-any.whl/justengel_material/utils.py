from typing import ClassVar


__all__ = ['Message']


class Message:
    msg_type: str
    msg: str

    MESSAGE_TYPES: ClassVar = {
        'debug': "rounded yellow",
        'info': "rounded light-blue",
        'success': "rounded green",
        'warning': "orange",
        'error': "red",
        }

    @property
    def msg_class(self):
        return self.MESSAGE_TYPES.get(self.msg_type, 'rounded light-blue')
