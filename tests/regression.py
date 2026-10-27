"""Проверки ошибок, найденных при ручном просмотре ответов и журнала."""
from http_client import Client
import json
from pathlib import Path
c=Client()
status,body,_=c.post('register','register',{})
checks=[{'test':'Неполный POST регистрации без предупреждений PHP','passed':status==200 and 'Warning' not in body and 'Deprecated' not in body},
        {'test':'Неизвестная страница возвращает 404','passed':c.get('/?page=unknown')[0]==404}]
print(json.dumps(checks,ensure_ascii=False,indent=2))
Path('evidence/regression.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2))
raise SystemExit(not all(c['passed'] for c in checks))
