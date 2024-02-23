import tkinter as tk
import tkinter.messagebox as messagebox
import random
import time
import pygame
pygame.mixer.init()
pygame.mixer.music.load('D:/Звуки для проекта/Во время всего/devil.mp3') # Загрузите ваш музыкальный файл
pygame.mixer.music.play(-1)
class TypingTrainer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Typing Trainer")  # Название окна
        self.geometry("900x400")  # Размеры окна

        self.words = ["try", "Astana", "Aktau","apple", "banana", "cherry", "date", "fig", "grape", "kiwi", "lemon"]
        self.current_level = 1  # Текущиц уровень
        self.repetition_count = 0  # Счетчик повторений
        self.keyboard_buttons = {}
        self.create_widgets()
        self.setup_level()
        self.configure(background='#f0f0f0') # Светлый серый фон

    def play_error_sound(self):
        error_sound_path = "D:\Звуки для проекта\После ошибки\error.mp3"  # Укажите путь к звуковому файлу ошибки
        pygame.mixer.Sound(error_sound_path).play()

    def play_completion_sound(self):
        completion_sound_path = "D:\Звуки для проекта\После уровня\level.mp3"  # Путь к звуковому файлу завершения
        pygame.mixer.Sound(completion_sound_path).play()

    def stop_music(self):
        pygame.mixer.music.stop()  # Остановить музыку

    def play_music(self):
        pygame.mixer.music.play(-1)  # Воспроизвести музыку в цикле

    def create_virtual_keyboard(self):
        # Создание фрейма для клавиатуры
        keyboard_frame = tk.Frame(self)
        keyboard_frame.pack(pady=10)

        # Макет клавиш QWERTY
        key_rows = [
            ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Backspace'],
            ['Tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\'],
            ['Caps Lock', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'', 'Enter'],
            ['Shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'Shift'],
            ['Space']
        ]

        for row_index, row in enumerate(key_rows):
            row_frame = tk.Frame(keyboard_frame)
            row_frame.pack(side=tk.TOP, fill=tk.X, padx=10)

            for key in row:
                if key in ['Backspace', 'Tab', 'Caps Lock', 'Enter', 'Shift', 'Space']:
                    width = 6 if key == 'Space' else 2
                    height = 2
                else:
                    width = 2
                    height = 2

                # Создаем кнопку для клавиши
                btn = tk.Button(row_frame, text=key, width=width, height=height)
                btn.pack(side=tk.LEFT, padx=1, pady=1)
                # Добавляем кнопку в словарь, если нужно отслеживать ее состояние
                if key not in ['Backspace', 'Tab', 'Caps Lock', 'Enter', 'Shift', 'Space']:
                    self.keyboard_buttons[key] = btn
    def create_widgets(self):
        self.speed_label = tk.Label(self, text="Speed: 0 WPM")
        self.speed_label.pack()  # или другой способ размещения в интерфейсе

        # Cоздание элементов интерфейса
        self.instructions = tk.Label(self, text="Type the text below and press Enter", font=("Helvetica", 14))
        self.instructions.pack(pady=(10, 2))

        self.level_label = tk.Label(self, text="", font=("Helvetica", 14))
        self.level_label.pack(pady=(0, 10))

        self.word_label = tk.Label(self, text="", font=("Helvetica", 24), fg="blue")
        self.word_label.pack(pady=(0, 20))

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(self, font=("Helvetica", 24), justify='center', textvariable=self.entry_var)
        self.entry.pack(fill='x', expand=True, pady=(0, 20))
        self.entry.focus_set()

        self.status_label = tk.Label(self, text="", font=("Helvetica", 14))
        self.status_label.pack(pady=(10, 0))



        # Метки для скорости печати и точности
        self.speed_label = tk.Label(self, text="Speed: 0 WPM", font=("Helvetica", 14))
        self.speed_label.pack()
        self.accuracy_label = tk.Label(self, text="Accuracy: 0%", font=("Helvetica", 14))
        self.accuracy_label.pack()



        self.instructions.config(bg='#f0f0f0', fg='#333')  # Цвета фона и текста
        self.level_label.config(bg='#f0f0f0', fg='#333')
        self.word_label.config(bg='#f0f0f0', fg='blue')
        self.status_label.config(bg='#f0f0f0', fg='#333')
        self.speed_label.config(bg='#f0f0f0', fg='#333')
        self.accuracy_label.config(bg='#f0f0f0', fg='#333')

        # Привязка событий к обработчикам
        self.entry.bind("<KeyPress>", self.on_key_press)
        self.entry.bind("<Return>", self.on_return_press)

        # Добавление кнопки для остановки музыки
        self.stop_music_button = tk.Button(self, text="Stop Music", command=self.stop_music)
        self.stop_music_button.pack(pady=5)

        # Добавление кнопки для воспроизведения музыки
        self.play_music_button = tk.Button(self, text="Play Music", command=self.play_music)
        self.play_music_button.pack(pady=5)
        # Кнопки с границами и отступами
        self.stop_music_button.config(borderwidth=1, relief="solid", padx=10, pady=5)
        self.play_music_button.config(borderwidth=1, relief="solid", padx=10, pady=5)
        # Кнопки с границами и отступами
        self.stop_music_button.config(borderwidth=1, relief="solid", padx=10, pady=5)
        self.play_music_button.config(borderwidth=1, relief="solid", padx=10, pady=5)
    def setup_level(self):
        # Определяем количество слов на основе текущего уровня
        if self.current_level <= 5:
            words_count = 1
        elif 5 < self.current_level <= 10:
            words_count = 2
        elif 10 < self.current_level <= 15:
            words_count = 3
        elif 15 < self.current_level <= 20:
            words_count = 4
        else:
            # Если уровень выше 20, можно выбирать случайное количество слов/предложений
            words_count = random.randint(1, len(self.words))  # Пример для демонстрации

        # Выбираем случайные слова из списка
        selected_words = random.sample(self.words, min(len(self.words), words_count))
        self.current_text = ' '.join(selected_words).lower()

        self.repetition_count = 0
        self.current_index = 0
        self.update_ui()

        self.start_time = time.time()
        self.total_characters = 0
        self.correct_characters = 0
        if self.current_level == 1 or self.current_level % 5 == 1:
            self.reset_counters()

    def update_ui(self):
        # Обновим интерфейс User
        self.level_label.config(text=f"Level: {self.current_level}")
        self.word_label.config(text=self.current_text)
        self.entry.delete(0, tk.END)
        self.status_label.config(text=f"Repetitions left: {2 - self.repetition_count}")

    def on_key_press(self, event):
        char = event.char.lower()
        if char in self.keyboard_buttons:
            # Изменение цвета кнопки
            self.keyboard_buttons[char].config(bg='lightblue')
            # Вернуть стандартный цвет через 500 мс
            self.after(500, lambda: self.keyboard_buttons[char].config(bg='SystemButtonFace'))
        # Обработка нажатий клавиш
        if event.keysym in ('Alt', 'BackSpace', 'Left', 'Right', 'Up', 'Down', 'Shift', 'Control', 'Tab'):
            return # Игнорим клавиш

        if len(self.entry_var.get()) >= len(self.current_text):
            return 'break' # Сравнение длину слов

        self.after(10, self.validate_entry) # Через 10миллисекунд проверяет на коррекность текста

    def validate_entry(self):
        current_text = self.entry_var.get().lower()
        if not self.current_text.startswith(current_text):
            self.status_label.config(text="Mistake made, keep going!", fg="red")
            self.entry_var.set(current_text[:-1])
            self.play_error_sound()  # Воспроизвести звук ошибки
        else:
            self.correct_characters += 1
            self.status_label.config(text="Correct so far...", fg="green")
        self.total_characters += 1
    def on_return_press(self, event):
        # Обработка ENTER
        current_text = self.entry_var.get().lower()
        if current_text == self.current_text:
            self.repetition_count += 1
            if self.repetition_count == 1:
                self.show_results()
                self.current_level += 1
                self.repetition_count = 0
                if self.current_level > 20:
                    self.handle_end_of_game() # Конец игры
                    return
                self.setup_level()
            else:
                self.update_ui()
        else:
            self.status_label.config(text="Finish the word/sentence before pressing Enter", fg="orange")

    def reset_counters(self):
        # Сброс счетчиков
        self.start_time = time.time()
        self.total_characters = 0
        self.correct_characters = 0

    def handle_end_of_game(self):
        # Обраотка конец игры
        restart = messagebox.askyesno("Game Over", "You've completed all levels! Do you want to restart?")
        if restart:
            self.current_level = 1  # Сброс уровня
            self.setup_level()  # Начать с первого уровня
        else:
            self.destroy() # Закрыть

    def show_results(self):
        # Перед отображением результатов воспроизведите звук завершения уровня
        self.play_completion_sound()

        # Код для отображения результатов уровня
        end_time = time.time()
        typing_duration = end_time - self.start_time
        words_typed = self.repetition_count * len(self.current_text.split())

        if typing_duration > 0:
            typing_speed = words_typed / (typing_duration / 60)
        else:
            typing_speed = 0

        accuracy = (self.correct_characters / self.total_characters) * 100 if self.total_characters else 0

        self.speed_label.config(text=f"Speed: {typing_speed:.2f} WPM")
        self.accuracy_label.config(text=f"Accuracy: {accuracy:.2f}%")


if __name__ == "__main__":
    app = TypingTrainer()
    app.create_virtual_keyboard()
    app.mainloop()
