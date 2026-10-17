
import json
import implement


def save_data(members, metadata):
    with open(implement.filename, "w", encoding="utf-8") as file:
        json.dump(members, file, indent=4)
    with open(implement.metadata_file, "w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=4)
