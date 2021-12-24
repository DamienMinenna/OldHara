# OldHara

![GitHub](https://img.shields.io/github/license/DamienMinenna/OldHara?style=flat-square)

![GitHub last commit](https://img.shields.io/github/last-commit/DamienMinenna/OldHara?style=flat-square)

The open-source reference management software.
*OldHara* is a web application to manage large number of scientific articles and books.



## Installation

### requirements

You will need the last version of Python, Django, and the lib PyPDF: 

```bash
sudo apt-get install python3.7
sudo apt-get install python3-pypdf2
pip install Django
```
<!--or // TODO
```bash
python -m pip install -r requirements.txt
```-->

### Project
You can download the git project or directly clone it.

```bash
git clone https://github.com/DamienMinenna/OldHara.git
```

Finally just launch the server.

```bash
python manage.py makemigrations OldHara_app && \
  python manage.py makemigrations && \
  python manage.py migrate && \
  python manage.py runserver
```

The following message should appear:

```bash
Django version 3.1.7, using settings 'OldHara.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
Leave the terminal open.

Now, you can open *OldHara* using any web browser at the address: http://127.0.0.1:8000/



## Usage

### Folders

* For your first use, you **must create at least one folder**. Folders are created in the *../OldHara/media/* directory. Every references, even without an associated file (pdf, jpg, ..) must be given a unique folder. 

* Sub directories can be created as *dir/subdir* if *dir* exist.


### Add entry

To add a reference, click on "Add entry". 

* The dropzone allows to create multiple references with their files. After using the dropzone, entries are put in the "Files to sort" section.
* A reference can be added using its DOI directly.

