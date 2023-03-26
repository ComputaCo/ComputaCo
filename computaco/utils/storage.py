import threading


class Storage:
    """Thread-local storage for stacks of singleton objects.

    with Storage() as storage:
        Storage.singleton.a = 1
        print(Storage.singleton.a)  # 1
        with Storage() as storage:
            Storage.a = 2
            print(Storage.singleton.a)  # 2
            with Storage() as storage:
                try:
                    print(Storage.a)  # error: not defined
                except:
                    pass
            print(Storage.singleton.a)  # 2
        print(Storage.singleton.a)  # 1
    """

    __stacks = {}
    __most_recent_init = {}

    @classmethod
    @property
    def singleton(cls):
        return cls.__stacks[threading.current_thread()][-1]

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        cls = self.__class__
        thread = threading.current_thread()
        cls.__most_recent_init[thread] = self
        if thread not in cls.__stacks:
            # If not, create a new stack for the thread
            cls.__stacks[thread] = []
        # Push a new singleton instance onto the stack for this thread
        cls.__stacks[thread].append(self)

    def __enter__(self):
        # Push a new singleton instance onto the stack for this thread
        return Storage.__most_recent_init[threading.current_thread()]

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Pop the current singleton instance from the stack for this thread and delete it
        thread = threading.current_thread()
        stack = self.__class__.__stacks[thread]
        stack.pop()
        if not stack:
            del self.__class__.__stacks[thread]
        del self

    def __setattr__(self, key, value):
        # Write directly to the object's dictionary
        self.__dict__[key] = value
