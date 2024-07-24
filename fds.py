a = 2

def mafin():
    global a
    a +=1
    return a

print('1', a)
print('2', mafin())
print('3', a)
