"""
Manual page script for Piqueserver.

Copyright © 2025 K6aV
License AGPLv3+: GNU AGPL version 3 or later <https://gnu.org/licenses/agpl.html>.
This script is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
"""

from piqueserver.commands import command, get_player
from piqueserver import commands
from piqueserver.config import ConfigStore

from os.path import realpath, join, commonprefix
import glob

config = ConfigStore()
man_dir = join(config.config_dir, 'man')

@command('man', 'manpage')
def man(self, key1=None, key2=None):
    """
    Displays a manual page by name.
    /man [section] <manpage>
    """
    if key2 is None:
        manpage = key1
        pagesection = None
    else:
        manpage = key2
        pagesection = key1

    if manpage is None:
        self.send_chat("For example, try 'man man'.")
        self.send_chat("What manual page do you want?")
        return

    return self.show_page(manpage, pagesection)


def apply_script(protocol, connection, config):
    class ManpageConnection(connection):

        def on_login(self, name):
            self.send_chat("Use the /man command to access reference manuals.")
            return connection.on_login(self, name)

        def show_page(self, manpage, pagesection):
            pagepath = realpath(glob.escape(join(man_dir, manpage)))

            if pagesection is None:
                pagepath = glob.glob("%s.*" % pagepath)[0]
            else:
                pagepath += ".%s" % pagesection

            if commonprefix((pagepath, man_dir)) != man_dir:
                print("[man] Invalid manpage path %s" % pagepath)
                return "Invalid manual entry name %s" % manpage

            try:
                with open(pagepath, 'r') as page:
                    lines = page.readlines()
                    self.send_chat(" ")
                    for l in lines[::-1]:
                        self.send_chat(l)
                    self.send_chat(" ")

            except:
                if pagesection is None:
                    return "No manual entry for %s" % manpage
                else:
                    return "No manual entry for %s(%s)" % (manpage, pagesection)
            return

    return protocol, ManpageConnection
