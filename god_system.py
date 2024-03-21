import disnake
from disnake.ext import commands
import json

secrets = {
    'stable': 'stable_token',
    'beta': 'beta_token'
}
bot = commands.Bot(command_prefix='.', help_command=None, intents=disnake.Intents.all(),
                   status=disnake.Status.do_not_disturb,
                   activity=disnake.Activity(
                       name=f'{json.load(open("db/embed_templates.json"))["О боте"]["desc"]}',
                       type=disnake.ActivityType.watching))

# ---------- [EVENTS] ---------- #


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
        await inter.send(embed=disnake.Embed(title='Ошибка',
                                             description=f'На эту команду наложен кулдаун.\n'
                                                         f'Вы сможете использовать ее повторно '
                                                         f'через'
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
        print(
            f'-----------------------------------------------------------------------------------------------------'
            f'\n'
            f'[GOD SYSTEM] [COMMAND ERROR] {inter.author.id} пытается использовать команду, но получает ошибку '
            f'(неизвестная ошибка)\n'
            f'[DEBUG] {error}')


@bot.event
async def on_slash_command_error(inter, error):
    if isinstance(error, commands.CommandOnCooldown):
        await inter.send(embed=disnake.Embed(title='Ошибка',
                                             description=f'На эту команду наложен кулдаун.\n'
                                                         f'Вы сможете использовать ее повторно через '
                                                         f'{str(error).split()[-1]}',
                                             color=0xb2b2b2))
        print(
            f'[GOD SYSTEM] [SLASH COMMAND ERROR] {inter.author.id} пытается использовать команду, '
            f'но получает ошибку (кулдаун)')
    else:
        await inter.send(embed=disnake.Embed(title='Ошибка', description=f'Неизвестная ошибка.\n\n'
                                                                         f'Код ошибки:\n'
                                                                         f'{error}', color=0xb2b2b2))
        print(
            f'-----------------------------------------------------------------------------------------------------'
            f'\n'
            f'[GOD SYSTEM] [SLASH COMMAND ERROR] {inter.author.id} пытается использовать команду, '
            f'но получает ошибку (неизвестная ошибка)\n'
            f'[DEBUG] {error}')

# ---------- [ECONOMY] ---------- #

bot.load_extension("cogs.economy")

# ---------- [ADM] ---------- #

bot.load_extension("cogs.adm")

# ---------- [EMBEDS] ---------- #

bot.load_extension("cogs.embeds")

# ---------- [VALORANT] ---------- #

bot.load_extension("cogs.valorant")

bot.run(secrets['beta'])
