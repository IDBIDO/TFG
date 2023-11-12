import curses

def main(stdscr):
    # Clear the screen
    stdscr.clear()

    # Define the menu items
    menu_items = ["Option 1", "Option 2", "Option 3"]
    selected_option = 0  # Index of the currently selected option

    # Main loop
    while True:
        # Clear the screen
        stdscr.clear()

        # Print the menu items
        for i, item in enumerate(menu_items):
            if i == selected_option:
                stdscr.addstr(i, 0, f"> {item}", curses.A_BOLD)
            else:
                stdscr.addstr(i, 0, f"  {item}")

        # Refresh the screen
        stdscr.refresh()

        # Get user input
        key = stdscr.getch()

        # Handle user input
        if key == curses.KEY_DOWN and selected_option < len(menu_items) - 1:
            selected_option += 1
        elif key == curses.KEY_UP and selected_option > 0:
            selected_option -= 1
        elif key == ord('\n'):
            # Enter key was pressed; perform an action based on the selected option
            stdscr.addstr(len(menu_items) + 1, 0, f"Selected: {menu_items[selected_option]}")
            stdscr.refresh()
            stdscr.getch()  # Wait for user to press any key
        elif key == ord('q'):
            break  # Exit the program if 'q' is pressed

if __name__ == "__main__":
    curses.wrapper(main)

