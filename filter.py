import datetime
applications = [
    {'priority': 1,
     'date_create': datetime.date(2021,2,22),
     'date_end': datetime.date(2022,1,23),
     'id': 4
     },
    {'priority': 3,
      'date_create':datetime.date(2022,3,25),
      'date_end': datetime.date(2024,4,20),
      'id': 5
      },
    {'priority': 2,
      'date_create': datetime.date(2022,5,21),
      'date_end': datetime.date(2024,6,22),
      'id': 2
      }
]
sort = 'data_create'
sort_how = 'down'
if sort_how == 'up':
    sorted_applications = sorted(applications, key=lambda x: x[sort])
elif sort_how == 'down':
    sorted_applications = sorted(applications, reverse=True, key=lambda x: x[sort])
    print('Ошибка')
print(sorted_applications)