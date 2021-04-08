import os
from apscheduler.schedulers.blocking import BlockingScheduler as scheduler
import shutil
from datetime import datetime

def send_request():
    import urllib.request
    contents = urllib.request.urlopen('https://api.turbovax.info/dashboard').read()
    my_json = contents.decode('utf8')
    import json
    data = json.loads(my_json)

    portals = get_portals(data['portals'])

    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Time: ' + datetime.now().strftime('%d/%m/%Y %H:%M:%S') + '  ~~~ START ~~~~~~~~~~~~~')
    manhattan_locations = []
    for x in data['locations']:
        if x['area'] == 'Manhattan':
            if x['available'] == True:
                manhattan_locations.append(x)
                log(x)
                print('Count: ' + str(len(manhattan_locations))
                      + '\n\t\tLocation: ' + x['name']
                      + '\n\t\tAppointment Count: ' + str(x['appointments']['count'])
                      + '\n\t\tURL: ' + get_url(x['portal'], portals)
                      + '\n\n')
        if x['area'] == 'Brooklyn':
            if x['available'] == True:
                log(x)
        if x['area'] == 'Queens':
            if x['available'] == True:
                log(x)
        if x['area'] == 'Bronx':
            if x['available'] == True:
                log(x)

    if len(manhattan_locations) > 0:
        os.system("say 'Vaccine Available'")

    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Time: ' + datetime.now().strftime('%d/%m/%Y %H:%M:%S') + '  ~~~ END ~~~~~~~~~~~~~~~\n\n')

def get_portals(portals):
    formatted_portals = []
    for a in portals:
        formatted_portals.append({'key': a.get('key'), 'site': a.get('url')})
    return formatted_portals

def get_url(id, portals):
    url = ''
    for p in portals:
        if p.get('key') == id:
            url = p.get('site')
    return url

def log(x):
    archive_records()
    f = open('records/manhattan_vaccine_history.csv', 'a')
    f.write(datetime.now().strftime('%d/%m/%Y %H:%M:%S') + ',' + x['area'] + ',' + x['name'] + ',' + str(x['appointments']['count']) + '\n')
    f.close()

def archive_records():
    if os.stat('records/manhattan_vaccine_history.csv').st_size > 1000000:
        file = 'records/archive/' + datetime.now().strftime('%d%m%Y%H%M%S') + '.csv'
        f = open(file, 'w+')
        f.close()
        shutil.move('records/manhattan_vaccine_history.csv', file)
        open('records/manhattan_vaccine_history.csv', 'w').close()

if __name__ == '__main__':
    send_request_sched = scheduler()
    send_request_sched.add_job(send_request, 'interval', seconds=30)
    print('waiting...')
    send_request_sched.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()