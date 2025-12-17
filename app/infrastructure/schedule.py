import threading
import time


def start_avatar_cleanup_scheduler(cleanup_service):
    def _run():
        while True:
            cleanup_service.cleanup_temp_avatars()
            time.sleep(300)

    threading.Thread(target=_run, daemon=True).start()
