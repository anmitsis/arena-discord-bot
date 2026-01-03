import requests
import time
from collections import defaultdict
import os


API_KEY = os.getenv("RIOT_API_KEY")
ROUTING_REGION = "europe"

HEADERS  = {
    "X-Riot-Token": API_KEY
}

PLAYERS = [
    ("boomer groomer", "AMEA"),
    ("eid3t1c", "EUNE"),
    ("theDogProgrammer", "EUNE")
]

# 1️⃣ Riot ID → PUUID
def get_puuid(game_name, tag_line):
    url = f"https://{ROUTING_REGION}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()["puuid"]


# 2️⃣ Get match IDs 
def get_match_ids(puuid, count, start=0):
    url = f"https://{ROUTING_REGION}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    params = {
        "start": start,
        "count": count
    }
    r = requests.get(url, headers=HEADERS, params=params)
    r.raise_for_status()
    return r.json()


# 3️⃣ Get damage for a specific player in a match
def get_damage(match_id, puuid):
    url = f"https://{ROUTING_REGION}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    data = r.json()

    if data["info"]["queueId"] != 1700:
        return None

    for p in data["info"]["participants"]:
        if p["puuid"] == puuid:
            return  p["totalDamageDealtToChampions"]
        
def fetch_damage_data(arena_games_target):
    results = {}

    for name, tag in PLAYERS:
        riot_id = f"{name}#{tag}"
        puuid = get_puuid(name, tag)

        collected_damages = []
        start = 0
        batch_size = 20   # safe chunk size

        while len(collected_damages) < arena_games_target:
            match_ids = get_match_ids(puuid, count=batch_size, start=start)

            if not match_ids:
                break  # no more matches

            for match_id in match_ids:
                if len(collected_damages) >= arena_games_target:
                    break

                dmg = get_damage(match_id, puuid)
                if dmg is not None:   # Arena only
                    collected_damages.append(dmg)

            start += batch_size

        if not collected_damages:
            continue

        total = sum(collected_damages)
        avg = total / len(collected_damages)

        results[riot_id] = {
            "games": len(collected_damages),
            "total": total,
            "avg": avg
        }

    return results

# def main():
#     results = defaultdict(list)

#     # resolve PUUIDs
#     puuids = {
#         f"{name}#{tag}": get_puuid(name, tag)
#         for name, tag in PLAYERS
#     }

#     # collect damage per match
#     for riot_id, puuid in puuids.items():
#         match_ids = get_match_ids(puuid)

#         for match_id in match_ids:
#             dmg = get_damage(match_id, puuid)
#             results[riot_id].append(dmg)

#     print("\n========== FINAL DAMAGE SUMMARY ==========")

#     for riot_id, damages in results.items():
#         games = len(damages)
#         total_damage = sum(damages)
#         avg_damage = total_damage / games if games > 0 else 0

#         print(
#             f"{riot_id} had {total_damage:,} total damage "
#             f"in {games} games "
#             f"({avg_damage:,.0f} avg per game)"
#         )


# if __name__ == "__main__":
#     main()

