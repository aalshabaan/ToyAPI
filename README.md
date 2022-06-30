# ToyAPI
A toy example of stock management RESTful API done in Flask as a test assignment for a technical interview at Swisscom.

## How to run:

 1. Clone this repository and open a shell in it.
 2. Create a conda environment with the needed dependancies using `conda env create --file environment.yml`. If you don't have conda see [here](https://docs.conda.io/en/latest/miniconda.html).
 3. Activate the new conda environment with `conda activate SwisscomAPI`
 4. start the server using `flask run`. It will start on `http://localhost:5000`

## How to use:
This is an example use

`curl localhost:5000/items` Shows all available items in stock

`curl localhost:5000/orders` Shows all current orders

`curl localhost:5000/items/sim` Shows the item with the name "sim"

`curl localhost:5000/items -X POST -d "name=phone&desc=A flip phone&type=mobile&count=100"` Creates a new item called "phone" of which there are 100 items in stock

`curl localhost:5000/items/phone -X PUT -d "count=40"` Add 40 items to the "phone"'s stock

`curl localhost:5000/orders -X POST -d "order_id=1&contents=sim,phone&content_counts=1,1"` Adds a new order of a phone and a sim card.

`curl localhost:5000/orders/1 -X PUT -d "action=fulfill"` Fulfills the added order 1

`curl localhost:5000/items/phone -X DELETE` Deletes the item `phone`


## Timekeeping:
Part of this assignment is the time limit set to acheive it, report of the time spent building this is available [here](https://app.clockify.me/shared/62b73b0ff1802b420f0c78ef)
