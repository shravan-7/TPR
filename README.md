<p align="center">
  <img src="https://img.icons8.com/?size=512&id=55494&format=png" width="100" />
</p>
<p align="center">
    <h1 align="center">TPR</h1>
</p>
<p align="center">
    <em>Your ultimate travel recommendation platform.</em>
</p>
<p align="center">
	<img src="https://img.shields.io/github/license/shravan-7/TRP?style=flat&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/shravan-7/TRP?style=flat&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/shravan-7/TRP?style=flat&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/shravan-7/TRP?style=flat&color=0080ff" alt="repo-language-count">
<p>
<p align="center">
		<em>Developed with the software and tools below.</em>
</p>
<p align="center">
	<img src="https://img.shields.io/badge/Django-092E20.svg?style=flat&logo=Django&logoColor=white" alt="Django">
	<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white" alt="Python">
		<img src="https://img.shields.io/badge/SQL-4479A1.svg?style=flat&logo=MySQL&logoColor=white" alt="SQL">
	<img src="https://img.shields.io/badge/JavaScript-F7DF1E.svg?style=flat&logo=JavaScript&logoColor=black" alt="JavaScript">
	<img src="https://img.shields.io/badge/HTML5-E34F26.svg?style=flat&logo=HTML5&logoColor=white" alt="HTML5">
	<img src="https://img.shields.io/badge/CSS3-1572B6.svg?style=flat&logo=CSS3&logoColor=white" alt="CSS3">
	<img src="https://img.shields.io/badge/Bootstrap-7952B3.svg?style=flat&logo=Bootstrap&logoColor=white" alt="Bootstrap">

</p>
</p>
<hr>

## 🔗 Quick Links

> -   [📍 Overview](#-overview)
> -   [📦 Features](#-features)
> -   [📂 Repository Structure](#-repository-structure)
> -   [🧩 Modules](#-modules)
> -   [🚀 Getting Started](#-getting-started)
>     -   [⚙️ Installation](#️-installation)
>     -   [🤖 Running TRP](#-running-TRP)
>     -   [🧪 Tests](#-tests)
> -   [🛠 Project Roadmap](#-project-roadmap)
> -   [🤝 Contributing](#-contributing)
> -   [📄 License](#-license)
> -   [👏 Acknowledgments](#-acknowledgments)

---

## 📍 Overview

Welcome to the Tourist Place Recommendation (TRP) project! This platform leverages machine learning to provide personalized travel recommendations based on user preferences and past behavior. Whether you're looking for a serene beach, a bustling city, or a historical site, TRP aims to be your go-to travel guide.

---

## 📦 Features

-   **Personalized Recommendations:** Get travel suggestions tailored to your interests.
-   **User Preferences:** Save and manage your favorite places.
-   **Detailed Place Information:** Access comprehensive details about each recommended location.
-   **Interactive UI:** Enjoy a user-friendly interface for seamless navigation.
-   **Data-Driven Insights:** Recommendations are based on extensive datasets and user reviews.

---

## 📂 Repository Structure

```sh
└── TRP/
    ├── README.md
    └── Tourist_Place_Recommendation
        ├── Tourist_App
        │   ├── migrations
        │   ├── static
        │   │   ├── css
        │   │   ├── images
        │   │   └── js
        │   ├── admin.py
        │   ├── apps.py
        │   ├── models.py
        │   ├── rawQuery.py
        │   ├── read_dataset.py
        │   ├── recommend.py
        │   └── views.py
        ├── Tourist_Place_recommendation
        │   ├── asgi.py
        │   ├── settings.py
        │   ├── urls.py
        │   └── wsgi.py
        ├── templates
        │   ├── base
        │   └── user
        ├── manage.py
        ├── feature.pkl
        ├── knnpickle_file(1)
        ├── replaced_locations.csv
        ├── review_dataset.csv
        └── user_ratings5.csv
```

<hr>

## 🧩 Modules

<details closed><summary>Tourist_Place_Recommendation</summary>

| File                                                                                             | Summary                                                                                             |
| ------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------- |
| [manage.py](https://github.com/shravan-7/TRP/blob/master/Tourist_Place_Recommendation/manage.py) | Django's command-line utility for administrative tasks in the Tourist Place Recommendation project. |

</details>

<details closed><summary>Tourist_Place_Recommendation.templates.base</summary>

| File                                                                                                                    | Summary                                                                   |
| ----------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| [messages.html](https://github.com/shravan-7/TRP/blob/master/Tourist_Place_Recommendation/templates/base/messages.html) | HTML template for displaying messages (e.g., success, error) to the user. |

</details>

<details closed><summary>Tourist_Place_Recommendation.templates.user</summary>

| File                                                                                                                                  | Summary                                                                           |
| ------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| [recommendation.html](https://github.com/shravan-7/TRP/blob/master/Tourist_Place_Recommendation/templates/user/recommendation.html)   | HTML template for displaying personalized tourist place recommendations.          |
| [top_rated.html](https://github.com/shravan-7/TRP/blob/master/Tourist_Place_Recommendation/templates/user/top_rated.html)             | HTML template for showcasing top-rated tourist places.                            |
| [login.html](https://github.com/shravan-7/TRP/blob/master/Tourist_Place_Recommendation/templates/user/login.html)                     | HTML template for user login page.                                                |
| [profile.html](https://github.com/shravan-7/TRP/blob/master/Tourist_Place_Recommendation/templates/user/profile.html)                 | HTML template for displaying and editing user profile information.                |
| [preferences.html](https://github.com/shravan-7/TRP/blob/master/Tourist_Place_Recommendation/templates/user/preferences.html)         | HTML template for setting user preferences for tourist place recommendations.     |
| [place_details.html](https://github.com/shravan-7/TRP/blob/master/Tourist_Place_Recommendation/templates/user/place_details.html)     | HTML template for displaying detailed information about a specific tourist place. |
| [navigation.html](https://github.com/shravan-7/TRP/blob/master/Tourist_Place_Recommendation/templates/user/navigation.html)           | HTML template for the navigation menu.                                            |
| [registration.html](https://github.com/shravan-7/TRP/blob/master/Tourist_Place_Recommendation/templates/user/registration.html)       | HTML template for user registration page.                                         |
| [home.html](https://github.com/shravan-7/TRP/blob/master/Tourist_Place_Recommendation/templates/user/home.html)                       | HTML template for the home page of the application.                               |
| [search.html](https://github.com/shravan-7/TRP/blob/master/Tourist_Place_Recommendation/templates/user/search.html)                   | HTML template for the search functionality of tourist places.                     |
| [favorite_places.html](https://github.com/shravan-7/TRP/blob/master/Tourist_Place_Recommendation/templates/user/favorite_places.html) | HTML template for displaying user's favorite tourist places.                      |

</details>

<details closed><summary>Tourist_Place_Recommendation.Tourist_Place_recommendation</summary>

| File                                                                                                                              | Summary                                                          |
| --------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| [asgi.py](https://github.com/shravan-7/TRP/blob/master/Tourist_Place_Recommendation/Tourist_Place_recommendation/asgi.py)         | ASGI configuration for the Tourist Place Recommendation project. |
| [wsgi.py](https://github.com/shravan-7/TRP/blob/master/Tourist_Place_Recommendation/Tourist_Place_recommendation/wsgi.py)         | WSGI configuration for the Tourist Place Recommendation project. |
| [urls.py](https://github.com/shravan-7/TRP/blob/master/Tourist_Place_Recommendation/Tourist_Place_recommendation/urls.py)         | URL configuration for the Tourist Place Recommendation project.  |
| [settings.py](https://github.com/shravan-7/TRP/blob/master/Tourist_Place_Recommendation/Tourist_Place_recommendation/settings.py) | Django settings for the Tourist Place Recommendation project.    |

</details>

<details closed><summary>Tourist_Place_Recommendation.Tourist_App</summary>

| File                                                                                                                     | Summary                                                                              |
| ------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ |
| [admin.py](https://github.com/shravan-7/TRP/blob/master/Tourist_Place_Recommendation/Tourist_App/admin.py)               | Django admin configuration for the Tourist_App models.                               |
| [apps.py](https://github.com/shravan-7/TRP/blob/master/Tourist_Place_Recommendation/Tourist_App/apps.py)                 | Django app configuration for the Tourist_App.                                        |
| [rawQuery.py](https://github.com/shravan-7/TRP/blob/master/Tourist_Place_Recommendation/Tourist_App/rawQuery.py)         | Module for executing raw SQL queries for the recommendation system.                  |
| [recommend.py](https://github.com/shravan-7/TRP/blob/master/Tourist_Place_Recommendation/Tourist_App/recommend.py)       | Implementation of the recommendation algorithm for tourist places.                   |
| [views.py](https://github.com/shravan-7/TRP/blob/master/Tourist_Place_Recommendation/Tourist_App/views.py)               | Django views for handling user requests and rendering responses.                     |
| [read_dataset.py](https://github.com/shravan-7/TRP/blob/master/Tourist_Place_Recommendation/Tourist_App/read_dataset.py) | Module for reading and processing the dataset used for recommendations.              |
| [models.py](https://github.com/shravan-7/TRP/blob/master/Tourist_Place_Recommendation/Tourist_App/models.py)             | Django models defining the database schema for the Tourist Place Recommendation app. |

</details>

<details closed><summary>Tourist_Place_Recommendation.Tourist_App.migrations</summary>

| File                                                                                                                                                        | Summary                                                           |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| [0001_initial.py](https://github.com/shravan-7/TRP/blob/master/Tourist_Place_Recommendation/Tourist_App/migrations/0001_initial.py)                         | Initial database migration for creating the necessary tables.     |
| [0002_user_location_prefs.py](https://github.com/shravan-7/TRP/blob/master/Tourist_Place_Recommendation/Tourist_App/migrations/0002_user_location_prefs.py) | Migration for adding user location preferences to the User model. |

</details>
<hr>

## 🚀 Getting Started

**_Requirements_**

Ensure you have the following dependencies installed on your system:

-   **Python**: `version 3.x`
-   **Django**: `version 3.x`

### ⚙️ Installation

1. **Clone the Repository**:

    ```sh
    git clone https://github.com/shravan-7/TRP.git
    cd TRP
    ```

2. **Create a Virtual Environment**:

    ```sh
    python -m venv venv
    source venv/bin/activate
    ```

3. **Install Dependencies**:

    ```sh
    pip install -r requirements.txt
    ```

### 🤖 Running TRP

1. **Apply Migrations**:

    ```sh
    python manage.py migrate
    ```

2. **Run the Development Server**:

    ```sh
    python manage.py runserver
    ```

3. **Access the Application**:

    Open your web browser and go to `http://127.0.0.1:8000/`

### 🧪 Tests

1. **Run Tests**:

    ```sh
    python manage.py test
    ```

## 🛠 Project Roadmap

-   Implement user authentication
-   Develop recommendation algorithm
-   Add support for more languages
-   Integrate with external travel APIs
-   Improve UI/UX for mobile devices

## 🤝 Contributing

We welcome contributions to TRP! To contribute, follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Make your changes and commit them: `git commit -m 'Add feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Submit a pull request.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/shravan-7/TRP/blob/main/LICENSE) file for details.

## 👏 Acknowledgments

-   Thanks to the open-source community for the tools and libraries used in this project.
-   Special thanks to all contributors who helped improve the platform.

<p align="center">
	Made with 💖 by Shravan Kumar
</p>
