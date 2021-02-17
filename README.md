# Master Thesis Resources
This is the resource repository to provide materials for the master thesis:  
Deep Reinforcement Learning in Forex Trading Using Metrics  

# Material List
Master Thesis: papers\latex\m5231142.pdf  
Presentation Slides: papers\presentation\m5231142_ThesisPresentation.pptx  
Source Code: src  
Result: src\result_MA*, src\analysis  
Dataset: data  

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

## 4. Analysis the result
$ ./extractTestReward.sh  
$ ./extractWating.sh

# About Citation
Some materials such as the presentation slide and image files may omit indicating the source of reference because the slide is based on the thesis or images comprise the part of the thesis. Note that all references in the repository is concentrated in References section of the thesis as m5231142.pdf.  
