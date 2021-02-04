# Ship radar simulation
A simple simulation for on-board radar system. Based on the behavior of the surrounding ships, a risk assessment model is proposed to assess the chance of being attacked by pirate ship.

## How it looks

![alt tag](https://github.com/ngocjr7/ship-radar-simulation/blob/master/demo.png?raw=true)

## How to run

### Requirements
```sh
pip install -r requirements.txt
```

### Run

```sh
python src/radar.py
```

## Risk assessment model

There are many factors affecting pirates' decision to attack including ship's type, ship's size, ship's flag, ship's current location, current date, time,...

We proposed a simple regression model to assess the risk score of a particular ship operating in an area.

* Dataset: Past pirate attacks (crawled from GISIS (IMO))
* Model: Logistic regression
* Input: A ship and its current information
* Output: A chance of being attacked

<!-- Drawback
* The model do not use lat, lon so far. Only use ocean area and place.

* The above model cannot capture the current circumstances of the ship. For example, the situation in which three ships approach us is more at risk than no one around. 

Then I add a simple `sigmoid` function with hand-tuned weight to capture the both number of suspicious ships around us with current risky from the previous risk assessment model. 

In the real-life application, we can deploy this system and collect datasets from the operating ships to improve this model. From the collected data, we can analyze more closely the behavioral features of the surrounding ships like the direction of the ship (stable or keep towards us or forestalling us). Theretofore, we can integrate both features of past attacks and the current circumstances into a single risk assessment model. -->
