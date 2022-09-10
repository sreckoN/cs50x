from cs50 import get_string


def main():
    # Asks the user for the card number and prints the type
    number = get_string("Number: ")
    cardType = getCardType(number)
    print(cardType)


def getCardType(number):
    # Accepts the card number and returns the type
    begining = number[0] + number[1]
    print(begining)
    if begining in ["34", "37"]:
        return "AMEX"
    elif begining in ["51", "52", "53", "54", "55"]:
        return "MASTERCARD"
    elif begining[0] in ["4"]:
        return "VISA"
    else:
        return "INVALID"


if __name__ == "__main__":
    main()