import time
import keyboard

start_time = time.time()
last_time = start_time

running = True
hangup = False
def key_pressed(e):
	global running, hangup
	if (e.name == 'esc'):
		running = False
	if (e.name == 'h'):
		hangup = True

keyboard.on_press(callback=key_pressed, suppress=False)

def init_print(args):
	global show_timing, is_verbose, vad_progress
	show_timing = args.show_timing if hasattr(args, 'show_timing') else False
	is_verbose = args.verbose if hasattr(args, 'verbose') else False
	vad_progress = args.vad_progress if hasattr(args, 'vad_progress') else False

def printv(text):
	if is_verbose:
		print(text)

def printt(text):
	if not show_timing:
		print(text)
	else:
		global last_time
		current_time = time.time()
		print(f"{format_seconds_to_time(current_time - start_time)} {(current_time - last_time):.3f} {text}")
		last_time = current_time

def format_seconds_to_time(float_seconds):
	minutes = int(float_seconds // 60)
	seconds = int(float_seconds % 60)
	milliseconds = int((float_seconds % 1) * 1000)
	return f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"

def printtv(text):
	if is_verbose:	
		printt(text)

def printa(text):
	if vad_progress:
		print(end=text, flush=True)

def printa_end(text = ""):
	if vad_progress:
		print(text)
