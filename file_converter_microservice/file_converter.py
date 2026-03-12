# A Flask app to convert files to TXT or XLS format. It checks if the file already exists and generates a new filename if necessary. The app listens on port 5001 and provides an endpoint for the file conversion. It takes the full path of the source file and the desired conversion option (1 for TXT or 2 for XLS) as input and returns a newly created file.

import os
from flask import Flask, request, jsonify

app = Flask(__name__)


def generate_new_filename(directory, base_name, extension):
    #If file exists, append number to filename. Example: file.txt, file_1.txt, file_2.txt
    counter = 0
    new_name = f"{base_name}.{extension}"
    full_path = os.path.join(directory, new_name)

    while os.path.exists(full_path):
        counter += 1
        new_name = f"{base_name}_{counter}.{extension}"
        full_path = os.path.join(directory, new_name)

    return full_path


@app.route("/convert", methods=["POST"])
def convert_file():

    data = request.json
    file_path = data.get("file_path")
    option = data.get("option")

    if not file_path or not os.path.exists(file_path):
        return jsonify({"error": "File path invalid or file not found"}), 400

    directory = os.path.dirname(file_path)
    base_name = os.path.splitext(os.path.basename(file_path))[0]

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Option 1 → TXT
    if option == 1:
        new_file = generate_new_filename(directory, base_name, "txt")

        with open(new_file, "w", encoding="utf-8") as f:
            f.write(content)

    # Option 2 → XLS
    elif option == 2:
        new_file = generate_new_filename(directory, base_name, "xls")

        with open(new_file, "w", encoding="utf-8") as f:
            f.write(content)

    else:
        return jsonify({"error": "Option select must be 1 or 2"}), 400

    return jsonify({
        "message": "File created successfully",
        "new_file": new_file
    })


if __name__ == "__main__":
    app.run(port=5001, debug=True)
