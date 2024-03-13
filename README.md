# GOD SYSTEM Bot ![](https://img.shields.io/badge/1.0-7393B3)
![](https://img.shields.io/badge/Developed_on-Disnake-blue) ![](https://img.shields.io/badge/VALORANT_API_by-Henrik_Mertens-red)

Бот для себя и друзей

# Хостинг
[client.pylexnodes.net](https://client.pylexnodes.net/) - всегда бесплатный

# Функционал
- /about - информация о боте
- Каждое действие логируется в консоль
### Экономика
- /registration - регистрация в боте
- /balance - просмотр баланса
- /transfer [сумма] [получтель] - перевод пользователю
- /antibomj - добирает пользователю баланс до установленного минимума (меняется в скрипте, кд 24 часа)
- /taxi - работа таксистом (оплата 5.000, кд 30 минут)
- /factory - работа на заводе (оплата 10.000, кд 1 час)
### VALORANT
- /valstats [ник] [тег] [регион] - краткий обзор профиля VALORANT
- /valmatches [ник] [тег] [регион] - отображает последние 5 рейтинговых игр
# Админский функционал
### Модерация
- .mute [@member] [hours: int] - выдает тайм-аут пользователю на указанное кол-во часов (минимально 1, максимально 672)
- .unmute [@member] - убирает тайм-аут с пользователя
- .kick [@member] - кикает пользователя
- .ban [@member] - банит пользвателя
- .clear [amount: int] - очищает указанное кол-во сообщений
### Экономика
- .godgive [amount: int] [@member] - выдает валюту
- .godtake [amount: int] [@member] - забирает валюту
### Embeds
- embed_templates.json - пресеты для .embed
- .embed [template: str] - отправляет указанный пресет embed
- .embeds_view - просмотр доступных пресетов для .embed
# Скрипты 
### economy_system.py
- balances.json - база данных
- .on_reg [user_id: int = inter/ctx.author.id] - вносит пользователя в базу данных и присваивает ему минимальный баланс (меняется в скрипте)
  - True: пользователь успешно внесен в базу данных
  - False: пользователь уже есть в базе данных
- .balance(user_id=inter/ctx.author.id, transfer_mode=True/False) - возвращает баланс пользователя из базы данных
  - Возвращает абсолютное число (например: 1000, 10000) если (transfer_mode=True), возвращает отформатированное число (например: 1.000, 10.000) если (transfer_mode=False)
  - False: пользователь не найден в базе данных
- .add(user_id=inter/ctx.author.id, amount: int) - добавляет указанное значение валюты пользователю в базу данных
  - Возвращает True в любом случае (форсированно обновляет базу данных, даже если там нет пользователя)
- .remove(user_id=inter/ctx.author.id, amount: int) - удаляет указанное значение валюты пользователя из базы данных
  - True: база данных успешно обновлена
  - False: пользователь не найден в базе данных
### valorant_system.py
- .get_player_info(name: str, tag: str, region: str) - возвращает словарь с краткой информацией о запрашиваемом пользователе
  - Возвращает
    - Уровень ('level')
    - Широкую версию карточки ('card': 'url')
    - Текущий ранг ('current_rank')
    - Иконку текущего ранга ('current_rank_icon': 'url')
    - Текущее эло ('current_elo)
    - Последнее изменение эло ('last_elo_change')
    - Наивысший ранг ('highest_rank')
    - Сезон наивысшего ранга ('highest_rank_season')
- .get_matches(name: str, tag: str, region: str) - возвращает словарь с 5-ю последними играми 
  - Возвращает
    - Карту (['game_{game_number}']['map'])
    - Персонажа (['game_{game_number}']['character'])
    - Личный счет (['game_{game_number}']['score'])
    - Кол-во убийств (['game_{game_number}']['kills'])
    - Кол-во смертей (['game_{game_number}']['deaths'])
    - Кол-во помощи (['game_{game_number}']['assists'],
    - К/Д (['game_{game_number}']['k/d'])
    - Результат игры (['game_{game_number}']['result'])
    - Счет команды запрашиваемого пользователя (['game_{game_number}']['team_a'])
    - Счет противоположной команды (['game_{game_number}']['team_b'])
    - Изменение эло после игры (['game_{game_number}']['elo'])
    - Месяц, число и год игры (['game_{game_number}']['date'])
    - Всего побед (['game_{game_number}']['total_wins'])
    - Всего поражений (['game_{game_number}']['total_lose'])
    - Всего игр в ничью (['game_{game_number}']['total_ff'])
    - Общее К/Д (['game_{game_number}']['total_k/d'])
    - Общее изменение эло (['game_{game_number}']['total_elo'])
