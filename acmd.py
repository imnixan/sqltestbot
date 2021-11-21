import sqlcommands
import re

def showuser(message):
    answer = sqlcommands.showsqluser(re.search('(?<=\.usr ).*(?=\()', str(message)).group(0), re.search('(?<=\().*(?=\))', str(message)).group(0))
    if (answer[0] == "Успешно"):
        result = answer[1]
    return result
def deluser(message):
    answer = sqlcommands.delsqluser(re.search('(?<=\.usr ).*(?=\()', str(message)).group(0), re.search('(?<=\().*(?=\))', str(message)).group(0))
    if (answer == "Успешно"):
        result ="Пользователь удален"
    return result
    #####