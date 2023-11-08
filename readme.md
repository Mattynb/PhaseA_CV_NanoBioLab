# Ampli Recognition System

This program is designed to load and process images from a specified folder, find the grid and Ampli blocks in the image, and then read the diagnostic result for each Ampli block. It includes the following components:

- `main.py`: The main script for loading and creating Image objects from a folder of images.
- `Image_loader.py`: A module for loading images from a folder.
- `Image_class.py`: A module for processing and resizing images.
- `Image_scanner.py`: A module for scanning and processing images.

## Getting Started

### Prerequisites

Before running the code, make sure you have the following prerequisites installed:

- Python 3.x
- OpenCV (cv2)
- Numpy (np)
- Pillow (PIL)
- pillow_heif

### Installation

Clone this repository to your local machine:

```bash
git clone "https://github.com/mattynb/your-repo.git"
```

### Usage
To use this toolkit, follow these steps:

1. Open the main.py script.
2. Set the path_to_imgs variable to the path of the folder containing your images.
3. Run the main function to load and process the images.
``` python
if __name__ == '__main__':
    path_to_imgs = r"C:\Users\YourUser\Desktop\YourImageFolder\*"
    main(path_to_imgs)
```

### Image Loading
The Image_loader.py module provides functions for loading images from a folder, including HEIC to JPG conversion.

### Image Processing
The Image_class.py module includes image preprocessing and resizing functions.

### Image Scanning
The Image_scanner.py module offers functionality for scanning and processing images, including removing the background and finding grid corners.

For more details, refer to the individual code files and their respective functions.

Contributing
If you'd like to contribute to this project, please follow these guidelines:

Fork the repository.
Create a new branch for your feature or bug fix.
Make your changes.
Test your changes thoroughly.
Create a pull request.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Contact
If you have any questions or need assistance, feel free to contact the project maintainers:

Your Name your.email@example.com
We hope you find this toolkit useful for your image processing needs!

less
Copy co