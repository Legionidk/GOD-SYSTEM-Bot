import disnake
from disnake.ext import commands
import valorant_system
from god_system import bot as main_bot


class Valorant(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(description='[VALORANT] Краткий обзор профиля VALORANT')
    async def valstats(self, inter: disnake.ApplicationCommandInteraction, name: str = commands.Param(name='ник'),
                       tag: str = commands.Param(name='тег'),
                       region: str = commands.Param(choices=['AP', 'BR', 'EU', 'KR', 'LATAM', 'NA'], name='регион')):
        await inter.response.defer()

        stats = valorant_system.get_player_info(name=name, tag=tag, region=region)
        if stats:
            last_match = valorant_system.get_matches(name=name, tag=tag, region=region)
            current_rank_icon = disnake.utils.get(main_bot.emojis, name=f'{stats["current_rank"].split()[0]}_'
                                                                        f'{stats["current_rank"].split()[1]}')
            pick_rank_icon = disnake.utils.get(main_bot.emojis, name=f'{stats["highest_rank"].split()[0]}_'
                                                                     f'{stats["highest_rank"].split()[1]}')
            if last_match[f'game_0']['character'] == 'KAY/O':
                character_icon = disnake.utils.get(main_bot.emojis,
                                                   name=f'{last_match[f"game_0"]["character"].split("/")[0]}'
                                                        f'{last_match[f"game_0"]["character"].split("/")[1]}')
            else:
                character_icon = disnake.utils.get(main_bot.emojis, name=f'{last_match[f"game_0"]["character"]}')
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
                                                          f'у{last_match[f"game_0"]["kills"]}/'
                                                          f'с{last_match[f"game_0"]["deaths"]}/'
                                                          f'п{last_match[f"game_0"]["assists"]}\n'
                                                          f'Агент: {character_icon}\n')
            pre_embed.set_image(url=stats['card']['wide'])
            pre_embed.set_thumbnail(url=stats['card']['small'])
            pre_embed.set_footer(text='lgnlgnlgn')
            await inter.send(embed=pre_embed)
            print(f'[GOD SYSTEM] [VALORANT] {inter.author.id} просмотривет профиль игрока {name}#{tag} ({region})')
        else:
            await inter.send(
                embed=disnake.Embed(title=f'Ошибка', description='Игрока с таким сочетанием ника и тега не '
                                                                 'найдено.',
                                    color=0xb2b2b2))
            print(f'[GOD SYSTEM] [VALORANT] {inter.author.id} пытается просмотреть профиль валорант '
                  f'({name}#{tag}, {region}), но получает ошибку (игрок не найден)')

    @commands.slash_command(description='[VALORANT] Отображает последний 5 рейтинговых игр')
    async def valmatches(self, inter: disnake.ApplicationCommandInteraction, name: str = commands.Param(name='ник'),
                         tag: str = commands.Param(name='тег'),
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
            list_of_results = f'{lose_and_wins[0]}{lose_and_wins[1]}' \
                              f'{lose_and_wins[2]}{lose_and_wins[3]}{lose_and_wins[4]}'
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
                    character_icon = disnake.utils.get(main_bot.emojis,
                                                       name=f'{matches[f"game_{c}"]["character"].split("/")[0]}'
                                                            f'{matches[f"game_{c}"]["character"].split("/")[1]}')
                else:
                    character_icon = disnake.utils.get(main_bot.emojis, name=f'{matches[f"game_{c}"]["character"]}')
                rank_icon = disnake.utils.get(main_bot.emojis, name=f'{matches[f"game_{c}"]["rank"][0]}_'
                                                                    f'{matches[f"game_{c}"]["rank"][1]}')
                pre_embed.add_field(name=f'{matches[f"game_{c}"]["date"]}',
                                    value=f'{matches[f"game_{c}"]["map"]}\n'
                                          f'{result_emoji} '
                                          f'{matches[f"game_{c}"]["team_a"]} - {matches[f"game_{c}"]["team_b"]}\n'
                                          f'{rank_icon} Эло: {matches[f"game_{c}"]["elo"]}')
                pre_embed.add_field(name='Личный счет',
                                    value=f'{matches[f"game_{c}"]["score"]}\n'
                                          f'у{matches[f"game_{c}"]["kills"]}/'
                                          f'с{matches[f"game_{c}"]["deaths"]}/'
                                          f'п{matches[f"game_{c}"]["assists"]}\n'
                                          f'Агент: {character_icon}\n')
                pre_embed.add_field(name='', value='', inline=False)
            pre_embed.set_thumbnail(
                url=valorant_system.get_player_info(name=name, tag=tag, region=region)['card']['small'])
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


def setup(bot: commands.Bot):
    bot.add_cog(Valorant(bot))
