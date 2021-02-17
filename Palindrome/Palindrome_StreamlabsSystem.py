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
ScriptName = "Palindrome"
Website = "https://www.streamlabs.com"
Description = "!palindrome (message) will check if something is a palindrome or not."
Creator = "Dan White"
Version = "1.0.0.0"



#---------------------------
#   Define Global Variables
#---------------------------
global SettingsFile
SettingsFile = "Services/Scripts/Palindrome/Settings/settings.json"
global ScriptSettings
ScriptSettings = MySettings(SettingsFile)
ScriptSettings.Command = "!palindrome"
ScriptSettings.Cooldown = 10

#---------------------------
#   [Required] Initialize Data (Only called on load)
#---------------------------
def Init():

    #   Create Settings Directory
    directory = os.path.join(os.path.dirname(__file__), "Services\Scripts\Palindrome\Settings")
    if not os.path.exists(directory):
        os.makedirs(directory)

    #   Load settings
    SettingsFile = os.path.join(os.path.dirname(__file__), "Services\Scripts\Palindrome\Settings\settings.json")
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
        Parent.SendStreamMessage(IsPalindrome(data.Message))    # Send your message to chat
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
#   Palindrome Checker
#---------------------------


def IsPalindrome(message):

    # find the spot where the palindrome begins
    index = message.find("!palindrome")
    index += len("!palindrome")
    index += 1

    # reset message variable and keep a copy for returning later
    message = message[index:]
    original_message = message

    if len(message) < 1:
        return "Follow the format: !palindrome (messaage). Example: !palindrome Never odd or even"

    # remove all special characters, white spaces, and convert everything to lower case
    message = message.lower()

    tmp_message = ""

    for c in message:
        if c.isalpha():
            tmp_message += c

    message = tmp_message

    #checks to see if the message is the same forwards and backwards
    checkPalindrome = message == message[::-1]

    if (checkPalindrome):
        return '"' + original_message + '" is a palindrome!'    
    else:
        return '"' + original_message + '" is not a palindrome!'    