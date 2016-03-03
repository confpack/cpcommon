
class NoBacktraceError(Exception):
  """This error will not print a stacktrace.

  It will simply print to stderr and sys.exit(1). This behaviour is handled by
  the Cmdline class.
  """
  pass
