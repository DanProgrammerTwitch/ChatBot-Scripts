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

#   Import your Settings class
from Settings_Module import MySettings
#---------------------------
#   [Required] Script Information
#---------------------------
ScriptName = "Rock, Paper, Scissors"
Website = "https://www.streamlabs.com"
Description = "!rps (rock/paper/scissors) will play rock paper scissors"
Creator = "Dan White"
Version = "1.0.0.0"

#---------------------------
#   Define Global Variables
#---------------------------
global SettingsFile
SettingsFile = "Services\Scripts\Quote\Settings\settings.json"
global ScriptSettings
ScriptSettings = MySettings()
ScriptSettings.Command = "!rps"

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
        Parent.SendStreamMessage(RPS(data.UserName, data.Message))    # Send your message to chat
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
#   Rock, Paper, Scissors
#---------------------------

def RPS(user, user_input):

    return_string = ""

    #define wins and rock paper scissors
    results = ["It's a draw", "You win!", "You lose!"]
    rps = ["rock","paper","scissors"]  

    

    if "rock" in user_input:
        user_input = 0
    elif "paper" in user_input:
        user_input = 1
    elif "scissors" in user_input:
        user_input = 2
    else:
        return "Please format as: !rps rock, !rps paper, or !rps scissors"

    try:
        
        #computer's choice is 0,1,2
        computer_input = Parent.GetRandom(0, 2)

        #compile a string with the user and the computer's choice
        return_string += "{} chose {} and I chose {}.".format(user, rps[user_input],rps[computer_input])
        return_string += " "
        
        # use modulo 3 to figure out of the user won or not
        return_string += results[compare (user_input,computer_input)]

        return return_string
    
    except Exception as e:
        return str(e)
        return "Sorry! That's not valid input!"

    return 0

#RPS Helper Function
def compare (user_input, computer_input):
    return (user_input - computer_input) % 3