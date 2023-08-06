import cassiopeia as cass
from cassiopeia import Summoner
from ezreal.utils import engine
from ezreal.core.summoner import get_summoner_info


def print_summoner(name: str, region: str):
    summoner = get_summoner_info(name, region)
    print("Name:", summoner.name)
    print("ID:", summoner.id)
    print("Account ID:", summoner.account_id)
    print("Level:", summoner.level)
    print("Revision date:", summoner.revision_date)
    print("Profile icon ID:", summoner.profile_icon.id)
    print("Profile icon name:", summoner.profile_icon.name)
    print("Profile icon URL:", summoner.profile_icon.url)
    print("Profile icon image:", summoner.profile_icon.image)
    return summoner


if __name__ == "__main__":
    summoner = print_summoner("Kassout", "EUW")
    # print(summoner)