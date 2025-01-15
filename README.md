# KyotoU-Python

## Introduction:

- In February, Germany will hold early elections.
- Due to the current crises in Europe and the chaotic end of the last coalition in Germany, we decided to create a turn-based election campaign game in Python using Tkinter.
- Quick disclaimer: The game is satirical, and we tried our best to keep our own political views out of it and avoided highly controversial topics.
- Although the game is in German (to make it authentic and allow for wordplay), we will explain everything in English so everyone can follow along.
- A quick structure of our presentation:
  - Briefly explain the game.
  - Show that and how it works.
  - Share challenges we faced during development.
  - Conclude with some final thoughts.
________________________________________

## Explanation of the Game and Demo:

- The game is a turn-based election campaign simulator.
- At the start, players choose the leading candidate of one of the major parties (CDU, AfD, SPD, Greens, BSW, FDP, or the Left Party) and dive into the campaign.
- Objective: Gather the most votes to become the Chancellor of Germany or at least be part of the coalition.
________________________________________
- Start Screen:
  - Players can enjoy the view on the German parliament and start the game.
- Candidate Selection:
  - Players can select their candidate here.
  - Each candidate has three stats: popularity, competence, and ambition (all two-digit values).
  - Parties also have initial approval ratings based on real polling data at the time of development. This basically means there are different difficulty levels.
  - The polling data is shown, once the game has started.
- Election Campaign:
  - The campaign lasts 15 weeks/turns (shown by a counter on the bottom right).
  - Players can perform one action per round, choosing from: Campaign events, Social media ads, Debates, Flyers and giveaways, Fundraising.
  - There is a special action that is different for each party. Once used, it disappears.
  - Actions affect poll numbers based on the candidate’s stats and some randomness.
  - Poll numbers and candidate stats are visible at any time, but how the stats influence specific actions is not shown. Players have to find out with reasoning and intuition and also have to be a little bit lucky.
  - As you can see, the poll changes are displayed after each action.
- Dynamic Events
  - To make the gameplay more dynamic, we also implemented an event system.
  - Random satirical events out of our event pool occasionally appear during gameplay.
  - Players must choose from three options.
  - As for the action, depending on the choice and some randomness, the poll numbers shift.
  - These events don’t count toward the 15 rounds.
  - As you can see, the poll changes after an event are also displayed. Only the changes caused by the event choice are displayed, not the changes from the action right before, even though those are also added to the poll scores.
  - After 10 rounds, a special kind of event occurs…
- Endscreen
  - After 15 rounds, an ending screen shows the final poll distribution as well as all possible and the most probable coalition.
  - Furthermore, the next chancellor is shown. It’s always the candidate from the strongest party within the most probable coalition.
________________________________________

## Challenges and Development Highlights

- Collaboration: We used GitHub to work on the project together.
- Initial Issues:
  - We started coding without much structure and struggled with frame transitions.
  - To fix this, we switched to an object-oriented approach.
  - A main class manages the container for all different game pages, and each game page (start screen, candidate selection, action page, event page, ending screen) has its own class.
  - We divided the code into three scripts (basically: main, start, and campaign) to stay organized.
- Technical/Logical Difficulties
  - So many technical/logical difficulties.
  - What we want to show you is the difficulty we had handling some of the calculations behind the scenes, specifically the simulation of the voter shift…
________________________________________

## Conclusion

- This game has infinite potential and could be made way more complex.
- We thought about implementing an election budget system or animations in the beginning, but at some point, we had to stop.
- Overall, we believe that we found a good compromise between complexity and feasibility.
