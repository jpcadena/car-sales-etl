# car-sales-etl

<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>

<!-- PROJECT SHIELDS -->
<!--
*** Markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
-->


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="assets/static/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">car-sales-etl</h3>

  <p align="center">
    Description for car-sales-etl project
    <br />
    <a href="https://github.com/jpcadena/car-sales-etl"><strong>Explore the docs »</strong></a>
    <br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->

## About the project

[![Project][project-screenshot]](https://example.com)

This project is about building a data pipeline to extract, transform, and
load (ETL) data from a source to a target. The data source is a CSV file
containing information about car sales. The target is a PostgreSQL database
table.

PostgreSQL was preferred for the richer data handling with multiple data types,
transaction management and its highly scalability to provide great performance
at CRUD operations.\
The project followed SQLAlchemy models scheme based on OOP concepts that
provide an excellent abstraction when working with multiple datasets for a
future process. This high level abstraction provides a greater control over the
data being inserted as the table structure can be defined with multiple
constraints and relationships.\
For more advanced requirements, transactions, migrations and more complex
operations can be performed through the ORM so managing large amounts of data
won't be an issue.\
The project also works with PEP8 style that is tested with Pylint and this
includes type hinting for variables, functions arguments and more.

If performance is critical, consider using Python 3.11 in terms of handling
exceptions that can be thrown and re-raised in shorter execution times.\
Assets are also included with future consideration for HTML and CSS files.\
Testing could be done using unittests (to be implemented in a future release).

### Transformations

- Remove any rows with missing values.
- Convert the date columns to a standard format.
- Create a new column to store the year of the sale.
- Replace the categorical values in the "Car Model" column with numerical
  values.

### Requirements

- The target database should be either PostgreSQL or MySQL.
- The pipeline should be runnable using a command-line interface.
- The pipeline should have error handling and logging capabilities.
- The pipeline should be modular and easily extendable to handle additional
  data sources and transformations.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Built with

* [![Python][Python.org]][Python-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->

## Getting started

### Prerequisites

* [Python 3.10+][Python-docs-url]

### Installation

1. Clone the **repository**
    ```
    git clone https://github.com/jpcadena/car-sales-etl.git
    ```
2. Change the directory to **root project**
    ```
    cd car-sales-etl
    ```
3. Create a **virtual environment** *venv*
    ```
    python3 -m venv venv
    ```
4. Activate **environment** in Windows
    ```
    .\venv\Scripts\activate
    ```
5. Or with Unix/Mac OS X
    ```
    source venv/bin/activate
    ```
6. Install requirements with PIP
    ```
    pip install -r requirements.txt
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->

### Usage

1. Rename file **sample.env** to **.env**.
2. Replace your **credentials** into the *.env* file.
3. Execute with console.
    ```
    python main.py
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->

## Contributing

If you have a suggestion that would make this better, please fork the repo and
create a pull request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Use docstrings with **reStructuredText** format by adding triple double quotes
**"""** after function definition.\
Add a brief function description, also for the parameters including the return
value and its corresponding data type.\
Please use **linting** to check your code quality
following [PEP 8](https://peps.python.org/pep-0008/).\
Check documentation
for [Visual Studio Code](https://code.visualstudio.com/docs/python/linting#_run-linting)
or [Jetbrains Pycharm](https://github.com/leinardi/pylint-pycharm/blob/master/README.md).\

Recommended plugin for
autocompletion: [Tabnine](https://www.tabnine.com/install)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->

## License

Distributed under the MIT License.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->

## Contact

LinkedIn: [Juan Pablo Cadena Aguilar][linkedin-url]

E-mail: [Juan Pablo Cadena Aguilar](mailto:jpcadena@espol.edu.ec?subject=[GitHub]car-sales-etl)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[linkedin-url]: https://linkedin.com/in/juanpablocadenaaguilar

[project-screenshot]: assets/static/project.png

[Python.org]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54

[Python-url]: https://www.python.org/

[Python-docs-url]: https://docs.python.org/3.10/
