import re 

def count_numbers(str_,blocks=False):
    '''
    Gives the count of numbers present in the string
    Usage : sirex.count_numbers("Hello123")
    Returns : int
    '''
    if blocks == True  : 
        pattern = "[0-9]*"
        L_str = re.findall(pattern , str_ )
        L_int = [int(k) for k in L_str if k != ''] 
        count = len(L_int)
    else :     
        pattern = "[0-9]"
        count = len(re.findall(pattern,str_))
    return count


def biggest_number(str_):
    '''
    Returns the biggest number that comes as a block
    Usage : sirex.biggest_number('Hel3 1l199-123') 
    Returns : str
    '''
    pattern = "[0-9]*"
    L_str = re.findall(pattern , str_ )
    L_int = [int(k) for k in L_str if k != '']  # Filter based on not null & convert each item into integer
    return max(L_int)

def smallest_number(str_):
    '''
    Returns the smallest number that comes as a block
    Usage : sirex.biggest_number('Hel3 1l199-123') 
    Returns : str
    '''
    pattern = "[0-9]*"
    L_str = re.findall(pattern , str_ )
    L_int = [int(k) for k in L_str if k != '']  # Filter based on not null & convert each item into integer
    return min(L_int)

def replace_numbers(str_,sub_=""):
    '''
    Replaces all numbers with the specified string ( or just removes the numbers - default option)
    Usage : sirex.replace_numbers("hell3o" , "")
    Returns : str
    '''
    pattern = "[0-9]"
    replaced_ = re.sub(pattern, sub_ , str_ )
    return replaced_


def is_number(str_):
    '''
    Checks if the given string is a number or not
    Usage : sirex.is_number("hello")
    Returns : boolean
    '''
    pattern = "[0-9]"
    if len(re.findall(pattern,str_)) == len(str_) :
        return True
    else : 
        return False
    
def remove_numbers(str_):
    '''
    Removes all the numbers from the string 
    Usage : sirex.remove_numbers(' Hel1lo123 123')
    Returns : str
    '''
    pattern = "[0-9]"
    replaced_ = re.sub(pattern, "" , str_ )
    return replaced_.strip()

def count_occurance(sub,parent,case_sensitive = False):
    '''
    Counts the occurance of a sub-string in a parent string
    Usage : sirex.count_occurance('He', 'Hello there' , True) # Searches for h and H
    Returns : int
    '''
    pattern  = sub
    if not case_sensitive:
        pattern = "(?i)"+sub
    count = len((re.findall(pattern,parent)))            
    return count 

# Checks if string ends with a number 


def endswith_number(str_):
    '''
    Checks if the string ends with a string character
    Usage : sirex.endswith_number("Hello4")  
    Returns : bool
    '''
    if count_numbers(str_[-1]):
        return True
    else : 
        return False


def beginswith_number(str_):
    '''
    Checks if the string begins with a string character
    Usage : sirex.endswith_number("4Hello4")  
    Returns : bool
    '''
    if count_numbers(str_[0]):
        return True
    else : 
        return False