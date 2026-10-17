
import json
from implement import(filename,metadata_file)


def save_data(members, metadata):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(members, file, indent=4)
    with open(metadata_file, "w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=4)

