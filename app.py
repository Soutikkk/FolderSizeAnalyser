import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def get_dir_size_and_stats(path):
    total_size = 0
    file_types = {}
    largest_files = []
    children_sizes = []
    
    try:
        # First gather immediate children
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            size = 0
            if os.path.exists(item_path):
                if os.path.isfile(item_path):
                    try:
                        size = os.path.getsize(item_path)
                        ext = os.path.splitext(item)[1].lower() or 'unknown'
                        file_types[ext] = file_types.get(ext, 0) + size
                        largest_files.append({"name": item, "path": item_path, "size": size})
                    except (PermissionError, OSError):
                        continue
                elif os.path.isdir(item_path):
                    dir_size = get_folder_size(item_path, file_types, largest_files)
                    size = dir_size
                
                children_sizes.append({"name": item, "is_dir": os.path.isdir(item_path), "size": size})
                total_size += size

        # Sort top files
        largest_files.sort(key=lambda x: x["size"], reverse=True)
        largest_files = largest_files[:10]
        
        # Sort children
        children_sizes.sort(key=lambda x: x["size"], reverse=True)

        return {
            "success": True,
            "total_size": total_size,
            "file_types": file_types,
            "largest_files": largest_files,
            "children": children_sizes
        }
    except PermissionError:
        return {"success": False, "error": f"Permission denied to access {path}. Try running as Administrator or select a different folder."}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_folder_size(path, file_types, largest_files):
    total_size = 0
    try:
        for root, dirs, files in os.walk(path):
            for f in files:
                fp = os.path.join(root, f)
                try:
                    if not os.path.islink(fp) and os.path.exists(fp):
                        size = os.path.getsize(fp)
                        total_size += size
                        ext = os.path.splitext(f)[1].lower() or 'unknown'
                        file_types[ext] = file_types.get(ext, 0) + size
                        largest_files.append({"name": f, "path": fp, "size": size})
                        # Keep list small to save memory during walk
                        if len(largest_files) > 100:
                            largest_files.sort(key=lambda x: x["size"], reverse=True)
                            del largest_files[10:]
                except (PermissionError, OSError):
                    pass # Skip files we can't access
    except (PermissionError, OSError):
        pass # Skip dirs we can't access reading
    return total_size

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.json
    path = data.get('path', '')
    
    if not path or not os.path.exists(path):
         return jsonify({"success": False, "error": "Invalid or non-existent path"})
    
    stats = get_dir_size_and_stats(path)
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
