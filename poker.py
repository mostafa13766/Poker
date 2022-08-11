#!/usr/bin/env python

from random import choice as randch
import re


class play_ground:
    list_cards = []  # list of all 52 cars made by __init__ method
    # list of 5 'table cards' + 'players' cards' that picked in current round
    list_cards_picked = []
    cards_table = []  # list of 5 cards on the table in current round
    dict_players_cards = {}  # list of players and their 2 cards in preflop
    player_data = {}  # dictionary of players that introduce based: key='player name' : value= f'player+{num}'
    # activated by __init__ method
    # dictionary of players' ranking. key= 'name of player',value='ranking-rankNum+cardsValue(ex.: flush-699899883)'
    player_rank = {}
    count = 0  # counting players in the table, activated by __init__ method

    def __init__(self, players: list):
        self.players = players
        for player in players:
            self.player = player  # extacting every player
            play_ground.count += 1  # counting every player
            play_ground.player_data[self.player] = 'player' + \
                str(play_ground.count)  # adding player ro the player_data dict

        self.making_cards()

    def __repr__(self):
        return f"""This is a poker table, with {len(self.players)} players.
    players are: {self.player_data}
    """

    def making_cards(self):
        '''
        first this function will clear all list and dictionaries,
        then make 52 new cards.

        inputs --->
        none

        outputs --->
        list_cards:  list of 52 cards.
        '''
        self.reset()
        list_suits = ['club', 'heart', 'spade', 'diamond']
        for suit in list_suits:
            for num in range(1, 14):
                self.list_cards.append(suit+'-'+str(num))
        return self.list_cards

    def reset(self):
        """
        reset values for new round

        """
        self.list_cards.clear()
        self.list_cards_picked.clear()
        self.cards_table.clear()
        self.dict_players_cards.clear()
        self.player_rank.clear()

    def pick_card(self):
        """
        picking randomly a card from list_cards and remove it
        from list_cards and add it to list_picked_cards

        inputs --->
        none

        outputs --->
        card: the picked card
        """
        card = randch(self.list_cards)
        self.list_cards.pop(self.list_cards.index(card))
        self.list_cards_picked.append(card)
        return card

    def preflop(self):
        """
        this function will distribute 2 cards to each palyer
        in preflop round and restore them in dict_players_cards
        dictionary.

        inputs --->
        players: List of current players

        outputs --->
        dict_players_cards: dictionary with keys that are player names
        and values are list of their 2 cards.

        """
        for player in range(len(self.players)):
            self.dict_players_cards[self.players[player]] = [
                self.pick_card(), self.pick_card()]
        return self.dict_players_cards

    def flop(self):
        """
        pick 3 cards in flop round

        inputs --->
        none

        outputs --->
        cards_table: list of cards on the table(=3)
        """
        for i in range(3):
            self.cards_table.append(self.pick_card())
        return self.cards_table

    def turn(self):
        self.cards_table.append(self.pick_card())

    def river(self):
        self.cards_table.append(self.pick_card())

    def ranking(self, players: list):
        """
        ranking the players based on their cards and return the
        result in 'player_rank' dictionary.

        inputs -->
        players: list, list of players

        outputs -->
        self.winner(): str,winner name
        player_rank: dict, players' ranking
        """
        for player in players:
            player_cards = []
            player_cards = self.cards_table + self.dict_players_cards[player]
            straight_set = set()
            striaght_flush = ''
            suits_dict = {
                'card-dict': {
                    'heart': {
                        'count': 0,
                        'cards': [],
                        'flush': False},
                    'spade': {
                        'count': 0,
                        'cards': [],
                        'flush': False},
                    'club': {
                        'count': 0,
                        'cards': [],
                        'flush': False},
                    'diamond': {
                        'count': 0,
                        'cards': [],
                        'flush': False}},
                'straight': {
                    'list': [],
                    'isstraight': False,
                    'isstraightflush': False
                },
                'number': {
                    '1': 0,

                    '2': 0,

                    '3': 0,

                    '4': 0,

                    '5': 0,

                    '6': 0,

                    '7': 0,

                    '8': 0,

                    '9': 0,

                    '10': 0,

                    '11': 0,

                    '12': 0,

                    '13': 0



                }}

            for card in player_cards:
                suits_dict['card-dict'][card.split('-')[0]]['count'] += 1
                suits_dict['card-dict'][card.split('-')[0]
                                        ]['cards'].append(int(card.split('-')[1]))
                suits_dict['number'][card.split('-')[1]] += 1
                straight_set.add(int(card.split('-')[1]))
                striaght_flush += card[0]

            for cards in suits_dict['card-dict'].values():
                cards['cards'].sort()
                if cards['count'] >= 5:
                    cards['flush'] = True

            suits_dict['straight']['list'] = list(straight_set)
            suits_dict['straight']['list'].sort()
            fix_num = suits_dict['straight']['list'][0]-1
            are_all_straight = ''
            for number in suits_dict['straight']['list']:
                if number - fix_num == 1:
                    are_all_straight += str(1)
                else:
                    are_all_straight += str(0)
                fix_num = number
            from re import match
            # match 5 executive (1)
            if bool(match('1\d*[1]{5}', are_all_straight)) == True:
                suits_dict['straight']['isstraight'] = True

            if bool(match('(h){5}', striaght_flush)) == True or bool(match('(d){5}', striaght_flush)) == True or bool(match('(c){5}', striaght_flush)) == True or bool(match('(s){5}', striaght_flush)) == True:  # match 5 executive (h|s|d|c)
                suits_dict['straight']['isstraightflush'] = True
            Stright_flush = False
            Flush = False
            Straight = suits_dict['straight']['isstraight']
            Kind = ''
            if suits_dict['straight']['isstraightflush'] == True and suits_dict['straight']['isstraight'] == True:
                Stright_flush = True
            for item in suits_dict['card-dict'].values():
                if item['flush'] == True:
                    Flush = True
                    break
            if Stright_flush == True:
                Flush = False
                Straight = False
            for item in suits_dict['number'].values():
                if item == 0:
                    continue
                else:
                    Kind += str(item)
            if '4' in Kind:
                Kind = 'four of a kind'
            elif '3' in Kind and '2' in Kind:
                Kind = 'full house'
            elif '3' in Kind:
                Kind = 'three of a kind'
            elif Kind.count('2') >= 2:
                Kind = 'two pair'
            elif '2' in Kind:
                Kind = 'pair'
            else:
                Kind = 'high card'

            if striaght_flush == True:
                self.player_rank[player] = 'straight flush-9'
            elif Kind == 'four of a kind':
                self.player_rank[player] = 'four of a kind-8'
            elif Kind == 'full house':
                self.player_rank[player] = 'full house-7'
            elif Flush == True:
                self.player_rank[player] = 'flush-6'
            elif Straight == True:
                self.player_rank[player] = 'straight-5'
            elif Kind == 'three of a kind':
                self.player_rank[player] = 'three of a kind-4'
            elif Kind == 'two pair':
                self.player_rank[player] = 'two pair-3'
            elif Kind == 'pair':
                self.player_rank[player] = 'a pair-2'
            elif Kind == 'high card':
                self.player_rank[player] = 'high card-1'

            # cards' num for calculation of high card
            num_players_cards = []
            for card in player_cards:
                num = int(card.split('-')[1])
                if num == 13:  # 2 digit numbers will begin with 9
                    num = 99
                elif num == 12:
                    num = 98
                elif num == 11:
                    num = 97
                elif num == 10:
                    num = 96
                elif int(num) < 10:  # one digit numbers will begin with 8
                    # first concatanate one digit numbers in str
                    num = str(8)+str(num)
                    num = int(num)  # convert str format to int
                num_players_cards.append(int(num))
            # sorting the list from top to down
            num_players_cards.sort(reverse=True)
            for num in num_players_cards:  # adding the number to players_rank dict
                self.player_rank[player] += str(num)

        # calling the winner function that returns the winner name
        return self.winner(players=players), self.player_rank
        # and player_rank dict

    def winner(self, players: list):
        """
        determine the final winner

        inputs -->
        playres: list, list of players

        output: -->
        winner_name: str, name of the winner
        """

        ranking_list = []
        for key, value in play_ground.player_rank.items():
            ranking_list.append((value.split('-')[1], key))
        ranking_list.sort(reverse=True)
        winner_name = ranking_list[0][1]
        return winner_name


class Dealer(play_ground):
    rounds = 0
    bet_size = 0
    this_round_betsize = 0
    pot_size = 0
    players_money = {}

    def __init__(Self, deafult_bet_size: int):
        """
        determining the beginig bet size.

        inputs -->
        deafult_bet_size: the number cant be <= 0

        outputs -->
        none
        """
        if deafult_bet_size > 0:
            Dealer.bet_size = deafult_bet_size
            Dealer.this_round_betsize = deafult_bet_size
        else:
            print(
                f'bet size can"t be {deafult_bet_size}, choose a number greater than zero')

    def result(self, winner_name: str):
        """
        it adds the pot_size money to the winner and at the end it makes
        the pot_size = 0, add one round to rounds, calling the 
        increase_bet_size method.

        inputs -->
        winner_name: str format.

        outputs -->
        Dealer.players_money: dict format

        """
        Dealer.rounds += 1

        Dealer.players_money[winner_name] += Dealer.pot_size
        Dealer.pot_size = 0
        current_bet_Size = Dealer.increase_bet_size(self, Dealer.rounds)
        Dealer.this_round_betsize = current_bet_Size
        return Dealer.players_money

    def increase_bet_size(self, rounds: int):
        """
        this function will be call when the result method from Dealer class
        is called and for each 5 round it makes the bet_size 2 times bigger
        than it's previous size.

        inputs -->
        rounds: int, number of rounds

        outputs -->
        Dealer.bet_size: current bet_size
        """
        if rounds % 5 == 0:
            Dealer.bet_size *= 2
            Dealer.this_round_betsize = Dealer.bet_size
        else:
            print(
                f'The bet size will be increased after {5-(rounds%5)} rounds.')
        return Dealer.bet_size


class Player(Dealer):
    def __init__(self, name: str, money: int):
        """
        the Player class constructor function will recieve the player name
        and it's beggining amount of money.

        inputs -->
        name: str, player's name
        money: int, the begging money amount

        outputs -->
        none
        """
        self.current_money = money
        self.name = name
        Dealer.players_money[self.name] = self.current_money

    @classmethod
    def is_money_remained(self, player: str, expense: int):
        """
        it is a controling class method that will be called when the player wants add
        to the pot size.

        inputs -->
        player: str, player name
        expense: int, amount of money that the player want to pay

        outpus -->
        none
        """
        if Dealer.players_money[player] - expense < 0:
            print(
                f'Oops,you can not bet/raise {expense}, your remaining money is: {Dealer.players_money[player]}')
            Dealer.players_money[player] += expense

    def bet(self, _bet, player):
        """
        this method will be used in post flop rounds.

        inputs -->
        _bet: int, how much player wants to bet.
        player: str, will use in is_money_remained().

        outpus -->
        none
        """
        Player.is_money_remained(
            player, _bet)  # checking if player has enough money
        if _bet < Dealer.this_round_betsize:
            print(
                f"your bet size must be at least {Dealer.this_round_betsize}")
        elif _bet >= Dealer.this_round_betsize:
            Dealer.players_money[self.name] -= _bet
            Dealer.pot_size += _bet
            Dealer.this_round_betsize = _bet

    def call(self, player):
        """
        it will use in prefolop to river.

        inputs -->
        player: str, will be use in is_money_remained().

        outputs -->
        none
        """
        Player.is_money_remained(player, Dealer.this_round_betsize)
        Dealer.players_money[player] -= Dealer.this_round_betsize
        Dealer.pot_size += Dealer.this_round_betsize

    def _raise(self, money, player):
        """
        it will use in preflop ro river.

        inputs -->
        money: int, amount of raise
        player: str, player name

        outputs -->
        none
        """
        Player.is_money_remained(player, money)
        if money >= Dealer.this_round_betsize * 2:
            Dealer.players_money[self.name] -= money
            Dealer.pot_size += money
            Dealer.this_round_betsize = money
        elif money < Dealer.this_round_betsize * 2:
            print(
                f'bet size must be at least 2 times larger than {Dealer.this_round_betsize}')


########################################## debugging lines #####################################
table = play_ground(['mostafa', 'javad', 'ali'])
table.preflop()
table.flop()
table.turn()
table.river()
x, y = table.ranking(['mostafa', 'javad', 'ali'])


# print('mostafa: ',table.dict_players_cards['mostafa']+table.cards_table)
# print('javad: ',table.dict_players_cards['javad']+table.cards_table)
# print('ali: ',table.dict_players_cards['ali']+table.cards_table)
# print('--'*20)
# print(x)
# print('--'*20)
# print(table.player_data)

mostafa = Player('mostafa', 2000)
javad = Player('javad', 3000)
ali = Player('ali', 3000)
mostafa.bet(300, 'mostafa')
javad.call('javad')
ali.call('ali')
mostafa.bet(500, 'mostafa')
javad._raise(1000, 'javad')
ali.call('ali')
mostafa.bet(1000, 'mostafa')
players_money = Dealer.result(Dealer, x)

print(table.cards_table)
print(table.dict_players_cards)
print(table.player_rank)
print(Dealer.players_money)
print('-'*15)
