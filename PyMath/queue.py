from typing import Optional, TypeVar, Type, Union, List


T = TypeVar("T")


class Queue:
    """My own implementation of a Queue

     Queue's are used to order items by their position in a list.
     Each item is added to the end of the Queue and items are
     retrieved in reverse order. Meaning that the first item
     added will be get before the second item.

     Queue is extended by Registry, which is basically a Queue of Queue's
     that orders by priority.
     """

    def __init__(self, unique: bool = False):
        self.__unique = unique
        self.__collection: list = list()

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

    def flush(self) -> List[T]:
        """Clear the Queue and return a list of it's items"""

        return [self.pull() for _ in range(len(self))]

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


if __name__ == "__main__":
    line = Queue(False)
    line.push([3, 1])
    line.push([1, 2, 3, 4, 5])
    print(iter(line))
    print(line)