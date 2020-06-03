HOSPITALAID [![HospitalAid](https://circleci.com/gh/HospitalAid/hospitalaid.svg?style=svg)](https://circleci.com/gh/HospitalAid/hospitalaid)
===

HospitalAid is an online forum for hospitals for requesting aids, and for people/organizations to offer help.


Install
---

- Install Python on your machine (at least 3.7).
- Install Pipenv - https://pipenv.readthedocs.io/en/latest/install/
- Install Git and clone this project locally.
- Run `cp .env.template .env`
- Run `pipenv shell`
- Run `pipenv sync --dev` to update dependencies
- Run `pre-commit install` to install precommit hooks
- Run `honcho -f Procfile.dev start`
- Open the browser at `http://localhost:8000/`

After having done this once, you can follow the abbreviated steps below


Run when installed
---

- Run `pipenv shell`
- Run `pipenv sync --dev` to update dependencies
- Run `honcho -f Procfile.dev start`
- Open the browser at `http://localhost:8000/`


Contributing
---

First of all, thanks for the interest! HospitalAid is a young project, and it needs your help on many fronts. The project is using Django. Django is very well-documented, familiarize yourself with it if you fancy contributing code.

Please check the issues page if you want to see what needs doing. Issues labelled "good first issue" are easy to do for anyone not yet familiar with the project.

For any contribution, please submit your code through a pull request. Try not to contribute code that breaks existing functionality. Commit automated tests if you can. Please discuss any major changes first with the contributors.

Format all code using isort and Black (python code formatters)


Areas of contribution that are welcome
---

- automated tests (integration/unit tests)
- convert designs to HTML/CSS
- research similar tech projects and see if we can reuse data/ideas/code
