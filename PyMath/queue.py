from __future__ import annotations
from typing import Optional, TypeVar, Iterable


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
        self.__collection: list = list(default) if default else list()

    def push(self, item: T) -> None:
        """Put an item at the end of the Queue"""

        if isinstance(item, (list, set, tuple)):
            if not self.__unique:
                self.__collection.extend(item)
            else:
                [self.__collection.append(item) for i in set(item) if i not in self.__collection]
        else:
            if not self.__unique:
                self.__collection.append(item)
            else:
                if item not in self.__collection:
                    self.__collection.append(item)

    def pull(self) -> T:
        """Get the first item in the Queue if any"""

        try:
            return self.__collection.pop(0)  # Pull first item
        except IndexError:
            return None                      # Empty List

    def flush(self) -> Queue:
        """Clear the Queue and return a new Queue of it's items"""

        return Queue([_ for _ in self])

    def __str__(self):
        return str("< {} >".format(" | ".join([str(x) for x in self.__collection]) if len(self) else "Empty Q"))
    
    def __repr__(self):
        return repr(self.__collection)

    def __len__(self):
        return len(self.__collection)

    def __iter__(self):
        self.__pos = 0
        return self

    def __next__(self):
        if self.__pos < len(self.__collection):
            return self.pull()
        raise StopIteration

    def __getitem__(self, item: T):
        raise NotImplementedError

    def __setitem__(self, key: str, value: T) -> None:
        raise NotImplementedError
