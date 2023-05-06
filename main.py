from downloader import Downloader, DownloaderDlp

import tkinter as tk
from tkinter import ttk, messagebox

class MainFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.init_ui()

    def init_ui(self):
        lbl_url = ttk.Label(self.master, text='Youtube URL')
        self.txt_url = ttk.Entry(self.master, width=40)
        btn_fetch_streams = ttk.Button(self.master, 
                                       text='Fetch Streams')
        btn_fetch_streams.bind('<Button-1>', self.btn_fetch_clicked)
        self.lbl_video_title = ttk.Label(self.master, text='[Title Here...]')
        self.table = ttk.Treeview(self.master, 
                                  show='headings', 
                                  columns=('itag', 'mime_type', 'resolution', 'type'))

        tbl = self.table
        tbl.bind('<Double-1>', self.row_double_clicked)

        lbl_url.pack(pady=5)
        self.txt_url.pack(padx=10, pady=5, fill='x')
        btn_fetch_streams.pack(pady=5)
        self.lbl_video_title.pack(pady=5)
        tbl.pack(padx=10, pady=5, fill='both', expand=True)

    def btn_fetch_clicked(self, event):
        url = self.txt_url.get()

        if url == "":
            # Show error message
            messagebox.showerror(title='Error', message='URL must not be empty.')
            return
        
        self.downloader = DownloaderDlp(self.txt_url.get())
        
        streams = self.downloader.fetch_streams()

        columns = list(streams[0].keys())
        self.table['columns'] = columns

        for col in columns:
            self.table.heading(col, text=col)
        
        self.populate_table(streams)

    def populate_table(self, streams):
        for item in self.table.get_children():
            self.table.delete(item)

        for item in streams:
            values = list(item.values())
            self.table.insert('', 'end', values=values)

    def row_double_clicked(self, evt):
        children = self.table.get_children()

        if len(children) == 0:
            messagebox.showwarning(title='No selected stream.', 
                                   message='Fetch streams for the youtube video first to download.')
            return

        selected_item = self.table.selection()[0]
        values = self.table.item(selected_item, 'values')
        id = values[0]
        self.downloader.download(id)



if __name__ == '__main__':
    root = tk.Tk()
    style = ttk.Style(root)
    style.theme_use('clam')
    root.title('Youtube Downloader')

    window = MainFrame(root)

    root.mainloop()
    