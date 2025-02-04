# -*- coding: utf-8 -*-

from PIL import Image, ImageTk
from tkinter import ttk
import tkinter as tk
import time

from Constants import (
    GUI_PHONE_PNG,
    GUI_MICROPHONE_B_PNG,
    GUI_MICROPHONE_R_PNG,
    OTHER_CLUB_ICO_ICO,
    OTHER_TURKISH_LANGUAGE,
    OTHER_ENGLISH_LANGUAGE,
    ANIM_ANIMATIONS,
    ANIM_DEFAULT,
    ANIM_DEFAULT_LISTENING,
    ANIM_teknofest,
    ANIM_HASHES,
    TURKISH_CHARS,
)

from Utilities import (
    get_gif_frame_count
)

from Utilities import (
    listen_text,
    translate_text,
)

class NormalAPP(tk.Toplevel) :

    def __init__(self, available_devices:list, mode, my_Args=None, *args, **kwargs) -> None:
        """
        Constructor method. Creates the main window of the application.
        @Params:
            available_devices (list): (Reqired) List of available devices.
            *args (tuple): (Optimal) Arguments.
            **kwargs (dict): (Optimal) Keyword arguments.
        @Returns:
            None
        """
        super().__init__(*args, **kwargs)

        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except:
            pass

        self.available_devices = available_devices
        
        style = ttk.Style()

        style.theme_use("clam")

        # set root background color to "clam" theme's background color
        self.configure(background=style.lookup("TFrame", "background"))

        #style.configure("StartButton.TButton", font=("Seoge UI", 18, "bold"), foreground="white", background="#00b300", borderwidth=0, cursor="hand2", relief="flat")

        style.configure("Output.TLabel", font=("Seoge UI", 14, "bold"), borderwidth=0, cursor="hand2", relief="flat")
        style.configure("SelectedDevice.TLabel", font=("Seoge UI", 13, "bold"), borderwidth=0, cursor="hand2", relief="flat")
        style.configure("SeelctionCombobox.TCombobox", font=("Seoge UI", 13, "bold"), borderwidth=0, cursor="hand2", relief="flat")

        self.title("Herkes İçin İşaret Dili")

        self.iconbitmap(OTHER_CLUB_ICO_ICO)

        self.output_text = tk.StringVar(value="Girdi Bekleniyor")

        self.current_device_name = tk.StringVar(value=self.available_devices[0])
        self.current_device_index = tk.IntVar(value=0)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.container = ttk.Frame(self)
        self.container.grid(row=0, column=0)

        self.background_label = ttk.Label(self.container)
        self.background_label.place(x=0, y=0)

        self.default_animation_image = ImageTk.PhotoImage(Image.open(ANIM_teknofest).resize((500, 500), Image.LANCZOS))
            
        self.default_listening_image = ImageTk.PhotoImage(Image.open(ANIM_teknofest).resize((500, 500), Image.LANCZOS))

        dummy_label = ttk.Label(self.container, text="")
        dummy_label.grid(row=0, column=0, pady=20)

        self.animation_label = ttk.Label(self.container, image=self.default_animation_image, justify="center", cursor="star", anchor="center", borderwidth=5, border=1)
        self.animation_label.grid(row=1, column=0, padx=45)

        self.output_text_label = ttk.Label(self.container, textvariable=self.output_text, justify="center", cursor="star", style="Output.TLabel")
        self.output_text_label.grid(row=2, column=0, pady=40)

        self.listen_button_photo = ImageTk.PhotoImage(Image.open(GUI_MICROPHONE_B_PNG).resize((100, 100), Image.LANCZOS))
        self.listen_button = ttk.Button(self.container, command=self.handle_start_listening, cursor="hand2", image=self.listen_button_photo)
        self.listen_button.grid(row=3, column=0)

        dummy_label2 = ttk.Label(self.container, text="")
        dummy_label2.grid(row=4, column=0, pady=20)

        self.device_selection_label = ttk.Label(self.container, text="Mikrofon Seçimi", justify="center", cursor="star", style="SelectedDevice.TLabel")
        self.device_selection_label.grid(row=5, column=0)

        self.device_selection_combobox = ttk.Combobox(self.container, textvariable=self.current_device_name, values=list(self.available_devices.values()), state="readonly", justify="center", cursor="hand2", width=50, style="SeelctionCombobox.TCombobox")
        self.device_selection_combobox.grid(row=6, column=0)

        dummy_label = ttk.Label(self.container, text="")
        dummy_label.grid(row=7, column=0, pady=5)

        self.available_languages = ["Türkçe", "English"]
        self.current_language = "Türkçe"

        self.language_selection_label = ttk.Label(self.container, text="Dil Seçimi", justify="center", cursor="star", style="SelectedDevice.TLabel")
        self.language_selection_label.grid(row=8, column=0)

        self.turkish_flag_image = ImageTk.PhotoImage(Image.open(OTHER_TURKISH_LANGUAGE).resize((50, 50), Image.LANCZOS))
        self.english_flag_image = ImageTk.PhotoImage(Image.open(OTHER_ENGLISH_LANGUAGE).resize((50, 50), Image.LANCZOS))

        fframe = ttk.Frame(self.container)
        fframe.grid(row=9, column=0)
        fframe.columnconfigure((0,1), weight=1)

        self.turkish_flag_button = ttk.Button(fframe, command=lambda: self.handle_language_selection("Türkçe"), cursor="hand2", image=self.turkish_flag_image, state="disabled")
        self.turkish_flag_button.grid(row=0, column=0)

        self.english_flag_button = ttk.Button(fframe, command=lambda: self.handle_language_selection("English"), cursor="hand2", image=self.english_flag_image)
        self.english_flag_button.grid(row=0, column=1)

        dummy_label = ttk.Label(self.container, text="")
        dummy_label.grid(row=11, column=0, pady=20)

        self.device_selection_combobox.bind("<<ComboboxSelected>>", self.handle_device_selection)

        self.should_ignore = False

        self.update()
        self.update_idletasks()

        tpl = (self.container.winfo_width(), self.container.winfo_height())
        self.minsize(*tpl)
        self.background_image = ImageTk.PhotoImage(Image.open(GUI_PHONE_PNG).resize(tpl, Image.LANCZOS))
        if mode == "phone" :
            self.background_label.config(image=self.background_image)

        self.update()
        self.update_idletasks()

    def close(self) -> None:
        """
        Class Method to close the application.
        @Params
            None
        @Returns
            None
        """
        self.destroy()

    def handle_language_selection(self, language: str) -> None:
        """
        Class Method to handle language selection.
        @Params
            language : (str) Language to be selected.
        @Returns
            None
        """

        if language == "Türkçe" :
            self.current_language = "Türkçe"
            self.turkish_flag_button.config(state="disabled")
            self.english_flag_button.config(state="enabled")
            self.title("Herkes İçin İşaret Dili")
            
            current_output = self.output_text.get()
            new_output = translate_text(source_language="en", target_language="tr", text=current_output)
            self.output_text.set(new_output)

            self.device_selection_label.config(text="Mikfrofon Seçimi")

            self.language_selection_label.config(text="Dil Seçimi")

        else :
            self.current_language = "English"
            self.turkish_flag_button.config(state="enabled")
            self.english_flag_button.config(state="disabled")
            self.title("Sign Language For Everyone")

            current_output = self.output_text.get()
            new_output = translate_text(source_language="tr", target_language="en", text=current_output)
            self.output_text.set(new_output)

            self.device_selection_label.config(text="Microphone Selection")

            self.language_selection_label.config(text="Language Selection")


    def handle_start_listening(self, *args, **kwargs) -> None:
        """
        Class Method to handle start listening button click event.
        @Params
            *args : (Optional) Variable length argument list.
            **kwargs : (Optional) Arbitrary keyword arguments.
        @Returns
            None
        """
        
        if self.should_ignore :
            return
        else :
            self.should_ignore = True

        self.new_listen_button_photo = ImageTk.PhotoImage(Image.open(GUI_MICROPHONE_R_PNG).resize((100, 100), Image.LANCZOS))
        self.listen_button.config(cursor="arrow", image=self.new_listen_button_photo)
        self.device_selection_combobox.config(state="disabled", cursor="arrow")
        self.animation_label.config(image=self.default_listening_image)
        
        self.update()
        self.update_idletasks()

        map = {"Türkçe" : "tr", "English" : "en"}

        listened = listen_text(map[self.current_language], self.current_device_index.get())

        output = listened
        # if output length is more than 40, just show the first 40 characters with "..." at the end
        if len(output) > 40 :
            output = output[:40] + "..."
        self.output_text.set(output)

        revized = listened.lower()
        if self.current_language == "English" :
            revized = translate_text(source_language="en", target_language="tr", text=listened).lower()

        for key in TURKISH_CHARS :
            revized = revized.replace(key, TURKISH_CHARS[key])
        
        output_for_animation = revized

        self.update()
        self.update_idletasks()

        self.animation_list = output_for_animation.split(" ")

        for i in range(len(self.animation_list)) :
            if self.animation_list[i][-1] in [".", ",", "?", "!", ";"] :
                self.animation_list[i] = self.animation_list[i][:-1]

        for word in self.animation_list :
            for key in ANIM_HASHES:
                if word in ANIM_HASHES[key] :
                    self.animation_list[self.animation_list.index(word)] = key
                    break

        print(self.animation_list)
        self.display_animations()

        self.animation_label.config(image=self.default_animation_image)
        self.listen_button.config(state="normal", cursor="hand2", image=self.listen_button_photo)
        self.device_selection_combobox.config(state="readonly", cursor="hand2")

        self.should_ignore = False

        self.update()
        self.update_idletasks()

    def display_animations(self) -> None:
        """
        Class Method to display animations.
        @Params
            None
        @Returns
            None
        """

        all_animation_frames = []

        animation_path = None

        for current_animation in self.animation_list :
            
            try :
                animation_path = ANIM_ANIMATIONS[current_animation]
            except :
                continue

            animation_length = get_gif_frame_count(animation_path)

            animation_frames = [None] * animation_length

            for i in range(animation_length) :
                # from the animation_path, read the frame with index i to with Image.open
                img = Image.open(animation_path)
                img.seek(i)
                # resize the frame to 500x500
                img = img.resize((500, 500), Image.LANCZOS)
                # convert the frame to PhotoImage
                animation_frames[i] = ImageTk.PhotoImage(img)

            all_animation_frames += animation_frames

        for current_frame in all_animation_frames :
            
            self.animation_label.config(image=current_frame)
            self.update()
            time.sleep(0.025)

    def handle_device_selection(self, *event) :
        """
        Class Method to handle device selection combobox selection event.
        @Params
            *event : (Optional) Variable length argument list.
        @Returns
            None
        """
        self.current_device_name.set(self.device_selection_combobox.get())
        self.current_device_index.set(list(self.available_devices.values()).index(self.current_device_name.get()))