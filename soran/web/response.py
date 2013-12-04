# -*- coding: utf-8 -*-
from flask import jsonify

def result(message='', status_code=400, ok=False, **kwards):
    return jsonify(status_code=status_code,
                   message=message,
                   ok=ok,
                   **kwards)


def notfound(message=''):
    return result(status_code=404, message=message)


def badrequest(message=''):
    return result(status_code=400, message=message)


def forbidden(message=''):
    return result(status_code=403, message=message)


def ok(message='', **kwards):
    return result(status_code=200, message=message, ok=True, **kwards)
