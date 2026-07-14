import os
from typing import Dict, List, Any

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

MAX_TOP_FILES = 10
MAX_CACHE_FILES = 100


def update_file_stats(
    file_path: str,
    file_name: str,
    file_types: Dict[str, int],
    largest_files: List[Dict[str, Any]]
) -> int:
    """
    Collect size information for a file.
    """
    try:
        if os.path.islink(file_path) or not os.path.exists(file_path):
            return 0

        size = os.path.getsize(file_path)
        extension = os.path.splitext(file_name)[1].lower() or "unknown"

        file_types[extension] = file_types.get(extension, 0) + size

        largest_files.append(
            {
                "name": file_name,
                "path": file_path,
                "size": size,
            }
        )

        return size

    except (PermissionError, OSError):
        return 0


def get_folder_size(
    folder_path: str,
    file_types: Dict[str, int],
    largest_files: List[Dict[str, Any]],
) -> int:
    """
    Recursively calculate folder size.
    """
    total_size = 0

    try:
        for root, _, files in os.walk(folder_path):

            for file in files:
                file_path = os.path.join(root, file)

                total_size += update_file_stats(
                    file_path,
                    file,
                    file_types,
                    largest_files,
                )

                if len(largest_files) > MAX_CACHE_FILES:
                    largest_files.sort(
                        key=lambda item: item["size"],
                        reverse=True,
                    )
                    del largest_files[MAX_TOP_FILES:]

    except (PermissionError, OSError):
        pass

    return total_size


def get_directory_statistics(path: str) -> Dict[str, Any]:
    """
    Analyze a directory and return its statistics.
    """
    total_size = 0
    file_types = {}
    largest_files = []
    children = []

    try:
        for item in os.listdir(path):

            item_path = os.path.join(path, item)

            if not os.path.exists(item_path):
                continue

            if os.path.isfile(item_path):
                size = update_file_stats(
                    item_path,
                    item,
                    file_types,
                    largest_files,
                )

            elif os.path.isdir(item_path):
                size = get_folder_size(
                    item_path,
                    file_types,
                    largest_files,
                )

            else:
                size = 0

            children.append(
                {
                    "name": item,
                    "is_dir": os.path.isdir(item_path),
                    "size": size,
                }
            )

            total_size += size

        largest_files.sort(
            key=lambda item: item["size"],
            reverse=True,
        )

        children.sort(
            key=lambda item: item["size"],
            reverse=True,
        )

        return {
            "success": True,
            "total_size": total_size,
            "file_types": file_types,
            "largest_files": largest_files[:MAX_TOP_FILES],
            "children": children,
        }

    except PermissionError:
        return {
            "success": False,
            "error": (
                f"Permission denied while accessing '{path}'. "
                "Run as Administrator or choose another folder."
            ),
        }

    except Exception as error:
        return {
            "success": False,
            "error": str(error),
        }


@app.route("/")
def home():
    """
    Render homepage.
    """
    return render_template("index.html")


@app.route("/api/analyze", methods=["POST"])
def analyze_directory():
    """
    Analyze a directory sent from the frontend.
    """
    data = request.get_json()

    if not data:
        return jsonify(
            {
                "success": False,
                "error": "No request data received.",
            }
        )

    path = data.get("path", "").strip()

    if not path:
        return jsonify(
            {
                "success": False,
                "error": "Directory path is required.",
            }
        )

    if not os.path.exists(path):
        return jsonify(
            {
                "success": False,
                "error": "Directory does not exist.",
            }
        )

    if not os.path.isdir(path):
        return jsonify(
            {
                "success": False,
                "error": "Provided path is not a directory.",
            }
        )

    return jsonify(get_directory_statistics(path))


if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000,
    )
