<a name="readme-top"></a>
<!-- PROJECT LOGO -->
<div align='center'>
  <a href="https://www.python.org/" target="_blank" rel="noreferrer">
    <img src="https://raw.githubusercontent.com/danielcranney/readme-generator/main/public/icons/skills/python-colored.svg" height="95" alt="Python">
  </a>
  <a>
    <img src="https://cdn.pixabay.com/photo/2023/01/26/08/21/business-7745315_1280.png" height="100" alt="Team" hspace="0">
  </a>
  </a>
  <a>
    <img src="https://cdn.pixabay.com/photo/2017/10/25/18/10/peer-review-icon-2888794_1280.png" height="100" alt="Review" hspace="10">
  </a>

<h3 align="center">reviews_api</h3>

  <p align="center">
    App to share your valuable reviews
    <br />
    <a href="#getting-started"><strong>--> Quick start <--</strong></a>
    <br />
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#features">Features</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#Get-project">Get project</a></li>
        <li><a href="#Run-as-python-script">Run as python script</a></li>
        <li><a href="#Secrets">Secrets</a></li>
      </ul>
    </li>
    <li><a href="#explanation">Explanations</a></li>
    <li><a href="#restrictions">Restrictions</a></li>
    <li><a href="#project-team">Project team</a></li>
  </ol>
</details>

## Features
- Adding your valuable reviews to each work (book, film, song, etc.).
- Selecting a work to review from one of the categories or genres.
- Adding a score from 1 to 10 to each work and getting the average score for all reviews.
- Adding your comments to reviews of other users.

## Built With
![](https://img.shields.io/badge/python-3.9.19-blue)
![](https://img.shields.io/badge/Django-3.2.3-blue)
![](https://img.shields.io/badge/DRF-3.12.4-blue)
![](https://img.shields.io/badge/DRF_simplejwt-4.7.2-blue)

![](https://img.shields.io/badge/test_coverage-98%25-green)

# Getting Started

## Run as python script
### Prerequisites

* python **3.9.19**
* pip

### Installation

1. Clone the repo
   ```sh
   $ git clone https://github.com/Alexandr-Safariantc/reviews_api
   ```
2. Activate virtual environment
   ```sh
   $ cd reviews_api
   $ python3 -m venv venv
* for Linux/macOS
    ```sh
    $ source .venv/bin/activate
    ```
* for windows
    ```sh
    $ source .venv/scripts/activate
    ```

3. Upgrage pip
    ```sh
    (venv) $ python3 -m pip install --upgrade pip
    ```

4. Install requirements
    ```sh
    (venv) $ pip install -r requirements.txt
    ```

5. Migrate database
    ```sh
    (venv) $ cd api_yamdb/
    (venv) $ python3 manage.py migrate
    ```

6. Add test data to database
    ```sh
    (venv) $ python3 manage.py import_csv
    ```

7. Run app
    ```sh
    (venv) $ python3 manage.py runserver
    ```

8. Get API docs
    ```sh
    http://127.0.0.1:8000/redoc/
    ```

### Secrets

#### .env secrets

`ALLOWED_HOSTS`: {IP address of server you want to deploy},127.0.0.1,localhost,{your domane name if exists}<br>
`DEBUG_VALUE`: if not setted debug mode is off, **not required**<br>
`SECRET_DJANGO_KEY`: secret key for Django app<br>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Explanation
### Database Structure

  `Category` <br>
  Contains name, slug.

  `Genre` <br>
  Contains name, slug.

  `Title` <br>
  Contains category, description, genre, name, year.

  `GenreTitle` <br>
  Linked model for Genre - Title relation.

  `Review` <br>
  Contains author, pub_date, score, text, title.

  `Comment` <br>
  Contains author, pub_date, review, text.

## Restrictions

**1. Year of title creation** <br>
We can't predict the future so only existing titles can be published in our feed.

**2. One author - one review** <br>
We value the opinions of all reviews' authors equally so you can add only one review to each title.

**3. Review score** <br>
Your review score must be integer number from 1 to 10.

**4. Username 'me'** <br>
The username 'me' isn't the best choice, is it? This value is limited for our application.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Project team

**Aleksandr Safariants** - Backend-developer

[![Gmail Badge](https://img.shields.io/badge/-safariantc.aa@gmail.com-c14438?style=flat&logo=Gmail&logoColor=white&link=mailto:safariantc.aa@gmail.com)](mailto:safariantc.aa@gmail.com)<p align='left'>

#### Models, views, endpoints for:
  * titles,
  * users.
#### Users management:
  * registration, authentification system,
  * permissions,
  * token management,
  * e-mail confirmation system.

**Iakov Kuznetsov** - Backend-developer

[![Gmail Badge](https://img.shields.io/badge/-jacob.sokolov.dev@gmail.com-c14438?style=flat&logo=Gmail&logoColor=white&link=mailto:jacob.sokolov.dev@gmail.com)](mailto:jacob.sokolov.dev@gmail.com)<p align='left'>

#### Models for:
* categories,
* genres.
#### Views endpoints for:
* categories,
* genres,
* reviews,
* comments.
#### Additional tasks:
* title scores,
* import from .csv files.

**Konstantin Leontiev** - Teamlead

[![Gmail Badge](https://img.shields.io/badge/-K.A.Leontyev@gmail.com-c14438?style=flat&logo=Gmail&logoColor=white&link=mailto:K.A.Leontyev@gmail.com)](mailto:K.A.Leontyev@gmail.com)<p align='left'>

#### Models for:
* reviews,
* comments.
#### Additional tasks:
* project management,
* code review,
* import from .csv files.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
