import csv
from datetime import datetime

po_dict={} #define object that stores po values

with open('lead times.csv',"r") as lead_times:
    reader = csv.DictReader(lead_times)
    for row in reader:
       created_from = row['Created From'].strip()
       ir = row['Transaction'].strip()
       ir_date = datetime.strptime(row['IR DATE'], '%m/%d/%Y')
       po_date = datetime.strptime(row['PO DATE'], '%m/%d/%Y')
       item = row['Item'].strip()
       quantity = row['Quantity'].strip()
       rate = row['Rate'].strip()
       if created_from not in po_dict:
          po_dict[created_from] = [[ir, po_date, ir_date]]
       else:
          po_dict[created_from].append([ir, po_date, ir_date])
    for i in po_dict:
        po_dict[i].sort(reverse=False, key=lambda x : x[2])

for key, value in po_dict.items():
   formatted_value = [[x[0], x[1].strftime('%m/%d/%Y'), x[2].strftime('%m/%d/%Y')] for x in value]
   print(key, formatted_value)
# Output
def write_po_csv(po_dict):
   headers = ['Created From', 'IR', 'PO Date', 'IR Date', 'lead_time']
   with open('computed_lead_times.csv','w', newline="") as new_file:
      writer = csv.DictWriter(new_file, fieldnames=headers)
      writer.writeheader()
      for i, j in po_dict.items():
         previous_lead_time = 0
         for idx, k in enumerate(j):
            if idx == 0:
               lead_time = (k[2] - k[1]).days
            else:
               lead_time = (k[2] - j[idx-1][2]).days
               if lead_time == 0:
                  if j[idx-1][2] == k[2]:
                     lead_time = previous_lead_time
                  else:
                     lead_time = (k[2] - k[1]).days
            previous_lead_time = lead_time
            
            writer.writerow({
               'Created From': i,
               'IR': k[0],
               'PO Date': k[1].strftime('%m/%d/%Y'),
               'IR Date': k[2].strftime('%m/%d/%Y'),
               'lead_time': lead_time
            })
write_po_csv(po_dict)