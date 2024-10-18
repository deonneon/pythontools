import os

# Set the root directory containing the HTML files
root_dir = r"/path/to/your/folder"  # Change this to your folder path


def generate_index(root_dir):
    # Create or open the index.html file
    with open(os.path.join(root_dir, "index.html"), "w") as index_file:
        # Write the basic structure of the index file
        index_file.write(
            """<html>
<head>
    <title>Index of HTML files</title>
    <style>
        body { display: flex; height: 100vh; margin: 0; }
        #file-list { width: 30%; padding: 10px; overflow-y: auto; background-color: #f7f7f7; }
        #file-viewer { width: 70%; border: none; }
        ul { list-style-type: none; padding: 0; }
        li { margin: 8px 0; }
    </style>
</head>
<body>
    <div id="file-list">
        <h1>Index of HTML files</h1>
        <ul>
"""
        )

        # Recursively walk the directory structure and generate the index with indentation
        for root, dirs, files in os.walk(root_dir):
            # Ignore the root index file itself
            if root == root_dir:
                files = [f for f in files if f != "index.html"]

            # Calculate indentation level based on folder depth
            depth = len(os.path.relpath(root, root_dir).split(os.sep)) - 1
            indent = " " * 4 * depth  # Use 4 spaces per level of depth

            # Write folder name at all levels, including root, and insert a break before each parent folder
            folder_name = os.path.relpath(root, root_dir)
            if depth > 0 or folder_name != ".":
                index_file.write(
                    f"{indent}<br>\n"
                )  # Insert a break before each parent folder
                index_file.write(f"{indent}<li><strong>{folder_name}/</strong></li>\n")
                index_file.write(f"{indent}<ul>\n")

            # Write file links with indentation and link them to the iframe
            for filename in files:
                if filename.endswith(".html"):
                    file_path = os.path.relpath(os.path.join(root, filename), root_dir)
                    index_file.write(
                        f'{indent}    <li><a href="{file_path}" target="file-viewer">{filename}</a></li>\n'
                    )

            # Close folder's list (if not root)
            if depth > 0 or folder_name != ".":
                index_file.write(f"{indent}</ul>\n")

        # Close the unordered list and the HTML tags
        index_file.write(
            """
        </ul>
    </div>
    <iframe id="file-viewer" name="file-viewer" src="" title="File Viewer"></iframe>

    <script>
        // Wait for the DOM to be fully loaded
        document.addEventListener('DOMContentLoaded', function() {
            const iframe = document.getElementById('file-viewer');
            
            // Function to fix image paths
            function fixImagePaths() {
                try {
                    const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
                    
                    // Get the current iframe's src (path to the HTML file)
                    const srcPath = iframe.src;
                    const basePath = srcPath.substring(0, srcPath.lastIndexOf('/')) + '/';
                    
                    // Find all img elements in the iframe document
                    const images = iframeDoc.querySelectorAll('img');
                    
                    // Adjust the src of each image to be relative to the HTML file's directory
                    images.forEach(img => {
                        const imgSrc = img.getAttribute('src');
                        if (imgSrc && !imgSrc.startsWith('http') && !imgSrc.startsWith(basePath)) {
                            img.src = basePath + imgSrc;
                        }
                    });
                } catch (e) {
                    console.log('Error fixing image paths:', e);
                }
            }

            // Attach the fixImagePaths function to iframe's load event
            iframe.addEventListener('load', fixImagePaths);
        });
    </script>
</body>
</html>
"""
        )

    print(
        "Formatted index file with dynamic image path correction generated successfully."
    )


# Call the function to generate the index
generate_index(root_dir)
