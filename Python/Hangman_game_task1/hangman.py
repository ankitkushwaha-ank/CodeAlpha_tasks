import random

def hangman():
    words = ["python", "java", "developer", "error", "random"]
    word = random.choice(words)

    guessed = ["_"] * len(word)
    guessed_letters = []
    attempts = 6

    print("🎮 Welcome to Hangman!")
    print("I’m thinking of a word related to programming.")
    print("Your challenge: Guess the word, one letter at a time!")
    print("👉 Word to guess: ", " ".join(guessed))

    while attempts > 0 and "_" in guessed:
        guess = input("\n🔤 Enter a letter: ").lower()

        if len(guess) != 1 or not guess.isalpha():
            print("⚠️ Please enter just *one* alphabet letter.")
            continue

        if guess in guessed_letters:
            print(f"🤔 You already tried '{guess}'. Pick another letter.")
            continue

        guessed_letters.append(guess)

        if guess in word:
            for i in range(len(word)):
                if word[i] == guess:
                    guessed[i] = guess
            print(f"✅ Nice! '{guess}' is in the word.")
            print("👉 Word now: ", " ".join(guessed))
        else:
            attempts -= 1
            print(f"❌ Oops! '{guess}' is not in the word.")
            print(f"💡 Attempts left: {attempts}")
            print("👉 Word so far: ", " ".join(guessed))

    if "_" not in guessed:
        print("\n🎉 Woohoo! You guessed the word:", word.upper())
        print("👏 Great job, programmer!")
    else:
        print("\n💀 Game Over!")
        print("The word was:", word.upper())
        print("Don’t worry, you’ll crack it next time 😉")


hangman()
