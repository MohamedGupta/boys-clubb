import slack_config
import pickle, time
from slackclient import SlackClient
from os import path

sc = SlackClient(slack_config.key)

grouplist = list(sc.api_call('groups.list')['groups'])
groupsfile = 'groups.list'
print grouplist
if path.isfile(groupsfile):
    groups = list(open(groupsfile, 'r').read())
else:
    groups = list(dict(gp) for gp in grouplist)
    for gp in groups:
        gp['oldest_id'] = '0'

class Listen:
    def __call__(self):
        for gp in groups:
            print gp
            hist = sc.api_call('groups.history', channel=gp['id'], oldest=gp['oldest_id'])
            print 'calling {1} with oldest_id {0}'.format(gp['oldest_id'], gp['name'])
            messages = hist['messages']
            if messages != []: 
                gp['oldest_id'] = hist['messages'][0]['ts']
                print gp['oldest_id']
                print hist['messages'][-1]['ts']
                min_ts = messages[0]['ts']
                max_ts = min_ts
                for msg in messages:
                    print msg
                    #states[gp]['user': msg
                    #print 'call finished'
                    #print 'min_ts: {0}\nmax_ts:{1}\n0_tx:{2}'.format(min_ts, max_ts, messages[0]['ts']) 
            with open(groupsfile, 'w') as file:
                print 'writing out..'
                file.write(str(groups))

listener = Listen()
#schedule.every(2).seconds.do(listener())
while True:
    #schedule.run_pending()
    listener()
    time.sleep(3)


#sc.api_call('chat.postMessage', as_user='true:', channel=chan, text=response)

