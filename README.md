# WorldCup ReadMe

# Welcome to the Python World Cup made by samwcounsell and githubkeano.

- This programme uses a binomial simulation to predict the outcome of the World Cup Qualifiers and tournament. 
- Every nations ratings and squads are our choices, so expect some weird outcomes, we don't know as much as we wish we did...

- We hope you enjoy a relatively realistic run through of the 2022 World Cup

## Setup

Install the requirements. We recommend you do this inside a virtual environment:

```bash
# Set up virtual environment using virtualenv
python -m virtualenv .venv
# Or set up virtual environment with python's venv module
python -m venv .venv
# Activate virtual environment [Windows]
.venv\Scripts\activate
# Activate virtual environment [Linux/Mac]
source .venv/bin/activate
# Install requirements
pip install -r requirements.txt
```

## 1.0 The World Cup

Run the `World_Cup_Simulation.py` file, when asked if this is a test we reccomend N the first time, and Y afterwards (this allows skipping most of the qualifiers). For the qualifiers we reccomend setting the time delay to 0, otherwise the simulation will take quite a while.

```bash
cd Python_Files
python World_Cup_Cimulation.py
```

## 2.0 The Dash App:

After running the World Cup, run the `Dash_App.py` file in the other folder, you should see your three custom csv's that have saved and you will be able to use this app to do a deep dive into the intricacies of your personal simulation.

```bash
cd DashApp
python Dash_App.py
```

# Known Issues:
  #1.0 UEFA qualifying uses the nations league, this has not been added yet so we use a second round of group stages to select the final two teams to qualify from UEFA.
  
# Please let us know of any more issues you find, we really appreciate any feedback.
  
