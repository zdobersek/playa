#!/usr/bin/env python

#    Playa - piping the 8-bit hits through aplay
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import random
import subprocess
import threading
import time

_sounds = [
    # source: http://www.reddit.com/r/linux/comments/14udch/troll_like_a_pro/c7gpa9a
    lambda i: (((i * (i >> 8 | i >> 9) & 46 & i >> 8) ^ (i & i >> 13 | i >> 6)) & 0xFF),
]

class AplayThread(threading.Thread):
    def __init__(self, sound):
        super(AplayThread, self).__init__(target=self._play)
        self._should_play = True
        self._sound = sound
        self._aplay = subprocess.Popen(["aplay", "-q"], stdin=subprocess.PIPE)

    def _play(self):
        i = 0
        while self._should_play:
            try:
                self._aplay.stdin.write('%c' % self._sound(i))
            except IOError, e:
                pass
            i += 1
        self._aplay.kill()

    def stop(self):
        self._should_play = False

def main():
    aplayThread = AplayThread(random.choice(_sounds))
    aplayThread.start()
    try:
        while True:
            time.sleep(0.01)
    except KeyboardInterrupt:
        print
        aplayThread.stop()
        return

if __name__=="__main__":
    main()
