# lucastamatescu-python-package

Instanstiate the class, passing in the file as a argument, and the name of the window used in the imshow function later in the script
>>> objectvideo = overlay.video_overlay_class('logo.png','video_output')

Within the video processing loop, use the below line to add the overlay:
>>> frame = objectvideo.overlay_image(frame)



Commands to create package:

python3 setup.py sdist bdist_wheel

python3 -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*



