#Projected Progress Timeline#

This is an addendum to the the literature review (Part B). It adds a little more detail regarding implementation plans. Most of the logic-related code will be written in Python, although Java may be used for the GUI. This is mainly because this project will make use of classifiers and matrices, and Python has handy libraries for these sorts of things.

* April 3: Initialization 
    - Each agent should be implemented as a class.
    - A simple GUI representing the cellular nature of the environment should be constructed.
    - Agents should be represented in a cellular automata GUI, although their behavior at this point may not mean anything. They should move randomly although they may not obey restrictions imposed by the environment (e.g., whales may swim on land at this point).
* April 10: Lay of the Land (and Ocean)
    - Environmental factors (e.g., icebergs, smells, beaches) should be fully implemented at this point.
    - Agents should obey their restrictions imposed upon them upon the environment (e.g., whales lose the ability to walk on land :()
    - Agents should be "aware" of their environment and learning from it. When I say "aware", I mean they should be observing environmental variables and transforming them into features. 
    - The whales agents should be able to communicate with one another.
* April 17: Running the Simulation
    - If something has not been completed yet, it should be now.
    - Various parameters should be tuned and evaluated.
    - A kickass GUI should be included. There should be options for changing various parameters (e.g., seal hearing range, number of orcas, etc.).
    - Some sort of report with figures and such should be generated each time the simulation is run.

