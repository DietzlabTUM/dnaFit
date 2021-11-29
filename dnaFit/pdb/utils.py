#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2021  Elija Feigl
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see https://www.gnu.org/licenses/gpl-3.0.html.

import string
from typing import Dict


def int_2_cifSegID(number: int) -> str:
    upper = string.ascii_uppercase
    n_upper = len(upper)
    if number < n_upper:
        return upper[number]
    else:
        n = number - n_upper
        i = n // n_upper
        j = n % n_upper
        return upper[i] + upper[j]


def int_2_chimeraSegID(number: int) -> str:
    char = string.ascii_uppercase + string.ascii_lowercase + string.digits
    n_char = len(char)
    i = number // n_char
    j = number % n_char
    return char[i] + char[j]


digits_upper = string.digits + string.ascii_uppercase
digits_lower = digits_upper.lower()
digits_upper_values = dict([pair for pair in zip(digits_upper, range(36))])
digits_lower_values = dict([pair for pair in zip(digits_lower, range(36))])


def _decode(digits_values: Dict[str, int], inp_string: str) -> int:
    """ decodes string using digits_values associations for each character"""
    result = 0
    n = len(digits_values)
    for c in inp_string:
        result *= n
        result += digits_values[c]
    return result


def h36_2_int(inp_string: str) -> int:
    """ decodes hybrid36 string to integer"""
    width = len(inp_string)
    n_baseDigits = 10 * 36 ** (width - 1)
    n_baseChar = 26 * 36 ** (width - 1)
    max_int = 10 ** width

    if inp_string.isdigit():
        return int(inp_string)
    shift = max_int
    if inp_string[0] in digits_upper_values:
        shift -= n_baseDigits
        return _decode(digits_upper_values, inp_string=inp_string) + shift

    elif inp_string[0] in digits_lower_values:
        shift += (n_baseChar - n_baseDigits)
        return _decode(digits_lower_values, inp_string=inp_string) + shift
    raise ValueError("invalid number literal.")


def _encode(digits: str, value: int) -> str:
    """ encodes value using the given digits"""
    if value == 0:
        return digits[0]
    n = len(digits)
    result = []
    while value != 0:
        rest = value // n
        result.append(digits[value - rest * n])
        value = rest
    result.reverse()
    return "".join(result)


def int_2_h36(number: int, width: int) -> str:
    """ integer to hybrid36 string with "width" digits"""
    n_baseDigits = 10 * 36 ** (width - 1)
    n_baseChar = 26 * 36 ** (width - 1)
    max_int = 10 ** width

    if number < max_int:
        return "{:{width}d}".format(number, width=width)
    number -= max_int
    if number < n_baseChar:
        return _encode(digits_upper, (number + n_baseDigits))
    number -= n_baseChar
    if number < n_baseChar:
        return _encode(digits_lower, (number + n_baseDigits))
    else:
        raise ValueError("value out of range.")
