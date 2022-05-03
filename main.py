from os.path import abspath
from getopt import getopt, GetoptError
from client import random_playlist_from_json
import contextlib, time, threading, uvicorn
import sys, getopt


# from https://stackoverflow.com/questions/61577643/python-how-to-use-fastapi-and-uvicorn-run-without-blocking-the-thread
class Server(uvicorn.Server):
    def install_signal_handlers(self):
        pass

    @contextlib.contextmanager
    def run_in_thread(self):
        thread = threading.Thread(target=self.run)
        thread.start()
        try:
            while not self.started:
                time.sleep(1e-3)
            yield
        finally:
            self.should_exit = True
            thread.join()


def launcher(argv):
    help_string = 'Usage : main.py -f <json-file> -g <number-of-songs> -s <server-hostname> -p <server-port>'
    mode = 'server'
    hostname = 'localhost'
    port = 8000
    file = ''
    songs = 20
    ok = True
    try:
        opts, args = getopt.getopt(argv, "hf:g:s:p:", ["help", "file=", "songs=", "server=", "port="])
    except GetoptError:
        print(help_string)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(help_string)
            sys.exit()
        elif opt in ("-f", "--file"):
            mode = 'client'
            file = abspath(arg)
        elif opt in ("-g", "--songs"):
            try:
                songs = int(arg)
            except ValueError:
                print(help_string)
                sys.exit(2)
        elif opt in ("-s", "--server"):
            hostname = arg
        elif opt in ("-p", "--port"):
            try:
                port = int(arg)
            except ValueError:
                print(help_string)
                sys.exit(2)
    if mode == "server" or (mode == "client" and hostname in ("localhost", "127.0.0.1", "::1")):
        if mode == "server":
            uvicorn.run("server:app", host=hostname, port=port, log_level="info")
        else:
            server = Server(uvicorn.Config("server:app", host=hostname, port=port, log_level="info"))
            with server.run_in_thread():
                ok = random_playlist_from_json(hostname, port, file, songs)
    else:
        ok = random_playlist_from_json(hostname, port, file, songs)
    if ok:
        sys.exit()
    else:
        sys.exit(1)


if __name__ == "__main__":
    launcher(sys.argv[1:])
