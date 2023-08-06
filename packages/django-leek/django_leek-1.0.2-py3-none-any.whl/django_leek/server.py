from datetime import datetime
from sys import platform
import json
import logging
import socketserver
import multiprocessing
import queue
import threading

from .helpers import load_task
from . import helpers
from django.utils import timezone
import django


log = logging.getLogger(__name__)


def target(queue):
    django.setup()
    log.info('Worker Starts')
    while True:
        task_id = queue.get()
        if task_id is None:
            return

        log.info('running task...')

        # workaround to solve problems with django + psycopg2
        # solution found here: https://stackoverflow.com/a/36580629/10385696
        django.db.connection.close()

        task = load_task(task_id=task_id)
        pickled_task = helpers.unpack(task.pickled_task)
        try:
            task.started_at = timezone.now()
            task.save()
            return_value = pickled_task()
            task.finished_at = timezone.now()
            task.pickled_return = helpers.serialize(return_value)
            task.save()

            log.info('...successfully')
        except Exception as e:
            log.exception("...task failed")
            task.finished_at = timezone.now()
            task.pickled_exception = helpers.serialize(e)
            task.save()


class Pool(object):
    def __init__(self):
        if platform == 'darwin':
            # OSX does not support forking
            self.queue = queue.Queue()
            self.worker = threading.Thread(target=target, args=(self.queue,))
        else:
            self.queue = multiprocessing.Queue()
            self.worker = multiprocessing.Process(target=target, args=(self.queue,))

    def stop(self):
        self.queue.put(None)


class TaskSocketServer(socketserver.BaseRequestHandler):
    DEFAULT_POOL = 'default'
    # pools holds a mapping from pool names to process objects
    pools = {}

    def handle(self):
        try:
            data = self.request.recv(5000).strip()

            # assume a serialized task
            log.info('Got a task')
            response = None
            try:
                task_id = int(data.decode())
                
                # Connection are closed by tasks, force it to reconnect
                django.db.connections.close_all()
                task = load_task(task_id=task_id)
                
                # Ensure pool got a worker processing it
                pool_name = task.pool or self.DEFAULT_POOL
                pool = self.pools.get(pool_name)
                if pool is None or not pool.worker.is_alive():
                    # Spawn new pool
                    log.info('Spawning new pool: {}'.format(pool_name))
                    self.pools[pool_name] = Pool()
                    self.pools[pool_name].worker.start()

                self.pools[pool_name].queue.put(task_id)

                response = {'task': 'queued', 'task_id': task_id}
            except Exception as e:
                log.exception("failed to queue task")
                response = (False, "TaskServer Put: {}".format(e).encode(),)
                response = {
                    'task': 'failed to queue',
                    'task_id': task_id,
                    'error': str(e)
                }
            
            self.request.send(json.dumps(response).encode())

        except OSError as e:
            # in case of network error, just log
            log.exception("network error")

    @staticmethod
    def stop():
        for name, pool in TaskSocketServer.pools.items():
            print('Stopping pool:', name)
            pool.stop()
