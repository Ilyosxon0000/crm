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

# raqam=0
# i=2
# numbers=[]
# while i<268:
#     if raqam<2:
#         i+=1
#         raqam+=1
#     elif raqam==2:
#         raqam-=1
#         i+=3
#     numbers.append(i)
# print(sorted(numbers,reverse=True))

student_amount=-1000_000
amount=0
amount_2=0
amount_3=0
def st_pay(amount,amount_2,amount_3):
    global student_amount
    if student_amount>0:
        amount+=student_amount
    if amount>0:
        if amount_2>=0:
            amount_2+=amount
        else:
            amount_2+=amount
        student_amount+=amount_2
        amount_3+=amount_2
    elif amount==0:
        if amount_2<0 and amount_2!=amount_3:
            student_amount+=amount_2
            amount_3+=amount_2
    amount=0
    return {
        "student_amount":student_amount,
        "amount":amount,
        "amount_2":amount_2,
        "amount_3":amount_3,
    }
qiymat=st_pay(
    amount=3000_000,
    amount_2=-1000_000,
    amount_3=0,
)
print(qiymat)
print(student_amount)
qiymat1=st_pay(
    amount=0,
    amount_2=-1000_000,
    amount_3=0,
)
print(qiymat1)
print(student_amount)

qiymat2=st_pay(
    amount=0,
    amount_2=1000_000,
    amount_3=1000_000,
)
print(qiymat2)
print(student_amount)
