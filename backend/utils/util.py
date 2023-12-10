# Adding a util to fetch a key from a dictionary 
# object for a particular value existing in the dictionary.
def get_key_from_dict(dictionary, value):
    for key, val in dictionary.items():
        if val == value:
            return key
    # If the value is not found, you can return a default value or raise an exception.
    return None