import random
random.seed()

symbols = [chr(n) for n in range(32, 127)]

def generate_key(length=50):
    return ''.join([random.choice(symbols) for n in xrange(length)])
