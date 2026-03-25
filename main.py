import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

# --- ЛОГИКА РАСЧЕТА (Та же самая, что мы проверили) ---
def calculate_schedule(orders, specs):
    orders = orders.sort_values(by=['Priority', 'Deadline'], ascending=[False, True])
    schedule_list = []
    machine_free_at = {}
    simulation_start = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)

    for _, order in orders.iterrows():
        product = order['Product_Type']
        product_steps = specs[specs['Product_Type'] == product].sort_values(by='Operation_Order')
        current_order_ready_at = simulation_start

        for _, step in product_steps.iterrows():
            machine = step['Machine']
            total_duration = step['Time_Per_Unit_Min'] * order['Quantity']
            start_time = max(current_order_ready_at, machine_free_at.get(machine, simulation_start))
            end_time = start_time + timedelta(minutes=total_duration)
            
            schedule_list.append({
                'Order': f"Order {order['Order_ID']}",
                'Machine': machine,
                'Start': start_time,
                'Finish': end_time,
                'Product': product
            })
            machine_free_at[machine] = end_time
            current_order_ready_at = end_time

    return pd.DataFrame(schedule_list)

# --- ИНТЕРФЕЙС (GUI) ---
class SchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Production Scheduler Pro v1.0")
        self.root.geometry("500x350")
        self.root.configure(bg='#2e2e2e') # Темный фон

        self.file_path = ""

        # Стили для кнопок
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TButton", padding=10, font=('Helvetica', 10, 'bold'))

        # Заголовок
        self.label = tk.Label(root, text="FACTORY OPTIMIZER", fg="#00FF7F", bg="#2e2e2e", font=("Helvetica", 18, "bold"))
        self.label.pack(pady=20)

        self.info_label = tk.Label(root, text="Please select your Excel data file", fg="white", bg="#2e2e2e")
        self.info_label.pack(pady=5)

        # Кнопка выбора файла
        self.btn_browse = tk.Button(root, text="📂 SELECT EXCEL FILE", command=self.browse_file, 
                                   width=30, bg="#4a4a4a", fg="white", font=("Helvetica", 10))
        self.btn_browse.pack(pady=10)

        # Кнопка запуска
        self.btn_run = tk.Button(root, text="🚀 GENERATE GANTT CHART", command=self.run_process, 
                                state=tk.DISABLED, width=30, bg="#00FF7F", fg="black", font=("Helvetica", 10, "bold"))
        self.btn_run.pack(pady=20)

        # Подпись
        self.footer = tk.Label(root, text="Ready to optimize production flow", fg="#888888", bg="#2e2e2e", font=("Helvetica", 8))
        self.footer.pack(side=tk.BOTTOM, pady=10)

    def browse_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if self.file_path:
            self.info_label.config(text=f"File: ...{self.file_path[-30:]}", fg="#00FF7F")
            self.btn_run.config(state=tk.NORMAL)

    def run_process(self):
        try:
            orders_df = pd.read_excel(self.file_path, sheet_name='Orders')
            specs_df = pd.read_excel(self.file_path, sheet_name='Specs')
            
            result_df = calculate_schedule(orders_df, specs_df)
            
            fig = px.timeline(result_df, x_start="Start", x_end="Finish", y="Machine", color="Order",
                              title="Production Schedule - Optimized Timeline")
            fig.update_yaxes(autorange="reversed")
            
            # Та самая строка для сетки по часам
            fig.update_xaxes(dtick=10800000, tickformat="%H:%M\n%d %b", showgrid=True)
            
            fig.show()
            messagebox.showinfo("Success", "Schedule generated successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process file:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerApp(root)
    root.mainloop()