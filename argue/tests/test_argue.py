#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argue

@argue.command(usage='%name [-n] MESSAGE')
def main(message, nonewline=('n', False, 'don\'t print a newline')):
    ''' Simple echo program for this and that.
	    And this is a test.
	    Whoot.
	'''
    sys.stdout.write(message)
    if not nonewline:
        sys.stdout.write('\n')

if __name__ == '__main__':
    main()