import threading
import requests
import queue
import logging


class APE:
    """
    Acynchronous Page gEtter
    get multiple html pages asynchronously
    """

    def __init__(self, threads=2):
        self._threads = threads if threads > 0 else 1  # run in single thread if invalid input
        self._queue = queue.Queue()
        logging.basicConfig(filename='log.log', level=logging.INFO)
        logging.getLogger('requests').setLevel(logging.WARNING)  # ignore INFO from requests
        logging.info('threads = %s', self._threads)

    @staticmethod
    def _get_page(url):
        try:
            page = requests.get(url)
            return {'status_code': page.status_code,
                    'url': url,
                    'content': page.content,
                    }
        except Exception as e:
            return {'status_code': -1,
                    'err': e,
                    'url': url,
                    }

    def _worker(self, results):
        while not self._queue.empty():
            url = self._queue.get_nowait()
            logging.info('%s got %s', threading.current_thread().name, url)
            page = self._get_page(url)
            results.append(page)
            logging.info('%s %s', threading.current_thread().name, page)
            self._queue.task_done()

    def get_pages(self, urls):
        for url in urls:
            self._queue.put(url)

        threads = []
        results = []
        for i in range(self._threads):
            t = threading.Thread(target=self._worker, args=(results,), name='thread{}'.format(i))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        return results
