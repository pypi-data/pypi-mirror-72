import hashlib #line:1
import hmac #line:2
import base64 #line:3
import time #line:4
from Crypto .PublicKey import RSA #line:5
from Crypto .Cipher import PKCS1_OAEP #line:6
from urllib import request ,parse ,error #line:7
import ssl #line:8
import simplejson #line:9
import json #line:10
s_time =2 *60 *60 *1000 #line:12
l_time =30 *24 *60 *60 *1000 #line:13
sk ='knoczslufdasvhbivbewnrvuywachsrawqdpzesccknrhhetgmrcwfqfudywbeon'#line:15
pubkey =b'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAokFjy0wLMKH0/39hxPN6JYRkMDXzvVIGQh55Keo2LIsP/jRU/yZHT/Vkg34yU9koNjSaacPvooXEoI5eFGuRrsBMrotZ5xfejCrTbGvZqjhnMPBheDmxfflIZzRrF/zoQvF0nIbmGNkxEfROHtDDkgNuGRdthXrNavCgfM2z3LNF83UT9CGpxJWBeKK3pXfYLsQ4f8uyrQRcy2BhKfJ/PKai1mocXYqr07JfQ0XZM4xIzuQ7E4ybNk5IFreDuuhF63wXAi1uonGzqjEYcbC1xT2boNiZORoOQWpAHhSbIRpljmW/uHBvoKZ573PQbbxE62hXv1Z1iVky0dtAV65dXwIDAQAB'#line:16
ssl ._create_default_https_context =ssl ._create_unverified_context #line:18
def __OO000O000OO0OO000 (OOOO00OOOO000O000 ,O0OOO0OOO00O00000 ):#line:21
 O0000O0O0O0O0O0OO =[OOOO00OOOO000O000 .split ("-")[1 ],O0OOO0OOO00O00000 .split ("-")[1 ]]#line:22
 O0OO0O00OO0O00OOO =''.join (O0000O0O0O0O0O0OO )#line:23
 return str (int (O0OO0O00OO0O00OOO ,16 )).zfill (9 )[:6 ]#line:24
def __O000OO0O0OO0O00OO (O0000OO000OO0O0OO ,OOO0000000O00O000 ,O0OOO0O0000O0OOO0 ):#line:27
 O00O00OOO0O000OO0 =O0000OO000OO0O0OO +str (int (round (time .time ()*1000 ))+OOO0000000O00O000 )#line:28
 OOO0000O0O0OO0000 =O0000OO000OO0O0OO +str (int (round (time .time ()*1000 ))+O0OOO0O0000O0OOO0 )#line:29
 OO000OOOO0O0OO00O =list ()#line:31
 OO000OOOO0O0OO00O .append (hmac .new (sk .encode ('UTF-8'),O00O00OOO0O000OO0 .encode ('UTF-8'),hashlib .sha256 ).hexdigest ())#line:32
 OO000OOOO0O0OO00O .append (hmac .new (sk .encode ('UTF-8'),OOO0000O0O0OO0000 .encode ('UTF-8'),hashlib .sha256 ).hexdigest ())#line:33
 return OO000OOOO0O0OO00O #line:35
def __OO0OO000OOO00OO0O (O00OOO0OOO00O000O ,OO00O0OOOO0OOO00O ):#line:38
 O0OO0OO0O0000000O =O00OOO0OOO00O000O +str (int (round (time .time ()*1000 ))+OO00O0OOOO0OOO00O )#line:39
 return hmac .new (sk .encode ('UTF-8'),O0OO0OO0O0000000O .encode ('UTF-8'),hashlib .sha256 ).hexdigest ()#line:41
def __OOO00OO0O00O00OOO (OO00O0O0OO0O0OO0O ,O00OOOOO00OOO00OO ,OOOO0OOOOOOO0OO0O ,O000O0OOO00O0000O ,OO00OOO0OO0OOOOOO ):#line:44
 OO0O000OOO0O0O000 =OO00O0O0OO0O0OO0O +'$'+O00OOOOO00OOO00OO +'$'+OOOO0OOOOOOO0OO0O +'$'+O000O0OOO00O0000O +'$'+OO00OOO0OO0OOOOOO #line:45
 O0OOOO0OOOO0O0000 =base64 .b64decode (pubkey )#line:46
 OOO00OO00OOO0O00O =RSA .importKey (O0OOOO0OOOO0O0000 )#line:47
 OOO0O0O0000OO0OO0 =PKCS1_OAEP .new (OOO00OO00OOO0O00O )#line:48
 O0O00OOOOO0000OO0 =OOO0O0O0000OO0OO0 .encrypt (OO0O000OOO0O0O000 .encode ('UTF-8'))#line:49
 return base64 .b64encode (O0O00OOOOO0000OO0 ).decode ()#line:50
def urlopen (O0000O0000O000O00 ,O00000OO0OO0OOOO0 ,O00OO00O0OO0O0O0O ,data =None ,headers ={},method =None ):#line:53
 OO0OOO0OO00O0OOOO =__OO000O000OO0OO000 (O0000O0000O000O00 ,O00000OO0OO0OOOO0 )#line:54
 O00O0OO000O00OO00 =__O000OO0O0OO0O00OO (OO0OOO0OO00O0OOOO ,s_time ,l_time )#line:55
 OOOOOOO00O00O00OO =__OOO00OO0O00O00OOO (OO0OOO0OO00O0OOOO ,O0000O0000O000O00 ,O00000OO0OO0OOOO0 ,O00O0OO000O00OO00 [0 ],O00O0OO000O00OO00 [1 ])#line:56
 if data is not None :#line:58
  data =json .dumps (data );#line:59
  data =bytes (data ,'UTF-8')#line:60
 O000O0OOOO000O0OO =request .Request (O00OO00O0OO0O0O0O ,data )#line:62
 if method is not None :#line:63
  O000O0OOOO000O0OO .method =method #line:64
 O000O0OOOO000O0OO .add_header ('apim-accesstoken',OOOOOOO00O00O00OO )#line:66
 O000O0OOOO000O0OO .add_header ('Content-Type','application/json;charset=utf-8')#line:67
 O000O0OOOO000O0OO .add_header ('User-Agent','Python_enos_api')#line:68
 for O0000O0000O000O00 ,O0O0O00O00OOOO00O in headers .items ():#line:70
  O000O0OOOO000O0OO .add_header (O0000O0000O000O00 ,O0O0O00O00OOOO00O )#line:71
 try :#line:73
  O0OO00OO0OOO0O000 =request .urlopen (O000O0OOOO000O0OO )#line:74
  OOO000OO0OOO0O0O0 =O0OO00OO0OOO0O000 .read ().decode ('UTF-8')#line:76
  OOOOOO0OO0O0000OO =simplejson .loads (OOO000OO0OOO0O0O0 )#line:77
  try :#line:78
   O00OOOO0O0OOOOO00 =OOOOOO0OO0O0000OO ['apim_status']#line:79
   if O00OOOO0O0OOOOO00 ==4011 :#line:81
    O0O00OO00OOO0OO0O =OOOOOO0OO0O0000OO ['apim_refreshtoken']#line:82
    OO00OO00O0O0O0O0O =__OO0OO000OOO00OO0O (OO0OOO0OO00O0OOOO ,s_time )#line:83
    OOOOOOO00O00O00OO =__OOO00OO0O00O00OOO (OO0OOO0OO00O0OOOO ,O0000O0000O000O00 ,O00000OO0OO0OOOO0 ,OO00OO00O0O0O0O0O ,O0O00OO00OOO0OO0O )#line:84
   elif O00OOOO0O0OOOOO00 ==4012 :#line:85
    O00O0OO000O00OO00 =__O000OO0O0OO0O00OO (OO0OOO0OO00O0OOOO ,s_time ,l_time )#line:86
    OOOOOOO00O00O00OO =__OOO00OO0O00O00OOO (OO0OOO0OO00O0OOOO ,O0000O0000O000O00 ,O00000OO0OO0OOOO0 ,O00O0OO000O00OO00 [0 ],O00O0OO000O00OO00 [1 ])#line:87
   else :#line:88
    return OOOOOO0OO0O0000OO #line:89
   print ('the second time request')#line:91
   if data !=None :#line:93
    data =json .dumps (data );#line:94
    data =bytes (data ,'UTF-8')#line:95
   O000O0OOOO000O0OO =request .Request (O00OO00O0OO0O0O0O ,data )#line:97
   O000O0OOOO000O0OO .add_header ('apim-accesstoken',OOOOOOO00O00O00OO )#line:98
   O000O0OOOO000O0OO .add_header ('Content-Type','application/json;charset=utf-8')#line:99
   O000O0OOOO000O0OO .add_header ('User-Agent','Python_enos_api')#line:100
   for O0000O0000O000O00 ,O0O0O00O00OOOO00O in headers .items ():#line:102
    O000O0OOOO000O0OO .add_header (O0000O0000O000O00 ,O0O0O00O00OOOO00O )#line:103
   O0OO00OO0OOO0O000 =request .urlopen (O000O0OOOO000O0OO )#line:105
   return O0OO00OO0OOO0O000 .read ().decode ('UTF-8')#line:106
  except KeyError :#line:107
   return OOOOOO0OO0O0000OO #line:108
 except error .URLError as O00OO0OOO0OOOOO0O :#line:109
  print (O00OO0OOO0OOOOO0O )#line:110
