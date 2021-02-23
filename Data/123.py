wr = open('map1.txt', mode='r')
a = wr.read()
wr.close()

for i in range(2, 11):
    with open(f'map{i}.txt', mode='w') as f:
        f.write(a)
