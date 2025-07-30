import time
import tracemalloc
import psutil
import threading
import resource
import os
import platform
import pandas as pd
from memory_profiler import memory_usage

def run_benchmark(func, func_args=None, func_kwargs=None, label=""):
    """
    Ejecuta una función y registra estadísticas detalladas de rendimiento.
    """
    if func_args is None:
        func_args = []
    if func_kwargs is None:
        func_kwargs = {}

    # Información del sistema
    system_info = {
        "Hostname": platform.node(),
        "OS": platform.system(),
        "CPU": platform.processor(),
        "Logical_CPUs": psutil.cpu_count(logical=True),
        "Physical_CPUs": psutil.cpu_count(logical=False),
        "Total_RAM_GB": round(psutil.virtual_memory().total / 1e9, 2),
    }

    # Preparación
    process = psutil.Process(os.getpid())

    # Iniciar monitoreo de memoria con tracemalloc
    tracemalloc.start()

    # Iniciar temporizador y CPU stats
    start_time = time.perf_counter()
    start_cpu_times = process.cpu_times()

    # Monitoreo de memoria en paralelo
    mem_usage = memory_usage((func, func_args, func_kwargs), interval=0.1, timeout=None, retval=True)
    peak_memory_mb = max(mem_usage[0])
    result = mem_usage[1]

    # Finalización
    end_time = time.perf_counter()
    end_cpu_times = process.cpu_times()
    current, peak_tracemalloc = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    duration = end_time - start_time
    user_time = end_cpu_times.user - start_cpu_times.user
    sys_time = end_cpu_times.system - start_cpu_times.system
    rss_memory_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    # Resultado
    benchmark_data = {
        "Label": label,
        "Duration_s": round(duration, 4),
        "User_Time_s": round(user_time, 4),
        "Sys_Time_s": round(sys_time, 4),
        "RSS_Memory_KB": rss_memory_kb,
        "Peak_Memory_MB": round(peak_memory_mb, 2),
        "Peak_Tracked_Bytes": peak_tracemalloc,
        **system_info,
    }

    return benchmark_data, result