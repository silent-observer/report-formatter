_logstring = ''

def log(s):
    global _logstring
    _logstring += s + '\n'

def have_logs():
    return len(_logstring) > 0
def get_logs():
    return _logstring
