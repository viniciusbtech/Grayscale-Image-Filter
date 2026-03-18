🖼️ Image Editor in Python
📌 Description

This project is a Graphical Image Editor developed in Python, using the Tkinter library for the interface and Pillow (PIL) for image manipulation.
The application allows the user to:
Add images from the computer
Download images from the internet
Apply visual filters
View saved images
Clean images from the program directory
The goal of this project is to practice object-oriented programming, image processing, and graphical user interface development in Python.

🚀 Features

✔ Add local images
✔ Download images via URL
✔ Apply image filters
✔ View images saved in the directory
✔ Automatically clean images from the directory
✔ Simple and interactive graphical interface

🎨 Available Filters

The system includes several filters that can be applied to images:
Grayscale
Black and White
Cartoon
Negative
Edge Detection
Blur

Each filter generates a new image automatically saved in the directory with a timestamp.

🖥️ System Interface

The interface was built using Tkinter and includes the following buttons:
Add Image
Choose Filter
Show Images
Clear Images
Exit

Images are displayed directly in the interface after loading or applying filters.

🛠️ Technologies Used

Python 3
Tkinter – Graphical interface
Pillow (PIL) – Image processing
Requests – Downloading images from the internet
OS / Shutil – File manipulation

📦 Installation

Clone the repository:
git clone https://github.com/seuusuario/editor-imagens-python.git
Navigate to the project folder:
cd editor-imagens-python
Install the dependencies:

pip install pillow
pip install requests
▶️ How to Run

Run the main file:
python projetofinal5.py
The image editor interface will open automatically.


📁 Project Structure
editor-imagens-python
│
├── projetofinal5.py
├── imagem.jpg (interface background image)
└── README.md
📚 Concepts Used


This project applies several important programming concepts:

Object-Oriented Programming (OOP)
File manipulation
Graphical user interface development
File downloading via HTTP
Image processing
Code organization using classes
