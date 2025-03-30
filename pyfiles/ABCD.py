# ABCD.py 

ABC = [
    "Alice", 
    "Bob", 
    "Catherine", 
    "Doggy", 
    "Egg", 
    "Fuck",
    "Gun",
]

Adj = [
    "Angry", 
    "Bombed",
    "Cao",
]

def reflection(userNO):
    if userNO == 0:
        return "洞主"
    if userNO % 26 > 0 and userNO % 26 <= 7:
        return ABC[userNO]
    return "Default"
    