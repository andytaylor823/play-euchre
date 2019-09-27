import basicprogs as b
import turns_and_play as t
import call
import showturn as s

# TODO later:
# ---Add variables to the "card" class called "isleft" and "isright", set true when trump is declared
# ---Adjust the rest of the functions to accomodate this
# ---Eventually add in going alone
# ---Add in knowledge about what cards have already been played

ns, ew = t.play_a_hand(0, 0)
print(ns, ew)

exit(10)












hands = b.deal()
print('------------------------')

trump_suit, caller_pos, called_first_round, turn_card = t.call_trump(hands)
if called_first_round:
	hands[3] = call.dealer_new_hand(hands[3], hands[-1][0])
	b.order_hand(hands[3], trump_suit = trump_suit)
print(trump_suit, called_first_round, caller_pos)
h, w = t.play_a_trick(hands, trump_suit, 'o1', caller_pos)


exit(10)


o1hand, phand, o2hand, dhand, kitty = b.deal()
hands = [o1hand, phand, o2hand, dhand, kitty]

trump_suit, caller_pos, called_first_round, turn_card = t.call_trump(hands)






s.show_turn(hands, cards_played = [[phand[0],"p"], [o1hand[0], "o1"], [dhand[0], "d"], [o2hand[0], "o2"]])
#s.show_turn(hands)
kitty[0].print_card()
print('')

for hand in hands[0:4]:
	if call.call_first_round(hand, kitty[0]):
		b.print_hand(hand)






