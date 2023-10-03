import openpyxl

# bu komputerdagi excel fayl manzili
re = openpyxl.load_workbook('/home/ilyosxon/Asosiy/crm/Ishchi sinflar jadvali 11.09.2023.xlsx')

print()
s = re.sheetnames
data = re[s[0]]

sinf = [
  '1-A sinf  ',
  '1-A sinf  ',
  '1-B sinf  ',
  '2-A sinf  ',
  '2-B sinf  ',
  '3-A sinf  ',
  '3-B sinf  ',
  '4-A sinf  ',
  '4-B sinf  ',
  '5-A sinf  ',
  '5-B sinf  ',
  '6-A sinf  ',
  '6-B sinf  ',
  '7-A sinf  ',
  '7-B sinf  ',  
  '8-A sinf  ',
  '8-B sinf  ',  
  '9-A sinf  ',
  '9-B sinf  ',  
  '10-A sinf  ',
  '10-B sinf  ',  
  '11-A sinf  ',
  ]
kunlar = ('Dushanba', 'Seshanba', 'Chorshanba', 'Payshanba', 'Juma', 'Shanba')
kunlar_ = ('#', 'Vaqt', 'Dushanba', 'Seshanba', 'Chorshanba', 'Payshanba', 'Juma', 'Shanba')

li = []
for x in data.values:
  # print(all(x))

  if x[0] in sinf:
    a = {}
    sinfi = x[0]

    a[sinfi] = []
    for d in kunlar:
      r = {}
      fan = {}
      teach = {}
      r[d] = [fan, teach]
      a[sinfi].append(r)
    continue
  
  
  if type(x[0]) == int:
    # fan = {}
    for f in range(2,len(x)):
      if 'fanlar' in a[sinfi][f-2][kunlar_[f]][0].keys():
        a[sinfi][f-2][kunlar_[f]][0]['fanlar'].append(x[f])
      else:
        a[sinfi][f-2][kunlar_[f]][0]['fanlar'] = [x[f]]  
      
      # a[sinfi][f-2][kunlar_[f]].append(fan)  
    
  if any(x) and x[0]==x[1]:
    for f in range(2,len(x)):
      if 'teachers' in a[sinfi][f-2][kunlar_[f]][1].keys():
        a[sinfi][f-2][kunlar_[f]][1]['teachers'].append(x[f])
      else:
        a[sinfi][f-2][kunlar_[f]][1]['teachers'] = [x[f]]  
      if f==len(x) and a[sinfi]=='11-A sinf  ':
        break  
    
  if x[0]==9:
    li.append(a)    
  
for w in li:
  print()
  print(w)
  print()