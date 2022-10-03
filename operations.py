# Define feature functions (user story functions) and variables in this file:

from datetime import date, datetime

# Import helper functions
from helpers import convertDateStrToDateTuple

# Import constants 
from helpers import DAY_IND, MONTH_IND, YEAR_IND
 
# familes = []
# individuals = []

# Input: an id string and a list of individuals (list of dictionaries w/ each dictionary representing a personObj)
# Output: The name of the person corresponding to the inputted id OR an error message.
# Note: Does NOT modify the input.
def getNameFromId(id, people):    
    for indi in people:
        if indi['ID'] == id:
            return indi['name']
    return 'Error: Id does not exist!'

# Input: an id string and a list of individuals (list of dictionaries w/ each dictionary representing a personObj)
# Output: The Date of Death of the person corresponding to the inputted id OR an error message.
# Note: Does NOT modify the input.
def GetDeathFromId(people,id):
    for indi in people:
        if indi['ID'] == id:
            return indi['death']
    return 'Error: Id does not exist!'

# Input: two dates in tuple format
# Output: returns true if a date occurs after death date, or false of otherwise
def compareDeath(date, death):
        if date[YEAR_IND] < death[YEAR_IND]:
            return False
        elif date[YEAR_IND] > death[YEAR_IND]:
            return True
        else:
            # Check month:
            if date[MONTH_IND] > death[MONTH_IND]:
                return True
            elif date[MONTH_IND] < death[MONTH_IND]:
                return False
            else:
                # Check day:
                return date[DAY_IND] >= death[DAY_IND]

# Input: A family ID as a string, a list of family objects/dictionaries, and a list of individual objects/dictionaries
# Output: returns the death dates of both parents in a given family
def getParentsDeathDates(familyID, families, people):
    for family in families:
        if family["ID"] == familyID:
            return [GetDeathFromId(people, family['husband_id']), GetDeathFromId(people, family['wife_id'])]


# Input: The death date of a husband of a family in tuple format, and the birthday of a child in tuple format
# Output: Returns True if the husband died at least nine months before the birth of a child or after, and false otherwise
def HusToChild(hus, child):
        if child[YEAR_IND] - hus[YEAR_IND] == 1:
            if (child[MONTH_IND] + 12) - hus[MONTH_IND] >= 9:
                return False
        
        if child[YEAR_IND] - hus[YEAR_IND] > 1:
            return False
        elif hus[YEAR_IND] > child[YEAR_IND]:
            return True
        else:
            # Check month:
            if hus[MONTH_IND] > child[MONTH_IND]:
                return True
            elif hus[MONTH_IND] < child[MONTH_IND] and (abs(hus[MONTH_IND] - child[MONTH_IND]) >= 9):
                return False
            else:
                return True
            

# User Story #2 -- Ankit
# Input: A person object/dictionary
# Output: Returns true if birth occurs before death on an individual. False otherwise.
# Note: Returns true if person is not dead. 
# Question: Can someone die on the same day they were born? This function assumes thats allowed
def birthBeforeDeath(personObj):
    if personObj['alive']:
        return True
    else:
        birthdayTuple = convertDateStrToDateTuple(personObj['birthday'])
        deathdayTuple = convertDateStrToDateTuple(personObj['death'])
        
        if birthdayTuple[YEAR_IND] > deathdayTuple[YEAR_IND]:
            return False
        elif birthdayTuple[YEAR_IND] < deathdayTuple[YEAR_IND]:
            return True
        else:
            # Check month:
            if birthdayTuple[MONTH_IND] < deathdayTuple[MONTH_IND]:
                return True
            elif birthdayTuple[MONTH_IND] > deathdayTuple[MONTH_IND]:
                return False
            else:
                # Check day:
                return birthdayTuple[DAY_IND] <= deathdayTuple[DAY_IND]
            
# User Story #5 -- Zane
# Input: A Family object/dictionary, a list of individual objects/dictionaries
# Output: Return true if marriage occurs before death, and false if otherwise   
def MarriageBeforeDeath(familyObj, people):
    marriedTuple = convertDateStrToDateTuple(familyObj['married'])
    hus_death = GetDeathFromId(people, familyObj['husband_id'])
    wife_death = GetDeathFromId(people, familyObj['wife_id'])
    ans, ans2 = True, True;
    
    if not hus_death == 'NA':
        husbandTuple = convertDateStrToDateTuple(hus_death)
        ans = compareDeath(husbandTuple, marriedTuple)
    
    if not wife_death == 'NA':
        wifeTuple = convertDateStrToDateTuple(wife_death)
        ans2 = compareDeath(wifeTuple, marriedTuple)
    return ans and ans2


# User Story #9 -- Zane
# Input: A person object, a list of family objects, and a list of people objects
# Output: Return false if mother dies before personObj's birthday or the father dies more than nine months before birthday
# Returns true otherwise   
def BirthBeforeParentsDeath(personObj, families, people):
    for famID in personObj['child']:
        arr = getParentsDeathDates(famID, families, people)
        hus_death = arr[0];
        wife_death = arr[1];
        birthdayTuple = convertDateStrToDateTuple(personObj['birthday'])
        ans, ans2 = True, True;
    
        if not hus_death == 'NA':
            husbandTuple = convertDateStrToDateTuple(hus_death)
            ans = HusToChild(husbandTuple, birthdayTuple)
        
        if not wife_death == 'NA':
            wifeTuple = convertDateStrToDateTuple(wife_death)
            ans2 = compareDeath(wifeTuple, birthdayTuple)
        if not (ans and ans2):
            return False
    return True


# User Story #27 -- Ankit
# Input: a person object/dictionary
# Output: Computes the age of the person
# Note: DOES modify the input- slightly formats the person object to make date extraction easier for future uses.
# Question: SHould the program accept future dates?
def computeAge(personObj):       
    bdayLen = len(personObj['birthday'].split(' ')[0])
    if bdayLen == 1:
        personObj['birthday'] = '0' + personObj['birthday'] 

    birthday_datetime_obj = datetime.strptime(personObj['birthday'], '%d %b %Y')
    
    end = ''
    
    if personObj['death'] == 'NA':
        end = date.today()
    else:
        ddayLen = len(personObj['death'].split(' ')[0])
        if ddayLen == 1:
            personObj['death'] = '0' + personObj['death']
        end = datetime.strptime(personObj['death'], '%d %b %Y')
         
    age = end.year - birthday_datetime_obj.year - ((end.month, end.day) < (birthday_datetime_obj.month, birthday_datetime_obj.day))
    return age

