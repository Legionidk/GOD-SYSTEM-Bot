import disnake
from disnake.ext import commands
from datetime import timedelta


class Adm(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mute(self, inter, member: disnake.Member, hours: int):
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

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unmute(self, inter, member: disnake.Member):
        await inter.message.delete()
        await member.timeout(duration=None, reason=None)
        await inter.send(
            embed=disnake.Embed(title=f'Успешно', description=f'<@{inter.author.id}> убирает мут с <@{member.id}>.',
                                color=0xb2b2b2))
        print(f'[GOD SYSTEM] [ADM] {inter.author.id} убирает мут с {member.id}')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kick(self, inter, member: disnake.Member):
        await inter.message.delete()
        await member.kick()
        await inter.send(
            embed=disnake.Embed(title=f'Успешно', description=f'<@{inter.author.id}> кикает <@{member.id}>.',
                                color=0xb2b2b2))
        print(f'[GOD SYSTEM] [ADM] {inter.author.id} кикает {member.id}')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban(self, inter, member: disnake.Member):
        await inter.message.delete()
        await member.ban()
        await inter.send(
            embed=disnake.Embed(title=f'Успешно', description=f'<@{inter.author.id}> банит <@{member.id}>.',
                                color=0xb2b2b2))
        print(f'[GOD SYSTEM] [ADM] {inter.author.id} банит {member.id}')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear(self, inter, amount: int):
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


def setup(bot: commands.Bot):
    bot.add_cog(Adm(bot))
