import os
import json
import implement


def load_metadata():
    if not os.path.exists(implement.metadata_file):
        return {
            "current_week": 1,
            "payout_history": []
        }
    try:
        with open(implement.metadata_file, "r", encoding="utf-8") as file:
            metadata = json.load(file)

    except json.JSONDecodeError as error:
        raise ValueError(
            f"{implement.metadata_file} contains invalid JSON. "
            "Correct the file before continuing."
        ) from error

    except OSError  as error:
        raise ValueError(
            f"Couldn't read {implement.metadata_file}: {error}"
        ) from error
    
    if not isinstance(metadata, dict):
        raise ValueError("The metadata file has an invalid structure.")
    current_week = metadata.get("current_week", 1)
    if (
        type(current_week) is not int
        or current_week < 1
    ):
        raise ValueError("The current week must be a positive integer.")
    payout_history = metadata.get("payout_history", [])
    if not isinstance(payout_history, list):
        raise ValueError("The payout history has an invalid structure.")
    metadata["current_week"] = current_week
    metadata["payout_history"] = payout_history
    return metadata
