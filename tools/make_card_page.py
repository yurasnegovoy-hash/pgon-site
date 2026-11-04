"""Собирает card.html, страницу для рекламы в Meta, из index.html.
Подача как у одобренных Meta конкурентов, Swapster и MarketcoinPay: карта Visa в Telegram для поездок, подписок и жизни за границей.
Убраны рубли, СБП, QR СБП, USDT, P2P и обменники. Пиксель и передача визита в бота остаются как на главной.
Запуск после правок index.html: python3 tools/make_card_page.py"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
t = (ROOT / "index.html").read_text()


def cut(start, end_marker="</section>"):
    """Вырезает блок от start до ближайшего end_marker включительно."""
    global t
    i = t.index(start)
    j = t.index(end_marker, i) + len(end_marker)
    t = t[:i] + t[j:]


def rep(a, b):
    global t
    assert a in t, a[:60]
    t = t.replace(a, b)


rep('<a href="#how">Как работает</a><a href="#family">Родным</a>', '<a href="#services">Сервисы</a><a href="#trust">Документы</a>')
cut('<div class="cur-band"', "</div></div>")
cut('<section id="how">')
cut('<section class="manifesto"')
cut('<section id="who">')
cut('<section id="family">')
cut('<section id="calc">')
t = re.sub(r"// калькулятор, курс примерный\n.*?calc\(40000\);\n", "", t, flags=re.S)

rep('<title>PGON для релокантов</title>', '<title>PGON: карта Visa в Telegram</title>\n<meta name="robots" content="noindex">')
rep(t[t.index('<meta name="description"'):t.index('>', t.index('<meta name="description"')) + 1],
    '<meta name="description" content="Международная карта Visa в Telegram для поездок, подписок и покупок онлайн. Выпуск за 2 минуты, Apple Pay и Google Pay">')
rep('<span class="eyebrow"><i></i>Для тех, кто давно живёт не в России</span>', '<span class="eyebrow"><i></i>Для поездок и жизни за границей</span>')
h1 = t[t.index("<h1>"):t.index("</h1>") + 5]
rep(h1, '<h1>Одна карта Visa<br><span class="grad">для покупок в </span><span class="rot" id="rot"><span class="on">поездках</span><span>сервисах</span><span>отелях</span><span>магазинах</span><span>кафе</span><span>такси</span></span></h1>')
lead = t[t.index('<p class="lead">'):t.index("</p>", t.index('<p class="lead">')) + 4]
rep(lead, '<p class="lead">Международная карта PGON живёт прямо в Telegram. Бронируй жильё и билеты, оплачивай подписки и покупки онлайн, а в магазине плати телефоном через Apple Pay и Google Pay</p>')
rep('<a class="btn btn-ghost" href="#how">Как это работает</a>', '<a class="btn btn-ghost" href="#services">Где работает карта</a>')
t1 = t[t.index('<div class="toast glass t1">'):t.index("</div>\n", t.index('<div class="toast glass t1">')) + 6]
rep(t1, '<div class="toast glass t1"><span class="ic" style="background:#ff385c">A</span><div><b>Airbnb</b><small>Visa · жильё в поездке</small></div><span class="amt">−€340</span></div>\n')
rep('<span class="ic" style="background:#222">Pay</span><div><b>Кофейня в Тбилиси</b>', '<span class="ic" style="background:#222">Pay</span><div><b>Кофейня у моря</b>')
rep('−12 GEL', '−€4,50')
rep('которые снова проходят</span></h2><p>Карта PGON с реальными реквизитами Visa работает там, где российская карта не проходит</p>',
    'в одной карте</span></h2><p>Карта PGON с реальными реквизитами Visa для сервисов, поездок и покупок онлайн</p>')
rep('<span class="eyebrow"><i></i>Друзья тоже уехали</span>', '<span class="eyebrow"><i></i>Путешествуйте вместе</span>')
rep('Друзья платят картой и по QR, а ты', 'Друзья платят картой, а ты')
fees = t[t.index('<div class="fees">'):t.index("</div>\n  </div>\n</section>", t.index('<div class="fees">'))]
rep(fees, '<div class="fees">\n      <div class="fee"><span>Выпуск виртуальной карты Visa</span><b class="hi">$8 один раз</b></div>\n'
          '      <div class="fee"><span>Пополнение баланса</span><b class="hi">0%</b></div>\n'
          '      <div class="fee"><span>Время до готовой карты</span><b>2 минуты</b></div>\n'
          '      <div class="fee"><span>Apple Pay и Google Pay</span><b>есть</b></div>\n    ')
faq = t[t.index('<div class="faq">'):t.index("</div>\n  </div>\n</section>", t.index('<div class="faq">'))]
rep(faq, '<div class="faq">\n'
         '      <details><summary>В каких странах работает карта?</summary><p>Карта Visa работает в любой стране, где принимают Visa, онлайн и в магазинах. Её можно добавить в Apple Pay и Google Pay</p></details>\n'
         '      <details><summary>Что можно оплачивать?</summary><p>Подписки и сервисы, жильё, билеты, такси, покупки в интернет-магазинах и в обычных магазинах телефоном</p></details>\n'
         '      <details><summary>В какой валюте баланс?</summary><p>В долларах. Если платишь в евро или другой валюте, пересчёт делает Visa в момент оплаты</p></details>\n'
         '      <details><summary>Сколько стоит карта?</summary><p>Выпуск виртуальной карты Visa стоит $8 один раз, карта готова через 2 минуты</p></details>\n'
         '      <details><summary>Нужна ли верификация?</summary><p>Да, все пользователи проходят проверку KYC по политике AML. Шаги верификации бот показывает при открытии кошелька</p></details>\n'
         '      <details><summary>Что если платёж не прошёл?</summary><p>Деньги не списываются и остаются на балансе. Поддержка в Telegram поможет разобраться за 15 минут</p></details>\n    ')
rep('<h2>Деньги из дома<br><span class="grad">работают везде</span></h2>', '<h2>Одна карта<br><span class="grad">для всего мира</span></h2>')

t = re.sub(r"/\*[^*]*?(?:рубл|РУБЛ|России)[^*]*?\*/", "/* */", t)
for bad in ("рубл", "СБП", "USDT", "P2P", "обменник", "российск", "России", "₽"):
    for m in re.finditer(bad, t):
        print("ОСТАЛОСЬ:", bad)
        break
(ROOT / "card.html").write_text(t)
print("card.html", len(t))
