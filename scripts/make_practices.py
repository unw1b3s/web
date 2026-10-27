from pathlib import Path
from html import escape as h
import json, shutil
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'practices'; P.mkdir(exist_ok=True)
NAMES={1:'Анализ предметной области и требования',2:'Проектирование базы данных и ER-диаграмма',3:'Разработка модулей ИС',4:'Подсистема безопасности',5:'Поиск и анализ информации',6:'Требования к дизайну',7:'Дизайн-концепция',8:'Современный и мобильный дизайн',9:'Улучшение форм и интерфейса',10:'Разработка интерфейса пользователя',11:'Разработка веб-приложения',12:'Доработка структуры БД',13:'Интеграция адаптивного дизайна',14:'Анимация и микро-анимации',15:'Оптимизация кода и производительности',16:'Финальное тестирование',17:'Адаптация тематики ИС',18:'Тестирование вариативной части',20:'Разбор ошибок и план устранения пробелов'}
F={n:P/f'{n:02d} {name}' for n,name in NAMES.items()}
for f in F.values(): f.mkdir(exist_ok=True)
CSS='body{font:16px/1.6 Arial,sans-serif;color:#202b3c;background:#f7f8fa;margin:0}main{max-width:1080px;margin:32px auto;padding:32px;background:white;border:1px solid #dce2ea;border-radius:8px}h1,h2{font-family:Georgia,serif;line-height:1.25}h1{font-size:30px}a{color:#285cbd}img{max-width:100%}pre{white-space:pre-wrap;background:#f1f4f8;padding:16px}table{border-collapse:collapse;width:100%}td,th{border:1px solid #dce2ea;text-align:left;padding:10px}.muted{color:#5e6c7e}.swatch{display:inline-block;width:150px;padding:30px 10px;margin:8px;border-radius:6px} @media(max-width:600px){main{margin:0;padding:20px}h1{font-size:26px}}'
def page(title,body): return f'<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{h(title)}</title><style>{CSS}</style><main>{body}</main></html>'
def mdhtml(text):
    out=[]
    for block in text.strip().split('\n\n'):
        if block.startswith('# '):out.append('<h2>'+h(block[2:])+'</h2>')
        elif block.startswith('## '):out.append('<h3>'+h(block[3:])+'</h3>')
        else:out.append('<p>'+h(block).replace('\n','<br>')+'</p>')
    return ''.join(out)
# Векторная диаграмма без сетевых зависимостей.
boxes=[(25,35,'users',['id INT UNSIGNED PK','login VARCHAR(40) UNIQUE','password_hash VARCHAR(255)','email VARCHAR(254) UNIQUE','phone VARCHAR(12)','role ENUM(participant,admin)']), (715,35,'events',['id INT UNSIGNED PK','title VARCHAR(160)','event_date DATETIME','location VARCHAR(160)','description TEXT','theme ENUM(conference,workshop)']), (370,285,'applications',['id INT UNSIGNED PK','user_id INT UNSIGNED FK','event_id INT UNSIGNED FK','status_id TINYINT UNSIGNED FK','payment ENUM(card,invoice)','room ENUM(main,small,online)','created_at TIMESTAMP','UNIQUE(user_id,event_id)']), (25,365,'statuses',['id TINYINT UNSIGNED PK','code VARCHAR(20) UNIQUE','name VARCHAR(30)']), (715,365,'reviews',['id INT UNSIGNED PK','application_id INT UNSIGNED FK UNIQUE','body TEXT','rating TINYINT UNSIGNED CHECK 1..5','created_at TIMESTAMP'])]
def diagram(initial=False):
    b=['<svg xmlns="http://www.w3.org/2000/svg" width="1060" height="680" viewBox="0 0 1060 680"><rect width="1060" height="680" fill="#f7f8fa"/><g fill="none" stroke="#6782aa" stroke-width="2"><path d="M185 224 L185 270 L370 320"/><path d="M875 224 L875 270 L680 320"/>']
    if not initial:b.append('<path d="M335 435h35M680 435h35"/>')
    b.append('</g><g font-family="Arial" fill="#202b3c" font-size="13">')
    for x,y,title,fields in boxes:
        if initial and title in ['statuses','reviews']:continue
        if initial and title=='applications':fields=[v.replace('status_id TINYINT UNSIGNED FK','status ENUM(new,assigned,completed)') for v in fields]
        height=45+len(fields)*24
        b.append(f'<rect x="{x}" y="{y}" width="310" height="{height}" rx="7" fill="white" stroke="#bccbdc"/><text x="{x+15}" y="{y+25}" font-weight="bold" font-size="18">{title}</text>')
        for i,field in enumerate(fields):b.append(f'<text x="{x+15}" y="{y+53+i*24}">{h(field)}</text>')
    b.append('<text x="30" y="640">users 1 → N applications; events 1 → N applications; users N ↔ M events через applications</text>')
    if not initial:b.append('<text x="30" y="665">statuses 1 → N applications; applications 1 → 0..1 reviews</text>')
    return ''.join(b)+'</g></svg>'
(ROOT/'docs/er-final.svg').write_text(diagram())
(ROOT/'docs/er-initial.svg').write_text(diagram(True))
for n in [2,12]:
    shutil.copy(ROOT/'docs/er-final.svg',F[n]/'er-final.svg');shutil.copy(ROOT/'docs/er.mmd',F[n]/'er.mmd')
shutil.copy(ROOT/'docs/er-initial.svg',F[2]/'er-initial.svg')
shutil.copy(ROOT/'database/001_initial.sql',F[2]/'001_initial.sql')
shutil.copy(ROOT/'database/migrations/002_statuses_reviews.sql',F[12]/'002_statuses_reviews.sql')
shutil.copy(ROOT/'evidence/migration.json',F[12]/'migration.json')
REPORTS={
1:'Я описал назначение портала, роли гостя, участника и администратора. Определил требования к заявкам, статусам, отзывам, безопасности и мобильной версии. Подробности — requirements.md.',
2:'Я выделил пользователей, мероприятия, заявки, статусы и отзывы. Связь пользователей и мероприятий многие-ко-многим реализовал через заявки; отзыв связан с одной заявкой. В ER-диаграмме указал типы, первичные, внешние и уникальные ключи. Сохранил исходную и итоговую схемы; справочник статусов и отзывы внедрил миграцией в №12.',
3:'Я разделил проект на public, app и database. Написал классы Database, Auth и Portal. Реализовал регистрацию с проверками, вход, создание и просмотр заявок, административную панель. Рабочие исходники находятся в ../../app и ../../public; первый коммит реализации 2f54b6d.',
4:'Я добавил password_hash/password_verify, подготовленные SQL-запросы, экранирование HTML, CSRF-токены и проверку роли на сервере. При входе обновляется ID сессии; cookie HttpOnly и SameSite=Lax, Secure при HTTPS. Проверил запрет чужого удаления, смены статуса участником, SQL-инъекцию и XSS. Результаты — security-tests.json.',
5:'Я составил краткий офлайн-справочник по PHP/PDO и использовал локальную справку CLI. При анализе журнала обнаружил Undefined array key при неполной регистрации. Добавил значения по умолчанию. Сохранил исходные сообщения, воспроизведение и результат повторной проверки. История исправления — коммит e3b7204.',
6:'Я определил аудиторию, цвета, типографику, список страниц и требования к каждой форме. Для телефонов выбрал одну колонку, крупные кнопки и перенос навигации. Требования сохранил в design.md.',
7:'Я собрал мудборд с простыми векторными мотивами общения и обучения, палитрой и парой Georgia/Arial. Сделал HTML-макеты регистрации, входа, кабинета, заявок, создания заявки и админки. Сопоставил макеты с выбранным синим фирменным стилем. Согласование с внешним заказчиком не проводилось.',
8:'Я использовал карточки, свободное пространство и короткие реакции кнопок. Создал отдельные mobile-*.html для шести экранов под 390×844. Графика — небольшие SVG без внешних шрифтов и фотографий. Проверил макеты в браузере с мобильным размером; физический смартфон не использовал.',
9:'Я вывел ошибки прямо в форме, заменил оплату и помещение выпадающими списками. В админке добавил фильтр статуса и карточки заявок. Проверил, что сервер запрещает отзыв до завершения заявки и даты мероприятия.',
10:'Я сверстал все страницы на HTML, CSS и JavaScript. Проверил Chrome и WebKit, настольную ширину 1280 и мобильную 390. Горизонтального переполнения нет. Протокол — crossbrowser.json, снимок — screenshot.png.',
11:'Я связал формы с PHP и MySQL. Добавление выполняется для пользователей, заявок и отзывов; чтение — в списках; изменение — в статусах; удаление — для своей новой заявки. Статусы меняются последовательно, отзыв сохраняется один раз после завершения. Протокол HTTP-тестов приложен.',
12:'Я добавил отдельные таблицы statuses и reviews. Миграция преобразует строковый статус старой заявки в внешний ключ. На отдельной заполненной БД проверил сохранение id, user_id, event_id и статуса assigned, внешние ключи, CHECK оценки и отсутствие потерянных связей. Обновил ER-диаграмму; результаты — migration.json.',
13:'Я проверил главную, регистрацию, вход, кабинет, форму заявки, свои заявки и админку при 390×844. Применил гибкую сетку, перенос навигации и медиазапрос. Браузерная проверка ширины не обнаружила горизонтальной прокрутки; приложены мобильные снимки.',
14:'Я добавил появление содержимого страницы (250 мс), реакции карточек и кнопок, выделение фокуса. Анимации используют opacity и transform; prefers-reduced-motion их отключает. Проверил это в браузере; ошибок JavaScript нет. Сетевого фреймворка анимаций не потребовалось.',
15:'Я вынес общую работу с БД и правами в классы, использовал JOIN вместо отдельных запросов для каждой карточки. Добавил индекс status_created и уникальный индекс user_id/event_id. Подключил минифицированные CSS/JS, сохранив читаемые исходники. Замеры локальных запросов — performance.json; они не являются нагрузочным тестом.',
16:'Я проверил регистрацию, вход, создание и удаление заявки, роли, статусы, отзывы и защиту форм. Исправил найденные предупреждения PHP и неверный HTTP-код неизвестной страницы. Результаты HTTP, регрессионной и браузерной проверки сохранены. История коммитов приложена; завершающий коммит материалов есть в git log.',
17:'Я адаптировал портал под творческие мастер-классы «Мастерские.РФ». Изменил тексты, коричневую палитру, SVG и список мероприятий. Вариант запускается с APP_THEME=workshop, использует ту же PHP-логику и MySQL. Заявки отображаются только для текущей тематики. Исходники варианта — общий app и public; запуск — ../../scripts/variant.sh.',
18:'Я повторил 30 HTTP-проверок для «Мастерские.РФ», включая регистрацию, заявку, статусы, удаление и отзыв. Проверил вариант в Chrome и WebKit. Протокол — variant-tests.json; снимок сделан с работающего приложения. История коммитов приложена.',
20:'Я разобрал реальные ошибки локальных проверок: предупреждения при неполной регистрации и код 200 для отсутствующей страницы. Сохранил воспроизведение до исправления и регрессионные проверки после. Пробный экзамен №19 не проходил; его результаты и оценку не указываю. Составил план повторения и вопросы для итоговой консультации. Консультация с преподавателем ещё не проведена.'}
EXTRA={}
for n,src in [(1,'requirements.md'),(6,'design.md'),(5,'offline-handbook.md')]:
    shutil.copy(ROOT/'docs'/src,F[n]/src);EXTRA[n]=mdhtml((ROOT/'docs'/src).read_text())
for n in [2,12]:EXTRA[n]='<h2>Итоговая ER-диаграмма</h2><img src="er-final.svg" alt="ER-диаграмма пяти таблиц">'
# Мудборд: реальные локальные векторные материалы и типографика.
mood='<h2>Мудборд: знания и общение</h2><img src="../../public/assets/conference.svg" width="190" alt="Конференция"><p>Спокойный фон, контурные иллюстрации, карточки без декоративных эффектов.</p>'
for color in ['#285cbd','#202b3c','#eaf0fc','#f7f8fa']:
    mood+=f'<span class="swatch" style="background:{color};color:{"white" if color in ["#285cbd","#202b3c"] else "#202b3c"}">{color}</span>'
mood+='<h2>Georgia — заголовки</h2><p>Arial — основной текст и элементы форм.</p>'
EXTRA[7]=mood
(F[7]/'moodboard.html').write_text(page('Мудборд',mood))
# Шесть отдельных статических макетов, и шесть самостоятельных мобильных HTML.
mockups={
'register':('Регистрация','<label>Логин<input placeholder="student"></label><label>Почта<input placeholder="student@example.ru"></label><label>Телефон<input placeholder="+79991234567"></label><label>Пароль<input type="password" value="Student123"></label><button type="button">Зарегистрироваться</button>'),
'login':('Вход','<label>Логин<input placeholder="student"></label><label>Пароль<input type="password"></label><button type="button">Войти</button>'),
'account':('Личный кабинет','<h2>Здравствуйте, student!</h2><p>Почта: student@example.ru</p><p>Телефон: +79991234567</p><a class="button" href="mobile-applications.html">Мои заявки</a>'),
'applications':('Мои заявки','<article class="card"><span class="badge">Новая</span><h2>Веб-разработка: первые шаги</h2><p>15.03.2027 · Москва</p><p>Карта · Большой зал</p><button class="secondary" type="button">Удалить заявку</button></article>'),
'apply':('Новая заявка','<label>Мероприятие<select><option>Веб-разработка: первые шаги</option></select></label><label>Оплата<select><option>Карта</option><option>По счёту</option></select></label><label>Помещение<select><option>Большой зал</option><option>Малый зал</option></select></label><button type="button">Отправить заявку</button>'),
'admin':('Все заявки','<label>Статус<select><option>Все статусы</option><option>Новая</option></select></label><article class="card"><span class="badge">Новая</span><h2>Веб-разработка: первые шаги</h2><p>Участник: student</p><button type="button">Назначить</button></article>')}
for key,(title,body) in mockups.items():
    for n,prefix in [(7,'mockup-'),(8,'mobile-')]:
        nav=' '.join(f'<a href="{prefix}{k}.html">{h(t)}</a>' for k,(t,_) in mockups.items())
        content=f'<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{h(title)} — макет</title><link rel="stylesheet" href="../../public/assets/style.min.css"><header><a class="brand" href="{prefix}account.html">Конференции.РФ</a></header><main><p class="eyebrow">МАКЕТ · {"390×844" if n==8 else "НАСТОЛЬНЫЙ ЭКРАН"}</p><section class="form-panel"><h1>{h(title)}</h1>{body}</section><p>{nav}</p></main></html>'
        (F[n]/f'{prefix}{key}.html').write_text(content)
EXTRA[7]+='<h2>Макеты страниц</h2>'+''.join(f'<p><a href="mockup-{k}.html">{h(t)}</a></p>' for k,(t,_) in mockups.items())
EXTRA[8]='<h2>Мобильные HTML-макеты 390×844</h2>'+''.join(f'<p><a href="mobile-{k}.html">{h(t)}</a></p>' for k,(t,_) in mockups.items())
# Копии протоколов рядом с соответствующей работой.
for n,src,dest in [(4,'http-8080.json','security-tests.json'),(10,'crossbrowser.json','crossbrowser.json'),(11,'http-8080.json','http-tests.json'),(13,'browser.json','mobile-tests.json'),(14,'browser.json','animation-tests.json'),(15,'http-8080.json','performance.json'),(16,'http-8080.json','http-tests.json'),(16,'regression.json','regression.json'),(18,'http-8081.json','variant-tests.json'),(20,'probe-before.json','before.json'),(20,'regression.json','after.json')]:
    if (ROOT/'evidence'/src).exists():shutil.copy(ROOT/'evidence'/src,F[n]/dest)
for n,src in [(5,'bugs-before.txt'),(20,'bugs-before.txt')]:shutil.copy(ROOT/'evidence'/src,F[n]/src)
for n in [15,16,18]:
    src='http-8081.json' if n==18 else 'http-8080.json';data=json.loads((ROOT/'evidence'/src).read_text());
    EXTRA[n]=f'<h2>Фактические результаты</h2><p>HTTP-проверки: {data["passed"]} / {data["total"]}. Сервер: {h(data["base"])}.</p><p>10 локальных запросов главной: min {data["home_ms"]["min"]} мс, среднее {data["home_ms"]["mean"]} мс, max {data["home_ms"]["max"]} мс.</p>'
    if n!=15:EXTRA[n]+='<table><tr><th>Проверка</th><th>Результат</th></tr>'+''.join('<tr><td>'+h(x['test'])+'</td><td>'+('Пройдена' if x['passed'] else 'Ошибка')+'</td></tr>' for x in data['tests'])+'</table>'
# План основан только на воспроизведённых дефектах.
plan='''# План устранения пробелов

Я использовал результаты локальной проверки приложения. Пробный экзамен №19 не выполнял, экзаменационную оценку не получал.

1. Неполный POST регистрации: в ответ попадали PHP Warning Undefined array key login/email/phone. Причина — прямое чтение необязательных ключей массива. Исправил: задал пустые значения по умолчанию, сохранил серверную валидацию, отключил display_errors. Проверка tests/regression.py теперь проходит. Относится к направлению задания 1: обработка данных и безопасность.

2. Неизвестная страница: /?page=unknown возвращала 200. Причина — отсутствовала проверка списка страниц. Исправил: добавил разрешённые маршруты и HTTP 404. Повторная проверка проходит. Относится к направлению задания 3: финальное тестирование и исправление ошибок.

3. При просмотре результата сборки заметил, что CSS уменьшился только на 1 байт: исходник уже был записан одной строкой. Сделал исходник читаемым и оставил отдельную сборку. Итог: 5135 → 4448 байт CSS, 806 → 570 байт JS. Относится к направлению задания 3: читаемость и оптимизация.

По направлению задания 2 в выполненных проверках ошибок адаптивности не обнаружил; оснований приписывать их себе нет. Проверка выполнена в браузерной эмуляции, физический смартфон не использовался.

Сопоставление с КИМ 09.02.07-3-2027, том 1, таблица 8 (стр. 14): ошибка 1 затрагивает проверку данных и защиту системы; ошибка 2 — корректность работы модулей и интерфейса; замечание 3 — качество кода и оптимизацию. Это мой разбор рисков относительно критериев, а не официальный перечень типичных ошибок: отдельного списка типичных ошибок в тексте спецификации я не нашёл. Экзаменационные баллы себе не выставлял. Копия спецификации опубликована на сайте колледжа: https://kpiot.ru/kpiot.ru/%D0%A1%D1%82%D1%83%D0%B4%D0%B5%D0%BD%D1%82%D1%83/%D0%93%D0%98%D0%90/09.02.07/%D0%9A%D0%98%D0%9C%2009.02.07-3-2027%20%D0%A2%D0%BE%D0%BC%201.pdf

План: перед следующей проверкой повторить обработку пустых/подменённых POST-данных (30 минут), HTTP-коды и маршрутизацию (20 минут), сборку и чтение замеров (20 минут). Критерий готовности: регрессионные и функциональные тесты проходят, журнал PHP не содержит предупреждений, в репозитории есть исходники и минифицированные файлы.

Для консультации подготовил вопросы: достаточно ли принятого состава полей заявки для конкретного варианта КИМ; какие требования комиссии к оформлению схем и отчётов; как будет организована итоговая консультация на индивидуальном графике. Консультация пока не проведена.
'''
(F[20]/'plan.md').write_text(plan);EXTRA[20]=mdhtml(plan)
for n in [2,4,12,15]:
    if (ROOT/'evidence/database.json').exists(): shutil.copy(ROOT/'evidence/database.json',F[n]/'database.json')
for n in [5,16,18]:
    if (ROOT/'docs/history.txt').exists(): shutil.copy(ROOT/'docs/history.txt',F[n]/'history.txt')
if (ROOT/'docs/php-cli.txt').exists(): shutil.copy(ROOT/'docs/php-cli.txt',F[5]/'php-cli.txt')
# Номера работ и ссылки на единый рабочий код явно указаны в каждом отчёте.
for n,f in F.items():
    report=f'# Практическая работа №{n}. {NAMES[n]}\n\n{REPORTS[n]}\n\nРабочий код: ../../app, ../../public, ../../database. Скриншот результата: screenshot.png. Проверки и дополнительные материалы перечислены в result.html.\n'
    (f/'report.md').write_text(report)
    files=''.join(f'<li><a href="{h(x.name)}">{h(x.name)}</a></li>' for x in sorted(f.iterdir()) if x.suffix in ['.md','.json','.sql','.svg','.mmd','.txt'])
    (f/'result.html').write_text(page(NAMES[n],f'<p class="muted">МДК · Индивидуальный график</p><h1>Практическая работа №{n}<br>{h(NAMES[n])}</h1><p>{h(REPORTS[n])}</p>'+EXTRA.get(n,'')+f'<h2>Материалы</h2><ul>{files}</ul><p><a href="screenshot.png">Скриншот результата</a></p><p><a href="../../README.md">Запуск приложения и рабочие исходники</a></p>'))
(P/'index.html').write_text(page('Практические работы','<h1>Конференции.РФ · Практические работы</h1><p>№1–18 и №20. Рабочее приложение: PHP и MySQL. №19 не выполнялась.</p><ol>'+''.join(f'<li value="{n}"><a href="{h(f.name)}/result.html">{h(NAMES[n])}</a></li>' for n,f in F.items())+'</ol>'))
(ROOT/'evidence/practice-map.json').write_text(json.dumps({str(n):str(f.relative_to(ROOT)) for n,f in F.items()},ensure_ascii=False,indent=2))
print('Создано папок:',len(F))
