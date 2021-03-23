# AdaptiveApplicationsTeamOtter

## Environment set-up

1. `python3 -m venv env`
1. `. env/bin/activate`


## Run the Flask service

1. Download dataset from Kaggle: https://www.kaggle.com/shuyangli94/food-com-recipes-and-user-interactions
    * Copy `RAW_recipes.csv` to the resources folder
    * (`RAW_recipes.csv` is called in `food_api.py`)

1. `python3 service.py`


## Resource files (in resources directory)

* `features.ini` - contains list of possible allergies, cuisines, etc user can select
    * (this is a TODO - want to avoid having these values hard-coded in)
* `stereotypes.ini` - contains the features/attributes of each health goal
* `dataset_info.txt` - contains 2 excerpts from dataset and list of all the possible tags
