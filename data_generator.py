import csv
import os

import random
import string
import datetime

# pip install names
from names import *
import pandas as pd
import psycopg2

from tqdm import tqdm

def get_time():
	start_year = random.choice(years)
	start_month = random.choice(range(1, 13))
	start_day = random.choice(range(1, month_day[start_month] + 1))
	start_hour = random.choice(hours)
	start_minute = random.choice(minutes)
	start_second = random.choice(seconds)
	starting = datetime.datetime(start_year, start_month, start_day, start_hour, start_minute, start_second)
	return starting

# connect to database
conn = psycopg2.connect(host="35.243.220.243", database="proj1part2", user="yl4323", password="2262")
cur = conn.cursor()

# fix random seed to reproduce results
random.seed(0)

# values to use
email_exts = ['columbia.edu', 'gmail.com', 'cs.columbia.edu', 'outlook.com', 'mail.com', 'yahoo.com']
letters = [s for s in string.ascii_lowercase]
numbers = [str(i) for i in range(10)]

tags = [None, 'housing', 'transport', 'food', 'utilities', 'clothing', 'health', 'insurance', 'household', 'personal', 'debt', 'education', 'finance', 'entertain', 'gift', 'tax']

years = [2019, 2020]
month_day = {1: 31, 2: 28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
hours = range(24)
minutes = range(60)
seconds = range(60)

sources = ['University', 'Company', 'Restaurant', 'Supermarket', 'Art', 'Transportation', 'Hospital', 'Apartment'] 
banks = ['Alipay', 'CreditCard', 'Check', 'Cash', 'Venmo', 'Paypal', 'ApplePay', 'GooglePay']

# enum
cmpr = ['leq', 'beq']
tstep = ['week', 'month', 'quarter', 'half-year', 'year']

# read in stock symbol
sids = pd.read_csv("./data/symbol-name.csv")['Symbol'].values

# generate data in csv for a particular table
# table: which table to generate(table names)
# num: how many tuples in this table
# fk_1: foreign key list 1
# fk_2: foreign key list 2
def generate_csv(table, num, fk_1=[], fk_2=[]):
	
	# account.csv
	# aid: fixed-length 10, lowercase + number
	# name: valid first names
	# email: random-length name combine with server name (picked from list)
	# pwd: random length, lowercase + number
	if table == 'account':
		# not allowed to repeat
		aids = []
		names = []
		emails = []
		with open("./data/%s.csv" % table, "w") as f:
			writer = csv.writer(f, delimiter=',')
			for j in tqdm(range(num)):
				# aid
				while True:
					aid = ''.join(random.choice(letters+numbers) for j in range(10))
					if aid not in aids:
						aids.append(aid)
						break
				# name
				while True:
					name = get_first_name()
					if name not in names and len(name) <= 20:
						names.append(name)
						break
				# email
				while True:
					email = '@'.join([''.join([random.choice(letters+numbers) for  k in range(random.choice(range(1, 21)))]), random.choice(email_exts)])
					if email not in emails and len(email) <= 20:
						emails.append(email)
						break
				# pwd
				pwd = ''.join(random.choice(letters+numbers) for p in range(random.choice(range(1, 21))))
				
				writer.writerow([aid, name, email, pwd])
		return aids

	# honors.csv
	# honors are only related with outcomes!
	# hid: as aid
	# name: type-tag-amt
	# type: 
	# - if starting & ending: leq/beq
	# - if starting & not ending: beq
	# - if not starting & ending: leq
	# - if not starting & not ending: beq
	# tag: pick from list
	# amt: 100*integer in [1, 100]
	elif table == 'honors':
		# not allowed to repeat
		hids = []
		names = []
		with open("./data/%s.csv" % table, "w") as f:
			writer = csv.writer(f, delimiter=',')
			for j in tqdm(range(num)):
				# hid
				while True:
					hid = ''.join(random.choice(letters+numbers) for j in range(10))
					if hid not in hids:
						hids.append(hid)
						break

				# name, type_, tag, amt
				while True:
					type_ = random.choice(cmpr)
					tag = random.choice(tags)
					amt = (100 + 100 * random.randrange(100))
					name = '-'.join([tag if tag is not None else '_', type_, str(amt)])
					if name not in names and len(name) <= 20:
						names.append(name)
						break
				amt = float(amt)
					

				# starting & ending
				while True:
					starting = get_time()
					ending = get_time()
					if starting < ending:
						break
					
				starting = starting.strftime('%Y-%m-%d %H:%M:%S') 
				ending = ending.strftime('%Y-%m-%d %H:%M:%S')
				# while there's None in times
				p = random.random()
				if p > 0.5:
					writer.writerow([hid, name, type_, tag, amt, starting, ending])
				else:
					names = names[:-1]
					while True:
					    type_ = 'leq' if (p > 0.3) else 'beq'
					    name = '-'.join([tag if tag is not None else '_', type_, str(amt)])
					    if name not in names and len(name) <= 20:
					    	names.append(name)
					    	break
	
					if p > 0.3:
						writer.writerow([hid, name, type_, tag, amt, None, ending])
					elif p > 0.1:
						writer.writerow([hid, name, type_, tag, amt, starting, None])
					else:
						writer.writerow([hid, name, type_, tag, amt, None, None])
		return hids
	
	# plans.csv
	# plans are only related with outcomes!
	# pid: same as aid
	# starting & ending
	# - if cycle is set, starting not None, ending None or not None
	# - if cycle is None, starting None or not None, ending not None 
	# credit: remaining amount of this plan, could update
	# budget: the total amount of this plan, set initially, positive
	# aid: pick from foreign key list fk_1
	elif table == 'plans':
		pids = []
		with open("./data/%s.csv" % table, "w") as f:
			writer = csv.writer(f, delimiter=',')
			for j in tqdm(range(num)):
				# pid
				while True:
					pid = ''.join(random.choice(letters+numbers) for j in range(10))
					if pid not in pids:
						pids.append(pid)
						break
				# cycle
				cycle = random.choice([None] + tstep)

				# starting & ending
				while True:
					starting = get_time()
					ending = get_time()
					if starting < ending:
						break
				starting = starting.strftime('%Y-%m-%d %H:%M:%S') 
				ending = ending.strftime('%Y-%m-%d %H:%M:%S')
				
				if cycle is None:
					if random.random() < 0.3:
						starting = None
				else:
					if random.random() < 0.3:
						ending = None
				# credit & budget
				budget = float(100 + 100 * random.randrange(100))
				credit = float(100 + 100 * random.randrange(100)) - 5000.

				aid = random.choice(fk_1)

				writer.writerow([pid, starting, ending, cycle, credit, budget, aid])
			   
		
		return pids
	# defaults.csv
	# template financial flows
	# be_from: amt -> be_to
	# income: amt <= 0
	# outcome: amt > 0
	# needs starting, ending is optional
	# if cycle does not exist, only use this default once
	# remark: possible to be None
	# aid: fk_1
	elif table == 'defaults':
		dids = []
		did_names = []
		with open("./data/%s.csv" % table, "w") as f:
			writer = csv.writer(f, delimiter=',')
			for j in tqdm(range(num)):
				# did
				while True:
					did = ''.join(random.choice(letters+numbers) for j in range(10))
					if did not in dids:
						dids.append(did)
						break
				# be_from, be_to, amt, tag, name
				while True:
					amt = float(100 + 100 * random.randrange(100)) - 5000.
					be_from = random.choice([None] + banks)
					be_to = random.choice([None] + sources)
					if amt <= 0:
						be_from, be_to = be_to, be_from
					tag = random.choice([None] + tags)
					name = '-'.join([tag if tag is not None else '_', be_from if be_from is not None else '_', be_to if be_to is not None else '_', str(int(amt))])
					if len(name) <= 20 and (did, name) not in did_names:
						did_names.append((did, name))
						break
					
				# starting & ending
				while True:
					starting = get_time()
					ending = get_time()
					if starting < ending:
						break
				starting = starting.strftime('%Y-%m-%d %H:%M:%S') 
				ending = ending.strftime('%Y-%m-%d %H:%M:%S')
				
				if random.random() < 0.4:
					ending = None

				# cycle
				cycle = random.choice([None] + tstep)

				# remark
				if random.random() < 0.5:
					remark = None
				else:
					remark = ''.join(random.choice(letters) for j in range(50))

				# aid
				aid = random.choice(fk_1)

				writer.writerow([did, name, be_from, be_to, amt, starting, ending, cycle, remark, aid, tag])
			   
		
		return dids 

	elif table == 'records':
		reids = []
		with open("./data/%s.csv" % table, "w") as f:
			writer = csv.writer(f, delimiter=',')
			for j in tqdm(range(num)):
				# reid
				while True:
					reid = ''.join(random.choice(letters+numbers) for j in range(10))
					if reid not in reids:
						reids.append(reid)
						break
				# be_from, be_to, amt, tag, name
				amt = float(100 + 100 * random.randrange(100)) - 5000.
				be_from = random.choice([None] + banks)
				be_to = random.choice([None] + sources)
				if amt <= 0:
					be_from, be_to = be_to, be_from
				tag = random.choice([None] + tags)
				name = '-'.join([tag if tag is not None else '_', be_from if be_from is not None else '_', be_to if be_to is not None else '_', str(int(amt))])
				if len(name) > 20 or random.random() < 0.3:
					name = None
						
				# time
				time = get_time()
				time = time.strftime('%Y-%m-%d %H:%M:%S')
				
				# remark
				if random.random() < 0.5:
					remark = None
				else:
					remark = ''.join(random.choice(letters) for j in range(50))

				# aid
				aid = random.choice(fk_1)

				writer.writerow([reid, name, be_from, be_to, amt, tag, time, remark, aid])
		return reids
	elif table == 'races':
		rids = []
		names = []
		with open("./data/%s.csv" % table, "w") as f:
			writer = csv.writer(f, delimiter=',')
			for j in tqdm(range(num)):
				# rid
				while True:
					rid = ''.join(random.choice(letters+numbers) for j in range(10))
					if rid not in rids:
						rids.append(rid)
						break
				
				# starting & ending
				# type_, tag, name
				while True:
					while True:
						starting = get_time()
						ending = get_time()
						if starting < ending:
							break
					starting = starting.strftime('%Y-%m-%d %H:%M:%S') 
					ending = ending.strftime('%Y-%m-%d %H:%M:%S')
					if random.random() < 0.4:
						ending = None
					type_ = random.choice(cmpr)
					tag = random.choice([None] + tags)			
					name = '-'.join([tag if tag is not None else '_', type_] + starting.split('-')[:2])
					
					if len(name) <=20 and name not in names:
						names.append(name)
						break
						

				writer.writerow([rid, name, type_, starting, ending, tag])
			   		
		return rids 		   
	elif table == 'logs':
		lid_aids = []
		with open("./data/%s.csv" % table, 'w') as f:
			writer = csv.writer(f, delimiter=',')
			for j in tqdm(range(num)):
				# lid, aid
				while True:
					lid = ''.join(random.choice(letters+numbers) for j in range(10))
					aid = random.choice(fk_1)
					if (lid, aid) not in lid_aids:
						lid_aids.append((lid, aid))
						break

				# if_log_in
				if_log_in = random.choice([None, True, False])

				# time
				time = get_time()
				time = time.strftime('%Y-%m-%d %H:%M:%S')
				if random.random() < 0.2:
					time = None

				# location
				location = ''.join(random.choice(letters+numbers) for j in range(random.choice(range(1, 51))))
				if random.random() < 0.4:
					location = None

				writer.writerow([lid, if_log_in, time, location, aid])
		return lid_aids

	elif table == 'friend':
		aidss = []
		with open("./data/%s.csv" % table, 'w') as f:
			writer = csv.writer(f, delimiter=',')
			for j in tqdm(range(num)):
				# aid_1, aid_2
				while True:
					aid_1 = random.choice(fk_1)
					aid_2 = random.choice(fk_2)
					if (aid_1 != aid_2) and (aid_1, aid_2) not in aidss and (aid_2, aid_1) not in aidss:
						aidss.append((aid_1, aid_2))
						break
				writer.writerow([aid_1, aid_2])
		return aidss
	elif table == 'in_race':
		aidss_rids = []
		with open("./data/%s.csv" % table, 'w') as f:
			writer = csv.writer(f, delimiter=',')
			for j in tqdm(range(num)):
				# (aid_1, aid_2), rid
				while True:
					aid_1, aid_2 = random.choice(fk_1)
					rid = random.choice(fk_2)
					if (aid_1, aid_2, rid) not in aidss_rids:
						aidss_rids.append((aid_1, aid_2, rid))
						break
				writer.writerow([aid_1, aid_2, rid])
		return aidss_rids
	elif table == 'win_honor':
		aid_hids = []
		with open("./data/%s.csv" % table, 'w') as f:
			writer = csv.writer(f, delimiter=',')
			for j in range(num):
				# (aid_1, aid_2), rid
				while True:
					aid = random.choice(fk_1)
					hid = random.choice(fk_2)
					if (aid, hid) not in aid_hids:
						aid_hids.append((aid, hid))
						break
				writer.writerow([aid, hid])
		return aid_hids
	elif table == 'rec_stk':
		aid_sids = []
		with open("./data/%s.csv" % table, 'w') as f:
			writer = csv.writer(f, delimiter = ',')
			for j in range(num):
				while True:
					aid = random.choice(fk_1)
					sid = random.choice(fk_2)
					if (aid, sid) not in aid_sids:
						aid_sids.append((aid, sid))
						break
				writer.writerow([aid, sid])
		return aid_sids
	elif table == 'own_stk':
		aid_sids = []
		with open("./data/%s.csv" % table, 'w') as f:
			writer = csv.writer(f, delimiter = ',')
			for j in range(num):
				while True:
					aid = random.choice(fk_1)
					sid = random.choice(fk_2)
					if (aid, sid) not in aid_sids:
						aid_sids.append((aid, sid))
						break
				writer.writerow([aid, sid, random.randint(10000, 200000) / 100, random.randint(50, 200)])
		return aid_sids
	else:
		assert False, "Table " + table + " does not exists!"
 
# generate data
print("generating account.csv")
aids = generate_csv('account', 1000)
print("generating honors.csv")
hids = generate_csv('honors', 100)
print("generating plans.csv")
pids = generate_csv('plans', 1000, aids)
print("generating defaults.csv")
dids = generate_csv('defaults', 500, aids)
print("generating records.csv")
reids = generate_csv('records', 10000, aids)
print("generating races.csv")
rids = generate_csv('races', 100)
print("generating logs.csv")
lid_aids = generate_csv('logs', 100000, aids)
print("generating friend.csv")
aidss = generate_csv('friend', 1000, aids, aids)
print("generating in_race.csv")
aidss_rids = generate_csv('in_race', 2000, aidss, rids)
print("generating win_honor.csv")
aid_hids = generate_csv('win_honor', 10000, aids, hids)
print("generating rec_stk.csv")
aid_sids = generate_csv('rec_stk', 1000, aids, sids)
print("generating own_stk.csv")
aid_sids = generate_csv('own_stk', 1000, aids, sids)

print("clearing tables")
# clear all the tables in server
cur.execute("DELETE FROM rec_stk;")
cur.execute("DELETE FROM own_stk;")
cur.execute("DELETE FROM win_honor;")
cur.execute("DELETE FROM in_race;")
cur.execute("DELETE FROM friend;")
cur.execute("DELETE FROM logs;")
cur.execute("DELETE FROM races;")
cur.execute("DELETE FROM records;")
cur.execute("DELETE FROM defaults;")
cur.execute("DELETE FROM plans;")
cur.execute("DELETE FROM honors;")
cur.execute("DELETE FROM account;")

print("copying csv to tables")
# copy csv to db
cur.copy_from(open('./data/account.csv', 'r'), 'account', sep=',', null='')
cur.copy_from(open('./data/honors.csv', 'r'), 'honors', sep=',', null='')
cur.copy_from(open('./data/plans.csv', 'r'), 'plans', sep=',', null='')
cur.copy_from(open('./data/defaults.csv', 'r'), 'defaults', sep=',', null='')
cur.copy_from(open('./data/records.csv', 'r'), 'records', sep=',', null='')
cur.copy_from(open('./data/races.csv', 'r'), 'races', sep=',', null='')
cur.copy_from(open('./data/logs.csv', 'r'), 'logs', sep=',', null='')
cur.copy_from(open('./data/friend.csv', 'r'), 'friend', sep=',', null='')
cur.copy_from(open('./data/in_race.csv', 'r'), 'in_race', sep=',', null='')
cur.copy_from(open('./data/win_honor.csv', 'r'), 'win_honor', sep=',', null='')
cur.copy_from(open('./data/rec_stk.csv', 'r'), 'rec_stk', sep=',', null='')
cur.copy_from(open('./data/own_stk.csv', 'r'), 'own_stk', sep=',', null='')
print("done!")


conn.commit()
conn.close()
