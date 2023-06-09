# News-Aggregator

This is a Django project that retrieves data from Reddit and NEWS API. It implements some of the backend functionalities like storing data into the Database, marking a news article as favorite and unmarking it. 

## Requirements

Before running this project, you will need to have Python and Django installed on your system. If you don't have them installed, you can download them from the following links:

- [Python](https://www.python.org/downloads/)
- [Django](https://www.djangoproject.com/download/)

## Installation

1. Clone the repository:

        git clone <https://github.com/abidrazaa/News-Aggregator>

2. Set up the virtual environment:

    It is always recommended to set up a virtual environment for each project. A virtual environment ensures that the dependencies required for your project do not conflict with other projects on your system. To set up a virtual environment for your Django project, navigate to the project directory in your terminal and run the following commands:

        python -m venv env
        source env/bin/activate  # on Linux/MacOS
        .\env\Scripts\activate  # on Windows

3. Install project dependencies:

    Once you have activated your virtual environment, you need to install the dependencies required for your Django project.

4. Run the project:

    To run the project, navigate to the project directory in your terminal and run the following command:

        python manage.py runserver

    This will start the development server at `http://localhost:8000/`.
    
    
 ## End Points
 1. news/list => to list news and the feature to search in the list of news.
 2. news/get => If the latest updated news is before 5 minutes, it will make an API call. else, it will retrieve data from the DB.
 3. news/favourite?user=[name] => It will list all the news that are marked favorite by the user.
 4. news/favourite?user=[name]&id=[id] => It will mark the news with the id={given_id} favorite and viceversa.
 
