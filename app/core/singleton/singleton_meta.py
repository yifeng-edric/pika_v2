import threading


class SingletonMeta(type):
    _instances = {}
    _lock: threading.Lock = threading.Lock()  # 添加一个锁

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:  # 使用锁保护关键区段
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]
