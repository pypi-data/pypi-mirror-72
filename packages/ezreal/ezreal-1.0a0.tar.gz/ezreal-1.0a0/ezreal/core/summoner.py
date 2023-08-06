import cassiopeia as cass


def get_summoner_info(name: str, region: str):
    summoner = cass.get_summoner(name=name, region=region)
    return summoner