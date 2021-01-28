# Master Thesis Resources
This is the resource repository to provide the source code, the dataset, and the result for the master thesis: 

Deep Reinforcement Learning in Forex Trading Using Metrics
HARUGUHCI Takuma

# Initial setting the environment

  $ python -m venv venv
  $ source venv/bin/activate
  $ pip install -r requirements.txt

# How to run for each setting
## 1. Change the current directory
  $ source venv/bin/activate
  $ cd src

## 2. Overwrite main.py from result_MA direcotry you want to run

E.g.

  $ cp ./result_MA3/main.py .

## 3. Run the experiment

  $ ./experiment.sh

or

  $ python main.py
