def to_datetime(element):   #清晰奇怪的日期格式，单个便利，可配合apply
    from datetime import datetime
    if isinstance(element, datetime):
        return element
    s = str(element)
    s = s.replace('00:00:00', '').replace(' ', '').replace('/', '-').replace('.', '-').replace('\n', '').lstrip('0')
    return datetime.strptime(s, '%Y-%m-%d')

def force_to_beginning(date):#强制更改到月初
    from datetime import datetime,timedelta
    nextdate = date + timedelta(days=2)
    if nextdate.month != date.month:
        return nextdate.replace(day=1)
    else:
        return date