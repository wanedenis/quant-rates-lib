# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print("Welcome to tip calculator!")
    total = float(input("what was the total bill? \n"))

    tip = int(input("How much tip would you like to give? 10, 12, or 15? \n"))

    number = int(input("How many people to split the bill? \n"))

    rounded_tip = round(total * tip / 100, 2)

    print(f'Hi, {name} + each person should pay; {total // number} ')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
