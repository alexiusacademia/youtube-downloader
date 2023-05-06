from downloader import DownloaderDlp

import tkinter as tk
from tkinter import ttk, messagebox

import threading

class MainFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.init_ui()

    def init_ui(self):
        """
        Initialize the widgets
        """
        lbl_url = ttk.Label(self.master, text='Youtube URL')
        self.txt_url = ttk.Entry(self.master, width=40)
        btn_fetch_streams = ttk.Button(self.master, 
                                       text='Fetch Streams')
        self.lbl_video_title = ttk.Label(self.master, text='[Title Here...]')
        self.table = ttk.Treeview(self.master, 
                                  show='headings', 
                                  columns=('itag', 'mime_type', 'resolution', 'type'))

        tbl = self.table

        lbl_url.pack(pady=5)
        self.txt_url.pack(padx=10, pady=5, fill='x')
        btn_fetch_streams.pack(pady=5)
        self.lbl_video_title.pack(pady=5)
        tbl.pack(padx=10, pady=5, fill='both', expand=True)

        self.lbl_percent = ttk.Label(self.master, text='Status: 0%')
        self.lbl_percent.pack(pady=5)

        self.progress_bar = ttk.Progressbar(self.master, orient='horizontal', mode='determinate', maximum=100, value=0)
        self.progress_bar.pack(padx=10, pady=5, fill='x')

        # Bindings
        btn_fetch_streams.bind('<Button-1>', self.btn_fetch_clicked)
        tbl.bind('<Double-1>', self.row_double_clicked)

    def btn_fetch_clicked(self, event):
        url = self.txt_url.get()  # Fetch the URL from the input

        if url == "":
            # Show error message when there is no URL input
            # Note that we are only testing the rror against empty input here and not the invalid input yet.
            messagebox.showerror(title='Error', message='URL must not be empty.')
            return
        
        # Initialize the downloader object
        self.downloader = DownloaderDlp(self.txt_url.get(), self.progress_bar, self.lbl_percent)

        # Update the title of the video in the UI
        self.lbl_video_title.config(text=self.downloader.get_title())

        # Get the available stream formats of the video
        streams = self.downloader.fetch_streams()

        # Set the table column keys
        columns = list(streams[0].keys())
        self.table['columns'] = columns

        # Set the column header titles
        for col in columns:
            self.table.heading(col, text=col)
        
        # Populate the table
        self.populate_table(streams)

    def populate_table(self, streams):
        """
        Populate the table rows

        Args:
            streams (list): List of dictionaries for the stream formats.
        """
        # Clear any existing rows if any
        for item in self.table.get_children():
            self.table.delete(item)

        # Repopulate the table rows
        for item in streams:
            values = list(item.values())
            self.table.insert('', 'end', values=values)

    def row_double_clicked(self, evt):
        """
        Function to call when a row in the table is double-clicked using the left
        mouse button.
        """
        children = self.table.get_children()

        if len(children) == 0:
            messagebox.showwarning(title='No selected stream.', 
                                   message='Fetch streams for the youtube video first to download.')
            return

        selected_item = self.table.selection()[0]
        values = self.table.item(selected_item, 'values')
        id = values[0]

        thread_download = threading.Thread(target=self.downloader.download, args=[id])
        thread_download.start()


if __name__ == '__main__':
    root = tk.Tk()
    style = ttk.Style(root)
    style.theme_use('clam')
    root.title('Youtube Downloader')

    window = MainFrame(root)

    root.mainloop()
    