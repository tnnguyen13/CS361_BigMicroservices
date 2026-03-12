from flask import Flask, request, Response, jsonify
import csv
import io

app = Flask(__name__)


def validate_items(data):
    """
    Validates the JSON body sent by client

    Expected format:
    {
        "items": [
            {"name": "Send a V6", "completed": true},
            {"name": "Travel to Japan", "completed": false}
        ]
    }

    Returns a 3-part result:
    1. true/false: Whether validation succeeded
    2. If valid: List of items
       If invalid: JSON error response object
    3. If valid: None (no error code needed)
       If invalid: HTTP status code (such as 400)
    """
    # Ensure request body exists and is JSON object/Python dictionary
    if not isinstance(data, dict):
        return False, jsonify({"error": "Request body must be a JSON object"}), 400

    # Ensure required field "items" is present
    if "items" not in data:
        return False, jsonify({"error": "Request must include an 'items' field"}), 400

    # Extract items list from JSON body
    items = data["items"]
    if not isinstance(items, list):
        return False, jsonify({"error": "'items' must be a list"}), 400

    for item in items:
        if not isinstance(item, dict):
            return False, jsonify({"error": "Each item in 'items must be a dictionary"}), 400

    # If all checks pass:
    return True, items, None


def get_all_keys(items):
    """
    Builds a list of unique dictionary keys found across all items

    Example:
    items = [
        {"name": "Send a V6", "completed": true},
        {"name": "Travel to Japan", "completed": false, "priority": "high"}
    ]

    Returns:
        ["name", "completed", "priority"]

    This enables exporter to work with different main programs that may not use the same fields
    """
    keys = []

    for item in items:
        for key in item:

            # Only add unique key
            if key not in keys:
                keys.append(key)

    return keys


@app.route("/export/csv", methods=["POST"])
def export_csv():
    """
    Exports the provided items list as CSV text

    Client sends:
    POST /export/csv
    with JSON body:
    {
        "items": [...]
    }

    Response:
    Plain CSV text
    """
    # Read JSON body from HTTP request
    data = request.get_json()

    # Validate request body and unpack the 3 returned values
    valid, result, error = validate_items(data)

    # If invalid request, return JSON error response with corresponding status code
    if not valid:
        return result, error

    # If valid, result contains the items list
    items = result

    if len(items) == 0:
        return Response("No items to export.\n", mimetype="text/csv")

    # Determine column names from keys found in dictionaries
    keys = get_all_keys(items)

    # Create in-memory text buffer that acts like a file
    output = io.StringIO()

    # Create a CSV writer that writes dictionaries into CSV format
    # fieldnames=keys indicates CSV columns to use those key names
    csv_writer = csv.DictWriter(output, fieldnames=keys)

    # Write CSV header row first; Example: name, completed
    csv_writer.writeheader()

    # Write each dictionary in items as one CSV data row
    csv_writer.writerows(items)

    # Return final CSV text stored in-memory
    return Response(output.getvalue(), mimetype="text/csv")


@app.route("/export/markdown", methods=["POST"])
def export_markdown():
    """
    Exports the provided items list as a Markdown table

    Client sends:
    POST /export/markdown
    with JSON body:
    {
        "items": [...]
    }

    Response:
    Plain Markdown text
    """
    data = request.get_json()
    valid, result, error = validate_items(data)

    if not valid:
        return result, error

    items = result
    if len(items) == 0:
        return Response("No items to export.\n", mimetype="text/markdown")

    # All keys for table columns
    keys = get_all_keys(items)

    # Store each row of Markdown table as separate string
    lines = []

    # Build header row; Ex: | name | completed |
    header_row = "| " + " | ".join(keys) + " |"

    # Build required separator row for Markdown table; Ex: | --- | --- |
    separator_row = "| " + " | ".join(["---"] * len(keys)) + " |"

    lines.append(header_row)
    lines.append(separator_row)

    # Build one Markdown row per item
    for item in items:
        row_values = []

        # For each expected column/key, get value from this item
        for key in keys:
            row_values.append(str(item.get(key, "")))

        # Ex result: | Send a V6 | True |
        data_row = "| " + " | ".join(row_values) + " |"

        lines.append(data_row)

    # Join all rows into one multi-line string
    markdown_output = "\n".join(lines)

    return Response(markdown_output, mimetype="text/markdown")


if __name__ == "__main__":
    app.run(port=5002, debug=True)
