#---------------------------
#   Import Libraries
#---------------------------
import os
import sys
import json
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
ScriptName = "Number Guesser"
Website = "https://www.streamlabs.com"
Description = "!guess (number) will try to guess the secret number"
Creator = "Dan White"
Version = "1.0.0.0"



#---------------------------
#   Define Global Variables
#---------------------------
global SettingsFile
SettingsFile = "Services/Scripts/Quote/Settings/settings.json"
global ScriptSettings
ScriptSettings = MySettings(SettingsFile)
ScriptSettings.Command = "!guess"
ScriptSettings.Cooldown = 1

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
        Parent.SendStreamMessage(GuessNumber(data.UserName, data.Message))    # Send your message to chat
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
#   Number Guessing Game
#---------------------------
def GuessNumber(user, user_input):

    f = open('number.txt')
    guess_number = f.read()
    f.close()

    guess_number = int(guess_number)

    return_string = ""

    #pull out the numbers
    user_number = ""
    for c in user_input:
        if c.isnumeric():
            user_number += c 

    user_number = int(user_number)

    return_string += "{} guessed {}. ".format(user,'{:,}'.format(user_number))

    if user_number == guess_number:
        new_number = Parent.GetRandom(0, 1000000)
        f = open("number.txt","w")
        f.write(str(new_number))
        f.close()
        return_string += " Amazing!!! {} got it right!!! Congratulations!!! The number has been reset to a random number between 1 and 1,000,000.".format(user)
    elif user_number > guess_number:
        return_string += " Sorry. The number I'm thinking of us lower than that."
    elif user_number < guess_number:
        return_string += " Sorry. The number I'm thinking of is higher than that."
    else:
        return_string += " Something went wrong. Please follow the format: !guess (number). Example: !guess 123456"
    return return_string
    