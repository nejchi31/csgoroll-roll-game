import random
import numpy as np
import csv
import math
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns


#settings
dataLenght = 1000000000 # define your data lenght in batches 
# Your data lenght: ----------------------------------------------
# Your data in batches: --------   --------   --------   --------    --------  
array_raw = []

#for x in range(array_length):
#    random_decimal = round(random.uniform(1,10),2)
#    array_raw.append(random_decimal)
black = 0
red = 0
green = 0
with open('G:\Projects\csgoroll-roll\DATASET_14-2_1-3-color.csv', newline='') as myFile:
    reader = csv.reader(myFile, delimiter=',', quoting=csv.QUOTE_NONE)
    for lists in reader:
        for row in lists:
            array_raw.append(row)
            if(row=='Black'):
                black += 1
            if(row=='Red'):
                red += 1
            if(row=='Green'):
                green += 1

myFile.close()
partToSplit = math.ceil(len(array_raw)/dataLenght)
print("Data length is: " + str(len(array_raw)))
print("Black distribution percentage value is: " + str(black*100/len(array_raw)) + ' %')
print("Red distribution percentage value is: " + str(red*100/len(array_raw)) + ' %')
print("Green distribution percentage value is: " + str(green*100/len(array_raw)) + ' %')
batch = np.array_split(array_raw, partToSplit)


def consecutive_rounds (data, result_type):
    rounds = 0
    max_rounds = 0
    for result in data:
        if result == result_type:
            rounds += 1
        else:
            if rounds<=max_rounds:
                rounds = 0
            else:
                max_rounds = rounds
                rounds = 0
    if rounds>max_rounds:
        max_rounds = rounds
    print("Most consecutive rounds of type " + str(result_type) + " is " + str(max_rounds) + ' in a row!')

def no_consecutive_rounds (data, result_type):
    rounds = 0
    max_rounds = 0
    for result in data:
        if result != result_type:
            rounds += 1
        else:
            if rounds<=max_rounds:
                rounds = 0
            else:
                max_rounds = rounds
                rounds = 0
    if rounds>max_rounds:
        max_rounds = rounds
    print("Most consecutive rounds of NO type " + str(result_type) + " is " + str(max_rounds) + ' in a row!')

def patern_finder(data, pattern, result_type):
    round_to_switch = 0
    rounds = 0
    max_rounds = 0
    switch = False
    for result in data:
        if result == result_type:
            if switch == True:
                if rounds<=max_rounds:
                    rounds = 0
                else:
                    max_rounds = rounds
                    rounds = 0
            elif round_to_switch < pattern:
                rounds += 1
                round_to_switch += 1
                if round_to_switch == pattern:
                    switch = True
                    round_to_switch = 0
            elif round_to_switch >= pattern:
                switch = False
                round_to_switch = 0
                if rounds<=max_rounds:
                    rounds = 0
                else:
                    max_rounds = rounds
                    rounds = 0
            else:
                pass
        elif result == 'Green':
            switch = False
            round_to_switch = 0
            if rounds<=max_rounds:
                rounds = 0
            else:
                max_rounds = rounds
                rounds = 0
        else:
            if switch == True:
                rounds += 1
                if round_to_switch < pattern:
                    round_to_switch += 1
                    if round_to_switch == pattern:
                        switch = False
                        round_to_switch = 0
                elif round_to_switch == pattern:
                    switch = False
                    round_to_switch = 0
                else:
                    pass
            else:
                round_to_switch = 0
                if rounds<=max_rounds:
                    rounds = 0
                else:
                    max_rounds = rounds
                    rounds = 0
    print("Most consecutive rounds of pattern alternating " + str(pattern) + " of blacks and reds, starting with " + str(pattern) + " " + result_type + "s is " + str(max_rounds) + ' in a row!')

def sim_always_red(data, startingBalance):  
    bankroll = startingBalance
    bankroll_history = []
    for result in data:
        if result == "Red":
            bankroll += 1
        else:
            bankroll -= 1
        bankroll_history.append(bankroll)
    print("With starting balance: " + str(startingBalance) + ". Final balance would be: " + str(bankroll))
    return bankroll_history

def sim_train(data, startingBalance, validation, breakWhenZero):  
    bankroll = startingBalance
    bankroll_history = []
    last_color = None
    in_train_flag = 0
    for result in data:
        if result == last_color or in_train_flag==validation:
            in_train_flag += 1
        if in_train_flag > validation:
            if result == last_color:
                bankroll += 1
            else:
                bankroll -= 1
                in_train_flag = 1
        else:
            pass
        last_color = result
        bankroll_history.append(bankroll)
        if bankroll == 0 and breakWhenZero==True:
            break
    print("With starting balance: " + str(startingBalance) + ". Final balance would be: " + str(bankroll))
    return bankroll_history

def doubling_sim(data, startingBalance, validation, init_bet, breakWhenZero):
    bankroll = startingBalance
    bankroll_history = []
    last_color = None
    in_train_flag = 1
    init_bet = init_bet
    bet = init_bet
    for result in data:
        if result == last_color or result == 'Green':
            in_train_flag += 1
        if in_train_flag > validation:
            if result != last_color and result != 'Green':
                bankroll += bet
                bet = init_bet
                in_train_flag = 1
            else:
                bankroll -= bet
                bet *= 2
        else:
            pass
        if result == 'Green':
            pass
        else:
            last_color = result
        bankroll_history.append(bankroll)
        if bankroll < 0 and breakWhenZero==True:
            break
    print("With starting balance: " + str(startingBalance) + " and validation number " + str(validation) + ". Final balance would be: " + str(bankroll))
    return bankroll_history

def doubling_green(data, startingBalance, validation, init_bet, breakWhenZero):
    bankroll = startingBalance
    bankroll_history = []
    last_color = None
    in_train_flag = 0
    init_bet = init_bet
    bet = init_bet
    last_100 = []
    count = 0
    bet_pattern = [1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2.5,2.5,2.5,3,3,3,3,3,3,3,3,3.5,3.5,4,4,4,4,4,4,4,4,4,4,4,5,5,5,5,5,5,5,6,6,6,6,6,6,6,6,7,7.5,8,9,10,10,10,12,12,15,15,15,16,16,16,17,17,17,20,30,50,40,60,100,100]
    iteration = 0
    for result in data:
        if result != 'Green':
            in_train_flag += 1
        else:
            pass
        if in_train_flag > validation:
            if result == 'Green':
                bankroll = bankroll + (bet * 14)
                bet = init_bet
                in_train_flag = 0
            else:
                bankroll -= bet
                bet *= 1
        else:
            pass
        
        bankroll_history.append(bankroll)
        if bankroll < 0 and breakWhenZero==True:
            break
    print("With starting balance: " + str(startingBalance) + " and validation number " + str(validation) + ". Final balance would be: " + str(bankroll))
    return bankroll_history

def check_element(data, element):
    count = 0
    for result in data:
        if result == element:
            count += 1
    return count

sns.set(rc={'figure.figsize':(10,7)})
##################################
#        Testing Arrays          #
##################################
test_array = ['Black', 'Black', 'Red', 'Red', 'Black', 'Black', 'Green', 'Black', 'Black', 'Red', 'Red', 'Red', 'Red']
test_array1 = ['Black', 'Red', 'Black', 'Red', 'Black', 'Red', 'Black', 'Red','Black', 'Red', 'Black', 'Red', 'Red', 'Red', 'Red', 'Red']
test_array2 = ['Red', 'Red', 'Black', 'Black', 'Red', 'Black', 'Black', 'Black', 'Red', 'Red', 'Red','Black', 'Black', 'Black', 'Red', 'Red', 'Red', 'Red', 'Red']


patern_finder(array_raw, 3, 'Red')
no_consecutive_rounds(array_raw, 'Red')
no_consecutive_rounds(array_raw, 'Black')
no_consecutive_rounds(array_raw, 'Green')
consecutive_rounds(array_raw, 'Red')
consecutive_rounds(array_raw, 'Green')
consecutive_rounds(array_raw, 'Black')
sim_always_red(array_raw, 100)
#sim_train(array_raw, 100, 10)

##############################################
#        Ploting Simulation Results          #
##############################################
i=1
#for i in range(10):
plt.plot(doubling_green(data=array_raw, startingBalance=100, validation=40, init_bet=1, breakWhenZero=False), linewidth=2)
plt.xlabel("Number of Games", fontsize=18, fontweight="bold")
plt.ylabel("Balance", fontsize=18, fontweight="bold")
plt.xticks(fontsize=16, fontweight="bold")
plt.yticks(fontsize=16, fontweight="bold")
plt.title("Balance Over Time", fontsize=22, fontweight="bold")
plt.show()
