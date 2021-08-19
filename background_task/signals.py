from django.dispatch import Signal
from django.db import connections

from background_task.settings import app_settings

# Those signals provide the related task as the `task` argument
task_created = Signal()
task_error = Signal()
task_rescheduled = Signal()

# Those signals provide the related `task_id` and `completed_task` as arguments
task_failed = Signal()
task_successful = Signal()

task_started = Signal()
task_finished = Signal()


# Register an event to reset saved queries when a Task is started.
def reset_queries(**kwargs):
    if app_settings.BACKGROUND_TASK_RUN_ASYNC:
        for conn in connections.all():
            conn.queries_log.clear()


task_started.connect(reset_queries)


# Register an event to reset transaction state and close connections past their lifetime
def close_old_connections(**kwargs):
    if app_settings.BACKGROUND_TASK_RUN_ASYNC:
        for conn in connections.all():
            conn.close_if_unusable_or_obsolete()


task_started.connect(close_old_connections)
task_finished.connect(close_old_connections)
