import requests


def get_player_info(name, tag, region):
    if requests.get(url=f'https://api.henrikdev.xyz/valorant/v1/account/{name}/{tag}').json()['status'] == 404:
        return False
    else:
        requested = requests.get(url=f'https://api.henrikdev.xyz/valorant/v1/account/{name}/{tag}').json()
        requested_rating = \
            requests.get(url=f'https://api.henrikdev.xyz/valorant/v2/mmr/{region}/{name}/{tag}').json()
        player_info = {
            'level': requested['data']['account_level'],
            'card': requested['data']['card']['wide'],
            'current_rank': requested_rating['data']['current_data']['currenttierpatched'],
            'current_rank_icon': requested_rating['data']['current_data']['images']['large'],
            'current_elo': requested_rating['data']['current_data']['ranking_in_tier'],
            'last_elo_change': requested_rating['data']['current_data']['mmr_change_to_last_game'],
            'highest_rank': requested_rating['data']['highest_rank']['patched_tier'],
            'highest_rank_season': requested_rating['data']['highest_rank']['season']
        }
        return player_info


def get_matches(name, tag, region):
    if requests.get(url=f'https://api.henrikdev.xyz/valorant/v1/lifetime/matches/'
                        f'{region}/{name}/{tag}?mode=competitive&size=5').json()['status'] == 404:
        return False
    else:
        requested_matches = requests.get(url=f'https://api.henrikdev.xyz/valorant/v1/lifetime/matches/'
                                             f'{region}/{name}/{tag}?mode=competitive&size=5').json()
        requested_elo_changes = requests.get(url=f'https://api.henrikdev.xyz/valorant/v1/mmr-history/'
                                                 f'{region}/{name}/{tag}').json()
        matches = {}
        total_wins = 0
        total_lose = 0
        total_ff = 0
        total_kills = 0
        total_deaths = 0
        total_elo = 0
        for c in range(5):
            if requested_matches['data'][c]['stats']['team'] == 'Red':
                if requested_matches['data'][c]['teams']['red'] <= requested_matches['data'][c]['teams']['blue']:
                    result = 'Поражение'
                    total_lose += 1
                elif requested_matches['data'][c]['teams']['red'] == requested_matches['data'][c]['teams']['blue']:
                    result = 'Ничья'
                    total_ff += 1
                else:
                    result = 'Победа'
                    total_wins += 1
                team_a = requested_matches['data'][c]['teams']['red']
                team_b = requested_matches['data'][c]['teams']['blue']
            else:
                if requested_matches['data'][c]['teams']['blue'] <= requested_matches['data'][c]['teams']['red']:
                    result = 'Поражение'
                    total_lose += 1
                elif requested_matches['data'][c]['teams']['blue'] == requested_matches['data'][c]['teams']['red']:
                    result = 'Ничья'
                    total_ff += 1
                else:
                    result = 'Победа'
                    total_wins += 1
                team_a = requested_matches['data'][c]['teams']['blue']
                team_b = requested_matches['data'][c]['teams']['red']
            matches[f'game_{c}'] = {
                'map': requested_matches['data'][c]['meta']['map']['name'],
                'character': requested_matches['data'][c]['stats']['character']['name'],
                'score': '{:,}'.format(requested_matches['data'][c]['stats']['score']).replace(',', '.'),
                'kills': requested_matches['data'][c]['stats']['kills'],
                'deaths': requested_matches['data'][c]['stats']['deaths'],
                'assists': requested_matches['data'][c]['stats']['assists'],
                'k/d': round(requested_matches['data'][c]['stats']['kills'] /
                             requested_matches['data'][c]['stats']['deaths'], 2),
                'result': result,
                'team_a': team_a,
                'team_b': team_b,
                'elo': requested_elo_changes['data'][c]['mmr_change_to_last_game'],
                'rank': requested_elo_changes['data'][c]['currenttierpatched'].split(),
                'date': f'{requested_elo_changes["data"][c]["date"].split()[1]} '
                        f'{requested_elo_changes["data"][c]["date"].split()[2]} '
                        f'{requested_elo_changes["data"][c]["date"].split()[3]}'
            }
            total_kills += requested_matches['data'][c]['stats']['kills']
            total_deaths += requested_matches['data'][c]['stats']['deaths']
            total_elo += requested_elo_changes['data'][c]['mmr_change_to_last_game']
        matches['total_wins'] = total_wins
        matches['total_lose'] = total_lose
        matches['total_ff'] = total_ff
        matches['total_k/d'] = round(total_kills / total_deaths, 2)
        matches['total_elo'] = total_elo
    return matches
