
letter_table = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_ "
def check_name(name:str)->bool:
    for c in name:
        if( c not in letter_table ):
            return False
    return True