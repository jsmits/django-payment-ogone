import sha

def create_hash(*params):
    s = "".join([str(param) for param in params])
    return sha.new(s).hexdigest().upper()