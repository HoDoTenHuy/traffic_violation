import time
import threading
from greenlet import getcurrent as get_ident


class StreamingEvent:
    """An Event-like class that signals all active clients when a new frame is
    available.
    """

    def __init__(self, timeout: int) -> None:
        self.events = {}
        self.timeout = timeout

    def wait(self) -> bool:
        """Invoked from each client's thread to wait for the next frame."""
        ident = get_ident()
        if ident not in self.events:
            # this is a new client
            # add an entry for it in the self.events dict
            # each entry has two elements, a threading.Event() and a timestamp
            self.events[ident] = [threading.Event(), time.time()]
        return self.events[ident][0].wait()

    def set(self) -> None:
        """Invoked by the camera thread when a new frame is available."""
        now = time.time()
        remove = []
        for ident, event in self.events.items():
            if not event[0].isSet():
                # if this client's event is not set, then set it
                # also will update the last set timestamp to now
                event[0].set()
                event[1] = now
            else:
                # if the client's event is already set, it means the client
                # did not process a previous frame
                # if the event stays set for more than timeout seconds, then assume
                # the client is gone and remove it
                if now - event[1] > self.timeout:
                    remove.append(ident)

        for ident in remove:
            del self.events[ident]

    def clear(self) -> None:
        """Invoked from each client's thread after a frame was processed."""
        self.events[get_ident()][0].clear()
