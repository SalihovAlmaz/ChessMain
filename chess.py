letter_coord = ['a','b','c','d','e','f','g','h']
digit_coord = range(1,9)
doska = [[[(j,i)] for j in letter_coord] for i in digit_coord[::-1]]
print(*doska,sep = "\n")