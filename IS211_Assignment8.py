import random
import argparse
import time


class Player:
    def __init__(self, identity):

        self.identityEnc = identity
        self.scoreEnc = 0
        self.tempScore = 0
        self.tempScorePrev = 0
        self.isWinnerEnc = False

    def identity(self):

        return self.identityEnc

    def score(self):

        return self.scoreEnc

    def subtract_from_score(self, sub):

        self.scoreEnc -= sub

    def previous_hold_score(self):

        return self.tempScorePrev

    def is_winner(self):

        return self.isWinnerEnc

    def make_winner(self):

        self.isWinnerEnc = True

    def roll_die(self):
        random.seed(time.time())
        current_roll = int(random.random() * 6) + 1
        self.tempScore += current_roll

        if current_roll == 1:
            print "YOU ROLLED A 1. 0 POINTS FOR THIS ROLL. NEXT PLAYER'S TURN."
        else:
            print "\nROLL : %i , POSSIBLE POINTS: %i"% (current_roll, self.tempScore)

        return current_roll

    def decide(self, rolled_value):

        if rolled_value == 1:
            self.tempScore = 0
            print "PLAYER %i'S SCORE IS NOW %i\n" % \
                  (self.identity(), self.scoreEnc)
            return 1

        if self.tempScore + self.scoreEnc >= 100:
            print "Total points      : %i" % \
                  (self.tempScore + self.scoreEnc)
            print "\n********************\n      PLAYER %i      \n" \
                  "      %i points      \n   IS THE WINNER    \n" \
                  "********************" % (self.identity(),
                                            self.tempScore + self.scoreEnc)
            self.isWinnerEnc = True
            return 0

        decision = raw_input("Type 'r' for roll and 'h' for hold. "
                             "Decision: ")

        while decision != "r" and decision != "h":
            decision = raw_input("Error. Please only type 'r' for roll "
                                 "and 'h' for hold. Decision: ")

        if decision == "h":
            self.scoreEnc += self.tempScore
            self.tempScorePrev = self.tempScore
            self.tempScore = 0
            print "PLAYER %i'S SCORE IS NOW %i\n" % \
                  (self.identity(), self.scoreEnc)
            return 2

        if decision == "r":
            return 3

        print ""


class ComputerPlayer(Player):
    def decide(self, rolled_value):

        if rolled_value == 1:
            self.tempScore = 0
            print "PLAYER %i'S SCORE: %i\n" % \
                  (self.identity(), self.scoreEnc)
            return 1

        if self.tempScore + self.scoreEnc >= 100:
            print "\n********************\n      PLAYER %i      \n" \
                  "      %i points      \n   IS THE WINNER    \n" \
                  "********************" % (self.identity(),
                                            self.tempScore + self.scoreEnc)
            self.isWinnerEnc = True
            return 0

        decision = "h"

        if (100 - self.scoreEnc) >= 25:
            if self.tempScore < 25:
                decision = "r"
        else:
            if self.tempScore < (100 - self.scoreEnc):
                decision = "r"

        if decision == "h":
            print "  Computer has decided to HOLD."
            self.scoreEnc += self.tempScore
            self.tempScorePrev = self.tempScore
            self.tempScore = 0
            print "PLAYER %i'S SCORE IS NOW %i\n" % (self.identity(),
                                                     self.scoreEnc)
            return 2

        if decision == "r":
            print "  Computer has decided to ROLL."
            return 3

        print ""


class PlayerFactory:
    def get_player(self, identity, type_of_player):

        if type_of_player == "computer":
            return ComputerPlayer(identity)

        if type_of_player == "human":
            return Player(identity)


class Game:
    def __init__(self, player1, player2):
        self.listOfPlayers = []
        self.listOfPlayers.append(player1)
        self.listOfPlayers.append(player2)

    def number_of_players(self):
        return len(self.listOfPlayers)

    def player_list(self):
        return self.listOfPlayers

    def roll_game_die(self, player):
        return player.roll_die()

    def decide(self, roll_die_value, player):
        return player.decide(roll_die_value)

    def reset_game(self):
        for x in range(0, len(self.listOfPlayers)):
            self.listOfPlayers.pop()


class TimedGameProxy(Game):
    def __init__(self, playerA, playerB):

        self.listOfPlayers = []
        self.startTime = time.time()
        self.listOfPlayers.append(playerA)
        self.listOfPlayers.append(playerB)

    def start_game(self):

        winner = 0
        result = 3
        exists_no_winner = True

        while exists_no_winner and (60 - (time.time() - self.startTime)) > 0:

            for player in self.listOfPlayers:

                print "********************\n      PLAYER %i      " \
                      "\n      %i points\n********************" % \
                      (player.identity(), player.score())

                """From PLAYER's decide() function:

                0 = won game; game will be finished
                1 = lose turn; give the other player a turn
                2 = hold; give the other player a turn
                3 = roll; turn is yielded back to current player
                4 = ran out of time; game will be finished
                """
                while result == 3:
                    print "SECONDS LEFT: %f" % (60 - (time.time()
                                                      - self.startTime))
                    if (60 - (time.time() - self.startTime)) < 0:
                        result = 4
                        print "GAME OVER: Time is up!"
                        break
                    else:
                        resulting_face = self.roll_game_die(player)

                    print "SECONDS LEFT: %f" % (60 - (time.time()
                                                      - self.startTime))
                    if (60 - (time.time() - self.startTime)) < 0:
                        result = 4
                        print "GAME OVER: Time is up!"
                        break
                    else:
                        result = self.decide(resulting_face, player)

                        if (60 - (time.time() - self.startTime)) < 0:
                            print "GAME OVER: Time is up!"

                            if result == 2:
                                prev_score = player.previous_hold_score()
                                overtime = (time.time() - self.startTime) - 60
                                print "ALERT: Cannot add %i points since" \
                                      " game is already over by %f secon" \
                                      "ds." % (prev_score, overtime)
                                player.subtract_from_score(
                                    player.previous_hold_score())

                            result = 4
                            break

                if result == 4:
                    if self.listOfPlayers[0].score() > \
                            self.listOfPlayers[1].score():
                        self.listOfPlayers[0].make_winner()
                        winner = "1"
                    elif self.listOfPlayers[0].score() < \
                            self.listOfPlayers[1].score():
                        self.listOfPlayers[1].make_winner()
                        winner = "2"
                    else:
                        self.listOfPlayers[0].make_winner()
                        self.listOfPlayers[1].make_winner()
                        winner = "1 & 2"
                    exists_no_winner = False
                    print "\n********************\n      PLAYER %s      " \
                          "\n   IS THE WINNER    \n********************" \
                          "\nPlayer 1 Points: %i\nPlayer 2 Points: %i" % \
                          (winner, self.listOfPlayers[0].score(),
                           self.listOfPlayers[1].score())
                    break

                if result == 0:
                    exists_no_winner = False
                    break

                result = 3


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--player1", help="Indicate if player 1 is 'human'"
                                          " or 'computer'.")
    parser.add_argument("--player2", help="Indicate if player 2 is 'human'"
                                          " or 'computer'.")
    parser.add_argument("--timed", help="Indicate if game is timed to 60"
                                        " seconds. Type 'yes' or 'no'.")

    args = parser.parse_args()

    try:
        player1_choice = args.player1.lower()
        player2_choice = args.player2.lower()
        timed_game = args.timed.lower()

    except AttributeError:
        print "ALERT: You need to choose 'human' or 'computer' for " \
              "players and 'yes' or 'no' for a timed version."
        exit(1)

    if player1_choice != "human" and player1_choice != "computer":
        print "ALERT: You need to type 'human' or 'player' for --player1."
        exit(1)
    if player2_choice != "human" and player2_choice != "computer":
        print "ALERT: You need to type 'human' or 'player' for --player2."
        exit(1)
    if timed_game != "yes" and timed_game != "no":
        print "ALERT: You need to type 'yes' or 'no' for --timed. "
        exit(1)

    factory = PlayerFactory()
    player1 = factory.get_player(1, player1_choice)
    player2 = factory.get_player(2, player2_choice)

    print "\n==================================================\n" \
          "                BEGINNING PIG GAME                \n" \
          "=================================================="

    if timed_game == "yes":
        print "TIMED VERSION\n"
        timed_game = TimedGameProxy(player1, player2)
        timed_game.start_game()
        timed_game.reset_game()

    elif timed_game == "no":
        game1 = Game(player1, player2)

        exists_no_winner = True
        result = 3

        while exists_no_winner:

            for player in game1.player_list():
                print "********************\n      PLAYER %i      " \
                      "\n      %i points\n********************" % \
                      (player.identity(), player.score())

                while result == 3:
                    resulting_face = game1.roll_game_die(player)
                    result = game1.decide(resulting_face, player)

                if result == 0:
                    exists_no_winner = False
                    break

                result = 3

        game1.reset_game()

    print "\n==================================================\n" \
          "                     GAME END                     \n" \
          "==================================================\n"


if __name__ == "__main__":
    main()