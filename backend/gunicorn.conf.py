"""
backend/gunicorn.conf.py

Gunicorn hooks for Prometheus multiprocess mode.

prometheus_client keeps counters in memory-mapped files, one set per
process, and `/metrics` sums them at scrape time. Two things have to happen
around the worker lifecycle for that sum to be correct:

  * a dead worker's files must be marked dead, or its counters keep being
    added to the total forever — after a few restarts the request rate is
    whatever the workers *ever* served, not what they are serving;
  * the directory must be empty at boot, or files from the previous
    container run are picked up as if they were live workers.

Neither is optional, and neither is obvious from a stack trace when it goes
wrong — the numbers are simply too high.

Used automatically: docker-compose points gunicorn at this file with
`-c gunicorn.conf.py`.
"""
import os
import shutil

_MULTIPROC_DIR = os.environ.get("PROMETHEUS_MULTIPROC_DIR")


def on_starting(server):
    """Master process, before any worker forks: start from an empty slate."""
    if not _MULTIPROC_DIR:
        return
    if os.path.isdir(_MULTIPROC_DIR):
        shutil.rmtree(_MULTIPROC_DIR, ignore_errors=True)
    os.makedirs(_MULTIPROC_DIR, exist_ok=True)


def child_exit(server, worker):
    """A worker died — retire its metric files so its counters stop being
    summed into every future scrape."""
    if not _MULTIPROC_DIR:
        return
    try:
        from prometheus_client import multiprocess

        multiprocess.mark_process_dead(worker.pid)
    except Exception:  # noqa: BLE001 — never block a worker exit on telemetry
        pass
