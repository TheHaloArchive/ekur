import requests
import json


def main() -> None:
    response = requests.get("https://hi.cylix.guide/crab.json").json()

    regions = {}

    for item in response:
        if item.get("data") and item["data"].get("RegionData"):
            for region in item["data"]["RegionData"]:
                region_id = region["RegionId"]["m_identifier"]
                permutation_id = region["PermutationId"]["m_identifier"]

                if region_id not in regions:
                    regions[region_id] = {
                        "name": str(region_id),
                        "permutations": {},
                    }

                regions[region_id]["permutations"][permutation_id] = {
                    "name": item["title"]
                }

    with open("regions_and_permutations.json", "w") as f:
        json.dump(regions, f, indent=4)


if __name__ == "__main__":
    main()
