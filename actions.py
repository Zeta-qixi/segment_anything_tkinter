from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
from SegmentModel import sam
canvas_bind_list = []
point_id = 0

# Upload action function
def upload_action(tk, canvas):
    global image, photo
    filename = filedialog.askopenfilename()
    sam.set_image(filename)
    image = Image.open(filename)
    photo = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor=tk.NW, image=photo)


# unbind
def unbind_canvas(canvas):
    global canvas_bind_list
    for evnet in canvas_bind_list:
        canvas.unbind(evnet)
    canvas_bind_list = []

def get_point_tags():
    global point_id
    point_id+=1
    return f"point_{point_id}"

def btn1_action(canvas):
    # Mark star function on canvas
    def mark_star(event):
            x, y = event.x, event.y
            r = 3
            canvas.create_oval(x-r, y-r, x+r, y+r, fill="red", tags=get_point_tags())
            sam.set_point(x,y)

    print('btn')
    sam.clean_point()
    unbind_canvas(canvas)
    global point_id
    for i in range(point_id+1):
        canvas.delete(f"point_{i}")
    point_id = 0
    global canvas_bind_list
    canvas_bind_list.append("<Button-1>")
    canvas.bind("<Button-1>",mark_star)
    

# Drawing rectangle functions
def btn2_action(canvas):

    def start_draw(event):
        global rect_start
        rect_start = (event.x, event.y)
        print(rect_start)

    def on_drag(event):
        global rect_id
        x0, y0 = rect_start
        canvas.delete("tmp_rect")
        canvas.delete("rect")
        rect_id = canvas.create_rectangle(x0, y0, event.x, event.y, outline="blue", fill="blue",  stipple="gray25", width=2, tags="tmp_rect")

    def end_draw(event):
        x0, y0 = rect_start
        canvas.delete("tmp_rect")
        canvas.create_rectangle(x0, y0, event.x, event.y, outline="blue", fill="", width=1, tags="rect")
        sam.set_box([x0,y0,event.x,event.y])
 

    unbind_canvas(canvas)
    global canvas_bind_list
    canvas_bind_list.append("<ButtonPress-1>")
    canvas_bind_list.append("<B1-Motion>")
    canvas_bind_list.append("<ButtonRelease-1>")
    canvas.bind("<ButtonPress-1>", start_draw)
    canvas.bind("<B1-Motion>", on_drag)
    canvas.bind("<ButtonRelease-1>", end_draw)


def segment():
    sam.segment_item()
    sam.segment_box()
    sam.show()
