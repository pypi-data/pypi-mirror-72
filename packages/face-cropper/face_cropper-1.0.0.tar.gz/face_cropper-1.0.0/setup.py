import setuptools


with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name='face_cropper',
    version='1.0.0',
    author="Alexis Haim",
    author_email="alexishaim@outlook.fr",
    description="A image cropping library",
    install_requires=["numpy", "dlib", "Pillow", "click", "termcolor"],
    keywords=["computer vision", "crop", "face recognition"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dave-Lopper/face_cropper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
    ],
)
