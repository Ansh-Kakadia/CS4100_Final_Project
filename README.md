# PROJECT NAME HERE


## Beginner's Guide

To setup this project, take the following steps:

- Navigate to the project directory in your terminal

- Create your virtual environment with the command 
    - `python -m venv venv`

- Activate your virtual environment with one of the 
    - Windows: `.\venv\Scripts\activate`
    - Mac/Linux: `source venv/bin/activate`

- Run the following command in the terminal to install the correct dependencies
    - `pip install -r requirements.txt`

- Then run the `init_dataset.py` file

## General Plan

We plan ao make an AI system that uses Sinulated Annealing (or other local search techniques) to create an outfit from a given article of clothing.

We are using this [Kaggle dataset](https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-small/versions/1?resource=download). 

The system should be split into the following parts:
- A data cleaner, which organizes the data from the data set into a format the search and view can work with
- A search component, which first creates a random outfit with a given article of clothing, then locally searches the outfit space using some outfit huristic
- A view, which shows the initial and final products, and possibly some states in between

