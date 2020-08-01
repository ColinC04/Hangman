##
# A Hangman game created using pygame
#
# @authour Colin Chambachan
# @date 

"""
 Pygame base template for opening a window
 
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
 Explanation video: http://youtu.be/vRB_983kUMc
"""

import pygame
import random
import string
import time

## MODEL - Data used in system
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
LIGHTGRAY = (128, 128, 128)

pygame.init()
 
# Set the width and height of the screen [width, height]
size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Hangman!")

class HangmanImage(pygame.sprite.Sprite):
    """ A class created for the images being loaded into the game """
    ## Methods
    def __init__(self):
        """ The constructor function """
        # Call the parent constructor
        super().__init__

        # Creating attributes for the class
        self.image = pygame.image.load("hangman0.png")

        # Make the image mapped
        self.rect = self.image.get_rect()
        self.rect.x = 250
        self.rect.y = 125
    
    def updateImage(self, listOfHangmanImages, imageChosen):
        """ Updates the image of the hangman, depending on how the user is doing"""
        self.image = pygame.image.load(listOfHangmanImages[imageChosen])

    def draw(self):
        """ Blits the image onto the screen """
        screen.blit(self.image,self.rect)

def game_display(setGameAnswer, userGuessedLetters,fontForWords,fontForGuess,correct_sound):
    """ Displaying the word with blanks and guessed letters """
    global size
    ## Answer with words and blanks
    gameDisplay = ""
    for letter in gameAnswer:
        if letter in userGuessedLetters:
            gameDisplay += letter + " "

        else:
            gameDisplay += "_ "
            
    # Renders font and centers it on screen, then blits it to the screen
    gameDisplayText = fontForWords.render(gameDisplay,False, BLACK)
    textXLocation = (size[0]/2) - (gameDisplayText.get_width()/2)
    screen.blit(gameDisplayText,[textXLocation, 400])

    ## Displaying the letters that the users already guessed
    # Creating and rendering the letters the user already guessed
    joinedGuessedLetters = ', '.join(userGuessedLetters)
    lettersGuessedText = fontForGuess.render("Letters Guessed: ", False, BLACK)
    lettersChosenText = fontForGuess.render(joinedGuessedLetters, False, BLACK)
    # Displaying the letters that the user already guessed
    screen.blit(lettersGuessedText,[10,5])
    screen.blit(lettersChosenText,[10,50])

    return gameDisplay

def game_lost(fontForLoss,fontForWord,wordAnswer):
    global size
    # Render and blit the initial font for the lost screen
    text = fontForLoss.render("You Lost! The Word Was ", False, BLACK)
    screen.blit(text, [32.5, 350])

    # Render and blit the answer to the game
    pygame.draw.rect(screen,LIGHTGRAY,[0,410,70000])
    text = fontForWord.render(wordAnswer, False, BLACK)
    textXCoordinate = (size[0]/2) - (text.get_width()/2)
    screen.blit(text,[textXCoordinate,400])


    # Update the screen and end the game
    pygame.display.flip()
    time.sleep(3)

def game_won(fontForWin):
    global size
    # Render and blit the initial font for the lost screen
    text = fontForWin.render("Nice! You Got the Word!", False, BLACK)
    textXCoordinate = (size[0]/2) - (text.get_width()/2)
    screen.blit(text, [textXCoordinate, 350])

    # Update the screen and end the game
    pygame.display.flip()
    time.sleep(3)


## Creating the sounds of the game
# Music that going to played throughout the game
game_music = pygame.mixer.Sound("GameMusic.wav")
game_music.set_volume(0.5)
# Music to signify the user won
word_guessed = pygame.mixer.Sound("GameWon.wav")
word_guessed.set_volume(0.5)
# Music to signify the user lost
word_not_guessed = pygame.mixer.Sound("GameLost.wav")
word_not_guessed.set_volume(0.5)
# Music played when a guess is made, and dependant
correct_guess = pygame.mixer.Sound("CorrectGuess.wav")
correct_guess.set_volume(0.5)
incorrect_guess = pygame.mixer.Sound("IncorrectGuess.wav")

# Loop until the user clicks the close button.
done = False
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
## Hangman Image
# Create a list to easily change the image name of the list
listOfHangmanStages = ["hangman0.png","hangman1.png","hangman2.png","hangman3.png","hangman4.png","hangman5.png",]
imageSelector = 0
# Create an instance of the hangman image class
hangman_image = HangmanImage()

## Deciding the answer of the game
# Open the file containing all the possible answers
fileOfWords = open("PossibleWords.txt","r").readlines()
# Create a list of answers to randomly choose the answer
listOfPossibleAnswers = []
for line in fileOfWords:
    # Appends the line from the text file without the return key at the end
    listOfPossibleAnswers.append(line.strip())
# Decide on the answer for the game
gameAnswer = listOfPossibleAnswers[random.randrange(len(listOfPossibleAnswers)-1)]

## Creating fonts
WORDFONT = pygame.font.SysFont("comicsansms", 45, False, False)
GUESSFONT = pygame.font.SysFont("comicsansms", 30, True, False)
ENDFONT = pygame.font.SysFont("comicsansms", 50, True, False)
# Create a list of letters guessed by the user
lettersGuessed = []

# Play the game music
game_music.play()


# -------- Main Program Loop -----------
while not done:
    ## CONTROL
    # --- Main event loop

    for event in pygame.event.get():
        # Check to see if the user quit the game
        if event.type == pygame.QUIT:
            done = True
        # Check to see if the user made a guess
        elif event.type == pygame.KEYDOWN:
            inputtedKey = pygame.key.name(event.key).upper()
            # Data Validation as to whether or not the user pressed a vaild key
            if inputtedKey in string.ascii_uppercase:
                # Check to see if the letter was already guessed
                if inputtedKey not in lettersGuessed:
                    # Append the to a list holding all the letters the user guessed
                    lettersGuessed.append(inputtedKey)
                    # User got the answer wrong
                    if inputtedKey not in gameAnswer:
                        imageSelector +=1
                        # Play sound that the user got a letter right
                        incorrect_guess.play()

                    # User got the answer right
                    else:
                        correct_guess.play()
    
    
    # --- Game logic should go here


    # Update the image of the hangman
    hangman_image.updateImage(listOfHangmanStages, imageSelector)
    
    # --- Screen-clearing code goes here
    # background image.
    screen.fill(LIGHTGRAY)
      
    ## VIEW
    # --- Drawing code should go here
    # Draw the needed hangman image
    hangman_image.draw()
    # Output the word with the blanks and the letters that the users guessed    
    x = game_display(gameAnswer,lettersGuessed,WORDFONT,GUESSFONT, correct_guess)
    

    ## Test if the game ended
    # Check to see if the user lost the game by checking if the game is on the last image or if the user won by having no blanks remaning
    if imageSelector == 5 or "_" not in x:
        done = True

    
    # --- Go ahead and update the screen with what we've drawn.sld
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)

## Check to see if the user won or lost
if imageSelector == 5:
    # Play the sound queue that the user lost
    word_not_guessed.play()
    # Output the final screen then close
    game_lost(ENDFONT,WORDFONT,gameAnswer)


if "_" not in x:
    # Play the sound queue to see that the user won
    word_guessed.play()
    # Call the function which lets the user know that they won
    game_won(ENDFONT)

# Close the window and quit.
pygame.quit()