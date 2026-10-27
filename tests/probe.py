import urllib.request,urllib.parse,http.cookiejar,re,json
op=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
r=op.open('http://127.0.0.1:8080/?page=register').read().decode()
token=re.search('name="csrf" value="([^"]+)"',r)[1]
r=op.open('http://127.0.0.1:8080/?page=register',urllib.parse.urlencode({'csrf':token,'action':'register'}).encode())
body=r.read().decode()
print(json.dumps({'incomplete_registration_has_php_warning':'Warning' in body,'unknown_page_status':op.open('http://127.0.0.1:8080/?page=unknown').status},indent=2))
