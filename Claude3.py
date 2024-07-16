from tkinter import *
from tkinter import messagebox as mb
import g4f
import threading
import time
import pyperclip

root = Tk()
root.attributes('-fullscreen', True)
root.title('Claude 3')
root.iconbitmap('images/claude_3_70win_icon.ico')


class Gui:
    def __init__(self):
        self.bg_image = PhotoImage(file='images/png_bg_image.png')
        self.send_mess_image = PhotoImage(file='images/send_mess_image.png')
        self.down_but_image = PhotoImage(file='images/down_but.png')
        self.up_but_image = PhotoImage(file='images/up_but.png')
        self.home_but_image = PhotoImage(file='images/home_but.png')

        self.canvas = Canvas(root, width=1920, height=1080)
        # self.canvas.config(width=10000, height=10000)
        # self.vbar = Scrollbar(root, orient=VERTICAL)
        # self.vbar.pack(side=RIGHT, fill=Y)
        # self.vbar.config(command=self.canvas.yview)
        # self.canvas.config(yscrollcommand=self.vbar.set)
        # self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        # self.canvas.bind("<Button-4>", self.on_mouse_wheel)
        # self.canvas.bind("<Button-5>", self.on_mouse_wheel)

        self.bg = self.canvas.create_image((-200, -200), anchor='nw', image=self.bg_image, )

        self.ask_lab = self.canvas.create_text((100, 860), anchor='nw',
                                               text=f'Сообщение для Claude 3:',
                                               font='Consolas 14', fill='#1E90FF')
        self.chat_you_y = 70
        self.chat_you = self.canvas.create_text((100, self.chat_you_y), anchor='nw',
                                                text=f'',
                                                font='Consolas 11', fill='#00008B')

        self.chat_claude_3_y = 110
        self.chat_claude_3 = self.canvas.create_text((100, self.chat_claude_3_y), anchor='nw',
                                                     text=f'',
                                                     font='Consolas 11', fill='#00008B')

        self.wait_lab_y = 110
        self.wait_lab = self.canvas.create_text((100, self.chat_claude_3_y), anchor='nw',
                                                text=f'',
                                                font='Consolas 11', fill='#1E90FF')

        self.wait_flag = True

        self.send_request_but = self.canvas.create_image((1015, 890), anchor='nw', image=self.send_mess_image, )
        self.canvas.tag_bind(self.send_request_but, "<Button-1>", self.ask_claude3)
        self.canvas.pack()

        self.fullscreen_but = self.canvas.create_text((10, 10), anchor='nw',
                                                      text=f'Выйти из полноэкранного режима',
                                                      font='Consolas 14', fill='#1E90FF', activefill='#00008B', )

        self.canvas.tag_bind(self.fullscreen_but, "<Button-1>", self.fullscreen_swap)

        self.paste_but = self.canvas.create_text((745, 860), anchor='nw',
                                                 text=f'Вставить',
                                                 font='Consolas 14', fill='#1E90FF', activefill='#00008B', )
        self.canvas.tag_bind(self.paste_but, "<Button-1>", self.paste)

        self.copy_but = self.canvas.create_text((845, 860), anchor='nw',
                                                 text=f'Скопировать ответ',
                                                 font='Consolas 14', fill='#1E90FF', activefill='#00008B', )
        self.canvas.tag_bind(self.copy_but, "<Button-1>", self.copy_resp)

        self.up_but = self.canvas.create_image((1115, 870), anchor='nw', image=self.up_but_image, )
        self.canvas.tag_bind(self.up_but, "<Button-1>", self.page_up)

        self.down_but = self.canvas.create_image((1115, 910), anchor='nw', image=self.down_but_image, )
        self.canvas.tag_bind(self.down_but, "<Button-1>", self.page_down)

        self.home_but = self.canvas.create_image((1175, 890), anchor='nw', image=self.home_but_image, )
        self.canvas.tag_bind(self.home_but, "<Button-1>", self.home)

        self.request_str = Text(root, width=70, height=2, bg='#E0FFFF', fg='#1E90FF', font='Consolas 18')
        self.request_str.place(x=100, y=890)

    def paste(self, event):
        cursor_index = self.request_str.index(INSERT)
        self.request_str.insert(cursor_index, pyperclip.paste())

    def copy_resp(self, event):
        try:
            pyperclip.copy(self.string_resp)
        except AttributeError:
            mb.showwarning(title='Ошибка', message='Ошибка получения ответа\nТекст не скопирован')

    def home(self, event):
        self.chat_you_y = 70
        self.canvas.coords(self.chat_you, (100, self.chat_you_y))
        bounds = self.canvas.bbox(self.chat_you)
        height = bounds[3] - bounds[1]
        self.chat_claude_3_y = self.chat_you_y + height
        self.canvas.coords(self.chat_claude_3, (100, self.chat_claude_3_y))
        self.wait_lab_y = self.chat_you_y + height
        self.canvas.coords(self.wait_lab_y, (100, self.wait_lab_y))

    def page_up(self, event):
        self.chat_you_y += 70
        self.canvas.coords(self.chat_you, (100, self.chat_you_y))
        self.chat_claude_3_y += 70
        self.canvas.coords(self.chat_claude_3, (100, self.chat_claude_3_y))
        self.wait_lab_y += 70
        self.canvas.coords(self.wait_lab_y, (100, self.wait_lab_y))

    def page_down(self, event):
        self.chat_you_y -= 70
        self.canvas.coords(self.chat_you, (100, self.chat_you_y))
        self.chat_claude_3_y -= 70
        self.canvas.coords(self.chat_claude_3, (100, self.chat_claude_3_y))
        self.wait_lab_y -= 70
        self.canvas.coords(self.wait_lab_y, (100, self.wait_lab_y))

    def fullscreen_swap(self, event):
        if root.attributes('-fullscreen'):
            root.attributes('-fullscreen', False)
            self.canvas.itemconfig(self.fullscreen_but, text=f'Вернуться в полноэкранный режим')
            self.request_str.place(x=100, y=810)
            self.canvas.coords(self.send_request_but, (1015, 810))
            self.canvas.coords(self.ask_lab, (100, 780))
            self.canvas.coords(self.paste_but, (745, 780))
            self.canvas.coords(self.copy_but, (845, 780))
            self.canvas.coords(self.up_but, (1115, 790))
            self.canvas.coords(self.down_but, (1115, 830))
            self.canvas.coords(self.home_but, (1175, 810))

        else:
            root.attributes('-fullscreen', True)
            self.canvas.itemconfig(self.fullscreen_but, text=f'Выйти из полноэкранного режима')
            self.request_str.place(x=100, y=890)
            self.canvas.coords(self.send_request_but, (1015, 890))
            self.canvas.coords(self.ask_lab, (100, 860))
            self.canvas.coords(self.paste_but, (745, 860))
            self.canvas.coords(self.copy_but, (845, 860))
            self.canvas.coords(self.up_but, (1115, 870))
            self.canvas.coords(self.down_but, (1115, 910))
            self.canvas.coords(self.home_but, (1175, 890))

    def ask_claude3(self, event):
        self.prompt = self.request_str.get("1.0", END)
        self.canvas.itemconfig(self.chat_claude_3, text='')
        print(self.prompt)

        if self.prompt == '\n':
            mb.showwarning(title='Ошибка запроса', message='Отправлен пустой запрос')

        elif self.prompt != '\n':
            self.chat_you_y = 70
            self.canvas.coords(self.chat_you, (100, self.chat_you_y))
            self.canvas.itemconfig(self.chat_you,
                                   text=f'You: {self.refractoring_prompt(prompt=self.prompt, to_return="prompt")}')
            self.request_str.delete("1.0", END)

            def get_response():
                try:
                    resp = g4f.ChatCompletion.create(
                        model=g4f.models.claude_3_haiku,
                        messages=[{'role': 'user', 'content': self.prompt}]
                    )

                    self.refractoring_claude_3_resp(resp)
                except:
                    mb.showwarning(title='Ошибка запроса', message='Ошибка в работе нейросети')

            self.wait_flag = True
            self.t2 = threading.Thread(target=self.claude_3_waiting, daemon=True)
            self.t2.start()

            t1 = threading.Thread(target=get_response, daemon=True)
            t1.start()

    def claude_3_waiting(self, flag=True):
        bounds = self.canvas.bbox(self.chat_you)
        height = bounds[3] - bounds[1]
        self.wait_lab_y = self.chat_you_y + height
        self.canvas.coords(self.wait_lab, (100, self.wait_lab_y))
        while flag:
            self.canvas.itemconfig(self.wait_lab, text=f'Claude 3: .')
            time.sleep(0.1)
            if not self.wait_flag:
                break
            time.sleep(0.1)
            if not self.wait_flag:
                break
            self.canvas.itemconfig(self.wait_lab, text=f'Claude 3: ..')
            time.sleep(0.1)
            if not self.wait_flag:
                break
            time.sleep(0.1)
            if not self.wait_flag:
                break
            self.canvas.itemconfig(self.wait_lab, text=f'Claude 3: ...')
            time.sleep(0.1)
            if not self.wait_flag:
                break
            time.sleep(0.1)
        self.canvas.itemconfig(self.wait_lab, text=f'')

    def refractoring_prompt(self, prompt, to_return):
        refr_prompt_arr = list()
        refr_prompt_str = str()
        counter = 0
        strings = 1
        for i in range(len(prompt)):
            if counter < 120:
                refr_prompt_arr.append(prompt[i])
                counter += 1
            if counter == 120:
                refr_prompt_arr.append('\n')
                refr_prompt_arr.append(prompt[i])
                counter = 1
                strings += 1
        for i in range(len(refr_prompt_arr)):
            refr_prompt_str += refr_prompt_arr[i]

        if to_return == 'prompt':
            return refr_prompt_str
        if to_return == 'strings_count':
            return strings

    def refractoring_claude_3_resp(self, text):
        bounds = self.canvas.bbox(self.chat_you)
        height = bounds[3] - bounds[1]
        self.chat_claude_3_y = self.chat_you_y + height
        self.canvas.coords(self.chat_claude_3, (100, self.chat_claude_3_y))

        text = text.split('\n')
        text2 = list()
        # делю по буквам
        for elem in text:
            text2.append(elem.split())
        for elem in text2:
            for i in range(len(elem)):
                el_arr = list()
                for e in elem[i]:
                    el_arr.append(e)
                elem[i] = el_arr

        # displaying response
        self.string_resp = str()
        counter = 0
        # self.t2 = threading.Thread(target=lambda flag=False: self.claude_3_waiting(flag=flag), daemon=True)
        self.wait_flag = False
        for elem in text2:  # string
            for i in range(len(elem)):  # word
                for j in range(len(elem[i])):  # word's elems
                    if counter < 120:
                        self.canvas.itemconfig(self.chat_claude_3, text=f'Claude 3: {self.string_resp}' + elem[i][j])
                        self.string_resp += elem[i][j]
                        counter += 1
                        time.sleep(0.01)
                    elif counter >= 120:
                        self.string_resp += '\n'
                        self.canvas.itemconfig(self.chat_claude_3, text=f'Claude 3: {self.string_resp}' + elem[i][j])
                        self.string_resp += elem[i][j]
                        counter = 1
                        time.sleep(0.01)
                self.string_resp += ' '
            self.string_resp += '\n'
            counter = 0

        print(self.string_resp)


obj = Gui()
root.mainloop()
