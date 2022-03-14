# text-based-game
Fun in object oriented game


This text-based game follows its own storyline. It consists of 10 rooms (with doors) and 8 objects. The doors are either open, closed, locked, sealed or locked with code. The script is a little bit long because there are many details that need to be handled and I thought what would make the game easy to follow would be to foresee an answer for any type of the user’s input. The design is rather complicated as well; The script consists of 9 classes:

Class Program: retrieves the information from the Gameconfiguration file
Class First: print the start information and keeps track of rooms and cardinals 
Class Commands: prints commands and retrieves cardinals
Class Exit: exits game
Class Inventory: player’s inventory, includes what the user holds, takes or releases 
Class Information: prints information when we enter a room or when requested 
Class Items: handles items based on their features and on item commands
Class Doors: handles rooms, doors and their status based on direction commands 
Class Gameplay: handles user’s input which leads to the corresponding class
Main function: instantiates the game from terminal

Program/Commands/Exit/Inventory inherit no information from the other classes. There are some classes as well without constructors, because they were not needed (Python creates those automatically if not exist). Building the code was rather demanding because there was a great association between the commands and the storyline. Apart from basics, I should also take into consideration that:

• When leaving a room, the player should leave the previous door in the way he found it (e.g., if the previous door was closed, he should close it before leaving the room). In some rooms, the only way for the user to leave is to go back to the door where he came from. Thus, I created some conventional cardinals (like “S!”, “N!” etc.) in order to avoid overlaps between the basic cardinals.
• When releasing an item, then it should be located in the room where released, and not in the room mentioned in the specification file.
• The player cannot leave some rooms without fulfilling the room “mission”, like finding a key or hiding somewhere.

Apart from the pre-defined actions, the extra commands used for this game are: enter-exit(item), drink-hear(item), search(item), close(DIR),unlock(DIR) and keycode(DIR).
In order to keep track of rooms, cardinals and status, I tried to follow the notion of linked lists, but implement that on stack to avoid time complexity. Initially, I used a stack in which I kept adding the new status of the door (open, locked etc.) every time it was changed, since I only needed to access the last element and never loop through it. The stack is cleared when the room changes. I ended up though creating stacks in order to keep track of: the current room, the previous room, the previous door, the original status of the door (txt) and the last status of the previous door. The reason for that is the greatest difficulty I encountered: overriding. Instead of these stacks, I wanted to use simple strings to include that information, but for some reason, although the string (and Boolean) variables were updated, they never maintained the information every time I re-entered the class through the Gameplay, even if positioned outside the constructor. Concerning time complexity though, I feel the result is the same since I always make use of the last element. Simple lists are only used to store information from the configuration file. A hash table (dictionary) stores the commands of the game. I used that and not a simple string because apart from printing the dictionary whenever requested, I also had to extract the cardinals of the game (easier than doing that from the txt lines). Finally, I created a data frame to store the items with their features. In this way, I could avoid “if statements” when comparing items, rooms, action etc. because such comparisons are treated as Boolean Statements in data frame and it would be easier to categorize items based on their type.
Initially, I created a class for each room and included the corresponding commands. I realized though that I was being repetitive, which is definitely not desired in programming, resulting to a very long code. The final version of the script is slightly and rarely repetitive and only when it was not possible to avoid. I am pretty satisfied with the script, in the way classes “cooperate” and commands are handled. At some points, the script includes game information accessed manually and not from the configuration file, although it is avoided as much as possible. If that improved, I believe the script could be a little bit shorter. A demanding assignment, that for sure highly assisted me in improving my programming skills, especially when it comes to object oriented.


Tips!
• There is a code needed at some point. This is "2006".
• If a door is "locked", the user has to unlock it, open it and the move on.
• If a door is "unlocked" it means that it’s closed, so the user has to open it and move on.
• If a door is open, the user can simply move on.
• Ifthe"DIR"commandsareusedwithacardinalandanerrorisprinted,suchas"Wrongcommand" or "Wrong cardinal" it probably means that the user has to leave the room from the same door he entered. Thus, the conventional cardinals (with "!") need to be used.
