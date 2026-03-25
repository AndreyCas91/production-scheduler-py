# 🏭 Production Scheduler Pro v1.0

An automated production planning tool built with **Python**, **Pandas**, and **Plotly**. This application transforms raw Excel order data into an optimized, interactive Gantt chart.

## 🚀 Key Features
- **Smart Scheduling:** Uses Forward Scheduling logic to prevent machine overlaps.
- **Priority-Based:** Orders are automatically sorted by priority and delivery deadlines.
- **Modern GUI:** Built with Tkinter for a seamless user experience.
- **Interactive Visualization:** High-quality Gantt charts with hover-data for each workstation.

## 🛠️ Tech Stack
- **Python 3.13**
- **Data:** Pandas, OpenPyXL
- **Visualization:** Plotly Express
- **UI:** Tkinter (Standard Library)
- **Deployment:** Compiled via PyInstaller

## 📋 How to Use
1. Prepare your data in `production_data.xlsx` (tabs: *Orders* and *Specs*).
2. Run the `Production_Scheduler.exe` or `python main.py`.
3. Select your file and click **Generate**.
4. The interactive chart will open automatically in your default browser.

---
*Developed for professional manufacturing optimization.*