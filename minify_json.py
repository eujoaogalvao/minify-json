import argparse
import json


def minify_json(input_file, output_file=None):
    """
    Reads a JSON file, minifies its content, and writes it to an output file or prints it.

    Args:
        input_file (str): Path to the input JSON file.
        output_file (str, optional): Path to the output JSON file.
                                     If None, prints to stdout.
    """
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Minify by dumping with no indent and compact separators
        minified_json = json.dumps(data, separators=(",", ":"))

        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(minified_json)
            print(f"Successfully minified '{input_file}' to '{output_file}'")
        else:
            print(minified_json)

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{input_file}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Minify a JSON file.")
    parser.add_argument("input_file", help="Path to the input JSON file.")
    parser.add_argument(
        "-o",
        "--output_file",
        help="Path to the output minified JSON file (optional). "
        "If not provided, output will be printed to stdout.",
    )

    args = parser.parse_args()

    minify_json(args.input_file, args.output_file)
