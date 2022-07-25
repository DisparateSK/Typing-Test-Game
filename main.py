import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
import pandas as pd
from texts import text_test
import random

score = 0
game_length = 60  # set length of game to 60 second


class App:
    def __init__(self, root):
        # setting title
        root.title("Typing Speed Test")
        # setting window size
        root.minsize(width=920, height=700)

        self.text_mess = tk.Text(width=75, xscrollcommand="scrollbar")
        ft = tkFont.Font(family='Times', size=13)
        self.text_mess["font"] = ft
        self.text_mess.place(x=120, y=45, height=244)

        self.text_entry = tk.Text(width=75, xscrollcommand="scrollbar")
        ft = tkFont.Font(family='Times', size=13)
        self.text_entry["font"] = ft
        self.text_entry.place(x=120, y=370, height=244)

        start_button = tk.Button(root,
                                 fg="#ffffff",
                                 justify="center",
                                 text="START TEST",
                                 bg="#00babd",
                                 command=self.start_command)
        ft = tkFont.Font(family='Times', size=10)
        start_button["font"] = ft
        start_button.place(x=380, y=330, width=139, height=37)

        leaderdoard_button = tk.Button(root,
                                       fg="#ffffff",
                                       justify="center",
                                       text="TOP 3 Leaderboard",
                                       bg="#00babd",
                                       command=self.show_leaderboard)
        ft = tkFont.Font(family='Times', size=10)
        leaderdoard_button["font"] = ft
        leaderdoard_button.place(x=380, y=630, width=139, height=37)

        label_title = tk.Label(root, justify="center", text="Typing Speed Test")
        ft = tkFont.Font(family='Times', size=14)
        label_title["font"] = ft
        label_title.place(x=330, y=10, width=227, height=30)

        self.user_entry = tk.Entry(root, justify="center", width=20)
        ft = tkFont.Font(family='Times', size=13)
        self.user_entry["font"] = ft
        self.user_entry.place(x=450, y=290)

        label_nickname = tk.Label(root, text="Enter your nickname:")
        ft = tkFont.Font(family='Times', size=13)
        label_nickname["font"] = ft
        label_nickname.place(x=340, y=290, width=153, height=30)

    def show_leaderboard(self):
        leaderboard = rank_board.sort_values(by=['score'], ascending=False, ignore_index=True)
        leaderboard.index = leaderboard.index + 1
        messagebox.showinfo(title="TOP 3 Best of the best",
                            message=f"{leaderboard[0:3]}")

    def start_command(self):
        global text_list, user_nickname
        if len(self.user_entry.get()) < 1:
            messagebox.showinfo(title="Nickname",
                                message="Please, enter your nickname")
            return
        user_nickname = self.user_entry.get()
        self.text_mess.insert(tk.END, random.choice(text_test))
        text = self.text_mess.get("1.0", tk.END)
        text_list = text.split()
        root.after(1000 * game_length, self.count_score)

    def count_score(self):
        global score
        user_text = self.text_entry.get("1.0", tk.END)
        user_list = user_text.split()
        new_list = []
        for word_ind in range(len(user_list)):
            new_word = ''
            for cap_ind in range(min(len(text_list[word_ind]), len(user_list[word_ind]))):
                text_cap = text_list[word_ind][cap_ind]
                user_cap = user_list[word_ind][cap_ind]

                if text_cap == user_cap:
                    score += 1
                    new_word += user_cap
                else:
                    new_word += '\033[91m' + user_cap + '\033[0m'
            new_list.append(new_word)
        new_text = ""
        for word in new_list:
            new_text += word

        rank_board.loc[len(rank_board)] = [user_nickname, int(score)]
        sort_rank_board = rank_board.sort_values(by=['score'], ascending=False, ignore_index=True)
        place = sort_rank_board[sort_rank_board.user == user_nickname][sort_rank_board.score == score].index[0] + 1
        messagebox.showinfo(title=f"{user_nickname} result",
                            message=f"Your score is {score}. Your place is {place} in leaderboard")

        return print(*new_list)


if __name__ == "__main__":
    rank_board = pd.read_csv("rankboar.csv", usecols=["user", "score"])

    root = tk.Tk()
    app = App(root)
    root.mainloop()

    rank_board.to_csv("rankboar.csv")
