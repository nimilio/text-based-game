import sys
import pandas as pd

class Program:
    def __init__(self, file_name = "gameConfiguration.txt"):
        self.file_name = file_name
        
    
    def blank(self):
        with open(self.file_name,"r") as f_in:
            content = ""
            for line in f_in:
                if not line.startswith("#"): #ignore lines with #
                    content += line
        lines = content.replace("\n\n"," ") #ignore empty lines
        new_lines = lines.split("\n")
        return new_lines

    def door_info(self):
        all_doors = []
        status = ""
        room1 = ""
        room2 = ""
        cardinal1 = ""
        cardinal2 = ""
        content = self.blank()
        for tokens in content:
            if tokens.startswith("door"):
                all_doors.append(tokens.split(" "))
        for empty in all_doors:
            if "" in empty:
                empty.remove("")
        return all_doors


    def all_cardinals(self):
        cardinals_list = []
        content = self.door_info()
        for door_cardinal in content:
            for card in (door_cardinal[1].split("-")):
                if card not in cardinals_list:
                    cardinals_list.append(card)
        return cardinals_list

    def start_room(self):
        content = self.blank()
        for tokens in content:
            if tokens.startswith("start"):
                begin = tokens[6:]
        return begin

    def items(self):
        content = self.blank()
        my_list = []
        for tokens in content:
            if "item " in tokens:
                my_list.append(tokens)
        df = pd.DataFrame([sub.split(" ") for sub in my_list])
        df.drop(df.columns[[0]], axis=1, inplace=True)
        df.columns = ['Item', 'Room', 'Type', 'Action']
        return df



class First(Program):


    play_room = [Program().start_room()] #start room, changes throughout the game
    previous = [] # the previous room
    previous_status = [] # the status in which we left the previous door
    previous_original_status = [] # the first status of the door, like in the specification file
    previous_cardinal = [] # the cardinal of the previous door
    


    def intel(self): # this method contains a small storytelling and is executed once
        print("Welcome to the house game!\nIt's Wednesday evening.\nYour favourite band is at last in town for one show only and you are in no way going to miss that.\nThe band plays at 21.30 in a small local nightclub (no COVID situation currently).\nAs a teenager though, you are not allowed to stay out late on weekdays; but this shall not stop you.\nYou say goodnight to your parents and pretend to go to bed due to an early school examination the following morning.\nIn the living room, there is a key case holding everyone's keychains,\nso you only take the single key from your keychain that opens the main door, so as not to arouse suspicion.\nYou manage to leave the house secretly. You make it to the club at 22.30 and return home at around 1 am.\nBut the key is not in your pocket anymore! You probably lost it while you were having fun.\nIt seems though that your parents are still awake,\nso you could not enter from the main entrance without being noticed either way.\nYour bedroom is on the second floor. Find a way to make it to your room without being noticed!\n")
        input("Press Enter to continue...")
        print ("You are in the Garden\nThere are door(s) towards Main1,W\nPlease type commands in order to play game!")
        print ("\n\nTip!!!\nYou can change the status of the previous door with 'DIR + !', unless stated otherwise")


class Commands:
    def __init__(self):
        self.commands = {
        "go DIR:\t\t" : "Move to the room in direction DIR, if there is an open door in that direction",
        "take ITEM:\t" : "Take the item ITEM if it is in the same room",
        "release ITEM:\t" : "Release item ITEM, if it is being held",
        "open DIR:\t" : "Opens the door in direction DIR in the current room, if there is such a door, and if that door is closed",
        "close DIR:\t" : "Closes the door in direction DIR in the current room, if door is open",
        "unlock DIR:\t" : "Unlocks the door in direction DIR in the current room, if door is locked",
        "lock DIR:\t" : "Locks the door in direction DIR in the current room, if door is locked and key is held",
        "keycode DIR:\t" : "Unlock door using keycode in direction DIR",
        "open ITEM:\t" : "Open an item",
        "close ITEM:\t" : "Close an item",
        "enter ITEM:\t" : "Get in the item",
        "exit ITEM:\t" : "Get out of the item",
        "search ITEM\t" : "Search an item",
        "drink ITEM:\t" : "Drink item for energy",
        "hear ITEM:\t" : "Hear any noise",
        "show:\t\t" : "Room description",
        "commands:\t" : "All available commands in the game",
        "holding:\t" : "The items the player is currently holding",
        "quit:\t\t" : "Ends the game"
        }
        


    def print_com(self):
        for k, v in self.commands.items():
            print (k,v)
        print ("\nNot all commands are applicable to every room.")


    def dir(self): #create a list of the cardinals
        self.room_commands = []
        for key in self.commands.keys():
            if "DIR" in key:
                self.room_commands.append(key.split(' ')[0])
        return self.room_commands


class Exit:
    def __init__(self):
        print ("Thanks for playing, see you soon!")
        sys.exit(0) # zero is considered “successful termination”


class Inventory:
    items = []
        
    def add_item(self,item): # add an item to the inventory
        Inventory.items.append(item)

    def remove_item(self,item): #remove item from the inventory
        if item in Inventory.items:
            Inventory.items.remove(item)
            print ("You do not hold the " + item +" anymore") # item released
            Items().release_room(item)
        else:
            print ("You don't hold that item to release") # item not in inventory

    def prints(self): # print the inventory when requested
        if not Inventory.items:
            print ("You don't hold anything")
        else:
            for i in Inventory.items:
                print (i)


class Information(First): 

    def __init__(self): 
        self.present_room = First().play_room[-1] # the room the player is currently in


    def print_info(self):

        door_string = ""
        for door in Program().door_info(): # this loop retireves information of the current room
            if self.present_room == door[3]:
                if door_string == "":
                    door_string = door[1].split("-")[0]
                else:
                    door_string += "," + door[1].split("-")[0]

        if not door_string: 
            for door in Program().door_info(): # same loop function but to return to previous room
                if self.present_room == door[4] and First().previous[-1] == door[3]:
                    if door_string == "":
                        door_string = door[1].split("-")[1]
                    else:
                        door_string += "," + door[1].split("-")[1]


        if self.present_room == "Bedroom":
            print ("\n\n\nHurraaaaay! You made it!\nThanks for playing, see you next time!")
            sys.exit(0)
        if self.present_room == "Hall":
            print ("SECOND FLOOR")

        print ("\nYou are in the " + self.present_room + "\nHere are the door(s) " + door_string)


        df = Program().items() 
        df_items = df.loc[df['Room'] == self.present_room] # keep only the items of the current room
        items_to_list = df_items['Item'].tolist() # turn dataframe column to list
        if items_to_list:
            item_string = "" 
            for item in items_to_list:
                item_string += item+"\n"
            print ("\nHere are the following items\n" + item_string )

        if self.present_room == "Living_room":
            print ("Your dad smokes a cigarette in the balcony. No clue of your mom. Quickly, go upstairs.")
        elif self.present_room == "Attic":
            print ("\nSomeone is coming in the attic, you need to hide somewhere!")
        elif self.present_room == "Parent's_bedroom":
            print ("This is your parent's bedroom. Fortunately, nobody is here.")
        elif self.present_room ==  "Bathroom":
            print ("Your mother was here a few minutes ago. Lucky you.")

        
        


class Items(Inventory): #This class handles the items based on their features
    
    key_found = [1]
    empty_glass = [1]
    heared = [1]
    used_trunk = [1]
    toolbox = [1]
    df = Program().items()

    def __init__(self):
        self.items_room = First().play_room[-1]

    
    def categorization(self,answer):
        self.answer = answer.split(" ")
        in_room = ((self.df['Room'] == self.items_room) & (self.df['Item'] == self.answer[1])).any() 
        # assure an item is in the same room, otherwise we cannot move on in this method 
        
        if in_room: 
            stationary_bool = ((self.df['Item'] == self.answer[1]) & (self.df['Type'] == "STATIONARY")).any()
            move_bool = ((self.df['Item'] == self.answer[1]) & (self.df['Type'] == "MOVE")).any()
            use_bool = ((self.df['Item'] == self.answer[1]) & (self.df['Type'] == "USE")).any()

            if stationary_bool:
                self.stationary()
            elif move_bool:
                self.move()
            elif use_bool:
                self.use()
        else: # if item not in room
            print ("There is not such an item here")



    def release_room(self,item): # release item in a different room
        replaced_value = self.df.loc[self.df['Item'] == item, 'Room'].any() #find the room where the item originally belonged
        if replaced_value != self.items_room:
            self.df['Room'] = self.df['Room'].replace([replaced_value],self.items_room) #replace room with current



    def stationary(self):
        in_item = False
        action_item = ((self.df['Room'] == self.items_room) & self.df['Action'].str.contains(self.answer[0])).any()
        if action_item and self.answer[0] == "enter": # go in the item
            if not in_item: # if I am out of the item
                print ("You are in the " + self.answer[1])
                self.used_trunk[-1] = 0
                in_item = True
                while in_item:
                    item_answer = input(">")
                    if item_answer == "quit": 
                        Exit.__init__(self)
                    elif item_answer == "enter " + self.answer[1]:
                        print ("You are already in the " + self.answer[1])
                    elif item_answer != "exit " + self.answer[1]:
                        print ("You have to get out of the trunk first or wrong command")
                    elif item_answer == "exit " + self.answer[1]:
                        print ("You are out of the " + self.answer[1] + ". The danger has passed")
                        in_item = False
        elif action_item and self.answer[0] == "exit":
                print ("You are out of the " + self.answer[1])
        else:
            print ("You cannot " + self.answer[0] +" "+ self.answer[1] + " or no such command")

 
    def move(self):
        if self.answer[0] == 'take':
            if self.answer[1] not in Inventory().items:
                self.add_item(self.answer[1]) # add item in inventory
                print ("You took " + self.answer[1])
            else:
                print ("You already carry the " + self.answer[1])
        else:
            print ("No such command for this item")


    def use(self):
        
        if self.answer[0] == "take":
            if self.answer[1] not in Inventory().items:
                if self.answer[1] == "key" and self.key_found[-1] == 1:
                    print ("You need to find it first")
                elif self.answer[1] == "toolbox" and "ladder" not in Inventory().items:
                    print ("The " + self.answer[1] + " is high. You need something to reach it")
                else:
                    self.add_item(self.answer[1]) 
                    print ("You took the " + self.answer[1])
            else:
                print ("You already carry the " + self.answer[1])
        elif self.answer[0] == "search" and self.answer[1] == "pot":
            if self.key_found[-1] == 1:
                print ("You found the key!")
                self.key_found[-1] = 0
            else:
                print ("You already found the key")
        elif self.answer[0] == "search" and self.answer[1] == "toolbox":
            if "ladder" not in Inventory().items:
                print ("The " + self.answer[1] + "is high. You need something to reach it")
            else:
                print ("There is nothing here!")
        elif self.answer[0] == "drink" and self.answer[1] == "glass":
            if "glass" not in Inventory().items:
                print ("You don't carry the glass")
            elif "glass" in Inventory().items:
                if self.empty_glass[-1] == 1:
                    print ("You are not thirsty anymore! Now use the glass on the wall to hear any noises.")
                    self.empty_glass[-1] = 0
                else:
                    print ("The glass is already empty")
        elif self.answer[0] == "hear" and self.answer[1] == "glass":
            if self.empty_glass[-1] == 0:
                if self.heared[-1] == 1:
                    print ("You hear nothing from the next room. Go on.")
                    self.heared[-1] = 0
                else:
                    print ("You already checked noises, move fast before someone comes.")
            else:
                print ("You need to drink the water first. Aren't you thirsty?")
        else:
            print ("Wrong command")



class Doors(Items,Information,Exit):

    stack_status = [] # the current status, it changes through gameplay


    def __init__(self, answer, cardinal1, cardinal2, room1, room2, status):

        self.cardinal1 = cardinal1
        self.cardinal2 = cardinal2
        self.room1 = room1
        self.room2 = room2
        self.room_answer = answer 
        self.status = status

        if not Doors.stack_status or Doors.stack_status[-1] == "sealed": 
            Doors.stack_status.append(self.status)


        if self.previous_original_status and self.previous_status: # check if stacks are empty
            self.previous_original_status = First().previous_original_status[-1] 
            self.previous_status = First().previous_status[-1] # in what status we left the previosu door

        self.business = False # before we leave some rooms, things need to be done


        # Categorize commands to methods
        if "go" == self.room_answer.split(" ")[0] and  self.room_answer.split(" ")[1] == self.cardinal1:
            self.go() 
        elif First().previous_cardinal and First().previous and First().previous[-1] == "Hall": #check if empty
            if First().previous_cardinal[-1] == self.room_answer.split(" ")[1] :
                self.return_room()
        elif "open" == self.room_answer.split(" ")[0] and  self.room_answer.split(" ")[1] == self.cardinal1:
            self.open()
        elif "unlock" == self.room_answer.split(" ")[0] and  self.room_answer.split(" ")[1] == self.cardinal1:
            self.unlock()
        elif "keycode" == self.room_answer.split(" ")[0] and  self.room_answer.split(" ")[1] == self.cardinal1:
            self.code_unlock()
        elif self.room_answer == "close " + First().previous_cardinal[-1]: #this command concerns the status of the previous door
            self.close()
        elif self.room_answer == "lock " + First().previous_cardinal[-1]:  #it should be left as found before leaving the current room
            self.lock()
        elif self.room_answer == "keycode " + First().previous_cardinal[-1]:
            self.lock()
        else:
            print ("Wrong command")


    def go(self):
        
        if not First().previous_status: # This runs only once, to go from Garden to Garage and never again
            self.business = True
        elif Doors.stack_status[-1] == "open":
            if First().previous_original_status[-1] != First().previous_status[-1]:
                print ("Before you leave this room, you must leave the previous door in the status you found it: " + First().previous_original_status[-1] + " " + First().previous_cardinal[-1])  
            elif First().previous_original_status[-1] == First().previous_status[-1]:
                if self.room1 == "Basement" and "shoes" in Inventory().items:
                    self.business = True
                elif self.room1 == "Basement" and "shoes" not in Inventory().items:
                    print ("Take off your shoes before leaving to keep it quiet")
                elif self.room1 == "Garage" and "key" not in Inventory().items:
                    print ("Don't leave the key here, you will have to lock the door again")
                else:
                    self.business = True
        else:
            if  Doors.stack_status[-1] == "sealed":
                print ("This is the main door. It is locked and you have lost the key. Go for the other door.")
            else:
                print ("This door is locked or closed.")

        if self.business:

            if Doors.stack_status[-1] == "keycode":
                print ("The door is locked") 
            elif Doors.stack_status[-1] == "locked":
                print ("The door is locked")
            elif Doors.stack_status[-1] == "sealed":
                print ("This is the main door. It is locked and you have lost the key. Go for the other door.")
            elif Doors.stack_status[-1] == "open": #change room
                First().previous.append(self.room1)
                First().play_room.append(self.room2)
                First().previous_cardinal.append(self.cardinal2 + "!") # ! convention to avoid cardinal name overlap
                First().previous_status.append("open")
                First().previous_original_status.append(self.status)
                self.business = False
                Doors.stack_status.clear()
                Information().print_info()
            elif Doors.stack_status[-1] == "unlocked":
                print ("The door is unlocked, but still closed.")
            elif Doors.stack_status[-1] == "sealed":
                print ("This is the main door. It is locked and you have lost the key. Go for the other door.")
            

    def open(self):
        if Doors.stack_status[-1] == "unlocked":
            if self.room1 == "Kitchen" and Items().heared[-1] == 1:
                print ("You need to check (hear) first if there is any noise coming from the next room. Use the glass!")
            elif self.room1 == "Kitchen" and Items().heared[-1] == 0:
                Doors.stack_status[-1] = "open"
                print ("You opened the door")
            else:
                print ("Door is open")
                Doors.stack_status[-1] = "open"
        elif Doors.stack_status[-1] == "open":
            print ("The door is already open")
        elif Doors.stack_status[-1] == "locked" or Doors.stack_status[-1] == "keycode":
                print ("The door is locked")
        elif Doors.stack_status[-1] == "sealed":
            print ("This is the main door. It is locked and you have lost the key. Go for the other door.")


    def unlock(self):
        if Doors.stack_status[-1] == "locked":
            if "key" in Inventory().items:
                Doors.stack_status[-1] = "unlocked"
                print ("You unlocked the door")
            else:
                print ("You need to find and take the key first")
        elif Doors.stack_status[-1] == "open":
            print ("The door is already open")
        elif Doors.stack_status[-1] == "unlocked":
            print ("The door is already unlocked but closed")
        elif Doors.stack_status[-1] == "keycode":
            print ("This door is locked with a code, not a key")
        elif Doors.stack_status[-1] == "sealed":
            print ("This is the main door. It is locked and you have lost the key. Go for the other door.")


    def code_unlock(self):
        if Doors.stack_status[-1] == "open":
            print ("The door is already open")
        elif Doors.stack_status[-1] == "keycode": #locked with code
            print ("The door is locked with a key code: a four-digit number of the year you were born (you are 15). Insert code:")
            date = input(">")
            while date != "2006":
                print ("Wrong code, try again")
                date = input(">")
                if date == "quit": 
                    Exit.__init__(self)
            if date == "2006":
                print ("Door is unlocked.")
                Doors.stack_status[-1] = "unlocked"
        elif Doors.stack_status[-1] == "locked":
            print ("The door is locked, but with a key")
        elif Doors.stack_status[-1] == "unlocked":
            print ("The door is already unlocked. Just open it.")
        elif Doors.stack_status[-1] == "sealed":
            print ("This is the main door. It is locked and you have lost the key. Go for the other door.")


    def lock(self):
        if not self.business:
            if First().previous_status[-1] == "locked" or First().previous_status[-1] == "keycode":
                print ("The door is already locked")
            elif First().previous_status[-1] == "open":
                print ("The door is still open")
            elif First().previous_status[-1] == "unlocked":
                if First().previous_original_status[-1] == "locked" and "key" not in Inventory().items:
                    print ("You don't hold the key")
                elif First().previous_original_status[-1] == "locked" and "key" in Inventory().items:
                    First().previous_status[-1] = "locked"
                    print ("You locked the door")
                elif First().previous_original_status[-1] == "keycode":
                    First().previous_status[-1] = "keycode"
                    print ("You locked the door")
                elif First().previous_original_status[-1] == "unlocked":
                    print ("This door was not locked when you entered")


    def close(self):
        if not self.business:
            if First().previous_status[-1] == "locked" or First().previous_status[-1] == "keycode":
                print ("This door is locked")
            elif First().previous_status[-1] == "unlocked":
                print ("This door is already closed")
            elif First().previous_status[-1] == 'open':
                First().previous_status[-1] = "unlocked"
                print ("You closed the door")
        else:
            print ("You don't have to close that door or it's already closed")


    def return_room(self): # for rooms in which the only way to leave, is to go back, door is always unlocked (closed)

        safe = False
        if self.room1 == "Attic":
            if Items().used_trunk[-1] == 1:
                print ("Someone is coming in the attic, you need to hide somewhere!")
            elif Items().used_trunk[-1] == 0:
                safe = True
        elif self.room_answer.split(" ")[0] == "go":
                safe = True
        else:
            print ("Don't stall! Just leave right away!")
        if safe:
            First().previous.append(self.room1)
            First().play_room.append(self.room2)
            First().previous_cardinal.append(self.cardinal2) #! convention to avoid cardinal name overlap
            First().previous_status.append("open")
            First().previous_original_status.append(self.status)
            Doors.stack_status.clear()
            Information().print_info()



class Gameplay(Commands,Doors):

    def __init__(self):
        play = True
        cardinals = Program().all_cardinals()
        card_convention = [i+"!" for i in cardinals]
        direction_commands = Commands().dir()
        while play:
            current_room = First().play_room[-1]
            if current_room == "Bedroom":
                play = False
            answer = input(">")
            split_answer = answer.split(" ")
            if answer == "commands": 
                Commands().print_com()
            elif answer == "quit": 
                Exit.__init__(self)
            elif answer == "holding": 
                Inventory.prints(self)
            elif answer == "show":
                Information().print_info() 
            elif answer.startswith("take"): 
                Items().categorization(answer)
            elif answer.startswith("release"): 
                Inventory.remove_item(self,split_answer[1]) 
            elif answer == ("enter trunk"): 
                Items().categorization(answer)
            elif answer == ("exit trunk"): 
                Items().categorization(answer)
            elif answer.startswith("search"): 
                Items().categorization(answer)
            elif answer.startswith("drink"): 
                Items().categorization(answer)
            elif answer.startswith("hear"): 
                Items().categorization(answer)
            elif split_answer[0] in direction_commands and split_answer[1] in cardinals:
                correct_room = False
                # This loop handles the information related with the current room with a cardinal command
                for door in Program().door_info(): # for every list in the all_doors list
                    if current_room == door[3] and split_answer[1] == door[1].split("-")[0]:
                        correct_room = True
                        Doors(answer, door[1].split("-")[0], door[1].split("-")[1], door[3], door[4], door[2])
                if not correct_room: 
                    if current_room == door[4] and First().previous[-1] == door[3]:
                        correct_room = True
                        Doors(answer, door[1].split("-")[1], door[1].split("-")[0], door[4], door[3], door[2])
                if not correct_room:
                    print ("Wrong cardinal or something is weird!")
                else:
                    correct_room = False

                # This loop handles the information related with the current room with a cardinal convention    
            elif split_answer[0] in direction_commands and split_answer[1] in card_convention:
                correct_room = False
                try: # in case the previous_cardinal stack is empty
                    for door in Program().door_info(): # for every list in the all_doors list
                        if current_room == door[3] and split_answer[1] == First().previous_cardinal[-1]:
                            correct_room = True
                            Doors(answer, door[1].split("-")[0], door[1].split("-")[1], door[3], door[4], door[2])
                    if not correct_room:
                        for door in Program().door_info(): # for every list in the all_doors list
                            if current_room == door[4] and First().previous[-1] == door[3]:
                                correct_room = True
                                Doors(answer, door[1].split("-")[1], door[1].split("-")[0], door[4], door[3], door[2])
                    if not correct_room:
                        print ("Wrong cardinal or something is weird!!")
                    else:
                        correct_room = False
                except:
                    print ("Wrong cardinal")
                    pass
            else:
                print ("Wrong command.")
        




def Main():
    if sys.argv[1] == "gameConfiguration.txt":
        first = First()
        first.intel()
        gameplay = Gameplay()
        gameplay    
    else:
        sys.exit(1)

if __name__ == '__main__':
    Main()
