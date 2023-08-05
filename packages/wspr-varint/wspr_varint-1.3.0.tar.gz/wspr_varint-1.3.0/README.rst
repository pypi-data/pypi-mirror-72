===========
wspr-varint
===========

.. image:: https://img.shields.io/pypi/v/wspr_varint.svg
        :target: https://pypi.python.org/pypi/wspr_varint

A variable length integer implementation for the wspr project.

API
---

VarInt

- from_int
- from_bytes
- to_int
- to_bytes
- int
- bytes

Example
-------

.. code-block:: python3

   from wspr_varint import VarInt
   variable_integer = VarInt.from_int(-1)
   variable_integer.to_int()
   variable_integer.to_bytes()
