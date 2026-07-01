from color import Color

class Message:
    def plain(text):
        print(text)
    def error(text):
        print(f"{Color.BOLD}{Color.RED}Error:{Color.RESET} {text}")
    def warning(text):
        print(f"{Color.BOLD}{Color.YELLOW}Warning:{Color.RESET} {text}")
    def success(text):
        print(f"{Color.BOLD}{Color.GREEN}Success:{Color.RESET} {text}")