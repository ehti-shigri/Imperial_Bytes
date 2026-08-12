import random

print("Let's play Rock Paper Scissors!")

while True:
    print("\nPick one:")
    print("r = rock")
    print("p = paper")
    print("s = scissors")
    print("q = quit")
    
    player = input("Your choice: ")
    
    if player == "q":
        print("Thanks for playing!")
        break
    
    if player not in ["r", "p", "s"]:
        print("Type r, p, or s only!")
        continue
    

    if player == "r":
        player_choice = "rock"
    elif player == "p":
        player_choice = "paper"
    else:
        player_choice = "scissors"
    
  
    computer_list = ["rock", "paper", "scissors"]
    computer_choice = random.choice(computer_list)
    
    print(f"\nYou picked: {player_choice}")
    print(f"Computer picked: {computer_choice}")
    
    
    if player_choice == computer_choice:
        print("It's a tie!")
    elif player_choice == "rock" and computer_choice == "scissors":
        print("You win!")
    elif player_choice == "paper" and computer_choice == "rock":
        print("You win!")
    elif player_choice == "scissors" and computer_choice == "paper":
        print("You win!")
    else:
        print("Computer wins!")