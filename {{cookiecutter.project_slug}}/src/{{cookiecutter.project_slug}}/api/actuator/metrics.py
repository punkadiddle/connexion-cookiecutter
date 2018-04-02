import psutil
import time


def search():
    """
    Minimale Ausgaben von Prozessmetriken
    """
    now = time.time()
    vmem = psutil.virtual_memory()
    proc = psutil.Process()

    d = {'mem': vmem.total,
         'mem.free': vmem.free,
         'uptime': now - psutil.boot_time(),
         'httpsessions.active': len(proc.connections()),
         'instance.uptime': now - proc.create_time(),
         'processors': psutil.cpu_count(),
         'systemload.average': psutil.cpu_percent() / 100.0,
         'threads': proc.num_threads(),
    }
    return d, 200
