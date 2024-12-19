# KyotoU-Python
Soon it will be time: Early elections are scheduled for February in Germany. The current 
period is marked by crises in the European region and dissatisfaction with the last coalition. In 
such uncertain times, it would be irresponsible to leave the election campaign solely in the 
hands of politicians. That’s why we’ve decided to develop a turn-based election campaign game 
in tKinter. This game will allow players to choose the leading candidate of one of the major 
parties (CDU, AfD, SPD, Greens, BSW, FDP, and Left Party) and dive into the campaign. The goal 
is to gather as many votes as possible to ultimately become the Chancellor of the Federal 
Republic of Germany. 
How will the game work? 
At the start, the player selects the leading candidate they trust the most (or, alternatively, the 
one they despise the most). Each leading candidate has a two-digit value in each of the three 
metrics: popularity, competence, and ambition. Additionally, the corresponding party begins 
with approval ratings based on current polling data (at the time of the game’s creation). In other 
words, there are effectively varying difficulty levels. Regarding the GUI, we will aim to keep it in a 
retro style. For the starting screen, we will include retro-style photos of the politicians, as well as 
labels and buttons for selection. 
Then, the campaign begins. As mentioned, it is a turn-based game. The current plan is to give 
players the opportunity to select specific actions during, for example, 10 rounds (e.g., campaign 
events, social media advertising, debates, flyers & giveaways, or fundraising). Furthermore, each 
party will have special actions that can only be used once. Depending on the politician’s stats 
(popularity, competence, and ambition) and a bit of randomness, poll numbers will shift either in 
their favor or against them. Both the aforementioned metrics and the current poll numbers for all 
parties can be viewed by the player at any time. However, the outcome of the selected action will 
not be known in advance. 
To make the gameplay more dynamic, we also plan to implement an event system. In addition to 
the 10 action rounds, random events will occur with a certain probability. Here, we aim to 
include at least one party-specific event in addition to general events. An event will describe a 
specific situation, such as a flop during a TV debate, and offer the player several choices of 
action. Depending on the player’s decision, the politician's stats for popularity, competence and 
ambition will change.  
For both actions and events, we will primarily use labels, buttons, and photos. To visualize voter 
shifts, for example, we will likely dynamically update the text on labels. If necessary, we might 
also work with message boxes or other widgets. 
After the 10 action rounds and several events, it’s time to cross your fingers. Can the chosen 
candidate become the next Chancellor of the Federal Republic of Germany? 
Our aim is to keep the game somewhat satirical and avoid reflecting our own political opinions. 
Ultimately, every party should be playable to some extent. Regarding the exact implementation, 
the outlined concept is not set in stone. We may need to make adjustments for pragmatic 
reasons. 
We plan to program the game in German, as this feels more natural and allows for wordplay, 
humor, etc. However, our presentation will be in English, and if necessary, we’ll translate certain 
parts for presentation purposes to ensure that all students understand our concept and 
implementation.
