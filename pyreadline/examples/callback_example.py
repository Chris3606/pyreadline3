u'''
Example script using the callback interface of readline.

:author: strank
'''

__docformat__ = u"restructuredtext en"

import sys
import os
import time

import readline

import msvcrt
from pyreadline.rlmain import rl

prompting = True
count = 0
maxlines = 10


def main():
    readline.callback_handler_install(u'Starting test, please do type:' + os.linesep, lineReceived)
    index = 0
    start = int(time.time())
    while prompting:
        # demonstrate that async stuff is possible:
        if start + index < time.time():
            rl.console.title(u"NON-BLOCKING: %d" % index)
            index += 1
        # ugly busy waiting/polling on windows, using 'select' on Unix: (or use twisted)
        if msvcrt.kbhit():
            readline.callback_read_char()
    print u"Done, index =", index


def lineReceived(line):
    global count, prompting
    count += 1
    print u"Got line: %s" % line
    if count > maxlines:
        prompting = False
        readline.callback_handler_remove()
    else:
        readline.callback_handler_install(u'Got %s of %s, more typing please:' % (count, maxlines)
                                          + os.linesep, lineReceived)




if __name__ == u'__main__':
    main()
