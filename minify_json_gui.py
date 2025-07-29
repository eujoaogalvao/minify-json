import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


def minify_json_file(input_file, output_file=None):
    """
    Reads a JSON file, minifies its content, and writes it to an output file or returns it.

    Args:
        input_file (str): Path to the input JSON file.
        output_file (str, optional): Path to the output JSON file.
                                     If None, returns the minified string.

    Returns:
        str: The minified JSON string if output_file is None
    """
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Minify by dumping with no indent and compact separators
        minified_json = json.dumps(data, separators=(",", ":"))

        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(minified_json)
            return f"Arquivo minificado com sucesso: '{output_file}'"
        else:
            return minified_json

    except FileNotFoundError:
        return f"Erro: Arquivo de entrada '{input_file}' não encontrado."
    except json.JSONDecodeError:
        return f"Erro: Formato JSON inválido em '{input_file}'."
    except Exception as e:
        return f"Ocorreu um erro inesperado: {e}"


class JSONMinifierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Minificador de JSON")
        self.root.geometry("600x300")
        self.root.resizable(True, True)

        # Configuração do frame principal
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Entrada para o arquivo JSON
        ttk.Label(main_frame, text="Arquivo JSON de entrada:").grid(
            column=0, row=0, sticky=tk.W, pady=5
        )
        self.input_file_var = tk.StringVar()
        input_entry = ttk.Entry(main_frame, width=50, textvariable=self.input_file_var)
        input_entry.grid(column=0, row=1, sticky=(tk.W, tk.E), pady=5)

        ttk.Button(
            main_frame, text="Selecionar arquivo...", command=self.select_input_file
        ).grid(column=1, row=1, padx=5, pady=5)

        # Saída para o arquivo JSON minificado
        ttk.Label(main_frame, text="Arquivo JSON de saída (opcional):").grid(
            column=0, row=2, sticky=tk.W, pady=5
        )
        self.output_file_var = tk.StringVar()
        output_entry = ttk.Entry(
            main_frame, width=50, textvariable=self.output_file_var
        )
        output_entry.grid(column=0, row=3, sticky=(tk.W, tk.E), pady=5)

        ttk.Button(
            main_frame, text="Selecionar arquivo...", command=self.select_output_file
        ).grid(column=1, row=3, padx=5, pady=5)

        # Botão de minificação
        ttk.Button(main_frame, text="Minificar JSON", command=self.minify).grid(
            column=0, row=4, columnspan=2, pady=20
        )

        # Resultado
        ttk.Label(main_frame, text="Resultado:").grid(
            column=0, row=5, sticky=tk.W, pady=5
        )

        self.result_text = tk.Text(main_frame, wrap=tk.WORD, width=60, height=5)
        self.result_text.grid(
            column=0, row=6, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5
        )

        # Configurar expansão
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(6, weight=1)

    def select_input_file(self):
        filename = filedialog.askopenfilename(
            title="Selecione o arquivo JSON",
            filetypes=[("Arquivos JSON", "*.json"), ("Todos os arquivos", "*.*")],
        )
        if filename:
            self.input_file_var.set(filename)
            # Sugerir nome de arquivo de saída
            if not self.output_file_var.get():
                # Remove a extensão e adiciona .min.json
                base_filename = filename.rsplit(".", 1)[0]
                self.output_file_var.set(f"{base_filename}.min.json")

    def select_output_file(self):
        filename = filedialog.asksaveasfilename(
            title="Salvar arquivo JSON minificado",
            defaultextension=".json",
            filetypes=[("Arquivos JSON", "*.json"), ("Todos os arquivos", "*.*")],
        )
        if filename:
            self.output_file_var.set(filename)

    def minify(self):
        input_file = self.input_file_var.get()
        output_file = self.output_file_var.get()

        if not input_file:
            messagebox.showerror(
                "Erro", "Por favor, selecione um arquivo JSON de entrada."
            )
            return

        result = minify_json_file(input_file, output_file if output_file else None)

        # Limpar e exibir o resultado
        self.result_text.delete(1.0, tk.END)

        if not output_file:
            # Se não houver arquivo de saída, mostrar o JSON minificado
            self.result_text.insert(tk.END, result)
        else:
            # Se houver arquivo de saída, mostrar mensagem de sucesso
            self.result_text.insert(tk.END, result)


if __name__ == "__main__":
    root = tk.Tk()
    app = JSONMinifierApp(root)
    root.mainloop()
