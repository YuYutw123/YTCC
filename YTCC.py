# main library
import tkinter as tk  # GUI
from youtube_transcript_api import YouTubeTranscriptApi  # ytcaptions
from turtle import back, width  # Coordinate
from math import *  # calculate time stamp
import datetime  # calculate time stamp
from PIL import Image,  ImageTk  # image processing
import base64  # decode image
import os  # encode image
from itertools import cycle
from itertools import tee, islice, chain
import webbrowser  # hyperlink

# my file
from icon import iconImg  # icon image
from bg import bgimage  # background images
from subbtn import subbtnimage  # sub button image
from srtbtn import srtbtnimage  # srt button image

# timestamp calculate
def outputsub():
    link = en.get()
    arr = link.split('/')
    key = arr[3]
    srt = YouTubeTranscriptApi.get_transcript(key)
    result.delete('1.0', tk.END)
    for item, nxt in previous_and_next(reversed(srt)):
        if item['text'] == "[Music]" or item['text'] == "[Laughter]":
            continue
        else:
            begin = str(datetime.timedelta(seconds=floor(item['start'])))
            end = str(datetime.timedelta(
                seconds=floor(item['start']+item['duration'])))
            if nxt != None:
                if item['start']+item['duration'] > nxt['start']:
                    end = str(datetime.timedelta(seconds=floor(nxt['start'])))
            result.insert('1.0', end + " ~ " + begin +
                          ": " + str(item['text']) + "\n")

# just sec 2 time
def sec2time(sec, n_msec=3):
    ''' Convert seconds to 'D days, HH:MM:SS.FFF' '''
    if hasattr(sec, '__len__'):
        return [sec2time(s) for s in sec]
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    if n_msec > 0:
        pattern = '%%02d:%%02d:%%0%d.%df' % (n_msec+3, n_msec)
    else:
        pattern = r'%02d:%02d:%02d'
    if d == 0:
        return pattern % (h, m, s)
    return ('%d days, ' + pattern) % (d, h, m, s)

# so that I can fking get the next element of the list
def previous_and_next(some_iterable):
    items, nexts = tee(some_iterable, 2)
    nexts = chain(islice(nexts, 1, None), [None])
    return zip(items, nexts)

# srt file output
def outputsrt():
    link = en.get()
    arr = link.split('/')
    key = arr[3]
    srt = YouTubeTranscriptApi.get_transcript(key)
    num = 1
    srtcy = cycle(srt)
    with open("srt.srt", "w+") as f:
        f.write(str(1) + "\n" + "00:00:00.000 --> 00:00:00.001" +
                "\n" + "start" + "\n\n")
        for item, nxt in previous_and_next(srt):
            if item['text'] == "[Music]" or item['text'] == "[Laughter]":
                continue
            else:
                num = num+1
                begin = str(sec2time(item['start']))
                end = str(sec2time(item['start']+item['duration']))
                if nxt != None:
                    if item['start']+item['duration'] > nxt['start']:
                        end = str(sec2time((nxt['start'])))

                f.write(str(num) + "\n")
                f.write(begin + " --> " + end + "\n")
                f.write(str(item['text']) + "\n\n")


# hyperlink
def callback(url):
    webbrowser.open_new(url)


win = tk.Tk()  # main window
win.title("YTCC tool")  # window title
win.geometry("778x600+150+100")  # window size
win.resizable(0, 0)  # cant resize

# iCON
tmpIcon = open('tmp.ico', 'wb+')
# open a file called "tmp.ico" and writing (and reading based on writing) in binary
# decode with base64 and get the code in iconImg
tmpIcon.write(base64.b64decode(iconImg))
tmpIcon.close()  # close file
win.iconbitmap("tmp.ico")  # set tmp.ico as icon

# color
# background color
win.config(bg="#404040")

# bg image
# basically same as Icon
bgpic = open('bg.png', 'wb+')
bgpic.write(base64.b64decode(bgimage))
bgpic.close()
img = tk.PhotoImage(file="bg.png")


# label
# background image
lb = tk.Label(image=img)
lb.pack()

# entry
# enter yt link
en = tk.Entry(win, font=24)
en.place(x=35, y=69, width=580, height=20)


# sub button
# get link button
subpic = open('subbtn.png', 'wb+')
subpic.write(base64.b64decode(subbtnimage))
subpic.close()
subbtnimage = tk.PhotoImage(file="subbtn.png")
btn = tk.Button(text="GetCC")
btn.config(image=subbtnimage)
btn.place(x=567, y=496, width=180, height=75)
btn.config(command=outputsub)

# srt button
# get link button
srtpic = open('srtbtn.png', 'wb+')
srtpic.write(base64.b64decode(srtbtnimage))
srtpic.close()
srtbtnimage = tk.PhotoImage(file="srtbtn.png")
srtbtn = tk.Button(text="GetCC")
srtbtn.config(image=srtbtnimage)
srtbtn.place(x=367, y=496, width=180, height=75)
srtbtn.config(command=outputsrt)


# result
# output captions
result = tk.Text(win, font=40)
result.place(x=35, y=105, width=690, height=375)


# scrollbar
scrollbar = tk.Scrollbar(win)
scrollbar.place(x=725, y=105, width=20, height=375)

# result + scrollbar
result.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=result.yview)


# link
link1 = tk.Label(win, text="Facebook", fg="white", bg="#00406d",
                 cursor="hand2", font=('Comic Sans MS', 12))
link1.place(x=190, y=540, width=89, height=30)
link1.bind("<Button-1>", lambda e: callback("https://www.facebook.com/yuyutw.877/"))
link2 = tk.Label(win, text="Twitter", fg="white", bg="#00406d",
                 cursor="hand2", font=('Comic Sans MS', 12))
link2.place(x=284, y=540, width=75, height=30)
link2.bind("<Button-1>", lambda e: callback("https://twitter.com/yu_yutw"))

os.remove("tmp.ico")  # remove tmp.ico
os.remove("bg.png")  # remove bg.png
os.remove("subbtn.png")  # remove subbtn.png
os.remove("srtbtn.png")  # remove srtbtn.png

win.mainloop()  # remain the window opened
