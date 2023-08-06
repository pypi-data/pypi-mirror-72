import requests,random
ua=['ala']
from bs4 import BeautifulSoup


def inputs(u,value=False,timeout=10,user_agent=None,bypass=False,proxy=None,cookie=None):
 '''
   this function is to get the names and values of input fields on a given webpage to scan.

   it takes 4 arguments:

   u: the page's link (http://...)
   value: (set by default to: False) to return the value of the fields set it to:True then the field's name and value will be string of 2 
   values sperated by ":"
   timeout: (set by default to: 10) timeout flag for the request
   bypass: (set by default to: False) to bypass anti-crawlers

  usage:

  >>>import bane
  >>>link='http://www.example.com'
  >>>bane.inputs(link)
  ['email','password','rememberme']
  >>>a=bane.inputs(link,value=True)
  ['email','password','rememberme:yes','rememberme:no']
  
 '''
 if user_agent:
  us=user_agent
 else:
  us=random.choice(ua)
 if proxy:
  proxy={'http':'http://'+proxy}
 if bypass==True:
  u+='#'
 if cookie:
  hea={'User-Agent': us,'Cookie':cookie}
 else:
  hea={'User-Agent': us}
 l=[]
 try:
  c=requests.get(u, headers = hea,proxies=proxy,timeout=timeout, verify=False).text
  soup= BeautifulSoup(c,'html.parser')
  p=soup.find_all('input')
  for r in p: 
    v=""
    if r.has_attr('name'):
     s=str(r)
     s=s.split('name="')[1].split(',')[0]
     s=s.split('"')[0].split(',')[0]
     if (r.has_attr('value') and (value==True)):
      v=str(r)
      v=v.split('value="')[1].split(',')[0]
      v=v.split('"')[0].split(',')[0]
    if value==True:
     y=s+":"+v
    else:
     y=s
    if y not in l:
     l.append(y)
 except Exception as e:
  pass
 return l

def forms(u,value=True,user_agent=None,timeout=10,bypass=False,proxy=None,cookie=None):
 '''
   same as "inputs" function but it works on forms input fields only
 '''
 if user_agent:
   us=user_agent
 else:
   us=random.choice(ua)
 if proxy:
   proxy={'http':'http://'+proxy}
 if bypass==True:
   u+='#'
 if cookie:
   hea={'User-Agent': us,'Cookie':cookie}
 else:
   hea={'User-Agent': us}
 l=[]
 fom=[]
 try:
  c=requests.get(u, headers = hea,proxies=proxy,timeout=timeout, verify=False).text
  soup= BeautifulSoup(c,'html.parser')
  i=soup.find_all('form')
  for f in i:
   #print(f)
   ma=str(f).split('>')[0]
   if "action" in ma:
    ac=ma.split("action=")[1]
    ac=ac.replace("'","")
    ac=ac.replace('"',"")
    ac=ac.replace(">","")
    ac=ac.split()[0]
   else:
    ac=""
   if "method" in ma:
    me=ma.split("method=")[1]
    me=me.replace("'","")
    me=me.replace('"',"")
    me=me.replace(">","")
    me=me.split()[0]
   else:
    me=""
   p=f.find_all('input')
   s=""
   for r in p: 
    v=""
    if r.has_attr('name'):
     s=str(r)
     s=s.split('name="')[1].split(',')[0]
     s=s.split('"')[0].split(',')[0]
     if (r.has_attr('value') and (value==True)):
      v=str(r)
      v=v.split('value="')[1].split(',')[0]
      v=v.split('"')[0].split(',')[0]
    if value==True:
     y=s+":"+v
    else:
     y=s
    if y not in l:
     l.append(y)
   fom.append({'inputs':l,'action':ac,'method':me}) 
   l=[]
 except Exception as e:
  pass
 return fom
print(forms('http://localhost/login.php'))