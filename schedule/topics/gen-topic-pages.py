# -*- coding: utf-8 -*-
# Generate topic pages for PyCon HK 2015
# Sammy Fung <sammy@sammy.hk>
import csv, re, os

def read_csv():
  csvfile = "/Users/sammyfung/Downloads/PyCON HK 2015 Program & Guest List (Internal Reference).csv"

  sessions = []

  with open(csvfile, 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
      #print row
      #print unicode(i, 'utf-8')
      session = {}
      session['speaker-photo'] = row[0]
      session['speaker-name'] = "%s %s"%(row[1],row[2])
      if len(session['speaker-photo'])==0:
        session['speaker-photo'] = '%s.jpg'%re.sub(" ","-",session['speaker-name'].lower())
      session['speaker-nick'] = row[3]
      if len(session['speaker-nick']) > 0:
        session['speaker-nick'] = " (%s)"%session['speaker-nick']
      session['country'] = row[4]
      session['speaker-bio'] = row[5]
      session['community'] = row[6]
      session['company'] = row[7]
      session['type'] = 'Talk'
      session['title'] = row[9]
      session['level-bar'] = "%s"%row[10]
      session['level'] = row[11]
      session['desc'] = row[12]
      session['lang'] = row[14]
      session['url'] = re.sub(" ","-",session['title'].lower())
      session['url'] = re.sub("[,!?':()/]","", session['url'])
      session['url'] = re.sub("[.-]$","", session['url'])
      #print session
      sessions.append(session)

  return sessions

def conv_to_p(s):
  o = "          <p>%s          </p>"%s
  o = re.sub("\n\n","</p>\n          <p>", o) 
  return o

def create_page(data):
  i = data
  template_file = '/Users/sammyfung/projects/pycon.hk/2015.pycon.hk/schedule/topics/template.html'
  dest_path = '/Users/sammyfung/projects/pycon.hk/2015.pycon.hk/schedule/topics'
  allowed_tags = ['type', 'title', 'url', 'speaker-name', 
    'speaker-nick', 'speaker-photo', 'speaker-bio', 
    'level-bar', 'level', 'lang', 'desc', 'company', 
    'community', 'country']
  try: 
    os.stat(i['url'])
  except: 
    i['speaker-bio'] = conv_to_p(i['speaker-bio'])
    i['desc'] = conv_to_p(i['desc'])
    os.mkdir(i['url'])
    infile = open(template_file, 'r')
    outfile = open('%s/%s/index.html'%(dest_path,i['url']), 'w')
    for j in infile.readlines():
      ln = j
      for k in allowed_tags:
        ln = re.sub(u'\{%% %s %%\}'%k,i[k], ln)
      outfile.write(ln)
    outfile.close()
    infile.close()

# Main    
data = read_csv()
print data

for i in data:
  try:
    os.stat(i['url'])
  except:
    create_page(i)

