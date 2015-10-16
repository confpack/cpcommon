from __future__ import print_function

import re
import sys

first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


def underscore(name):
    s1 = first_cap_re.sub(r'\1_\2', name)
    return all_cap_re.sub(r'\1_\2', s1).lower()


def get_class_name(command):
  camelized_command = "".join([w.capitalize() for w in command.split("_")])
  return "{}Main".format(camelized_command)


class HelpMain(object):
  def __init__(self, cmds=None):
    self.cmds = cmds

  def get_description(self):
    return "Displays this help screen. A command can be appended to this."

  def __call__(self, argv):
    if len(argv) == 0:
      utility_commands = [(underscore(k[:-4]), self.cmds[k]) for k in self.cmds]
      print("usage: {} command".format(sys.argv[0]))
      print("")
      print("commands:")
      for name, klass in utility_commands:
        print("  {}".format(name))
        print("    {}".format(klass().get_description()))
        print("")
    else:
      command = argv[0]
      cls_name = get_class_name(command)
      if cls_name not in self.cmds:
        print("error: {} is not a valid function".format(command), file=sys.stderr)
        self([])
      else:
        p = self.cmds[cls_name]()
        print(p.get_help())


class Cmdline(object):
  def __init__(self, script_names):
    self.script_names = set(script_names)
    self.cmds = {}

  def register_command(self, cmd_main):
    self.cmds[cmd_main.__name__] = cmd_main

  def main(self, argv):
    self.register_command(HelpMain)

    if argv[0] in self.script_names:
      argv.pop(0)

    if len(argv) == 0:
      argv.append("help")  # lol

    command = argv.pop(0)
    cls_name = get_class_name(command)
    if cls_name == "HelpMain":
      p = self.cmds[cls_name](self.cmds)
    elif cls_name in self.cmds:
      p = self.cmds[cls_name]()
    else:
      p = HelpMain(self.cmds)
      argv.insert(0, command)
      p(argv)
      sys.exit(1)

    return p(argv) or 0
