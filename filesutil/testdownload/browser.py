import subprocess
import tempfile
import os

def open_html_in_browser(html_content):
    """
    Opens the given HTML content in the default web browser on Ubuntu.

    Args:
    html_content (str): The HTML content to be displayed in the browser.

    Returns:
    None
    """
    # Create a temporary file
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
        # Write the HTML content to the temporary file
        f.write(html_content)
        temp_file_name = f.name

    # Use xdg-open to open the temporary file in the default web browser
    try:
        subprocess.run(['xdg-open', temp_file_name], check=True)
        print(f"Opened HTML content in browser. Temporary file: {temp_file_name}")
    except subprocess.CalledProcessError:
        print("Failed to open the browser. Make sure xdg-open is installed.")
    except FileNotFoundError:
        print("xdg-open not found. Make sure it's installed on your Ubuntu system.")

# Example usage
if __name__ == "__main__":
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Test Page</title>
    </head>
    <body>
        <h1>Hello, Ubuntu!</h1>
        <p>This is a test HTML page opened from Python on Ubuntu.</p>
    </body>
    </html>
    """
    open_html_in_browser(html_content)
