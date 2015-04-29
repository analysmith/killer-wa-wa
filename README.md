# README #
### What is this repository for? ###
* This repository holds code for simulating orca behavior and language!
* v0.1 --> I plan on working on it later. This is only a beginning.... mwahahaha
### How do I get set up? ###
* Please read the project_3_x.pdf files. They help one understand the origins of the project. 
* You'll need Python 2.6 at least to run the code.
* You'll also need some (pretty common) Python libraries:
     - scikit-learn
     - numpy
     - scipy
* If you have trouble running the code, you may want to consider installing [Anaconda](https://store.continuum.io/cshop/anaconda/). It contains a number of Python libraries that are useful for scientific computing, and it's FREE. Should you choose to run this application via Anaconda, you may opt to use the ipython command to run it. Example: ipython simulation.py -- -p 10 -o 5 -d 100 -i 200 -m
### Contribution guidelines ###
No code contributions are being accepted at this time; however, please feel free to comment, nitpick, suggest, or otherwise positively verbally contribute.
### Running the simulation ###
1. Download directory.
2. cd into killer-wa-wa/code/
3. Enter 'python simulation.py' in your terminal.
4. Sit back and watch orcas eat stuff.

Successful orca attacks are indicated by a magenta orb surrounding an orca. You may also notice the prey dots growing smaller after an orca attack. This indicates that the prey is being eaten. Morbid, I know. 

Note: I recommend choosing grid size much larger than the number of animals you are adding to the simulation. There is currently an intermittent index out of bounds error when this is not the case. Still trying to track it down. If you run into this problem, just increase the *--dim* parameter until it goes away.
### Changing parameters ###
Some parameters can be adjusted through command line arguments.

* -o, --orcas [input: Number of orcas][def:10]
* -p, --prey [input: Number of prey][def:5]
* -d, --dim [input: Single int representing length of side of square world][def:100]
* -i, --num_iter [input: Number of time steps][def:200]
* -m, --mammal [indicator: use mammal prey][def:False]

There are some additional parameters in code/action.py which I have yet to create commandline code for. These parameters control the success of each action an orca may take. They are as follows:

* *attack_success_no_sound*: success probabilities of each action assuming no sound made previously.
* *attack_success_sound*: success probabilities of each action after sound has been made while hunting seals.
* *attack_success_soundnfish*: success probabilities of each action after sound has been made while hunting fish.

Some other code handles the conditional nature of using the sound action before other types of actions.

### Who do I talk to? ###
* Ana Smith (gitskippy@gmail.com)
* [Cleverbot](http://www.cleverbot.com/) (I'd take anything it says with a grain of salt though)
### References ###
1. Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. Computing in science and engineering, 9(3), 90-95.

2. Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., ... & Duchesnay, É. (2011). Scikit-learn: Machine learning in Python. The Journal of Machine Learning Research, 12, 2825-2830.

3. Whitney B. Musser, Ann E. Bowles, Dawn M. Grebner, and Jessica L. Crance. Differences in acoustic features of vocalizations produced by killer whales cross-socialized with bottlenose dolphins. The Journal of the Acoustical Society of America, 2014 DOI: 10.1121/1.4893906.

4. Mock, K. J. and J. W. Testa. 2007. An agent-based model of predator-prey relationships between transient killer whales and other marine mammals, University of Alaska Anchorage, Anchorage, AK, May 31, 2007, Available online at http://www.math.uaa.alaska.edu/~orca/. 

5. Riesch, R. and V.B. Deecke. 2011. Whistle communication in mammal-eating killer whales (Orcinus orca): further evidence for acoustic divergence between ecotypes. Behavioral Ecology and Sociobiology, 65(7), 1377-1387.