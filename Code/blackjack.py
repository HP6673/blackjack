import tkinter as tk
import random

# Function to deal a card
def deal_card():
    return random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11])

# Function to calculate the score of a hand
def calculate_score(hand):
    score = sum(hand)
    if score == 21 and len(hand) == 2:  # Special case for Blackjack
        return 0
    if 11 in hand and score > 21:  # Adjust for Ace being 1 if over 21
        hand[hand.index(11)] = 1
    return sum(hand)

# Function to compare the scores of the player and dealer
def compare(player, dealer):
    if player > 21:
        return "You went over. You lose 😭"
    if dealer > 21:
        return "Dealer went over. You win 😁"
    if player == dealer:
        return "Draw 🙃"
    if player == 0:
        return "Blackjack! You win 😎"
    if dealer == 0:
        return "Dealer has Blackjack! You lose 😱"
    if player > dealer:
        return "You win 😃"
    return "You lose 😤"

# Blackjack game class
class Blackjack:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack Casino")

        # Initialize score counters
        self.wins = self.losses = self.draws = 0

        # Setting up the labels for the interface
        self.status = tk.Label(root, font=("Arial", 14))
        self.scoreboard = tk.Label(root, font=("Arial", 12))
        self.dealer_label = tk.Label(root, font=("Arial", 12))
        self.player_label = tk.Label(root, font=("Arial", 12))
        self.result = tk.Label(root, font=("Arial", 14, "bold"))

        # Place the labels in the window
        self.status.pack(pady=10)
        self.scoreboard.pack()
        self.dealer_label.pack()
        self.player_label.pack()
        self.result.pack(pady=10)

        # Frame for the buttons
        frame = tk.Frame(root)
        frame.pack()
        tk.Button(frame, text="Hit", width=12, command=self.hit).grid(row=0, column=0, padx=5)
        tk.Button(frame, text="Stand", width=12, command=self.stand).grid(row=0, column=1, padx=5)
        tk.Button(root, text="Play Again", width=25, command=self.start_game).pack(pady=10)

        # Start a new game
        self.start_game()

    # Update the labels to show the current hands
    def update_labels(self, reveal=False):
        player_score = calculate_score(self.player_hand)
        dealer_score = calculate_score(self.dealer_hand) if reveal else "?"
        dealer_hand = self.dealer_hand if reveal else [self.dealer_hand[0], "❓"]
        self.player_label.config(text=f"Your hand: {self.player_hand} (Score: {player_score})")
        self.dealer_label.config(text=f"Dealer's hand: {dealer_hand} (Score: {dealer_score})")

    # Start a new game
    def start_game(self):
        self.player_hand = [deal_card(), deal_card()]
        self.dealer_hand = [deal_card(), deal_card()]
        self.result.config(text="")
        self.status.config(text="Game in progress...")
        self.update_labels()

    # When player hits, they get a new card
    def hit(self):
        self.player_hand.append(deal_card())
        self.update_labels()
        if calculate_score(self.player_hand) > 21:
            self.end_game()

    # When player stands, the dealer plays
    def stand(self):
        while calculate_score(self.dealer_hand) < 17:
            self.dealer_hand.append(deal_card())
        self.end_game()

    # End the game, compare scores and update labels
    def end_game(self):
        self.update_labels(reveal=True)
        player_score = calculate_score(self.player_hand)
        dealer_score = calculate_score(self.dealer_hand)
        result_text = compare(player_score, dealer_score)
        self.result.config(text=result_text)
        self.status.config(text="Round over.")
        
        # Update win/loss/draw counters
        if "win" in result_text.lower():
            self.wins += 1
        elif "lose" in result_text.lower():
            self.losses += 1
        else:
            self.draws += 1
        self.scoreboard.config(text=f"Wins: {self.wins} | Losses: {self.losses} | Draws: {self.draws}")

# Run the game
root = tk.Tk()
Blackjack(root)
root.mainloop()
