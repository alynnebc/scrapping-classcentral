# Scrapping Online Courses in class central

This project scrape data about Engineering job offers in New York City from [classcentral.com](https://www.classcentral.com) using Scrapy, a framework for extracting the data from websites.

The project has one spider able to some textual data (name, platform, language and URL) of all online courses in a subject of study.

The textual data is available in `jobs.csv` file. The extracted images are in `images` folder.

# How to use

You will need Python 3.x to run the scripts.
Python can be downloaded [here](https://www.python.org/downloads/).

You have to install Scrapy framework:
* In command prompt/Terminal: `pip install scrapy`
* If you are using [Anaconda Python distribution](https://anaconda.org/anaconda/python): `conda install -c conda-forge scrapy`

You have to install also Selenium:
* In command prompt/Terminal: `pip install selenium`
* If you are using [Anaconda Python distribution](https://anaconda.org/anaconda/python): `conda install -c conda-forge selenium`

Once you have installed Scrapy and Selenium, just clone/download this project, access the folder in command prompt/Terminal and run the following command:

`scrapy crawl classcentral -o courses.csv`

This command will scrape, by default, all Data Science courses in class central. To scrape other [listed subject](https://www.classcentral.com/subjects) on class central, run the following command:

`scrapy crawl classcentral -a subject="Subject Name" -o courses.csv`

So, to scrape the Health & Medicine courses, you need to run the following command:

`scrapy crawl classcentral -a subject="Health & Medicine" -o courses.csv`

You can change the output format to JSON or XML by change the output file extension (ex: `jobs.json`).
