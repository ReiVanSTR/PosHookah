import datetime

def real_time():
	_time = datetime.datetime.now()

	_response = {
		"day": str(_time.day),
		"month": str(_time.month),
		"year": str(_time.year),
		"hour": str(_time.hour),
		"minute": str(_time.minute) if len(str(_time.minute)) > 1 else "0" + str(_time.minute)
	}

	return _response

def parse_time(time: dict):
	return f"{time['day']}.{time['month']}.{time['year']}  {time['hour']}:{time['minute']}"