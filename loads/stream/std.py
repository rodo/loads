import sys


class StdStream(object):
    name = 'stdout'
    options = {'total': ('Total Number of items', int, None, False)}

    def __init__(self, args):
        self.args = args
        self.current = 0
        self.total = args['stream_stdout_total']
        self.start = None
        self.end = None
        self.sockets = 0
        self.seconds = self.rps = self.data_received = 0

    def flush(self):
        sys.stdout.write("\nHits: %d" % self.total)
        sys.stdout.write("\nStarted: %s" % self.start)
        sys.stdout.write("\nDuration: %.2f seconds" % self.seconds)
        sys.stdout.write("\nApproximate Average RPS: %d" % self.rps)
        sys.stdout.write("\nOpened web sockets: %d" % self.sockets)
        sys.stdout.write("\nBytes received via web sockets : %d\n" %
                         self.data_received)
        sys.stdout.flush()

    def push(self, data):
        if 'websocket' in data:
            # web socket event
            event = data['websocket']['event']
            if event == 'opened':
                self.sockets += 1
            elif event == 'message':
                self.data_received += data['websocket']['size']
            return

        date = data['started']
        if self.start is None:
            self.start = self.end = date
        else:
            if date < self.start:
                self.start = date
            elif date > self.end:
                self.end = date
        self.current += 1
        percent = int(float(self.current) / float(self.total) * 100.)
        bar = '[' + '=' * percent + ' ' * (100 - percent) + ']'
        sys.stdout.write("\r%s %d%%" % (bar, percent))

        if self.current == self.total:
            seconds = (self.end - self.start).total_seconds()
            if seconds == 0:
                rps = self.total
            else:
                rps = float(self.total) / seconds
            self.rps = rps
            self.seconds = seconds

        sys.stdout.flush()
