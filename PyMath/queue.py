from __future__ import annotations
from typing import Optional, TypeVar, Iterable
import time
from threading import Thread


T = TypeVar("T")


class Queue:
    """My own implementation of a Queue

     Queue's are used to order items by their position in a list.
     Each item is added to the end of the Queue and items are
     retrieved in reverse order. Meaning that the first item
     added will be get before the second item.
 
     """

    def __init__(self, default: Optional[Iterable] = None, unique: Optional[bool] = False):
        self.__unique = unique
        self._collection: list = list(default) if default else list()

    def push(self, item: T) -> None:
        """Put an item at the end of the Queue"""

        if isinstance(item, (list, set, tuple)):
            if not self.__unique:
                self._collection.extend(item)
            else:
                [self._collection.append(item) for i in set(item) if i not in self._collection]
        else:
            if not self.__unique:
                self._collection.append(item)
            else:
                if item not in self._collection:
                    self._collection.append(item)

    def pull(self, blocking: Optional[bool] = False, timeout: Optional[int] = 0,
             if_timeout_reached: Optional[type] = None, *args, **kwargs) -> T:
        """Get the first item in the Queue if any"""
        result = [None]  # Set local result for modification inside inner and return later

        def b():
            s = time.time()
            while not self:
                if timeout and time.time() - s > timeout:
                    if if_timeout_reached:
                        if_timeout_reached(args, kwargs)
                    raise RuntimeError("Timeout Reached: ")
                else:
                    time.sleep(0.1)
            result[0] = self._collection.pop(0)

        t = Thread(target=b)
        t.start()
        if not blocking:
            t.join()
        return result[0] if result else None

    def flush(self) -> Queue:
        """Clear the Queue and return a new Queue of it's items"""

        return Queue([_ for _ in self])

    def __bool__(self):
        return len(self._collection) > 0

    def __str__(self):
        return str("< {} >".format(" | ".join([str(x) for x in self._collection]) if len(self) else "Empty Q"))
    
    def __repr__(self):
        return repr(self._collection)

    def __len__(self):
        return len(self._collection)

    def __iter__(self):
        self.__pos = 0
        return self

    def __next__(self):
        if self.__pos < len(self._collection):
            return self.pull()
        raise StopIteration

    def __getitem__(self, item: T):
        raise NotImplementedError

    def __setitem__(self, key: str, value: T) -> None:
        raise NotImplementedError
