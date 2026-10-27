"""Интеграционные проверки настоящего HTTP-сервера и MySQL, без пакетов."""
import http.cookiejar, urllib.request, urllib.parse, urllib.error, re, json, time, sys
from pathlib import Path
BASE = sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8080'
class Client:
    def __init__(self): self.opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    def get(self,path='/'):
        try:
            r=self.opener.open(BASE+path); return r.status,r.read().decode(),dict(r.headers)
        except urllib.error.HTTPError as r: return r.code,r.read().decode(),dict(r.headers)
    def post(self,page,action,data=None,token=True):
        _,html,_=self.get('/?page='+page)
        csrf=re.search('name="csrf" value="([^"]+)"',html)
        fields={'action':action, **(data or {})}
        if token and csrf: fields['csrf']=csrf[1]
        try:
            r=self.opener.open(BASE+'/?page='+page,urllib.parse.urlencode(fields).encode()); return r.status,r.read().decode(),dict(r.headers)
        except urllib.error.HTTPError as r: return r.code,r.read().decode(),dict(r.headers)
