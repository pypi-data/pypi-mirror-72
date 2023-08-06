# Author: echel0n <echel0n@sickrage.ca>
# URL: https://sickrage.ca
# Git: https://git.sickrage.ca/SiCKRAGE/sickrage.git
#
# This file is part of SiCKRAGE.
#
# SiCKRAGE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SiCKRAGE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SiCKRAGE.  If not, see <http://www.gnu.org/licenses/>.


import ctypes
import datetime
import threading
import traceback

from apscheduler.schedulers.tornado import TornadoScheduler
from tornado.queues import Queue, PriorityQueue

import sickrage


class QueueItemStopException(Exception):
    pass


class SRQueuePriorities(object):
    EXTREME = 5
    HIGH = 10
    NORMAL = 20
    LOW = 30
    PAUSED = 99


class SRQueue(object):
    def __init__(self, name="QUEUE"):
        super(SRQueue, self).__init__()
        self.name = name
        self.lock = threading.Lock()
        self.scheduler = TornadoScheduler({'apscheduler.timezone': 'UTC'})
        self.queue = PriorityQueue()
        self._result_queue = Queue()
        self._queue_items = []
        self.processing = []
        self.min_priority = SRQueuePriorities.EXTREME
        self.amActive = False
        self.stop = False

    def start(self):
        self.scheduler.start()

    async def run(self):
        """
        Process items in this queue
        """

        self.amActive = True

        if not self.stop and not self.queue.empty():
            if not self.is_paused and not len(self.processing) >= int(sickrage.app.config.max_queue_workers):
                sickrage.app.io_loop.run_in_executor(None, self.worker, await self.get())

        self.amActive = False

    def worker(self, item):
        with self.lock:
            threading.currentThread().setName(item.name)
            item.thread_id = threading.currentThread().ident

            try:
                item.is_alive = True
                self.processing.append(item)
                result = item.run()
                if result:
                    self._result_queue.put(result)
            except QueueItemStopException:
                pass
            except Exception:
                sickrage.app.log.debug(traceback.format_exc())
            finally:
                self.remove(item)
                self.queue.task_done()
                del item

    async def get(self):
        return await self.queue.get()

    async def put(self, item, *args, **kwargs):
        """
        Adds an item to this queue

        :param item: Queue object to add
        :return: item
        """
        if self.stop:
            return

        item.added = datetime.datetime.now()
        item.name = "{}-{}".format(self.name, item.name)
        self._queue_items.append(item)
        await self.queue.put(item)

        return item

    @property
    def queue_items(self):
        return self._queue_items + self.processing

    @property
    def is_busy(self):
        return bool(len(self.queue_items) > 0)

    @property
    def is_paused(self):
        return self.min_priority == SRQueuePriorities.PAUSED

    def pause(self):
        """Pauses this queue"""
        sickrage.app.log.info("Pausing {}".format(self.name))
        self.min_priority = SRQueuePriorities.PAUSED

    def unpause(self):
        """Unpauses this queue"""
        sickrage.app.log.info("Un-pausing {}".format(self.name))
        self.min_priority = SRQueuePriorities.EXTREME

    def remove(self, item):
        if item in self._queue_items:
            self._queue_items.remove(item)
        if item in self.processing:
            self.processing.remove(item)

    def stop_item(self, item):
        if not item.is_alive:
            return

        if ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(item.thread_id), ctypes.py_object(QueueItemStopException)) > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(item.thread_id, None)


class SRQueueItem(object):
    def __init__(self, name, action_id=0):
        super(SRQueueItem, self).__init__()
        self.name = name.replace(" ", "-").upper()
        self.action_id = action_id
        self.added = None
        self.result = None
        self.priority = SRQueuePriorities.NORMAL
        self.is_alive = False
        self.thread_id = None

    def __eq__(self, other):
        return self.priority == other.priority

    def __ne__(self, other):
        return not self.priority == other.priority

    def __lt__(self, other):
        return self.priority < other.priority
