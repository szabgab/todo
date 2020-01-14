import tkinter as tk
import os
import json

# TODO: make window much larger and resizable
# TODO: click-right event on an item
# TODO: move items up and down the list
# TODO: remove item
# TODO: double-click allow for editing of the item

class TODOApp(tk.Frame):
    def __init__(self, parent=None, dir_root=None):
        super().__init__(parent)
        self.pack()

        self.dir_root = dir_root
        self.db_path = os.path.join(self.dir_root, 'todo.json')
        if os.path.exists(self.db_path):
            with open(self.db_path) as fh:
                self.data = json.load(fh)
        else:
            self.data = {
                'version': 1,
                'items': [],
            }


        self.QUIT = tk.Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"] = "red"
        self.QUIT["command"] = self.quit
        self.QUIT.pack({"side": "left"})

        self.add_button = tk.Button(self)
        self.add_button["text"] = "Add"
        self.add_button["command"] =  self.show_add
        self.add_button.pack({"side": "left"})

        self.listbox = tk.Listbox(self)
        self.listbox.pack({"side": "bottom"})
        self.listbox.bind("<Double-Button-1>", lambda e:self.double_click())
        self.listbox.bind("<Button-3>", lambda e:self.right_click(e))
        for item in self.data['items']:
            self.listbox.insert(tk.END, item)
        # listbox.delete(0, END)
        # listbox.insert(END, newitem)

        parent.bind('<Alt_L><q>', lambda e: self.quit())
        parent.bind('<Alt_L><a>', lambda e: self.show_add())
        parent.bind('<Escape>', lambda e: print("ESC"))

    def right_click(self, e):
        # TODO: shall we use the right-click to change the current selection or to work on the item where we clicked?
        # print(e) # <ButtonPress event state=Mod1 num=3 x=17 y=6>
        items = self.listbox.curselection()
        print(items)

    def save_data(self):
        #print(self.db_path)
        #print(self.data)
        with open(self.db_path, 'w') as fh:
            json.dump(self.data, fh)

    def double_click(self):
        # TODO: this is a tuple, but when can it have more than one values?
        items = self.listbox.curselection()
        # print(items)
        ix = items[0]
        # print(ix)
        #print(self.listbox.get(ix))
        item = self.listbox.get(ix)
        print(item)

    def add_item(self):
        print("Add item")
        item = self.add_window.text.get()
        print(item)
        self.data['items'].append(str(item))
        # print(self.data)
        self.listbox.insert(tk.END, item)
        self.save_data()

        self.add_window.destroy()

    def show_add(self):
        print("show add")
        # print(self.add_button["text"])
        window = tk.Toplevel(self)
        # window.geometry("300x300+500+200")
        # window["bg"] = "navy"

        window.text = tk.Entry(window)
        window.text.pack({"side": "left"})

        window.add_button = tk.Button(window)
        window.add_button = tk.Button(window)
        window.add_button["text"] = "Add"
        window.add_button["command"] = self.add_item
        window.add_button.pack({"side": "left"})

        self.add_window = window


def main():
    dir_root = os.path.dirname(os.path.abspath(__file__))
    print(dir_root)
    tk_root = tk.Tk()
    app = TODOApp(parent=tk_root, dir_root=dir_root)

    tk_root.lift()
    tk_root.call('wm', 'attributes', '.', '-topmost', True)
    tk_root.after_idle(tk_root.call, 'wm', 'attributes', '.', '-topmost', False)

    app.mainloop()

main()
