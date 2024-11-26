#https://api.chess.com/pub/leaderboards

import requests, json


def newLeaderboardData():
    url = "https://api.chess.com/pub/leaderboards"
    data = requests.get(url)

    data = json.load(data)
    for player in data:
        if player["country"] == "https://api.chess.com/pub/country/IN":
            print(player)






 
# {
#       "player_id": 379601071,
#       "@id": "https://api.chess.com/pub/player/beastsdc01",
#       "url": "https://www.chess.com/member/BEASTSDC01",
#       "username": "BEASTSDC01",
#       "score": 2245,
#       "rank": 11,
#       "country": "https://api.chess.com/pub/country/IN",
#       "name": "Divyanshu chad+ha",
#       "status": "basic",
#       "avatar": "https://images.chesscomfiles.com/uploads/v1/user/379601071.e2e0cf20.200x200o.fe205e402e64.png",
#       "trend_score": {
#         "direction": 0,
#         "delta": 0
#       },
#       "trend_rank": {
#         "direction": 1,
#         "delta": 1
#       },
#       "flair_code": "discord_clyde",
#       "win_count": 14,
#       "loss_count": 1,
#       "draw_count": 0
#     },
#     {
#       "player_id": 106945802,
#       "@id": "https://api.chess.com/pub/player/oliv9136",
#       "url": "https://www.chess.com/member/oliv9136",
#       "username": "oliv9136",
#       "score": 2244,
#       "rank": 12,
#       "country": "https://api.chess.com/pub/country/FR",
#       "name": "Olivier 9136",
#       "status": "basic",
#       "avatar": "https://www.chess.com/bundles/web/images/noavatar_l.84a92436.gif",
#       "trend_score": {
#         "direction": 0,
#         "delta": 0
#       },
#       "trend_rank": {
#         "direction": 1,
#         "delta": 1
#       },
#       "flair_code": "nothing",
#       "win_count": 323,
#       "loss_count": 9,
#       "draw_count": 15
#     },
#     {
#       "player_id": 30809972,
#       "@id": "https://api.chess.com/pub/player/mrf8x8",
#       "url": "https://www.chess.com/member/mrf8x8",
#       "username": "mrf8x8",
#       "score": 2234,
#       "rank": 13,
#       "country": "https://api.chess.com/pub/country/IR",
#       "status": "basic",
#       "avatar": "https://www.chess.com/bundles/web/images/noavatar_l.84a92436.gif",
#       "trend_score": {
#         "direction": 0,
#         "delta": 0
#       },
#       "trend_rank": {
#         "direction": 1,
#         "delta": 1
#       },
#       "flair_code": "nothing",
#       "win_count": 35,
#       "loss_count": 8,
#       "draw_count": 7
#     },
#     {
#       "player_id": 33919518,
#       "@id": "https://api.chess.com/pub/player/huntwabow",
#       "url": "https://www.chess.com/member/huntwabow",
#       "username": "huntwabow",
#       "score": 2220,
#       "rank": 14,
#       "country": "https://api.chess.com/pub/country/US",
#       "name": "Walt",
#       "status": "basic",
#       "avatar": "https://images.chesscomfiles.com/uploads/v1/user/33919518.7519205f.200x200o.196e56e7a936.jpeg",
#       "trend_score": {
#         "direction": 0,
#         "delta": 0
#       },

