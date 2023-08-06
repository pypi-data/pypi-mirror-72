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