import tkinter as tk
import logic

# -------- Rounded Button using Canvas --------
class RButton(tk.Canvas):
    def __init__(self, parent, text, bg, cmd, w=70, h=55, r=18):
        super().__init__(parent, width=w, height=h, bg=parent["bg"], highlightthickness=0)
        self.cmd = cmd
        self.draw(bg, text, w, h, r)
        self.bind("<Button-1>", lambda e: self.cmd())

    def draw(self, bg, text, w, h, r):
        self.create_round(2, 2, w-2, h-2, r, fill=bg, outline="")
        self.create_text(w//2, h//2, text=text, fill="white",
                         font=("Segoe UI", 12, "bold"))

    def create_round(self, x1, y1, x2, y2, r, **kw):
        self.create_arc(x1, y1, x1+2*r, y1+2*r, start=90, extent=90, **kw)
        self.create_arc(x2-2*r, y1, x2, y1+2*r, start=0, extent=90, **kw)
        self.create_arc(x2-2*r, y2-2*r, x2, y2, start=270, extent=90, **kw)
        self.create_arc(x1, y2-2*r, x1+2*r, y2, start=180, extent=90, **kw)
        self.create_rectangle(x1+r, y1, x2-r, y2, **kw)
        self.create_rectangle(x1, y1+r, x2, y2-r, **kw)

# -------- UI --------
def build_ui(root):

    root.configure(bg="black")
    wrap = tk.Frame(root, bg="black")
    wrap.pack(padx=10, pady=10)

    # HISTORY
    history_box = tk.Frame(wrap, bg="#111")
    history_box.pack(fill="x", pady=8)

    tk.Label(history_box, text="History", fg="#aaa", bg="#111").pack(anchor="w")
    history_list = tk.Frame(history_box, bg="#111")
    history_list.pack(fill="x")

    def clear_history():
        for w in history_list.winfo_children():
            w.destroy()

    tk.Button(history_box, text="Clear History", bg="#2f2f31",
              fg="white", relief="flat", command=clear_history).pack(fill="x", pady=5)

    # DISPLAY
    small = tk.Label(wrap, fg="#aaa", bg="black")
    small.pack(anchor="e")

    display = tk.Entry(wrap, font=("Segoe UI", 26), bg="black",
                       fg="white", bd=0, justify="right")
    display.pack(fill="x", pady=10)

    def insert(v): display.insert(tk.END, v)
    def clear(): display.delete(0, tk.END); small.config(text="")
    def delete(): display.delete(len(display.get())-1)

    def sqrt_now():
        try:
            v=float(display.get()); display.delete(0,tk.END); display.insert(0,v**0.5)
        except: display.delete(0,tk.END); display.insert(0,"Error")

    def recip():
        try:
            v=float(display.get()); display.delete(0,tk.END); display.insert(0,1/v)
        except: display.delete(0,tk.END); display.insert(0,"Error")

    def calc():
        try:
            raw=display.get()
            res=logic.evaluate(raw)
            small.config(text=raw+" =")
            display.delete(0,tk.END); display.insert(0,str(res))
            tk.Label(history_list,text=f"{raw} = {res}",fg="#ccc",bg="#111").pack(anchor="w")
        except:
            display.delete(0,tk.END); display.insert(0,"Error")

    pad = tk.Frame(wrap, bg="black")
    pad.pack()

    def place(btn, r, c):
        btn.grid(row=r, column=c, padx=6, pady=6)

    trig_btns = {}

    place(RButton(pad,"2nd","#2f2f31",lambda:logic.toggle_2nd(trig_btns)),0,0)
    btn_deg = RButton(pad,"deg","#2f2f31",lambda:logic.toggle_deg(btn_deg))
    place(btn_deg,0,1)

    trig_btns["sin"]=RButton(pad,"sin","#2f2f31",lambda:logic.trig_insert("sin",insert))
    trig_btns["cos"]=RButton(pad,"cos","#2f2f31",lambda:logic.trig_insert("cos",insert))
    trig_btns["tan"]=RButton(pad,"tan","#2f2f31",lambda:logic.trig_insert("tan",insert))

    place(trig_btns["sin"],0,2)
    place(trig_btns["cos"],0,3)
    place(trig_btns["tan"],0,4)

    def B(t,bg,cmd,r,c): place(RButton(pad,t,bg,cmd),r,c)

    B("xʸ","#2f2f31",lambda:insert("^"),1,0)
    B("lg","#2f2f31",lambda:insert("lg("),1,1)
    B("ln","#2f2f31",lambda:insert("ln("),1,2)
    B("(","#2f2f31",lambda:insert("("),1,3)
    B(")","#2f2f31",lambda:insert(")"),1,4)

    B("√","#2f2f31",sqrt_now,2,0)
    B("AC","#ff9500",clear,2,1)
    B("⌫","#ff9500",delete,2,2)
    B("%","#ff9500",lambda:insert("%"),2,3)
    B("÷","#ff9500",lambda:insert("/"),2,4)

    nums=[("7",3,1),("8",3,2),("9",3,3),
          ("4",4,1),("5",4,2),("6",4,3),
          ("1",5,1),("2",5,2),("3",5,3),
          ("0",6,2)]

    for n,r,c in nums:
        B(n,"#3b3b3d",lambda x=n:insert(x),r,c)

    B("×","#ff9500",lambda:insert("*"),3,4)
    B("-","#ff9500",lambda:insert("-"),4,4)
    B("+","#ff9500",lambda:insert("+"),5,4)

    B("1/x","#2f2f31",recip,3,0)
    B("π","#2f2f31",lambda:insert("pi"),5,0)
    B("Rand","#2f2f31",lambda:insert(logic.rand()),6,0)
    B("e","#2f2f31",lambda:insert("e"),6,1)
    B(".","#3b3b3d",lambda:insert("."),6,3)
    B("=","#ff9500",calc,6,4)
