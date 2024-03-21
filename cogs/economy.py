import disnake
from disnake.ext import commands
import economy_system


class Economy(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(description='[ECONOMY] Регистрация в боте')
    async def registration(self, inter):
        if economy_system.on_reg(user_id=inter.author.id):
            await inter.send(embed=disnake.Embed(title='Успешно', description='Вы успешно зарегистрировались в боте.\n'
                                                                              'Ваш стартовый баланс: 10.000',
                                                 color=0xb2b2b2))
            print(f'[GOD SYSTEM] [ECONOMY] {inter.author.id} регистрируется в боте')
        else:
            await inter.send(embed=disnake.Embed(title='Ошибка',
                                                 description=f'Вы уже зарегистрированы в боте.\n'
                                                             f'Ваш баланс: '
                                                             f'{economy_system.balance(inter.author.id)}',
                                                 color=0xb2b2b2))
            print(f'[GOD SYSTEM] [ECONOMY] {inter.author.id} пытается зарегистрироваться, но получает ошибку '
                  f'(уже есть в бд)')

    @commands.slash_command(description='[ECONOMY] Проверка баланса')
    async def balance(self, inter):
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

    @commands.slash_command(description='[ECONOMY] Перевод пользователю')
    async def transfer(self, inter, amount: int = commands.Param(name='cумма'),
                       member: disnake.Member = commands.Param(name='получатель')):
        if not economy_system.balance(user_id=inter.author.id):
            await inter.send(embed=disnake.Embed(title='Ошибка', description='Вы не найдены в базе данных бота.\n'
                                                                             'Возможно, вы еще не зарегистрированы '
                                                                             '(/registration).',
                                                 color=0xb2b2b2))
            print(f'[GOD SYSTEM] [ECONOMY] {inter.author.id} пытается перевести some money ({amount}) {member.id}, но '
                  f'получает ошибку (не найден в бд)')
        elif amount >= economy_system.balance(inter.author.id, transfer_mode=True):
            await inter.send(embed=disnake.Embed(title='Ошибка',
                                                 description=f'На вашем счету недостаточно средств.\n'
                                                             f'Ваш баланс: '
                                                             f'{economy_system.balance(inter.author.id)}',
                                                 color=0xb2b2b2))
            print(f'[GOD SYSTEM] [ECONOMY] {inter.author.id} пытается перевести some money ({amount}) {member.id}, но '
                  f'получает ошибку (недостаточно средств)')
        elif member.id == inter.author.id:
            await inter.send(
                embed=disnake.Embed(title='Ошибка', description='Невозможно совершить перевод самому себе.',
                                    color=0xb2b2b2))
            print(f'[GOD SYSTEM] [ECONOMY] {inter.author.id} пытается перевести some money ({amount}) {member.id}, но '
                  f'получает ошибку (невозможно совершить перевод самому себе)')
        else:
            economy_system.add(user_id=member.id, amount=amount)
            economy_system.remove(user_id=inter.author.id, amount=amount)
            await inter.send(embed=disnake.Embed(title=f'Успешно',
                                                 description=f'Сумма: {amount}\n'
                                                             f'Получатель: <@{member.id}>\n\n'
                                                             f'Ваш текущий баланс: '
                                                             f'{economy_system.balance(inter.author.id)}',
                                                 color=0xb2b2b2))
            print(f'[GOD SYSTEM] [ECONOMY] {inter.author.id} успешно переводит some money ({amount}) {member.id}')

    @commands.slash_command(description='[ECONOMY] antibomj система которая подкинет тебе money')
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def antibomj(self, inter):
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

    @commands.slash_command(description='[ECONOMY] Работа таксистом')
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def taxi(self, inter):
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

    @commands.slash_command(description='[ECONOMY] Работа на заводе')
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def factory(self, inter):
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

    @commands.command()
    async def godgive(self, inter, amount: int, member: disnake.Member):
        economy_system.add(user_id=member.id, amount=amount)
        await inter.message.delete()
        await inter.send(
            embed=disnake.Embed(title=f'Успешно',
                                description=f'<@{member.id}>, система бога поощрила ваше существование.\n'
                                            f'На ваш счет переведено: '
                                            f'{"{:,}".format(amount).replace(",", ".")}\n\n'
                                            f'Ваш текущий баланс: '
                                            f'{economy_system.balance(member.id)}',
                                color=0xb2b2b2))
        print(f'[GOD SYSTEM] [ECONOMY] система бога поощряет {member.id} ({amount})')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def godtake(self, inter, amount: int, member: disnake.Member):
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
            print(f'[GOD SYSTEM] [ECONOMY] система бога пытается наказать {member.id} ({amount}), '
                  f'но не находит его в базе данных')


def setup(bot: commands.Bot):
    bot.add_cog(Economy(bot))
