import math
import random

def generate_items_with_prob(prob, num_items):
    if prob < 0 or prob > 1:
        print "Probability should be within [0, 1]"
        return None
    num_golds = int(prob * num_items)
    num_rest = num_items - num_golds

    golds_list = [1] * num_golds
    rest_list = [0] * num_rest

    items_list = []
    for g in golds_list:
        items_list.append(g)
    for r in rest_list:
        items_list.append(r)

    # shuffle the item list
    random.shuffle(items_list)
    #print items_list
    return items_list

def draw_one_item_from_bag(items_list):
    rand_idx = random.randrange(0, len(items_list))
    #print rand_idx + 1
    if items_list[rand_idx] == 1:
        return "GOLD"
    else:
        return "NOTGOLD"

def play_game_using_one_bag(prob, num_items):
    bag_of_items = generate_items_with_prob(prob, num_items)
    raw_input("Press ENTER to grab an item from bag!")
    grabbed = draw_one_item_from_bag(bag_of_items)
    if grabbed == "GOLD":
        print "Congratulations! You grab a gold! Win $5!"
    else:
        print "Not a gold :( Try again"

def play_game_using_two_bags_simutaniously(prob1, prob2, num_items):
    print "[SIMUTANIOUS MODE] To win $5, you have to grab two golds from both bags!"
    bag1 = generate_items_with_prob(prob1, num_items)
    #raw_input("Press ENTER to grab an item from 1st bag!")
    bag2 = generate_items_with_prob(prob2, num_items)
    #raw_input("Press ENTER to grab an item from 2nd bag!")
    grabbed1 = draw_one_item_from_bag(bag1)
    grabbed2 = draw_one_item_from_bag(bag2)
    result = ""
    if grabbed1 == "GOLD" and grabbed2 == "GOLD":
        print "Congratulations! You grabbed two golds from two bags simutaniously. You win $5"
        result = "WIN"
    else:
        print "Lose!"
        result = "LOSE"

    return result

def play_game_using_two_bags_sequentially(prob1, prob2, num_items):
    result = []
    print "[SEQUENTIAL MODE] If you lose from first bag, then you lose the game"
    bag1 = generate_items_with_prob(prob1, num_items)
    #raw_input("Press ENTER to grab an item from 1st bag!")
    grabbed1 = draw_one_item_from_bag(bag1)

    if grabbed1 != "GOLD":
        print "The first grab is not GOLD, you lose!"
        return ["LOSE", "LOSE"]

    print "Good, your first grab is GOLD! Now you gonna grab the 2nd one, Ready? GO!"
    bag2 = generate_items_with_prob(prob2, num_items)

    #raw_input("Press ENTER to grab an item from 2nd bag!")
    grabbed2 = draw_one_item_from_bag(bag2)
    if grabbed2 != "GOLD":
        print "The second grab is not GOLD, you lose!"
        return ["WIN", "LOSE"]
    else:
        print "Wow! You grab a gold again! You win $5!"
        return ["WIN", "WIN"]

def play_game_multiple_times(prob, num_items, num_play):
    num_win = 0
    num_lose = 0
    
    for i in range(num_play):
        bag_of_items = generate_items_with_prob(prob, num_items)
        #raw_input("Press ENTER to grab an item from bag!")
        grabbed = draw_one_item_from_bag(bag_of_items)
        if grabbed == "GOLD":
            num_win += 1
            #print "Congratulations! You grab a gold! Win $5!"
        else:
            num_lose += 1
            #print "Not a gold :( Try again"

    print num_win, num_lose, num_play

#play_game_using_two_bags_simutaniously(0.8, 0.8, 1000)
#play_game_using_two_bags_sequentially(0.6, 0.7, 1000)
