from sel import *

kiv = MyApp().run()
res = kiv.btn()

opencolws(res[0],res[1],res[2],res[3])
lis = copycontacts()
messenger(lis,res[4])
opencolws(res[0],res[1],res[2],res[3])
postnotes(res[5])

'''Hello. This is U-Haul Moving and Storage at West Oaks. Your storage unit payment is overdue. Please give us a call
back at (281)-556-5194. Thank you.'''

"Left a text message."