from Run.Solution import Solution

# from Game import Game

if __name__ == '__main__':
    action_list = Solution('./Assets/Input/map1.txt',
                           './Assets/Output/result1.txt').solve()
    print(action_list)
    # game = Game()
    # game.run()
