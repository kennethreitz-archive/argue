# -*- coding: utf-8 -*-

# Command exceptions
class CommandException(Exception):
    'Base class for command exceptions'

class AmbiguousCommand(CommandException):
    'Raised if command is ambiguous'

class UnknownCommand(CommandException):
    'Raised if command is unknown'

class ParseError(CommandException):
    'Raised on error in command line parsing'

class Abort(CommandException):
    'Abort execution'

class FOError(CommandException):
    'Raised on trouble with argue configuration'
