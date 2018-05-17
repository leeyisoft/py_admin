#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import random
import hmac

from decimal import Decimal

_PROTECTED_TYPES = (
    type(None), int, float, Decimal, datetime.datetime, datetime.date, datetime.time,
)

def _is_protected_type(obj):
    """Determine if the object instance is of a protected type.
    Objects of protected types are preserved as-is when passed to
    force_text(strings_only=True).
    """
    return isinstance(obj, _PROTECTED_TYPES)

class String():
    @staticmethod
    def constant_time_compare(val1, val2):
        """Return True if the two strings are equal, False otherwise."""
        return hmac.compare_digest(String.force_bytes(val1), String.force_bytes(val2))

    @staticmethod
    def safeunicode(obj, encoding='utf-8'):
        r"""s
        Converts any given object to unicode string.

            >>> safeunicode('hello')
            u'hello'
            >>> safeunicode(2)
            u'2'
            >>> safeunicode('\xe1\x88\xb4')
            u'\u1234'
        """
        t = type(obj)
        if t is unicode:
            return obj
        elif t is str:
            return obj.decode(encoding, 'ignore')
        elif t in [int, float, bool]:
            return unicode(obj)
        elif hasattr(obj, '__unicode__') or isinstance(obj, unicode):
            try:
                return unicode(obj)
            except Exception as e:
                return u""
        else:
            return str(obj).decode(encoding, 'ignore')

    @staticmethod
    def safestr(obj, encoding='utf-8'):
        r"""
        Converts any given object to utf-8 encoded string.

            >>> safestr('hello')
            'hello'
            >>> safestr(u'\u1234')
            '\xe1\x88\xb4'
            >>> safestr(2)
            '2'
        """
        if isinstance(obj, bytes):
            return obj.encode(encoding)
        elif isinstance(obj, str):
            return obj
        elif hasattr(obj, 'next'):  # iterator
            return itertools.imap(safestr, obj)
        else:
            return str(obj)

    @staticmethod
    def storify(mapping, *requireds, **defaults):
        """
        Creates a `storage` object from dictionary `mapping`, raising `KeyError` if
        d doesn't have all of the keys in `requireds` and using the default
        values for keys found in `defaults`.

        For example, `storify({'a':1, 'c':3}, b=2, c=0)` will return the equivalent of
        `storage({'a':1, 'b':2, 'c':3})`.

        If a `storify` value is a list (e.g. multiple values in a form submission),
        `storify` returns the last element of the list, unless the key appears in
        `defaults` as a list. Thus:

            >>> storify({'a':[1, 2]}).a
            2
            >>> storify({'a':[1, 2]}, a=[]).a
            [1, 2]
            >>> storify({'a':1}, a=[]).a
            [1]
            >>> storify({}, a=[]).a
            []

        Similarly, if the value has a `value` attribute, `storify will return _its_
        value, unless the key appears in `defaults` as a dictionary.

            >>> storify({'a':storage(value=1)}).a
            1
            >>> storify({'a':storage(value=1)}, a={}).a
            <Storage {'value': 1}>
            >>> storify({}, a={}).a
            {}

        Optionally, keyword parameter `_unicode` can be passed to convert all values to unicode.

            >>> storify({'x': 'a'}, _unicode=True)
            <Storage {'x': u'a'}>
            >>> storify({'x': storage(value='a')}, x={}, _unicode=True)
            <Storage {'x': <Storage {'value': 'a'}>}>
            >>> storify({'x': storage(value='a')}, _unicode=True)
            <Storage {'x': u'a'}>
        """
        _unicode = defaults.pop('_unicode', False)

        # if _unicode is callable object, use it convert a string to unicode.
        to_unicode = safeunicode
        if _unicode is not False and hasattr(_unicode, "__call__"):
            to_unicode = _unicode

        def unicodify(s):
            if _unicode and isinstance(s, str):
                return to_unicode(s)
            else:
                return s

        def getvalue(x):
            if hasattr(x, 'file') and hasattr(x, 'value'):
                return x.value
            elif hasattr(x, 'value'):
                return unicodify(x.value)
            else:
                return unicodify(x)

        stor = Storage()
        for key in requireds + tuple(mapping.keys()):
            value = mapping[key]
            if isinstance(value, list):
                if isinstance(defaults.get(key), list):
                    value = [getvalue(x) for x in value]
                else:
                    value = value[-1]
            if not isinstance(defaults.get(key), dict):
                value = getvalue(value)
            if isinstance(defaults.get(key), list) and not isinstance(value, list):
                value = [value]
            setattr(stor, key, value)

        for (key, value) in defaults.items():
            result = value
            if hasattr(stor, key):
                result = stor[key]
            if value == () and not isinstance(result, tuple):
                result = (result,)
            setattr(stor, key, result)

        return stor

    @staticmethod
    def force_bytes(s, encoding='utf-8', strings_only=False, errors='strict'):
        """
        Similar to smart_bytes, except that lazy instances are resolved to
        strings, rather than kept as lazy objects.

        If strings_only is True, don't convert (some) non-string-like objects.
        """
        # Handle the common case first for performance reasons.
        if isinstance(s, bytes):
            if encoding == 'utf-8':
                return s
            else:
                return s.decode('utf-8', errors).encode(encoding, errors)
        if strings_only and _is_protected_type(s):
            return s
        if isinstance(s, memoryview):
            return bytes(s)
        if isinstance(s, object) or not isinstance(s, str):
            return str(s).encode(encoding, errors)
        else:
            return s.encode(encoding, errors)

    @staticmethod
    def get_random_string(length=12,
                          allowed_chars='abcdefghijklmnopqrstuvwxyz'
                                        'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
        """
        Return a securely generated random string.

        The default length of 12 with the a-z, A-Z, 0-9 character set returns
        a 71-bit value. log_2((26+26+10)^12) =~ 71 bits
        """

        return ''.join(random.choice(allowed_chars) for i in range(length))
