import cv2, queue, threading


# bufferless VideoCapture
class VideoCaptureThread:

    def __init__(self, camera):
        self.cap = cv2.VideoCapture(camera)
        self.q = queue.Queue()
        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()
        self.ret = False

    # read frames as soon as they are available, keeping only most recent one
    def _reader(self):
        while True:
            ret, frame = self.cap.read()
            self.ret = ret
            if not ret:
                if not self.q.empty():
                    try:
                        self.q.get_nowait()   # discard previous (unprocessed) frame
                    except queue.Empty:
                        pass
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()   # discard previous (unprocessed) frame
                except queue.Empty:
                    pass
            self.q.put(frame)

    def read(self):
        if self.ret:
            return self.q.get()
        else:
            return None
