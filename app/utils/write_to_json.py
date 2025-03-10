import json
import datetime
import os


def write_json_to_file(data, prefix="output", paths="C:\\LangGraphTripPlanner-main\\app\\log_dir"):
    """
    Writes a dictionary to a JSON file with a timestamped filename.
    
    :param data: Dictionary containing JSON data
    :param prefix: Prefix for the filename (default: "output")
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}.json"

    file_path = os.path.join(paths, filename)

    print("file path is : ", file_path)

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error writing JSON file: {e}")


# Example usage
# data = {
#     "name": "John Doe",
#     "age": 30,
#     "city": "New York"
# }

# write_json_to_file(data, "my_data")
