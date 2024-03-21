import disnake
from disnake.ext import commands
import json


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
        pre_embed = disnake.Embed(title=f'{json.load(open("bd/embed_templates.json"))[self.values[0]]["title"]}',
                                  description=f'{json.load(open("bd/embed_templates.json"))[self.values[0]]["desc"]}',
                                  color=0xb2b2b2)
        for c in range(json.load(open('bd/embed_templates.json'))[self.values[0]]['fields_number']):
            if json.load((open('bd/embed_templates.json')))[self.values[0]][f'field_{c}']['inline'] == \
                    'True':
                inline = True
            else:
                inline = False
            pre_embed.add_field(
                name=json.load((open('bd/embed_templates.json')))[f'{self.values[0]}'][f'field_{c}']['name'],
                value=json.load((
                    open('bd/embed_templates.json')))[f'{self.values[0]}'][f'field_{c}']['value'],
                inline=inline)
        pre_embed.set_image(file=disnake.File('png/main.gif'))
        pre_embed.set_footer(text='lgnlgnlgn')
        await inter.response.edit_message(embed=pre_embed)
        print(f'[GOD SYSTEM] [EMBEDS] {inter.author.id} просматривает информацию о боте (вкладка {self.values[0]})')


class AboutView(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(About())


class Embeds(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def embed(self, inter, template: str):
        await inter.message.delete()
        if inter.author.id != 399839515134525440:
            await inter.send(
                embed=disnake.Embed(title='Ошибка', description='Я вас не узнаю! Вам запрещено использование '
                                                                'данной команды', color=0xb2b2b2))
            print(f'[GOD SYSTEM] [EMBEDS] {inter.author.id} пытается использовать embed ({template}), '
                  f'но получает ошибку (незнакомец)')
        else:
            if json.load(open("bd/embed_templates.json"))[template]['pass'] == 'true':
                await inter.send(
                    embed=disnake.Embed(title='Ошибка',
                                        description='Этот пресет недоступен для использования в .embed.',
                                        color=0xb2b2b2))
                print(f'[GOD SYSTEM] [EMBEDS] {inter.author.id} пытается использовать embed ({template}), '
                      f'но получает ошибку (пресет недоступен)')
            else:
                pre_components = []
                if template not in json.load(open('bd/embed_templates.json')):
                    await inter.send(embed=disnake.Embed(title='Ошибка',
                                                         description='Пресета с таким названием не найдено.',
                                                         color=0xb2b2b2))
                    print(f'[GOD SYSTEM] [EMBEDS] {inter.author.id} пытается использовать embed ({template}), '
                          f'но получает ошибку (пресет не найден)')
                else:
                    pre_embed = disnake.Embed(title=json.load(open('bd/embed_templates.json'))[template]['title'],
                                              description=json.load(open('bd/embed_templates.json'))[template]['desc'],
                                              color=0xb2b2b2)
                    if json.load(open('bd/embed_templates.json'))[template]['fields_number'] != 0:
                        for c in range(json.load(open('bd/embed_templates.json'))[template]['fields_number']):
                            pre_embed.add_field(name=json.load(open
                                                               ('bd/embed_templates.json'))[template][f'field_{c}'][
                                'name'],
                                                value=json.load(open
                                                                ('bd/embed_templates.json'))[template][f'field_{c}'][
                                                    'value'],
                                                inline=False)
                    if json.load(open('bd/embed_templates.json'))[template]['image'] != 'none':
                        pre_embed.set_image(
                            file=disnake.File(json.load(open('bd/embed_templates.json'))[template]['image']))
                    if json.load(open('bd/embed_templates.json'))[template]['footer'] == 'true':
                        pre_embed.set_footer(text=json.load(open('bd/embed_templates.json'))[template]['text'])
                    if json.load(open('bd/embed_templates.json'))[template]['buttons_number'] != 0:
                        for c in range(json.load(open('bd/embed_templates.json'))[template]['buttons_number']):
                            pre_components.append(disnake.ui.Button(
                                label=json.load(open('bd/embed_templates.json'))[template][f'button_{c}']['label'],
                                style=disnake.ButtonStyle.link,
                                url=json.load(open('bd/embed_templates.json'))[template][f'button_{c}']['url']))
                        await inter.send(embed=pre_embed, components=pre_components)
                    else:
                        await inter.send(embed=pre_embed)
                    print(f'[GOD SYSTEM] [EMBEDS] {inter.author.id} использует embed ({template})')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def embeds_view(self, inter):
        await inter.message.delete()
        if inter.author.id != 399839515134525440:
            await inter.send(
                embed=disnake.Embed(title='Ошибка', description='Я вас не узнаю! Вам запрещено использование '
                                                                'данной команды', color=0xb2b2b2))
            print(f'[GOD SYSTEM] [EMBEDS] {inter.author.id} пытается просмотреть список доступных пресетов для embed, '
                  f'но получает ошибку (незнакомец)')
        else:
            pre_embed = disnake.Embed(title='Список доступных пресетов', color=0xb2b2b2)
            for c in range(len(json.load(open('bd/embed_templates.json')))):
                if json.load(open('bd/embed_templates.json'))[list(json.load(open('bd/embed_templates.json')))[c]]['pass'] \
                        == 'true':
                    pass
                else:
                    value = \
                        json.load(open('bd/embed_templates.json'))[list(json.load(open('bd/embed_templates.json')))[c]][
                            'desc']
                    value2 = \
                        json.load(open('bd/embed_templates.json'))[list(json.load(open('bd/embed_templates.json')))[c]][
                            'image']
                    pre_embed.add_field(name=list(json.load(open('bd/embed_templates.json')))[c],
                                        value=f'{value}\n\n{value2}', inline=False)
            await inter.send(embed=pre_embed)
            print(f'[GOD SYSTEM] [EMBEDS] {inter.author.id} просматривает список доступных пресетов для embed')

    @commands.slash_command(description='[EMBEDS] Информация о боте и его командах')
    async def about(self, inter):
        await inter.response.defer()
        pre_embed = disnake.Embed(title=f'{json.load(open("bd/embed_templates.json"))["О боте"]["title"]}',
                                  description=f'{json.load(open("bd/embed_templates.json"))["О боте"]["desc"]}',
                                  color=0xb2b2b2)
        for c in range(json.load(open('bd/embed_templates.json'))['О боте']['fields_number']):
            if json.load((open('bd/embed_templates.json')))['О боте'][f'field_{c}']['inline'] == 'True':
                inline = True
            else:
                inline = False
            pre_embed.add_field(name=json.load((open('bd/embed_templates.json')))['О боте'][f'field_{c}']['name'],
                                value=json.load((open('bd/embed_templates.json')))['О боте'][f'field_{c}']['value'],
                                inline=inline)
        pre_embed.set_image(file=disnake.File('png/main.gif'))
        pre_embed.set_footer(text='lgnlgnlgn')
        await inter.send(embed=pre_embed, view=AboutView())
        print(f'[GOD SYSTEM] [EMBEDS] {inter.author.id} просматривает информацию о боте (первое использование)')


def setup(bot: commands.Bot):
    bot.add_cog(Embeds(bot))
