## Hydraulic Line

The hydraulic line feature allows for the user to see the hight mapping of each possible treament line in the scenario.

In the graphic each model is placed on the hight paramter that is set for them. Together with the dimensions of each process the hight changes over the entire process are mapped. 

Additionally supply and discharge pressure in water column height are displayed at inlet/outlet of each unit. 

For pressurized system like reverse osmosis or membrane degassing the required operating pressure is also taken into account. 

Calculation of the pressures at each unit and more importantly at the well pumps is done in 2 steps.

1. Backward move
Starting at the distribution pumps which have a necessary inlet pressure that is required as input parameter inlet and outlet pressure of each treatment step together with the pressure loss of each step. 

2. Forward move 
With this first step we move from the abstraction well pumps forward through each step again.
Based on the calculated pressure of the abstraction pumps we iterate the inlet pressure of the units. At points in the treatment where the outlet is lower than the inlet of the follwoing step an addition pump is placed for the pressure increase requirement. 


# Interaction with the elements
Each unit beside the abstraction pumps can be moved up and down to change the height level of the unit. 
This change will automatically update the corresponding parameter in the design table of the unit. 
Additionally the pressure calculations are updated and a booster pump if necessary due to the changes. 




