import threading


class GenericCollection:
    def __init__(self):
        self._data = {}
        self._lock = threading.Lock()

    def add(self, key, value):
        with self._lock:
            self._data[key] = value

    def remove(self, key):
        with self._lock:
            if key in self._data:
                del self._data[key]

    def get(self, key):
        with self._lock:
            return self._data.get(key)

    def keys(self):
        with self._lock:
            return list(self._data.keys())

    def values(self):
        with self._lock:
            return list(self._data.values())

    def items(self):
        with self._lock:
            return list(self._data.items())
