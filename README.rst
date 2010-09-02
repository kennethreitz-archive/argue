Argue
=====

Argue is a command line parser, intended to make writing command line
applications easy and painless. It uses built-in Python types (lists,
dictionaries, etc) to define options, which makes configuration clear and
concise. Additionally it contains possibility to handle subcommands (e.g.
``git commit`` or ``svn obliterate``).

Quick example
-------------

That's an example of an option definition::

  import sys
  import argue

  @argue.command(usage='%name [-n] MESSAGE')
  def main(message,
           nonewline=('n', False, 'don\'t print a newline')):
      'Simple echo program'
      sys.stdout.write(message)
      if not nonewline:
          sys.stdout.write('\n')

  if __name__ == '__main__':
      main()

Running this program will print the help::

  echo.py [-n] MESSAGE

  Simple echo program

  options:

   -n --nonewline  don't print a newline
   -h --help       show help

I think this mostly describes what's going on, except that I'd like to mention
one interesting feature - if you are using long name for option, you can use
only partial name, for example ``./echo.py --nonew`` a is valid command
line. This is also true for subcommands: read about that and everything else
you'd like to know in `documentation`_.

.. _documentation: http://hg.piranha.org.ua/opster/docs/
