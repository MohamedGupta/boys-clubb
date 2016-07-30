import slack_config
import pickle, time
from slackclient import SlackClient
from os import path

sc = SlackClient(slack_config.key)
group = 'testbed'
groups = sc.api_call('groups.list')['groups']
group_id = [g['id'] for g in groups if g['name']==group][0]
oldestfile = '/home/pi/git/rawbot/oldest.p'

if path.isfile(oldestfile):
    oldests = pickle.load(open(oldestfile, 'rb'))
else:
    oldests = {group: '0'}

class Listen:
    def __call__(self):
        oldest_id = oldests[group]
        hist = sc.api_call('groups.history', channel=group_id, oldest=oldest_id)
        print 'calling with oldest_id {0}'.format(oldest_id)
        messages = hist['messages']
        if messages == []:
            return 
        oldests[group] = hist['messages'][0]['ts']
        pickle.dump(oldests, open(oldestfile, 'wb'))
        min_ts = messages[0]['ts']
        max_ts = min_ts
        for msg in messages:
            print msg['text']
            if msg['ts']<min_ts:
                min_ts = msg['ts']
            if msg['ts']>max_ts:
                max_ts = msg['ts']
        #print 'call finished'
        #print 'min_ts: {0}\nmax_ts:{1}\n0_tx:{2}'.format(min_ts, max_ts, messages[0]['ts']) 

listener = Listen()
#schedule.every(2).seconds.do(listener())
while True:
    #schedule.run_pending()
    listener()
    time.sleep(3)


#sc.api_call('chat.postMessage', as_user='true:', channel=chan, text=response)


