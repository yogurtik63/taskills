from datetime import datetime

s = '2023 11 11'
n = datetime(*list(map(int, s.split())))
print(n)