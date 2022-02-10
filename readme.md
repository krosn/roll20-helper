# Using virtual environment
## Creation
The standard way to create an environment is 'python3 -m venv {path}'.
I used 'venv' as the path by specifying './venv'
## Activation
Activate with 'source {path}/bin/activate'
> Remember to 'pip install -r requirements.txt'
## Deactivation
'deactivate'

# Run locally
`uvicorn main:app --reload`

# Deployment
This project is integrated with [Heroku](https://dashboard.heroku.com/apps/roll20-helper).
The Procfile describes how to start the service.

# References
- [FastAPI](https://fastapi.tiangolo.com/) for Python API
- [fetch](https://javascript.info/fetch) for JS requests