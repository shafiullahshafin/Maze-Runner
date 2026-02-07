import sys
import pygame
import logging
import os
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, CAPTION
from src.menu import MainMenu

def setup_logging():
    log_file = os.path.join(os.path.expanduser("~"), "maze_runner_debug.log")
    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logging.info("Application started")

def main():
    setup_logging()
    try:
        logging.info("Initializing Pygame")
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(CAPTION)
        clock = pygame.time.Clock()

        logging.info("Creating MainMenu")
        menu = MainMenu(screen)
        
        running = True
        logging.info("Entering main loop")
        while running:
            # Handle events and state transitions
            try:
                result = menu.run()
            except Exception as e:
                logging.exception("Exception during menu.run()")
                running = False
                continue

            if result == "quit":
                logging.info("Main loop received 'quit' result")
                running = False
            
            pygame.display.flip()
            clock.tick(60)

        logging.info("Quitting Pygame")
        pygame.quit()
        sys.exit()
    except Exception as e:
        logging.exception("An unhandled exception occurred:")
        try:
            import traceback
            error_msg = traceback.format_exc()
            print(error_msg)
        except:
            pass
        raise e

if __name__ == "__main__":
    main()
