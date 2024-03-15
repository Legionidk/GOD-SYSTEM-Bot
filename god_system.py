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
                   status=disnake.Status.do_not_disturb,
                   activity=disnake.Activity(
                       name=f'{json.load(open("embed_templates.json"))["О боте"]["desc"]}',
                       type=disnake.ActivityType.watching))


class About(disnake.ui.StringSelect):
    def __init__(self):
        options = [
            disnake.SelectOption(
                label='О боте', description='Информация о боте'
            ),
            disnake.SelectOption(
                label='Команды экономики', description='Доступные команды из экономики'
            ),
            disnake.SelectOption(
                label='Команды VALORANT', description='Доступные команды из VALORANT'
            ),
            disnake.SelectOption(
                label='Админские команды', description='Команды доступные только администраторам'
            ),
            disnake.SelectOption(
                label='Список изменений', description='Список изменение последнего обновления'
            ),
        ]

        super().__init__(
            placeholder='Выберите вкладку...',
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, inter: disnake.MessageInteraction):
        pre_embed = disnake.Embed(title=f'{json.load(open("embed_templates.json"))[self.values[0]]["title"]}',
                                  description=f'{json.load(open("embed_templates.json"))[self.values[0]]["desc"]}',
                                  color=0xb2b2b2)
        for c in range(json.load(open('embed_templates.json'))[self.values[0]]['fields_number']):
            if json.load((open('embed_templates.json')))[self.values[0]][f'field_{c}']['inline'] == \
                    'True':
                inline = True
            else:
                inline = False
            pre_embed.add_field(
                name=json.load((open('embed_templates.json')))[f'{self.values[0]}'][f'field_{c}']['name'],
                value=json.load((
                    open('embed_templates.json')))[f'{self.values[0]}'][f'field_{c}']['value'],
                inline=inline)
        pre_embed.set_image(file=disnake.File('png/main.png'))
        pre_embed.set_footer(text='lgnlgnlgn')
        await inter.response.edit_message(embed=pre_embed)
        print(f'[GOD SYSTEM] [EMBEDS] {inter.author.id} просматривает информацию о боте (вкладка {self.values[0]})')


class AboutView(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(About())


@bot.event
async def on_ready():
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


@bot.slash_command(description='[ECONOMY] Регистрация в боте')
async def registration(inter):
    if economy_system.on_reg(user_id=inter.author.id):
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


@bot.slash_command(description='[ECONOMY] Проверка баланса')
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


@bot.slash_command(description='[ECONOMY] Перевод пользователю')
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


@bot.slash_command(description='[ECONOMY] antibomj система которая подкинет тебе money')
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


@bot.slash_command(description='[ECONOMY] Работа таксистом')
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


@bot.slash_command(description='[ECONOMY] Работа на заводе')
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
    await inter.message.delete()
    if economy_system.remove(user_id=member.id, amount=amount):
        await inter.send(embed=disnake.Embed(title=f'Успешно',
                                             description=f'<@{member.id}>, система бога наказала вас.\n'
                                                         f'С вашего счета исчезло: '
                                                         f'{"{:,}".format(amount).replace(",", ".")}\n\n'
                                                         f'Ваш текущий баланс: '
                                                         f'{economy_system.balance(member.id)}', color=0xb2b2b2))
        print(f'[GOD SYSTEM] [ECONOMY] система бога наказывает {member.id} ({amount})')
    else:
        await inter.send(embed=disnake.Embed(title=f'Ошибка', description=f'Пользователь не найден в базе данных.',
                                             color=0xb2b2b2))
        print(f'[GOD SYSTEM] [ECONOMY] система бога пытается наказать {member.id} ({amount}), но не находит его в базе'
              f'данных')


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
    if inter.author.id != 000:
        await inter.send(embed=disnake.Embed(title='Ошибка', description='Я вас не узнаю! Вам запрещено использование '
                                                                         'данной команды', color=0xb2b2b2))
        print(f'[GOD SYSTEM] [EMBEDS] {inter.author.id} пытается использовать embed ({template}), '
              f'но получает ошибку (незнакомец)')
    else:
        if json.load(open("embed_templates.json"))[template]['pass'] == 'true':
            await inter.send(
                embed=disnake.Embed(title='Ошибка', description='Этот пресет недоступен для использования в .embed.',
                                    color=0xb2b2b2))
            print(f'[GOD SYSTEM] [EMBEDS] {inter.author.id} пытается использовать embed ({template}), '
                  f'но получает ошибку (пресет недоступен)')
        else:
            pre_components = []
            if template not in json.load(open('embed_templates.json')):
                await inter.send(embed=disnake.Embed(title='Ошибка',
                                                     description='Пресета с таким названием не найдено.',
                                                     color=0xb2b2b2))
                print(f'[GOD SYSTEM] [EMBEDS] {inter.author.id} пытается использовать embed ({template}), '
                      f'но получает ошибку (пресет не найден)')
            else:
                pre_embed = disnake.Embed(title=json.load(open('embed_templates.json'))[template]['title'],
                                          description=json.load(open('embed_templates.json'))[template]['desc'],
                                          color=0xb2b2b2)
                if json.load(open('embed_templates.json'))[template]['fields_number'] != 0:
                    for c in range(json.load(open('embed_templates.json'))[template]['fields_number']):
                        pre_embed.add_field(name=json.load(open
                                                           ('embed_templates.json'))[template][f'field_{c}']['name'],
                                            value=json.load(open
                                                            ('embed_templates.json'))[template][f'field_{c}']['value'],
                                            inline=False)
                if json.load(open('embed_templates.json'))[template]['image'] != 'none':
                    pre_embed.set_image(file=disnake.File(json.load(open('embed_templates.json'))[template]['image']))
                if json.load(open('embed_templates.json'))[template]['footer'] == 'true':
                    pre_embed.set_footer(text=json.load(open('embed_templates.json'))[template]['text'])
                if json.load(open('embed_templates.json'))[template]['buttons_number'] != 0:
                    for c in range(json.load(open('embed_templates.json'))[template]['buttons_number']):
                        pre_components.append(disnake.ui.Button(
                            label=json.load(open('embed_templates.json'))[template][f'button_{c}']['label'],
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
    if inter.author.id != 000:
        await inter.send(embed=disnake.Embed(title='Ошибка', description='Я вас не узнаю! Вам запрещено использование '
                                                                         'данной команды', color=0xb2b2b2))
        print(f'[GOD SYSTEM] [EMBEDS] {inter.author.id} пытается просмотреть список доступных пресетов для embed, '
              f'но получает ошибку (незнакомец)')
    else:
        pre_embed = disnake.Embed(title='Список доступных пресетов', color=0xb2b2b2)
        for c in range(len(json.load(open('embed_templates.json')))):
            if json.load(open('embed_templates.json'))[list(json.load(open('embed_templates.json')))[c]]['pass'] == \
                    'true':
                pass
            else:
                value = \
                    json.load(open('embed_templates.json'))[list(json.load(open('embed_templates.json')))[c]]['desc']
                value2 = \
                    json.load(open('embed_templates.json'))[list(json.load(open('embed_templates.json')))[c]]['image']
                pre_embed.add_field(name=list(json.load(open('embed_templates.json')))[c],
                                    value=f'{value}\n\n{value2}', inline=False)
        await inter.send(embed=pre_embed)
        print(f'[GOD SYSTEM] [EMBEDS] {inter.author.id} просматривает список доступных пресетов для embed')


@bot.slash_command(description='[EMBEDS] Информация о боте и его командах')
async def about(inter):
    pre_embed = disnake.Embed(title=f'{json.load(open("embed_templates.json"))["О боте"]["title"]}',
                              description=f'{json.load(open("embed_templates.json"))["О боте"]["desc"]}',
                              color=0xb2b2b2)
    for c in range(json.load(open('embed_templates.json'))['О боте']['fields_number']):
        if json.load((open('embed_templates.json')))['О боте'][f'field_{c}']['inline'] == 'True':
            inline = True
        else:
            inline = False
        pre_embed.add_field(name=json.load((open('embed_templates.json')))['О боте'][f'field_{c}']['name'],
                            value=json.load((open('embed_templates.json')))['О боте'][f'field_{c}']['value'],
                            inline=inline)
    pre_embed.set_image(file=disnake.File('png/main.png'))
    pre_embed.set_footer(text='lgnlgnlgn')
    await inter.send(embed=pre_embed, view=AboutView())
    print(f'[GOD SYSTEM] [EMBEDS] {inter.author.id} просматривает информацию о боте (первое использование)')


# ---------- [VALORANT] ---------- #


@bot.slash_command(description='[VALORANT] Краткий обзор профиля VALORANT')
async def valstats(inter, name: str = commands.Param(name='ник'), tag: str = commands.Param(name='тег'),
                   region: str = commands.Param(choices=['AP', 'BR', 'EU', 'KR', 'LATAM', 'NA'], name='регион')):
    await inter.response.defer()
    stats = valorant_system.get_player_info(name=name, tag=tag, region=region)
    if stats:
        last_match = valorant_system.get_matches(name=name, tag=tag, region=region)
        current_rank_icon = disnake.utils.get(bot.emojis, name=f'{stats["current_rank"].split()[0]}_'
                                                               f'{stats["current_rank"].split()[1]}')
        pick_rank_icon = disnake.utils.get(bot.emojis, name=f'{stats["highest_rank"].split()[0]}_'
                                                            f'{stats["highest_rank"].split()[1]}')
        if last_match[f'game_0']['character'] == 'KAY/O':
            character_icon = disnake.utils.get(bot.emojis,
                                               name=f'{last_match[f"game_0"]["character"].split("/")[0]}'
                                                    f'{last_match[f"game_0"]["character"].split("/")[1]}')
        else:
            character_icon = disnake.utils.get(bot.emojis, name=f'{last_match[f"game_0"]["character"]}')
        if stats['last_elo_change'] <= -1:
            result_emoji = '<:L_:1217964189268705342>'
        else:
            result_emoji = '<:W_:1217964192288604212>'
        pre_embed = disnake.Embed(title=f'{name}#{tag} ({region})',
                                  description=f'{stats["level"]} уровень.',
                                  color=0xb2b2b2)
        pre_embed.add_field(name='Текущий ранг', value=f'{current_rank_icon} ({stats["current_elo"]}/100)')
        pre_embed.add_field(name='Наивысший ранг', value=f'{pick_rank_icon} ({stats["highest_rank_season"]})')
        pre_embed.add_field(name='', value='Последняя игра', inline=False)
        pre_embed.add_field(name=f'{last_match["game_0"]["date"]}', value=f'{last_match["game_0"]["map"]}\n'
                                                                          f'{result_emoji} '
                                                                          f'{last_match["game_0"]["team_a"]} - '
                                                                          f'{last_match["game_0"]["team_b"]}\n'
                                                                          f'Эло: {stats["last_elo_change"]}')
        pre_embed.add_field(name='Личный счет', value=f'{last_match[f"game_0"]["score"]}\n'
                                                      f'Агент: {character_icon}\n'
                                                      f'(У/С/П) {last_match[f"game_0"]["kills"]} - '
                                                      f'{last_match[f"game_0"]["deaths"]} - '
                                                      f'{last_match[f"game_0"]["assists"]}\n')
        pre_embed.set_image(url=stats['card']['wide'])
        pre_embed.set_thumbnail(url=stats['card']['small'])
        pre_embed.set_footer(text='lgnlgnlgn')
        await inter.send(embed=pre_embed)
        print(f'[GOD SYSTEM] [VALORANT] {inter.author.id} просмотривет профиль игрока {name}#{tag} ({region})')
    else:
        await inter.send(embed=disnake.Embed(title=f'Ошибка', description='Игрока с таким сочетанием ника и тега не '
                                                                          'найдено.',
                                             color=0xb2b2b2))
        print(f'[GOD SYSTEM] [VALORANT] {inter.author.id} пытается просмотреть профиль валорант '
              f'({name}#{tag}, {region}), но получает ошибку (игрок не найден)')


@bot.slash_command(description='[VALORANT] Отображает последний 5 рейтинговых игр')
async def valmatches(inter, name: str = commands.Param(name='ник'), tag: str = commands.Param(name='тег'),
                     region: str = commands.Param(choices=['AP', 'BR', 'EU', 'KR', 'LATAM', 'NA'], name='регион')):
    await inter.response.defer()
    matches = valorant_system.get_matches(name=name, tag=tag, region=region)
    if matches:
        lose_and_wins = []
        for c in range(5):
            if matches[f'game_{c}']['result'] == 'Победа' or matches[f'game_{c}']['result'] == 'Ничья':
                lose_and_wins.append('<:W_:1217964192288604212>')
            else:
                lose_and_wins.append('<:L_:1217964189268705342>')
        list_of_results = f'{lose_and_wins[0]}{lose_and_wins[1]}{lose_and_wins[2]}{lose_and_wins[3]}{lose_and_wins[4]}'
        pre_embed = disnake.Embed(title=f'{name}#{tag} ({region})',
                                  color=0xb2b2b2)
        pre_embed.add_field(name='Общая статистика', value=f'{list_of_results}\n'
                                                           f'Эло: {matches["total_elo"]}')
        pre_embed.add_field(name='Общее К/Д', value=f'{matches["total_k/d"]}')
        pre_embed.add_field(name='', value='Последние 5 игр', inline=False)
        for c in range(5):
            if matches[f'game_{c}']['elo'] <= -1:
                result_emoji = '<:L_:1217964189268705342>'
            else:
                result_emoji = '<:W_:1217964192288604212>'
            if matches[f'game_{c}']['character'] == 'KAY/O':
                character_icon = disnake.utils.get(bot.emojis,
                                                   name=f'{matches[f"game_{c}"]["character"].split("/")[0]}'
                                                        f'{matches[f"game_{c}"]["character"].split("/")[1]}')
            else:
                character_icon = disnake.utils.get(bot.emojis, name=f'{matches[f"game_{c}"]["character"]}')
            rank_icon = disnake.utils.get(bot.emojis, name=f'{matches[f"game_{c}"]["rank"][0]}_'
                                                           f'{matches[f"game_{c}"]["rank"][1]}')
            pre_embed.add_field(name=f'{matches[f"game_{c}"]["date"]}',
                                value=f'{matches[f"game_{c}"]["map"]}\n'
                                      f'{result_emoji} '
                                      f'{matches[f"game_{c}"]["team_a"]} - {matches[f"game_{c}"]["team_b"]}\n'
                                      f'{rank_icon} Эло: {matches[f"game_{c}"]["elo"]}')
            pre_embed.add_field(name='Личный счет',
                                value=f'{matches[f"game_{c}"]["score"]}\n'
                                      f'Агент: {character_icon}\n'
                                      f'(У/С/П) {matches[f"game_{c}"]["kills"]} - '
                                      f'{matches[f"game_{c}"]["deaths"]} - '
                                      f'{matches[f"game_{c}"]["assists"]}\n')
            pre_embed.add_field(name='', value='', inline=False)
        pre_embed.set_thumbnail(url=valorant_system.get_player_info(name=name, tag=tag, region=region)['card']['small'])
        pre_embed.set_image(url=valorant_system.get_player_info(name=name, tag=tag, region=region)['card']['wide'])
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
