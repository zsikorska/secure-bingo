import time

from game.game_screen.game_screen import GameScreen

def mock_game_screen():
    return GameScreen([1, 2, 3, 4, 5,
                       3, 4, 5, 61, 34,
                       1, 87, 3, 9, 5,
                       3, 4, 5, 61, 34,
                       1, 99, 3, 33, 5])

def main():
    screen = mock_game_screen()

    screen.init_game_screen()
    screen.displayer_driver.refresh()

    time.sleep(1)

    screen.mark_card_with_number(61)
    time.sleep(1)
    screen.displayer_driver.refresh()
    
    screen.mark_card_with_number(3)
    time.sleep(1)
    screen.displayer_driver.refresh()
    
    screen.mark_card_with_number(3)
    time.sleep(1)
    screen.displayer_driver.refresh()
    
    screen.mark_card_with_number(5)
    time.sleep(1)
    screen.displayer_driver.refresh()
    
    screen.mark_card_with_number(61)
    time.sleep(1)
    screen.displayer_driver.refresh()
    

    time.sleep(5)

    screen.end()


if __name__ == "__main__":
    exit(main())
