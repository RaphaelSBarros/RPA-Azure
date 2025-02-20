import sys
import os

root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, root)

from module import *
from controllers.get_files import start_download_process, open_browser
from controllers.manage_files import manage_files
from controllers.merge_files import merge_files
from views.alert_window import ToplevelWindow

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("RPA SZ Soluções")
        self.geometry("700x450")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.toplevel_window = None

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "Logo_SZ-sem-descricao.png")), size=(26, 26))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "Logo-SZ-Solucoes.png")), size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  HUB", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                fg_color="#ff8200",button_color="#ff8200", button_hover_color="#ff7100",command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=self.large_test_image)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        self.home_frame_button_1 = customtkinter.CTkButton(self.home_frame, text="Iniciar processo", fg_color='#ff8200', hover_color='#ff7100', command=self.start_loading_process)
        self.home_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
        
        self.loading_bar = customtkinter.CTkProgressBar(self.home_frame)

        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        # if name == "frame_2":
        #     self.second_frame.grid(row=0, column=1, sticky="nsew")
        # else:
        #     self.second_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)
        
    def open_toplevel(self):
        driver = open_browser()
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it
        is_canceled = self.toplevel_window.get_click_option()
        if is_canceled:
            self.status_indicator_text(text='operação cancelada', color='red')
        else:
            start_download_process(driver)
            manage_files()
            merge_files()
            self.status_indicator_text(text='operação concluída', color='green')
        self.loading_bar.grid_forget()
        self.home_frame_button_1.configure(state="normal")
        
        
    def start_loading_process(self):
        self.home_frame_button_1.configure(state="disabled")
        self.loading_bar.grid(row=2, column=0, padx=150, pady=(10, 10), sticky="ew")
        self.loading_bar.configure(determinate_speed=5)
        self.loading_bar.start()
        threading.Thread(target=self.open_toplevel).start()
        
    
    def status_indicator_text(self, text, color):
        self.status_indicator = customtkinter.CTkLabel(self.home_frame, text=text, text_color=color)
        self.status_indicator.grid(row=3, column=0, pady=10, sticky="nsew")
        
if __name__ == "__main__":
    app = App()
    app.mainloop()
