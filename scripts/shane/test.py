import hashlib as hasher
import random
import time

start_time = time.time()

data = []

for i in range(1000000):
    value = str(random.randint(1000000000, 2000000000))
    sha = hasher.sha256()
    sha.update(str(value))
    data.append(sha.hexdigest())

end_time = time.time()
print end_time - start_time
