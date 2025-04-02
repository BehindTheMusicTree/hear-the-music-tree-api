import json
from pathlib import Path


def combine_genre_trees():
    # Get the directory containing this script
    current_dir = Path(__file__).parent

    # Initialize the combined tree structure
    combined_tree = {"tree": []}

    # Find all JSON files in the directory
    json_files = list(current_dir.glob("*.json"))

    # Process each JSON file
    for json_file in json_files:
        if json_file.name == "complete_genre_tree.json":
            continue  # Skip the output file

        try:
            with open(json_file, "r") as f:
                data = json.load(f)

            # Add each genre from the file to the combined tree
            if "tree" in data:
                combined_tree["tree"].extend(data["tree"])

        except json.JSONDecodeError as e:
            print(f"Error reading {json_file}: {e}")
        except Exception as e:
            print(f"Unexpected error processing {json_file}: {e}")

    # Sort the genres alphabetically by name
    combined_tree["tree"].sort(key=lambda x: x["name"])

    # Write the combined tree to a new file
    output_file = current_dir / "complete_genre_tree.json"
    with open(output_file, "w") as f:
        json.dump(combined_tree, f, indent=2)

    print(f"Combined genre tree written to {output_file}")
    print(f"Total number of root genres: {len(combined_tree['tree'])}")


if __name__ == "__main__":
    combine_genre_trees()
