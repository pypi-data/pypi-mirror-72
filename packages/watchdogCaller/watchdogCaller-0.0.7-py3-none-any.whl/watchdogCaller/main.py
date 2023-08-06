import time
import signal
import argparse
from threading import Thread, Event
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from urllib.parse import urlparse
import urllib.request
import sys
import os

last_call = time.time()


def call_a_url(url, token=None):
	"""
	Just calls an API with an Authorization token header, *token is not necessary
	"""
	headers = {}
	if token is not None:
		headers = {"Authorization": token}
	req = urllib.request.Request(url,headers=headers)
	try:
		res = urllib.request.urlopen(req)
	except urllib.URLError as e1:
		print("URLError, this might be because of bad URL passed, or that theres no internet connection")
	except urllib.error.HTTPError as e2:
		if e2.code == 401:
			print("HTTP Error, UNAUTHORIZED, this might be because of no token was passed, or token passed was invalid")
		elif e2.code == 500:
			print("The server was off, HTTP Error was 500")
		elif e2.code == 404:
			print("The API Endpoint passed didnt exist into the server")
		else:
			print(f"Unhandled HTTP Error : {e2.code}")
	except Exception as e:
		print("Unknown exception", str(e))
	else:
		return True
		print(f"Response was {res.read()}")
	return False



def has_time_passed_out(start, duration):
	return start + duration <= time.time()


class Watcher:
	def __init__(self, delay, max_time, watchable, function=lambda: None):
		self.delay = delay
		self.observer = Observer()
		self.max_time = max_time
		self.DIRECTORY_TO_WATCH = watchable

	def run(self):
		event_handler = Handler()
		self.observer.schedule(
			event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
		self.observer.start()
		try:
			while True:
				time.sleep(delay)
				if has_time_passed_out(last_call, self.max_time):
					print("TIME HAS PASSED OUT")
					self.observer.stop()
					self.function()
					break
		except:
			print("WATCHDOG FAILED")
			self.observer.stop()
			self.function()

		self.observer.join()


# Just a static class that handles fs events
class Handler(FileSystemEventHandler):
	@staticmethod

	def on_any_event(event):
		if event.is_directory:
			pass
		print(
			f"Event call type: {event.event_type} in {event.src_path}, resetting timer")
		last_call = time.time()


def cli():
	parser = argparse.ArgumentParser(
		description="Entry for Watchdog API Caller, api, timeout, and directory are mandatory arguments")

	parser.add_argument("-t", "--timeout", type=int, required=True,
						help="Timeout for the watchdog to call the api, if no file has modified between this time, api will be called\n")

	parser.add_argument(
		"--api", type=str, help="An HTTP API URL, should be a simple api call, so pass the final api path\n", required=True)

	parser.add_argument("-d", "--dir", type=str,
						help="The directory to watch, mandatory, be careful with system paths that are in constantly change\n", required=True)

	parser.add_argument(
		"--token", type=str, help="If a token was needed to be passed to the Authorization header, this is it\n", default=None)

	# parser.add_argument("-v", "--verbose",
	# 					action="store_true", help="Increase output\n")
	parser.add_argument(
		"--delay", type=int, help="The time watchdog checks the directory, default 3 seconds\n", default=3)

	parsed_args = parser.parse_args()

	TIMEOUT = parsed_args.timeout
	API = parsed_args.api
	DIR = parsed_args.dir
	token = parsed_args.token
	verbose = parsed_args.verbose
	delay = parsed_args.delay

	parsed_url = None
	try:
		assert os.path.exists(DIR),f"Passed DIR {DIR} doesnt exist"
		if os.path.isfile(DIR):
			print("Passed directory is a file, take that into account.")
		
		parsed_url = urlparse(API)
		assert (parsed_url.scheme == 'http' or parsed_url.scheme == 'https'),"Url should be http(s)"
	except Exception as e:
		print(str(e))
	else:
		def fn():
			if not call_a_url(parsed_url.geturl(), token):
				print("Function was called, and returned an error, exitting")
				sys.exit(1)
			else:
				return None
		w = Watcher(delay, TIMEOUT, DIR, fn)
		w.run()

if __name__ == "__main__":
	cli()