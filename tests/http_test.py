"""Интеграционные проверки настоящего HTTP-сервера и MySQL, без пакетов."""
import http.cookiejar, urllib.request, urllib.parse, urllib.error, re, json, time, sys
from pathlib import Path
BASE = sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8080'
results=[]
from http_client import Client
def check(name,condition):
    results.append({'test':name,'passed':bool(condition)})
    print(('PASS ' if condition else 'FAIL ')+name)
guest=Client(); status,home,headers=guest.get()
check('Главная страница и CSP',status==200 and 'Content-Security-Policy' in headers)
check('Защищённая cookie', 'HttpOnly' in headers.get('Set-Cookie','') and 'SameSite=Lax' in headers.get('Set-Cookie',''))
check('Гость перенаправлен на вход','Введите логин и пароль.' in guest.get('/?page=admin')[1])
check('CSRF отклонён', guest.post('register','register',{},False)[0]==403)
check('Неполная регистрация обрабатывается без 500', guest.post('register','register',{})[0]==200)
check('Короткий пароль отклонён','Пароль:' in guest.post('register','register',{'login':'validlogin','email':'new@example.ru','phone':'+79991234567','password':'123'})[1])
check('Неверные форматы отклонены','корректную почту' in guest.post('register','register',{'login':'bad!','email':'bad','phone':'123','password':'Student123'})[1])
login='test_'+str(time.time_ns())[-12:]
data={'login':login,'email':login+'@example.ru','phone':'+79991234567','password':'Student123'}
check('Регистрация успешна','Регистрация завершена' in guest.post('register','register',data)[1])
check('Дубликат отклонён','уже заняты' in guest.post('register','register',data)[1])
check('SQL-инъекция не даёт вход','Неверный логин' in guest.post('login','login',{'login':"' OR 1=1 -- ",'password':'x'})[1])
check('Вход участника','Здравствуйте' in guest.post('login','login',{'login':login,'password':'Student123'})[1])
check('Участнику запрещена админка',guest.get('/?page=admin')[0]==403)
_,form,_=guest.get('/?page=apply'); event=re.search(r'<option value="(\d+)"',form)[1]
check('Подмена способа оплаты отклонена','Выберите оплату' in guest.post('apply','apply',{'event':event,'payment':'hack','room':'main'})[1])
check('Создание заявки','Изменения сохранены' in guest.post('apply','apply',{'event':event,'payment':'card','room':'main'})[1])
check('Повторная заявка отклонена','уже подали' in guest.post('apply','apply',{'event':event,'payment':'card','room':'main'})[1])
_,apps,_=guest.get('/?page=applications'); aid=re.search(r'Заявка №(\d+)',apps)[1]
check('Ранний отзыв отклонён','Отзыв доступен только' in guest.post('applications','review',{'id':aid,'body':'Хорошая конференция','rating':'5'})[1])
check('Подмена роли отклонена',guest.post('applications','status',{'id':aid,'status':'2'})[0]==403)
other=Client(); other.post('login','login',{'login':'other','password':'Student123'})
check('Чужая заявка скрыта',('Заявка №'+aid+'<') not in other.get('/?page=applications')[1])
check('Чужое удаление отклонено','Можно удалить только' in other.post('applications','cancel',{'id':aid})[1])
check('Своя новая заявка удалена','Изменения сохранены' in guest.post('applications','cancel',{'id':aid})[1])
admin=Client(); admin.post('login','login',{'login':'admin','password':'Admin12345'})
_,allapps,_=admin.get('/?page=admin'); check('Администратор видит заявки','Участник:' in allapps)
reviewer=Client(); reviewer.post('login','login',{'login':'reviewer','password':'Student123'})
_,rapps,_=reviewer.get('/?page=applications'); rid=re.search(r'Заявка №(\d+)',rapps)[1]
# Фикстура содержит прошедшее мероприятие и новую заявку.
check('Нельзя пропустить статус','Разрешён только следующий' in admin.post('admin','status',{'id':rid,'status':'3'})[1])
status_text=admin.post('admin','status',{'id':rid,'status':'2'})[1]
check('Новая → назначено','Изменения сохранены' in status_text)
check('Назначено → завершено','Изменения сохранены' in admin.post('admin','status',{'id':rid,'status':'3'})[1])
check('Фильтр статусов','Назначено</span>' not in admin.get('/?page=admin&status=3')[1])
check('Некорректная оценка отклонена','оценка от 1 до 5' in reviewer.post('applications','review',{'id':rid,'body':'Отличное мероприятие','rating':'9'})[1])
body='<script>alert(1)</script> Полезная встреча'
check('Отзыв после завершения сохранён','Изменения сохранены' in reviewer.post('applications','review',{'id':rid,'body':body,'rating':'5'})[1])
check('XSS экранирован','&lt;script&gt;' in reviewer.get('/?page=applications')[1] and '<script>alert(1)</script>' not in reviewer.get('/?page=applications')[1])
check('Повторный отзыв отклонён','уже оставлен' in reviewer.post('applications','review',{'id':rid,'body':'Ещё один отзыв','rating':'5'})[1])
check('Выход завершает доступ','Введите логин' in guest.post('account','logout')[1] or 'Войти' in guest.get('/?page=account')[1])
times=[]
for _ in range(10):
    start=time.perf_counter(); guest.get(); times.append(round((time.perf_counter()-start)*1000,2))
report={'base':BASE,'tests':results,'passed':sum(r['passed'] for r in results),'total':len(results),'home_ms':{'min':min(times),'mean':round(sum(times)/len(times),2),'max':max(times)},'note':'Локальные запросы, не нагрузочный тест.'}
Path('evidence/http-'+BASE.rsplit(':',1)[-1]+'.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
sys.exit(0 if all(r['passed'] for r in results) else 1)
