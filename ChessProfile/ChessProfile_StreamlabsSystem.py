#---------------------------
#   Import Libraries
#---------------------------
import os
import sys
import json
import time


sys.path.append(os.path.join(os.path.dirname(__file__), "lib")) #point at lib folder for classes / references

import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

#   Import your Settings class
from Settings_Module import MySettings
#---------------------------
#   [Required] Script Information
#---------------------------
ScriptName = "Chess.com Profile"
Website = "https://www.streamlabs.com"
Description = "!chess (username) will give the chess.com profile of a user"
Creator = "Dan White"
Version = "1.0.0.0"

#---------------------------
#   Define Global Variables
#---------------------------
global SettingsFile
SettingsFile = "Services\Scripts\ChessProfile\Settings\settings.json"
global ScriptSettings
ScriptSettings = MySettings()
ScriptSettings.Command = "!chess"

#---------------------------
#   [Required] Initialize Data (Only called on load)
#---------------------------
def Init():

    #   Create Settings Directory
    directory = os.path.join(os.path.dirname(__file__), "Services\Scripts\ChessProfile\Settings")
    if not os.path.exists(directory):
        os.makedirs(directory)

    #   Load settings
    SettingsFile = os.path.join(os.path.dirname(__file__), "Services\Scripts\ChessProfile\Settings\settings.json")
    ScriptSettings = MySettings(SettingsFile)
    ScriptSettings.Command = "!chess"
    return

#---------------------------
#   [Required] Execute Data / Process messages
#---------------------------
def Execute(data):

     

    if data.IsChatMessage() and data.GetParam(0).lower() == ScriptSettings.Command and Parent.IsOnUserCooldown(ScriptName,ScriptSettings.Command,data.User):
        Parent.SendStreamMessage("Time Remaining " + str(Parent.GetUserCooldownDuration(ScriptName,ScriptSettings.Command,data.User)))

    #   Check if the proper command is used, the command is not on cooldown and the user has permission to use the command
    if data.IsChatMessage() and data.GetParam(0).lower() == ScriptSettings.Command and not Parent.IsOnUserCooldown(ScriptName,ScriptSettings.Command,data.User) and Parent.HasPermission(data.User,ScriptSettings.Permission,ScriptSettings.Info):
        Parent.BroadcastWsEvent("EVENT_MINE","{'show':false}")
        Parent.SendStreamMessage(GetChessStats(str(data.Message)))    # Send your message to chat
        Parent.AddUserCooldown(ScriptName,ScriptSettings.Command,data.User,ScriptSettings.Cooldown)  # Put the command on cooldown

    
    return

#---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
#----------w-----------------
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
#   Get Chess.Com Profile Information
#---------------------------

class Player:
    def __init__(self):

        self.name = "No Name"
        self.url = ""
        self.join_date = ""
        self.rapid_rating = "No Games"
        self.blitz_rating = "No Games"
        self.bullet_rating = "No Games"
        self.daily_rating = "No Games"
        self.tactics_rating = "No Tactics"

def GetChessStats(message):

    index = message.find("!chess ") + len("!chess ")
    user = message[index:]

    if (user == ""):
        user = "programmerdan"

    info_url = 'https://api.chess.com/pub/player/' + user
    info = GetUrlData(info_url)

    stats_url = 'https://api.chess.com/pub/player/' + user + '/stats'
    stats = GetUrlData(stats_url)

    player = Player()

    join_date = GetSubstring('\\"joined\\":',',\\"', info)
    if join_date != False:
        player.join_date = join_date        
        player.join_date = time.strftime('%Y-%m-%d', time.localtime(int(player.join_date)))
    else:
        return "Sorry, user: '" + user + "' does not exist."
    player.url = 'https://www.chess.com/member/' + user
    
    rapid_rating = GetSubstring('chess_rapid\\":{\\"last\\":{\\"rating\\":', ',\\"', stats)
    if rapid_rating != False:
        player.rapid_rating = rapid_rating

    blitz_rating = GetSubstring('chess_blitz\\":{\\"last\\":{\\"rating\\":', ',\\"', stats)
    if blitz_rating != False:
        player.blitz_rating = blitz_rating

    bullet_rating = GetSubstring('chess_bullet\\":{\\"last\\":{\\"rating\\":', ',\\"', stats)
    if bullet_rating != False:
        player.bullet_rating = bullet_rating
    
    daily_rating = GetSubstring('chess_daily\\":{\\"last\\":{\\"rating\\":', ',\\"', stats)
    if daily_rating != False:
        player.daily_rating = daily_rating

    tactics_rating = GetSubstring('"tactics\\":{\\"highest\\":{\\"rating\\":', ',\\"', stats)
    if tactics_rating != False:
        player.tactics_rating = tactics_rating


    name = GetSubstring('"name\\":\\"', '\\",', info)
    if name != False:
        player.name = name
        
    return_string = ""
    return_string += "User Name: " + user
    return_string += " | Name: " + player.name
    return_string += " | Join Date: " + player.join_date
    return_string += " | Bullet: " + player.bullet_rating
    return_string += " | Blitz: " + player.blitz_rating
    return_string += " | Rapid: " + player.rapid_rating
    return_string += " | Daily: " + player.daily_rating
    return_string += " | Tactics: " + player.tactics_rating
    return_string += " | URL: " + player.url

    return return_string
    

def GetSubstring(start, end, string):
    starting_index = string.find(start)
    if starting_index == -1:
        return False
    starting_index = starting_index + len(start)
    final_index = string.find(end, starting_index)
    return string[starting_index:final_index]


def GetUrlData(url):
    try:
        headers = {}
        result = Parent.GetRequest(url,headers)
        return result
    except:
        return False
