# This file is a part of Arjuna
# Copyright 2015-2020 Rahul Verma

# Website: www.RahulVerma.net

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import threading
import multiprocessing

from arjuna.core.error import TestGroupsFinished
from signal import signal, SIGINT

class TestGroupRunner(multiprocessing.Process):

    def __init__(self, nprefix, wnum, commands):
        super().__init__(name="{}t{}".format(nprefix, wnum))
        self.__commands =  commands
        self.daemon = True # The process is killed when Arjuna exits.

    @property
    def commands(self):
        return self.__commands

    def handle_interrupt(self, signum, frame):
        self.terminate()

    def run(self):
        signal(SIGINT, self.handle_interrupt)
        from arjuna import log_info
        log_info("Group runner started")
        while True:
            try:
                child = self.__commands.next()
            except TestGroupsFinished as e:
                log_info("Groups finished")
                return
            except Exception as e:
                log_info("An exception occured in thread pooling. Would continue executing.")
                log_info(e)
                import traceback
                traceback.print_exc()
                return
            
            try:
                log_info("Running child")
                child.thread_name = self.name
                child.run()
            except Exception as e:
                import traceback
                log_info(str(e) + traceback.format_exc())
                continue
        log_info("Group runner started")
