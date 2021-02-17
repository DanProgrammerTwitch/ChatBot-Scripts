#---------------------------
#   Import Libraries
#---------------------------
import os
import sys
import json
import random
from collections import Counter
sys.path.append(os.path.join(os.path.dirname(__file__), "lib")) #point at lib folder for classes / references


import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

# Deal with encoding
import sys
reload(sys)
sys.setdefaultencoding('UTF8')


#   Import your Settings class
from Settings_Module import MySettings
#---------------------------
#   [Required] Script Information
#---------------------------
ScriptName = "Anagram Finder"
Website = "https://www.streamlabs.com"
Description = "!anagram (message) will attempt to find anagrams"
Creator = "Dan White"
Version = "1.0.0.0"



#---------------------------
#   Define Global Variables
#---------------------------
global SettingsFile
SettingsFile = "Services/Scripts/Quote/Settings/settings.json"
global ScriptSettings
ScriptSettings = MySettings(SettingsFile)
ScriptSettings.Command = "!anagram"
ScriptSettings.Cooldown = 10

#---------------------------
#   [Required] Initialize Data (Only called on load)
#---------------------------
def Init():

    #   Create Settings Directory
    directory = os.path.join(os.path.dirname(__file__), "Services\Scripts\Quote\Settings")
    if not os.path.exists(directory):
        os.makedirs(directory)

    #   Load settings
    SettingsFile = os.path.join(os.path.dirname(__file__), "Services\Scripts\Quote\Settings\settings.json")
    ScriptSettings = MySettings(SettingsFile)
    #ScriptSettings.Command = "!quote"
    return

#---------------------------
#   [Required] Execute Data / Process messages
#---------------------------
def Execute(data):

    if data.IsChatMessage() and data.GetParam(0).lower() == ScriptSettings.Command and Parent.IsOnUserCooldown(ScriptName,ScriptSettings.Command,data.User):
        Parent.SendStreamMessage("Time Remaining " + str(Parent.GetUserCooldownDuration(ScriptName,ScriptSettings.Command,data.User)))

    #   Check if the propper command is used, the command is not on cooldown and the user has permission to use the command
    if data.IsChatMessage() and data.GetParam(0).lower() == ScriptSettings.Command and not Parent.IsOnUserCooldown(ScriptName,ScriptSettings.Command,data.User) and Parent.HasPermission(data.User,ScriptSettings.Permission,ScriptSettings.Info):
        Parent.BroadcastWsEvent("EVENT_MINE","{'show':false}")
        Parent.SendStreamMessage(GetAnagrams(data.Message))    # Send your message to chat
        Parent.AddUserCooldown(ScriptName,ScriptSettings.Command,data.User,ScriptSettings.Cooldown)  # Put the command on cooldown

    return


#---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
#---------------------------
def Tick():
    
    return

#---------------------------
#   [Optional] Parse method (Allows you to create your own custom $parameters) 
#---------------------------
def Parse(parseString, userid, username, targetid, targetname, message):
    
    if "$myparameter" in parseString:
        return parseString.replace("$myparameter","I am a cat!")
    
    return parseString

#---------------------------
#   [Optional] Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI)
#---------------------------
def ReloadSettings(jsonData):
    # Execute json reloading here
    ScriptSettings.__dict__ = json.loads(jsonData)
    ScriptSettings.Save(SettingsFile)
    return

#---------------------------
#   [Optional] Unload (Called when a user reloads their scripts or closes the bot / cleanup stuff)
#---------------------------
def Unload():
    return

#---------------------------
#   [Optional] ScriptToggled (Notifies you when a user disables your script or enables it)
#---------------------------
def ScriptToggled(state):
    return



#---------------------------
#   Anagram Finder
#---------------------------


with open('words.txt', 'r') as f:
    dictionary = f.read()

dictionary = [x.lower() for x in dictionary.split('\n')]

with open('words.txt', 'r') as f:
    dictionary = f.read()

dictionary = [x.lower() for x in dictionary.split('\n')]

common_words = ["in", "a", "be", "to", "of", "an", "i", "it", "on", "he", "as", "do", "at", "we", "it", "go", "me", "no", "us"]


#main function
def GetAnagrams(letters):

    index = letters.find("anagram") + 7

    letters = letters[index:]

    if len(letters) > 30:
        "Sorry, please reduce the length of your anagram request. (Maximum 30 characters)."

    try:
        if len(letters) < 4:
            return "Please follow: !anagram (thing to be anagrammed)"
    except:
        return "Please follow: !anagram (thing to be anagrammed)"

    anagram_string = ""
    anagram_list = ReturnAnagrams(letters)

    
    if anagram_list == False:
        return "Sorry, I couldn't find any decent anagrams! Try something else!"

    rng=random.WichmannHill()
    rng.shuffle(anagram_list)
    first = True
    for i in anagram_list:
        
        if first != True:
            anagram_string += " "
        else:
            first = False
            
        anagram_string += i    

    return '"' + anagram_string + '" is an anagram of "' + letters + '".'

# helper function
def ReturnAnagrams(original_letters, letters = "", anagram = [], tries = 0):

    global dictionary

    assert isinstance(letters,
                      str), 'Scrambled letters should only be of type string.'

    letters = letters.lower()
    tmp_letters = ""
    
    for c in letters:
        if c.isalpha():
            tmp_letters += c

    letters = tmp_letters

    letters_count = Counter(letters)

    anagrams = set()
    for word in dictionary:
        # Check if all the unique letters in word are in the
        # scrambled letters
        if not set(word) - set(letters):
            check_word = set()
            # Check if the count of each letter is less than or equal
            # to the count of that letter in scrambled letter input
            for k, v in Counter(word).items():
                if v <= letters_count[k]:
                    check_word.add(k)
            # Check if check_words is exactly equal to the unique letters
            # in the word of dictionary
            if check_word == set(word):
                if (len(word) != len(letters)-1 and len(word) != len(letters)-2):
                    anagrams.add(word)

    #anagrams.remove('')
    anagrams = sorted(list(anagrams), key=lambda x: len(x))
    
    #remove all characters that are not 3 to 6 characters long
    tmp_anagrams = []
    for i in anagrams:
        if len(i) < 8 and len(i) > 1:
            tmp_anagrams.append(i)
        elif i in common_words:
            tmp_anagrams.append(i)

    anagrams = tmp_anagrams

    if len(anagrams) == 0:
        if tries < 20:
            return ReturnAnagrams(original_letters, original_letters, [], tries + 1)
        else:
            return False

    rng=random.WichmannHill()
    ri=rng.randint(0, 5)
    ri = ri % len(anagrams)
    cur_anagram = anagrams[(ri*-1)]

    for i in cur_anagram:
        index = letters.find(i)
        letters = letters[:index]+letters[index+1:] 
    
    #return cur_anagram + " " + letters
    
    anagram.append(cur_anagram)
    if len(letters) == 0:
        return anagram
    else:
        #print(anagram)
        return(ReturnAnagrams(original_letters, letters, anagram, tries))



