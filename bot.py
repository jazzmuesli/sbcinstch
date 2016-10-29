microlife = 0.0

print("I’m <Name of assistant> and I’m part of the <Insurer> team. Who am I talking to?")
fName = input("> ")

print("Hi " + <fName> + ", thanks for showing your interest in our policy, I'd like to get to know a little about your daily habits and lifestyle before we proceed. Is that OK?")
cont1 = input("> ")
if(cont1 == "No"):
    break

print("Could I have your gender please?")
gender = input("> ")
if(gender == "Male"):
    microlife -= 4
if(gender != "Male" or gender != "Female"):
    print("I'm sorry, I didn't really get that, could you be a bit more concise please?") #TODO: Needs some form of a loop here

print("Alright, now that we’ve got your name and gender out of the way. I need to know if you’re a smoker.")
smoker = input("> ")

if(smoker == "Yes"):
    print("So how many cigarettes do you smoke per day?")
    cig = int(input("> "))
    if(cig != 0):
        microlife -= (cig/3)


[If smoker = True] --->
