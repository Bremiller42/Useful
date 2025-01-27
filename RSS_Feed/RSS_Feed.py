import feedparser
import webbrowser
import tkinter as tk
from tkinter import ttk  # Import ttk for themed widgets
from datetime import datetime, timedelta

DAYS = 7
feed_urls = [
    "https://openai.com/blog/rss.xml",
    "https://machinelearningmastery.com/blog/feed/",
    "https://towardsdatascience.com/feed"
]


class Feed:
    def __init__(self, master):
        self.master = master
        self.master = tk.Tk()
        # self.window = tk.Toplevel(master)
        self.master.title("RSS Feed")
        self.master.geometry("400x800")
        self.master.resizable(False, True)

        # Taskbar
        style = ttk.Style()
        style.configure('TFrame', background='gray')
        self.taskbar = ttk.Frame(self.master, height=65, style='TFrame')
        self.taskbar.pack(side="top", fill="x")

        self.days_label = tk.Label(self.master, text=f"Gathering from last {DAYS} days", font=("Helvetica", 15),
                                   bg="gray")
        self.days_label.place(x=3, y=3)
        self.sources_label = tk.Label(self.master, text=f"{len(feed_urls)} Sources", font=("Helvetica", 15),
                                   bg="gray")
        self.sources_label.place(x=175, y=30)

        self.rss_button = ttk.Button(self.master, text="Get RSS Feeds", command=self.get_feeds)
        self.rss_button.place(x=295, y=6, width=100, height=29)

        self.textbox_scrollbar = tk.Scrollbar(master=self.master)
        self.textbox_scrollbar.pack(side="right", fill="y")
        self.textbox = tk.Text(self.master, height=20, width=50, state="disabled", borderwidth=0, relief="flat",
                               bg="dark gray", wrap=tk.WORD, yscrollcommand=self.textbox_scrollbar.set)
        self.textbox.pack(side="bottom", fill="both", expand=True)
        self.textbox_scrollbar.config(command=self.textbox.yview)
        self.textbox_scrollbar.bind("<Enter>", lambda event: self.textbox_scrollbar.config(cursor="hand2"))
        self.textbox_scrollbar.bind("<Leave>", lambda event: self.textbox_scrollbar.config(cursor=""))

        self.textbox.bind("<Configure>", self.update_scrollbar)

        self.days_combobox = ttk.Combobox(self.master, values=["1", "3", "7", "14", "30"], width=6, state="readonly")
        self.days_combobox.set(7)  # Set default value to 7
        self.days_combobox.place(x=335, y=40)
        self.days_combobox.bind("<<ComboboxSelected>>", self.update_days)

        self.days_text = tk.Label(self.master, height=1, width=4, state="normal", borderwidth=0,
                                  fg='black', bg="gray", text="Days", font=("Helvetica", 10))
        self.days_text.place(x=295, y=42)

    def update_scrollbar(self, *args):
        self.textbox_scrollbar.config(command=self.textbox.yview)

    def mainloop(self):
        self.master.mainloop()

    def get_feeds(self):
        self.textbox.config(state="normal")  # Enable the Textbox
        self.textbox.delete('1.0', tk.END)  # Clear the Textbox
        self.textbox.insert(tk.END, f"Feeds from last {DAYS} days:\n")
        for feed_url in feed_urls:
            posts = self.fetch_posts_from_feed(feed_url)
            self.display_posts(posts)
        self.textbox.config(state="disabled")  # Disable the Textbox after updating

    def fetch_posts_from_feed(self, feed_url):
        print(f"Reading Feed: {feed_url}")
        feed = feedparser.parse(feed_url)
        posts = []
        thirty_days_ago = datetime.now() - timedelta(days=DAYS)
        for entry in feed.entries:
            published_date_str = entry.published[5:16]
            published_date = datetime.strptime(published_date_str, "%d %b %Y")
            if published_date >= thirty_days_ago:
                post = {
                    'title': entry.title,
                    'link': entry.link,
                    'published': entry.published,
                }
                posts.append(post)
            else:
                continue
        if posts:
            return posts
        else:
            print("No new posts found\n")

    def open_link(self, link):
        webbrowser.open_new(link)

    def display_posts(self, posts):
        if posts:
            for idx, post in enumerate(posts):
                self.textbox.insert(tk.END, f'{post["title"]}\n', ('title_text',))
                self.textbox.tag_configure('title_text', font=('Helvetica', 14))  # Change 14 to the desired font size

                self.textbox.insert(tk.END, f'Published: {post["published"]}\n')
                # Insert the link with a tag to make it clickable
                self.textbox.insert(tk.END, f'{post["link"]}\n\n', "link")
                # Make the link clickable
                self.textbox.tag_config("link", foreground="blue", underline=True)
                self.textbox.tag_bind("link", "<Button-1>", lambda event, link=post["link"]: self.open_link(link))
                self.textbox.tag_bind("link", "<Enter>", lambda event: self.textbox.config(cursor="hand2"))
                self.textbox.tag_bind("link", "<Leave>", lambda event: self.textbox.config(cursor=""))

    def update_days(self, event):
        global DAYS
        DAYS = int(self.days_combobox.get())
        if DAYS == 1:
            self.days_label.config(text=f"Gathering from last {DAYS} day")
        else:
            self.days_label.config(text=f"Gathering from last {DAYS} days")


def main():
    feed = Feed(None)
    feed.mainloop()


if __name__ == '__main__':
    main()