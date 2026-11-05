import string as s
from random import SystemRandom as sr  # noqa: N813

char_qt = 64

secret_key = "".join(sr().choices(s.ascii_letters + s.punctuation, k=char_qt))
print(secret_key)
