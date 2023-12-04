import fitz
from gtts import gTTS
import tkinter as tk
from tkinter import filedialog
import threading


class PDFToAudioConverter:
    def __init__(self, master):
        self.master = master
        master.title("Конвертер PDF в аудио")

        self.pdf_file_path = None
        self.is_converting = False

        self.pdf_label = tk.Label(master, text="PDF Файл:")
        self.pdf_label.grid(row=0, column=0, sticky='w', padx=10, pady=10)

        self.pdf_entry = tk.Entry(master, width=50, state='disabled')
        self.pdf_entry.grid(row=0, column=1, padx=10, pady=10)

        self.browse_button = tk.Button(master, text="Обзор", command=self.browse_pdf)
        self.browse_button.grid(row=0, column=2, padx=10, pady=10)

        self.convert_button = tk.Button(master, text="Конвертировать в аудио", command=self.convert_to_audio)
        self.convert_button.grid(row=1, column=0, columnspan=3, pady=10)

        self.status_label = tk.Label(master, text="")
        self.status_label.grid(row=2, column=0, columnspan=3)

    def browse_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF файлы", "*.pdf")])
        if file_path:
            self.pdf_file_path = file_path
            self.pdf_entry.config(state='normal')
            self.pdf_entry.delete(0, tk.END)
            self.pdf_entry.insert(0, self.pdf_file_path)
            self.pdf_entry.config(state='disabled')

    def convert_to_audio(self):
        if not self.is_converting and self.pdf_file_path:
            output_audio_path = filedialog.asksaveasfilename(defaultextension=".mp3",
                                                             filetypes=[("MP3 файлы", "*.mp3")])
            if output_audio_path:
                self.is_converting = True
                self.browse_button.config(state='disabled')
                self.convert_button.config(state='disabled')

                conversion_thread = threading.Thread(target=self.perform_conversion, args=(output_audio_path,))
                conversion_thread.start()
            else:
                tk.messagebox.showwarning("Не выбран путь для сохранения",
                                          "Пожалуйста, выберите допустимый путь для сохранения.")
        elif self.is_converting:
            tk.messagebox.showwarning("Конвертация в процессе", "Конвертация уже выполняется.")
        else:
            tk.messagebox.showwarning("PDF файл не выбран", "Пожалуйста, выберите файл PDF.")

    def perform_conversion(self, output_audio_path):
        try:
            self.update_status("Идёт процесс конвертации...")
            text = pdf_to_text(self.pdf_file_path)
            text_to_audio(text, output_audio_path, language='ru')
            tk.messagebox.showinfo("Конвертация завершена", "Конвертация PDF в аудио успешно завершена.")
        except Exception as e:
            tk.messagebox.showerror("Ошибка", f"Произошла ошибка во время конвертации: {str(e)}")
        finally:
            self.is_converting = False
            self.browse_button.config(state='normal')
            self.convert_button.config(state='normal')
            self.update_status("")

    def update_status(self, text):
        self.status_label.config(text=text)


def pdf_to_text(pdf_path):
    text = ''
    with fitz.open(pdf_path, filetype='pdf') as pdf_document:
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text += page.get_text()
    return text


def text_to_audio(text, output_path='output.mp3', language='ru'):
    tts = gTTS(text=text, lang=language)
    tts.save(output_path)


if __name__ == "__main__":
    root = tk.Tk()
    app = PDFToAudioConverter(root)
    root.mainloop()