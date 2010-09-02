# -*- coding: utf-8 -*-

import sys
import inspect
import getopt
import traceback

from exceptions import * 


write = sys.stdout.write
err = sys.stderr.write


def trim(docstring):
	"""Intelligently undent given docstring."""
	if not docstring:
		return ''
	# Convert tabs to spaces (following the normal Python rules)
	# and split into a list of lines:
	lines = docstring.expandtabs().splitlines()
	# Determine minimum indentation (first line doesn't count):
	indent = sys.maxint
	for line in lines[1:]:
		stripped = line.lstrip()
		if stripped:
			indent = min(indent, len(line) - len(stripped))
	# Remove indentation (first line is special):
	trimmed = [lines[0].strip()]
	if indent < sys.maxint:
		for line in lines[1:]:
			trimmed.append(line[indent:].rstrip())
	# Strip off trailing and leading blank lines:
	while trimmed and not trimmed[-1]:
		trimmed.pop()
	while trimmed and not trimmed[0]:
		trimmed.pop(0)
	# Return a single string:
	return '\n'.join(trimmed)



def guess_options(func):
    args, varargs, varkw, defaults = inspect.getargspec(func)
    for name, option in zip(args[-len(defaults):], defaults):
        try:
            sname, default, hlp = option
            yield (sname, name.replace('_', '-'), default, hlp)
        except TypeError:
            pass

def guess_usage(func, options):
    usage = '%name '
    if options:
        usage += '[OPTIONS] '
    args, varargs = inspect.getargspec(func)[:2]
    argnum = len(args) - len(options)
    if argnum > 0:
        usage += args[0].upper()
        if argnum > 1:
            usage += 'S'
    elif varargs:
        usage += '[%s]' % varargs.upper()
    return usage

def catcher(target, help_func):
    '''Catches all exceptions and prints human-readable information on them
    '''
    try:
        return target()
    except UnknownCommand, e:
        err("unknown command: '%s'\n" % e)
    except AmbiguousCommand, e:
        err("command '%s' is ambiguous:\n    %s\n" %
            (e.args[0], ' '.join(e.args[1])))
    except ParseError, e:
        err('%s: %s\n' % (e.args[0], e.args[1]))
        help_func(e.args[0])
    except getopt.GetoptError, e:
        err('error: %s\n' % e)
        help_func()
    except FOError, e:
        err('%s\n' % e)
    except KeyboardInterrupt:
        err('interrupted!\n')
    except SystemExit:
        raise
    except:
        err('unknown exception encountered')
        raise

    raise Abort

def call_cmd(name, func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TypeError:
            if len(traceback.extract_tb(sys.exc_info()[2])) == 1:
                raise ParseError(name, "invalid arguments")
            raise
    return inner

def call_cmd_regular(func, opts):
    def inner(*args, **kwargs):
        funcargs, _, varkw, defaults = inspect.getargspec(func)
        if len(args) > len(funcargs):
            raise TypeError('You have supplied more positional arguments'
                            ' than applicable')

        funckwargs = dict((lname.replace('-', '_'), default)
                          for _, lname, default, _ in opts)
        if 'help' not in (defaults or ()) and not varkw:
            funckwargs.pop('help', None)
        funckwargs.update(kwargs)
        return func(*args, **funckwargs)
    return inner

def replace_name(usage, name):
    if '%name' in usage:
        return usage.replace('%name', name, 1)
    return name + ' ' + usage

def sysname():
    name = sys.argv[0]
    if name.startswith('./'):
        return name[2:]
    return name

try:
    from functools import wraps
except ImportError:
    def wraps(wrapped, assigned=('__module__', '__name__', '__doc__'),
              updated=('__dict__',)):
        def inner(wrapper):
            for attr in assigned:
                setattr(wrapper, attr, getattr(wrapped, attr))
            for attr in updated:
                getattr(wrapper, attr).update(getattr(wrapped, attr, {}))
            return wrapper
        return inner