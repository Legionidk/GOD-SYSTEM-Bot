import disnake
from disnake.ext import commands
from datetime import timedelta
import json
import economy_system
import valorant_system

secrets = {
    'stable': 'stable_token',
    'beta': 'beta_token'
}
bot = commands.Bot(command_prefix='.', help_command=None, intents=disnake.Intents.all(),
                   test_guilds=[000, 000, 000])


@bot.event
async def on_ready():
    await bot.change_presence(status=disnake.Status.do_not_disturb)
    print(f'[GOD SYSTEM] Бот запущен')


@bot.event
async def on_command_error(inter, error):
    if isinstance(error, commands.CommandNotFound):
        await inter.send(embed=disnake.Embed(title='Ошибка', description='Неизвестная команда.\n',
                                             color=0xb2b2b2))
        print(f'[GOD SYSTEM] [COMMAND ERROR] {inter.author.id} пытается использовать неизвестную команду')
    elif isinstance(error, commands.MissingPermissions):
        await inter.send(embed=disnake.Embed(title='Ошибка',
                                             description='Недостаточно прав для использования команды.\n',
                                             color=0xb2b2b2))
        print(f'[GOD SYSTEM] [COMMAND ERROR] {inter.author.id} пытается использовать команду, но получает ошибку '
              f'(недостаточно прав)')
    elif isinstance(error, commands.CommandOnCooldown):
        await inter.send(embed=disnake.Embed(title='Ошибка', description=f'На эту команду наложен кулдаун.\n'
                                                                         f'Вы сможете использовать ее повторно через '
                                                                         f'{str(error).split()[-1]}',
                                             color=0xb2b2b2))
        print(f'[GOD SYSTEM] [COMMAND ERROR] {inter.author.id} пытается использовать команду, но получает ошибку '
              f'(кулдаун)')
    elif isinstance(error, commands.MissingRequiredArgument):
        await inter.send(embed=disnake.Embed(title='Ошибка', description=f'Пропущен обязательный аргумент '
                                                                         f'({str(error).split()[0]}).',
                                             color=0xb2b2b2))
        print(f'[GOD SYSTEM] [COMMAND ERROR] {inter.author.id} пытается использовать команду, но получает ошибку '
              f'(пропущен обязательный аргумент)')
    elif isinstance(error, commands.MemberNotFound):
        await inter.send(embed=disnake.Embed(title='Ошибка', description='Пользователь не найден.',
                                             color=0xb2b2b2))
        print(f'[GOD SYSTEM] [COMMAND ERROR] {inter.author.id} пытается использовать команду, но получает ошибку '
              f'(пользователь не найден)')
    else:
        await inter.send(embed=disnake.Embed(title='Ошибка', description=f'Неизвестная ошибка.\n\n'
                                                                         f'Код ошибки:\n'
                                                                         f'{error}', color=0xb2b2b2))
        print(f'-----------------------------------------------------------------------------------------------------\n'
              f'[GOD SYSTEM] [COMMAND ERROR] {inter.author.id} пытается использовать команду, но получает ошибку '
              f'(неизвестная ошибка)\n'
              f'[DEBUG] {error}')


@bot.event
async def on_slash_command_error(inter, error):
    if isinstance(error, commands.CommandOnCooldown):
        await inter.send(embed=disnake.Embed(title='Ошибка', description=f'На эту команду наложен кулдаун.\n'
                                                                         f'Вы сможете использовать ее повторно через '
                                                                         f'{str(error).split()[-1]}',
                                             color=0xb2b2b2))
        print(f'[GOD SYSTEM] [SLASH COMMAND ERROR] {inter.author.id} пытается использовать команду, но получает ошибку '
              f'(кулдаун)')
    else:
        await inter.send(embed=disnake.Embed(title='Ошибка', description=f'Неизвестная ошибка.\n\n'
                                                                         f'Код ошибки:\n'
                                                                         f'{error}', color=0xb2b2b2))
        print(f'-----------------------------------------------------------------------------------------------------\n'
              f'[GOD SYSTEM] [SLASH COMMAND ERROR] {inter.author.id} пытается использовать команду, но получает ошибку '
              f'(неизвестная ошибка)\n'
              f'[DEBUG] {error}')


# ---------- [ECONOMY] ---------- #


@bot.slash_command(description='Регистрация в боте')
async def registration(inter):
    if economy_system.on_reg(user_id=inter.user.id):
        await inter.send(embed=disnake.Embed(title='Успешно', description='Вы успешно зарегистрировались в боте.\n'
                                                                          'Ваш стартовый баланс: 10.000',
                                             color=0xb2b2b2))
        print(f'[GOD SYSTEM] [ECONOMY] {inter.author.id} регистрируется в боте')
    else:
        await inter.send(embed=disnake.Embed(title='Ошибка', description=f'Вы уже зарегистрированы в боте.\n'
                                                                         f'Ваш баланс: '
                                                                         f'{economy_system.balance(inter.author.id)}',
                                             color=0xb2b2b2))
        print(f'[GOD SYSTEM] [ECONOMY] {inter.author.id} пытается зарегистрироваться, но получает ошибку '
              f'(уже есть в бд)')


@bot.slash_command(description='Проверка баланса')
async def balance(inter):
    if not economy_system.balance(user_id=inter.author.id):
        await inter.send(embed=disnake.Embed(title='Ошибка', description='Вы не найдены в базе данных бота.\n'
                                                                         'Возможно, вы еще не зарегистрированы '
                                                                         '(/registration).',
                                             color=0xb2b2b2))
        print(f'[GOD SYSTEM] [ECONOMY] {inter.author.id} пытается проверить баланс, но получает ошибку '
              f'(не найден в бд)')
    else:
        await inter.send(embed=disnake.Embed(title='Успешно',
                                             description=f'Ваш баланс: '
                                                         f'{economy_system.balance(user_id=inter.author.id)}',
                                             color=0xb2b2b2))
        print(f'[GOD SYSTEM] [ECONOMY] {inter.author.id} проверяет баланс')


@bot.slash_command(description='Перевод пользователю')
async def transfer(inter, amount: int = commands.Param(name='cумма'),
                   member: disnake.Member = commands.Param(name='получатель')):
    if not economy_system.balance(user_id=inter.author.id):
        await inter.send(embed=disnake.Embed(title='Ошибка', description='Вы не найдены в базе данных бота.\n'
                                                                         'Возможно, вы еще не зарегистрированы '
                                                                         '(/registration).',
                                             color=0xb2b2b2))
        print(f'[GOD SYSTEM] [ECONOMY] {inter.author.id} пытается перевести some money ({amount}) {member.id}, но '
              f'получает ошибку (не найден в бд)')
    elif amount >= economy_system.balance(inter.author.id, transfer_mode=True):
        await inter.send(embed=disnake.Embed(title='Ошибка', description=f'На вашем счету недостаточно средств.\n'
                                                                         f'Ваш баланс: '
                                                                         f'{economy_system.balance(inter.author.id)}',
                                             color=0xb2b2b2))
        print(f'[GOD SYSTEM] [ECONOMY] {inter.author.id} пытается перевести some money ({amount}) {member.id}, но '
              f'получает ошибку (недостаточно средств)')
    elif member.id == inter.author.id:
        await inter.send(embed=disnake.Embed(title='Ошибка', description='Невозможно совершить перевод самому себе.',
                                             color=0xb2b2b2))
        print(f'[GOD SYSTEM] [ECONOMY] {inter.author.id} пытается перевести some money ({amount}) {member.id}, но '
              f'получает ошибку (невозможно совершить перевод самому себе)')
    else:
        economy_system.add(user_id=member.id, amount=amount)
        economy_system.remove(user_id=inter.author.id, amount=amount)
        await inter.send(embed=disnake.Embed(title=f'Успешно', description=f'Сумма: {amount}\n'
                                                                           f'Получатель: <@{member.id}>\n\n'
                                                                           f'Ваш текущий баланс: '
                                                                           f'{economy_system.balance(inter.author.id)}',
                                             color=0xb2b2b2))
        print(f'[GOD SYSTEM] [ECONOMY] {inter.author.id} успешно переводит some money ({amount}) {member.id}')


@bot.slash_command(description='antibomj система которая подкинет тебе money')
@commands.cooldown(1, 86400, commands.BucketType.user)
async def antibomj(inter):
    if not economy_system.balance(user_id=inter.author.id):
        await inter.send(embed=disnake.Embed(title='Ошибка', description='Вы не найдены в базе данных бота.\n'
                                                                         'Возможно, вы еще не зарегистрированы '
                                                                         '(/registration).',
                                             color=0xb2b2b2))
        print(f'[GOD SYSTEM] [ECONOMY] {inter.author.id} пытается воспользоваться antibomj системой, но получает '
              f'ошибку (не найден в бд)')
    elif economy_system.balance(user_id=inter.author.id, transfer_mode=True) == 10000 or \
            economy_system.balance(user_id=inter.author.id, transfer_mode=True) >= 10000:
        await inter.send(embed=disnake.Embed(title=f'Ошибка', description='antibomj система не считает вас бомжом.',
                                             color=0xb2b2b2))
        print(f'[GOD SYSTEM] [ECONOMY] {inter.author.id} пытается воспользоваться antibomj системой, но получает '
              f'ошибку (не бомж)')
    else:
        amount = 10000 - economy_system.balance(user_id=inter.author.id, transfer_mode=True)
        economy_system.add(user_id=inter.author.id, amount=amount)
        await inter.send(
            embed=disnake.Embed(title=f'Успешно', description=f'antibomj система не дала вам стать бомжом.\n'
                                                              f'На ваш баланс переведено: '
                                                              f'{"{:,}".format(amount).replace(",", ".")}\n\n'
                                                              f'Ваш текущий баланс: '
                                                              f'{economy_system.balance(inter.author.id)}',
                                color=0xb2b2b2))
        print(f'[GOD SYSTEM] [ECONOMY] {inter.author.id} успешно получает ({amount}) от antibomj системы')


@bot.slash_command(description='Работа таксистом')
@commands.cooldown(1, 1800, commands.BucketType.user)
async def taxi(inter):
    if not economy_system.balance(user_id=inter.author.id):
        await inter.send(embed=disnake.Embed(title='Ошибка', description='Вы не найдены в базе данных бота.\n'
                                                                         'Возможно, вы еще не зарегистрированы '
                                                                         '(/registration).',
                                             color=0xb2b2b2))
        print(f'[GOD SYSTEM] [ECONOMY] {inter.author.id} пытается поработать таксистом, но получает '
              f'ошибку (не найден в бд)')
    else:
        economy_system.add(user_id=inter.author.id, amount=5000)
        await inter.send(embed=disnake.Embed(title='Успешно',
                                             description=f'Вы весь день прохуячили на таксе.\n\n'
                                                         f'Ваша заработная плата: 5.000\n'
                                                         f'Ваш текущий баланс: '
                                                         f'{economy_system.balance(user_id=inter.author.id)}.',
                                             color=0xb2b2b2))
        print(f'[GOD SYSTEM] [ECONOMY] {inter.author.id} успешно таксует, новый баланс: '
              f'{economy_system.balance(user_id=inter.author.id)}')


@bot.slash_command(description='Работа на заводе')
@commands.cooldown(1, 3600, commands.BucketType.user)
async def factory(inter):
    if not economy_system.balance(user_id=inter.author.id):
        await inter.send(embed=disnake.Embed(title='Ошибка', description='Вы не найдены в базе данных бота.\n'
                                                                         'Возможно, вы еще не зарегистрированы '
                                                                         '(/registration).',
                                             color=0xb2b2b2))
        print(f'[GOD SYSTEM] [ECONOMY] {inter.author.id} пытается поработать на заводе, но получает '
              f'ошибку (не найден в бд)')
    else:
        economy_system.add(user_id=inter.author.id, amount=10000)
        await inter.send(embed=disnake.Embed(title='Успешно',
                                             description=f'Вы весь день прохуячили на заводе.\n\n'
                                                         f'Ваша заработная плата: 10.000\n'
                                                         f'Ваш текущий баланс: '
                                                         f'{economy_system.balance(user_id=inter.author.id)}.',
                                             color=0xb2b2b2))
        print(f'[GOD SYSTEM] [ECONOMY] {inter.author.id} успешно отрабатывает на заводе, новый баланс: '
              f'{economy_system.balance(user_id=inter.author.id)}')


@bot.command()
@commands.has_permissions(administrator=True)
async def godgive(inter, amount: int, member: disnake.Member):
    economy_system.add(user_id=member.id, amount=amount)
    await inter.message.delete()
    await inter.send(
        embed=disnake.Embed(title=f'Успешно', description=f'<@{member.id}>, система бога поощрила ваше существование.\n'
                                                          f'На ваш счет переведено: '
                                                          f'{"{:,}".format(amount).replace(",", ".")}\n\n'
                                                          f'Ваш текущий баланс: '
                                                          f'{economy_system.balance(member.id)}',
                            color=0xb2b2b2))
    print(f'[GOD SYSTEM] [ECONOMY] система бога поощряет {member.id} ({amount})')


@bot.command()
@commands.has_permissions(administrator=True)
async def godtake(inter, amount: int, member: disnake.Member):
    economy_system.remove(user_id=member.id, amount=amount)
    await inter.message.delete()
    await inter.send(embed=disnake.Embed(title=f'Успешно', description=f'<@{member.id}>, система бога наказала вас.\n'
                                                                       f'С вашего счета исчезло: '
                                                                       f'{"{:,}".format(amount).replace(",", ".")}\n\n'
                                                                       f'Ваш текущий баланс: '
                                                                       f'{economy_system.balance(member.id)}',
                                         color=0xb2b2b2))
    print(f'[GOD SYSTEM] [ECONOMY] система бога наказывает {member.id} ({amount})')


# ---------- [ADM] ---------- #


@bot.command()
@commands.has_permissions(administrator=True)
async def mute(inter, member: disnake.Member, hours: int):
    await inter.message.delete()
    if hours >= 673 or hours <= 0:
        await inter.send(
            embed=disnake.Embed(title=f'Ошибка', description='Время мута должно быть не больше 672 и не меньше 1.',
                                color=0xb2b2b2))
        print(f'[GOD SYSTEM] [ADM] {inter.author.id} пытается замутить {member.id}, но получает ошибку '
              f'(некорректное время мута)')
    else:
        await member.timeout(duration=timedelta(hours=hours), reason=None)
        await inter.send(
            embed=disnake.Embed(title=f'Успешно', description=f'<@{inter.author.id}> выдает мут <@{member.id}>.\n\n'
                                                              f'({timedelta(hours=hours)})\n',
                                color=0xb2b2b2))
        print(f'[GOD SYSTEM] [ADM] {inter.author.id} выдает мут {member.id} ({timedelta(hours=hours)})')


@bot.command()
@commands.has_permissions(administrator=True)
async def unmute(inter, member: disnake.Member):
    await inter.message.delete()
    await member.timeout(duration=None, reason=None)
    await inter.send(
        embed=disnake.Embed(title=f'Успешно', description=f'<@{inter.author.id}> убирает мут с <@{member.id}>.',
                            color=0xb2b2b2))
    print(f'[GOD SYSTEM] [ADM] {inter.author.id} убирает мут с {member.id}')


@bot.command()
@commands.has_permissions(administrator=True)
async def kick(inter, member: disnake.Member):
    await inter.message.delete()
    await member.kick()
    await inter.send(embed=disnake.Embed(title=f'Успешно', description=f'<@{inter.author.id}> кикает <@{member.id}>.',
                                         color=0xb2b2b2))
    print(f'[GOD SYSTEM] [ADM] {inter.author.id} кикает {member.id}')


@bot.command()
@commands.has_permissions(administrator=True)
async def ban(inter, member: disnake.Member):
    await inter.message.delete()
    await member.ban()
    await inter.send(embed=disnake.Embed(title=f'Успешно', description=f'<@{inter.author.id}> банит <@{member.id}>.',
                                         color=0xb2b2b2))
    print(f'[GOD SYSTEM] [ADM] {inter.author.id} банит {member.id}')


@bot.command()
@commands.has_permissions(administrator=True)
async def clear(inter, amount: int):
    await inter.message.delete()
    if amount == 0 or amount <= -1:
        await inter.send(embed=disnake.Embed(title='Ошибка', description='Число сообщений должно быть больше 0.',
                                             color=0xb2b2b2))
        print(f'[GOD SYSTEM] [ADM] {inter.author.id} пытается удалить сообщения, но получает ошибку '
              f'(некорректное число сообщений)')
    else:
        await inter.channel.purge(limit=amount)
        await inter.send(embed=disnake.Embed(title='Успешно',
                                             description=f'Удалено сообщений: '
                                                         f'{"{:,}".format(amount).replace(",", ".")}.',
                                             color=0xb2b2b2))
        print(f'[GOD SYSTEM] [ADM] {inter.author.id} удаляет сообщения ({amount})')


# ---------- [EMBEDS] ---------- #


@bot.command()
@commands.has_permissions(administrator=True)
async def embed(inter, template: str):
    await inter.message.delete()
    pre_components = []
    if template not in json.load(open('embed_templates.json')):
        await inter.send(embed=disnake.Embed(title='Ошибка', description='Пресета с таким названием не найдено.',
                                             color=0xb2b2b2))
        print(f'[GOD SYSTEM] [EMBEDS] {inter.author.id} пытается использовать embed ({template}), но получает ошибку '
              f'(пресет не найден)')
    else:
        if json.load(open('embed_templates.json'))[template]['desc'] != 'none':
            pre_embed = disnake.Embed(title=json.load(open('embed_templates.json'))[template]['title'],
                                      description=json.load(open('embed_templates.json'))[template]['desc'],
                                      color=0xb2b2b2)
        else:
            pre_embed = disnake.Embed(title=json.load(open('embed_templates.json'))[template]['title'],
                                      color=0xb2b2b2)
        if json.load(open('embed_templates.json'))[template]['fields_number'] != 0:
            for c in range(json.load(open('embed_templates.json'))[template]['fields_number']):
                pre_embed.add_field(name=json.load(open('embed_templates.json'))[template][f'field_{c}']['name'],
                                    value=json.load(open('embed_templates.json'))[template][f'field_{c}']['value'],
                                    inline=False)
        if json.load(open('embed_templates.json'))[template]['image'] != 'none':
            pre_embed.set_image(file=disnake.File(json.load(open('embed_templates.json'))[template]['image']))
        if json.load(open('embed_templates.json'))[template]['footer'] == 'true':
            pre_embed.set_footer(text=json.load(open('embed_templates.json'))[template]['text'])
        if json.load(open('embed_templates.json'))[template]['buttons_number'] != 0:
            for c in range(json.load(open('embed_templates.json'))[template]['buttons_number']):
                pre_components.append(
                    disnake.ui.Button(label=json.load(open('embed_templates.json'))[template][f'button_{c}']['label'],
                                      style=disnake.ButtonStyle.link,
                                      url=json.load(open('embed_templates.json'))[template][f'button_{c}']['url']))
            await inter.send(embed=pre_embed, components=pre_components)
        else:
            await inter.send(embed=pre_embed)
        print(f'[GOD SYSTEM] [EMBEDS] {inter.author.id} использует embed ({template})')


@bot.command()
@commands.has_permissions(administrator=True)
async def embeds_view(inter):
    await inter.message.delete()
    pre_embed = disnake.Embed(title='Список доступных пресетов', color=0xb2b2b2)
    for c in range(len(json.load(open('embed_templates.json')))):
        value = json.load(open('embed_templates.json'))[list(json.load(open('embed_templates.json')))[c]]['desc']
        value2 = json.load(open('embed_templates.json'))[list(json.load(open('embed_templates.json')))[c]]['image']
        pre_embed.add_field(name=list(json.load(open('embed_templates.json')))[c],
                            value=f'{value}\n\n{value2}', inline=False)
    await inter.send(embed=pre_embed)
    print(f'[GOD SYSTEM] [EMBEDS] {inter.author.id} просматривает список доступных пресетов для embed')


@bot.slash_command(description='Информация о боте')
async def about(inter):
    pre_embed = disnake.Embed(title='GOD SYSTEM Bot', description='4friends only v1.0', color=0xb2b2b2)
    pre_embed.add_field(name='Developed by', value='<@399839515134525440>')
    pre_embed.add_field(name='Developed on', value=f'Python (disnake)')
    pre_embed.add_field(name='', value='', inline=False)
    pre_embed.add_field(name='VALORANT API by',
                        value='[Henrik Mertens](https://github.com/Henrik-3/unofficial-valorant-api)')
    pre_embed.add_field(name='Hosted on', value='[pylexnodes.net](https://client.pylexnodes.net/)')
    pre_embed.add_field(name='Source code', value='soon', inline=False)
    pre_embed.set_image(file=disnake.File('png/main.png'))
    pre_embed.set_footer(text='lgnlgnlgn')
    await inter.send(embed=pre_embed)

# ---------- [VALORANT] ---------- #


@bot.slash_command(description='Краткий обзор профиля Valorant')
async def valstats(inter, name: str = commands.Param(name='ник'), tag: str = commands.Param(name='тег'),
                   region: str = commands.Param(choices=['AP', 'BR', 'EU', 'KR', 'LATAM', 'NA'], name='регион')):
    stats = valorant_system.get_player_info(name=name, tag=tag, region=region)
    if stats:
        pre_embed = disnake.Embed(title=f'{name}#{tag} ({region})',
                                  description=f'{stats["level"]} уровень.',
                                  color=0xb2b2b2)
        pre_embed.add_field(name='Текущий ранг', value=f'{stats["current_rank"]} ({stats["current_elo"]}/100)')
        if stats['last_elo_change'] <= -1:
            pre_embed.add_field(name='Последняя игра', value=f'Поражение ({stats["last_elo_change"]})')
        else:
            pre_embed.add_field(name='Последняя игра', value=f'Победа ({stats["last_elo_change"]})')
        pre_embed.add_field(name='Наивысший ранг', value=f'{stats["highest_rank"]} ({stats["highest_rank_season"]})',
                            inline=False)
        pre_embed.set_thumbnail(url=stats['current_rank_icon'])
        pre_embed.set_image(url=stats['card'])
        pre_embed.set_footer(text='lgnlgnlgn')
        await inter.send(embed=pre_embed)
        print(f'[GOD SYSTEM] [VALORANT] {inter.author.id} просмотривет профиль игрока {name}#{tag} ({region})')
    else:
        await inter.send(embed=disnake.Embed(title=f'Ошибка', description='Игрока с таким сочетанием ника и тега не '
                                                                          'найдено.',
                                             color=0xb2b2b2))
        print(f'[GOD SYSTEM] [VALORANT] {inter.author.id} пытается просмотреть профиль валорант '
              f'({name}#{tag}, {region}), но получает ошибку (игрок не найден)')


@bot.slash_command(description='Отображает последний 5 рейтинговых игр')
async def valmatches(inter, name: str = commands.Param(name='ник'), tag: str = commands.Param(name='тег'),
                     region: str = commands.Param(choices=['AP', 'BR', 'EU', 'KR', 'LATAM', 'NA'], name='регион')):
    await inter.response.defer()
    matches = valorant_system.get_matches(name=name, tag=tag, region=region)
    if matches:
        pre_embed = disnake.Embed(title=f'{name}#{tag} ({region})',
                                  color=0xb2b2b2)
        pre_embed.add_field(name='Общая статистика', value=f'{matches["total_wins"]}+/{matches["total_lose"]}- '
                                                           f'(ничьи: {matches["total_ff"]})\n'
                                                           f'Эло: {matches["total_elo"]}')
        pre_embed.add_field(name='Общее К/Д', value=f'{matches["total_k/d"]}')
        pre_embed.add_field(name='', value='', inline=False)
        for c in range(5):
            pre_embed.add_field(name=f'{matches[f"game_{c}"]["map"]} ({matches[f"game_{c}"]["character"]})',
                                value=f'{matches[f"game_{c}"]["date"]}\n'
                                      f'({matches[f"game_{c}"]["team_a"]} - {matches[f"game_{c}"]["team_b"]}) '
                                      f'{matches[f"game_{c}"]["result"]} ')
            pre_embed.add_field(name='Индивидуальная статистика',
                                value=f'Счет: {matches[f"game_{c}"]["score"]}\n'
                                      f'(У/С/П) {matches[f"game_{c}"]["kills"]} - '
                                      f'{matches[f"game_{c}"]["deaths"]} - '
                                      f'{matches[f"game_{c}"]["assists"]}')
            pre_embed.add_field(name='', value='', inline=False)
        pre_embed.set_thumbnail(
            url=valorant_system.get_player_info(name=name, tag=tag, region=region)['current_rank_icon'])
        pre_embed.set_image(url=valorant_system.get_player_info(name=name, tag=tag, region=region)['card'])
        pre_embed.set_footer(text='lgnlgnlgn')
        await inter.send(embed=pre_embed)
        print(f'[GOD SYSTEM] [VALORANT] {inter.author.id} просматривает игры валорант ({name}#{tag}, {region})')
    else:
        await inter.send(embed=disnake.Embed(title=f'Ошибка', description='Игрока с таким сочетанием ника и '
                                                                          'тега не найдено.',
                                             color=0xb2b2b2))
        print(f'[GOD SYSTEM] [VALORANT] {inter.author.id} пытается просмотреть игры валорант '
              f'({name}#{tag}, {region}), но получает ошибку (игрок не найден)')


bot.run(secrets['beta'])
