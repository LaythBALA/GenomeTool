This tool is a web-Based Genome Browser and Annotation Tool for Visualizing and Analysing Genetic Data.
The functions of this tool are:
1. Visualize data from the UCSC Genome Browser
2. Annotate genes through a commenting feature
3. Search for genes by name or location
4. Upload and visualize your own genomic data sets using iframes
5. Sign up for an account to save your annotations and collaborate with others.  

## Installation
1. Clone the repository
2. Install the dependencies
3. Run the server

### Clone the repository
```bash
git clone
```

###set up venv and install dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Set up the database
```bash
python manage.py makemigrations
python manage.py migrate
```
Ensure you uncomment the following lines in __init__.py the first time you run the server to create the database:
# create_database(app)


```bash
### Run the server
```bash
python main.py runserver
```

All dependencies are listed in requirements.txt. To install them, run:
```bash
pip install -r requirements.txt
```
