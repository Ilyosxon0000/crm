# raqam=0
# i=0
# numbers=[]
# while i<270:
#     if raqam<2:
#         i+=1
#         raqam+=1
#     elif raqam==2:
#         raqam-=1
#         i+=3
#     numbers.append(i)
# print(numbers)

raqam=0
i=2
numbers=[]
while i<268:
    if raqam<2:
        i+=1
        raqam+=1
    elif raqam==2:
        raqam-=1
        i+=3
    numbers.append(i)
# numbers=numbers.sort(reverse=True)
# sorted(numbers,reverse=True)
print(sorted(numbers,reverse=True))