from cs50 import get_string
import string


def main():
    text = get_string("Text: ")
    grade = get_grade(text)
    if grade >= 16:
        print("Grade 16+")
    elif grade < 1:
        print("Before Grade 1")
    else:
        print(f"Grade: {grade}")
    
    
def get_countings(text):
    counts = {}
    lettersCounter = 0
    wordsCounter = 0
    sentencesCounter = 0
    for i in range(len(text)):
        if text[i] in string.ascii_uppercase + string.ascii_lowercase:
            lettersCounter += 1
        if text[i] == " ":
            wordsCounter += 1
        if text[i] in [".", "!", "?"]:
            sentencesCounter += 1
    counts["letters"] = lettersCounter
    counts["words"] = wordsCounter + 1
    counts["sentences"] = sentencesCounter
    return counts
    
    
def get_grade(text):
    countings = get_countings(text)
    # print(countings)
    L = (countings["letters"] * 100) / countings["words"]
    S = (countings["sentences"] * 100) / countings["words"]
    return round(((0.0588 * L) - (0.296 * S) - 15.8))
    

if __name__ == "__main__":
    main()