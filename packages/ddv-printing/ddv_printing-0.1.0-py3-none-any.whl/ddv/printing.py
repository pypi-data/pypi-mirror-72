from colorama import Fore, Back, Style

# Symbols from:
# https://fsymbols.com/signs/square/


def print_h1(message):
    if "\n" in message:
        lines = message.split("\n")
    else:
        lines = [message]
    for line in lines:
        print(f"\n{Style.BRIGHT}{Fore.BLUE}▉ {line.upper()}{Style.RESET_ALL}")


def print_h2(message):
    if "\n" in message:
        lines = message.split("\n")
    else:
        lines = [message]
    for line in lines:
        print(
            f"\n{Style.BRIGHT}{Fore.BLUE}▋ {Style.RESET_ALL}{Style.BRIGHT}{line}{Style.RESET_ALL}"
        )


def print_h3(message):
    if "\n" in message:
        lines = message.split("\n")
    else:
        lines = [message]
    for line in lines:
        print(f"\n{Fore.BLUE}▍ {Style.RESET_ALL}{line}{Style.RESET_ALL}")


def print_ok(message):
    if "\n" in message:
        lines = message.split("\n")
    else:
        lines = [message]
    for line in lines:
        print(f"{Style.BRIGHT}{Fore.GREEN}[ OK ]{Style.RESET_ALL} {line}")


def print_pass(message):
    if "\n" in message:
        lines = message.split("\n")
    else:
        lines = [message]
    for line in lines:
        print(f"{Style.BRIGHT}{Fore.GREEN}[ PASS ]{Style.RESET_ALL} {line}")


def print_warn(message):
    if "\n" in message:
        lines = message.split("\n")
    else:
        lines = [message]
    for line in lines:
        print(f"{Style.BRIGHT}{Fore.YELLOW}[ WARN ]{Style.RESET_ALL} {line}")


def print_fail(message):
    if "\n" in message:
        lines = message.split("\n")
    else:
        lines = [message]
    for line in lines:
        print(f"{Style.BRIGHT}{Fore.RED}[ FAIL ]{Style.RESET_ALL} {line}")


def print_error(message):
    if "\n" in message:
        lines = message.split("\n")
    else:
        lines = [message]
    for line in lines:
        print(
            f"{Style.BRIGHT}{Fore.RED}[ ERROR ]{Style.RESET_ALL} {Fore.RED}{line}{Style.RESET_ALL}"
        )


def print_fatal(message):
    if "\n" in message:
        lines = message.split("\n")
    else:
        lines = [message]
    for line in lines:
        print(f"{Style.BRIGHT}{Back.RED}{Fore.WHITE}[ FATAL ] {line}{Style.RESET_ALL}")
