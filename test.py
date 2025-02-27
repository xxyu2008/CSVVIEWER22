import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import os

# 创建主窗口
root = tk.Tk()
root.title("CSV Viewer")

# 创建matplotlib图形和轴对象
fig2 = Figure(figsize=(8, 4), dpi=100)
ax2 = fig2.add_subplot(111)

# 将matplotlib图形嵌入到Tkinter窗口中
canvas2 = FigureCanvasTkAgg(fig2, master=root)
canvas2.draw()
canvas2.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

# 创建滚动条
v_scrollbar = tk.Scrollbar(root, orient="vertical")
v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
h_scrollbar = tk.Scrollbar(root, orient="horizontal")
h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

# 创建文本框用于显示数据，并配置滚动条
text_widget = tk.Text(root, wrap='none', height=20, width=80, yscrollcommand=v_scrollbar.set,
                      xscrollcommand=h_scrollbar.set)
text_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# 配置滚动条
v_scrollbar.config(command=text_widget.yview)
h_scrollbar.config(command=text_widget.xview)

# 创建按钮用于加载CSV文件
load_button = tk.Button(root, text="Load CSV", command=lambda: load_csv())
load_button.pack(side=tk.LEFT, padx=10, pady=10)

# 创建下拉菜单用于选择列
column_var = tk.StringVar()
column_menu = ttk.Combobox(root, textvariable=column_var, state='readonly')
column_menu.pack(side=tk.LEFT, padx=10, pady=10)

# 创建整数输入框用于输入变量
int_variable_entry = tk.Entry(root, width=10)
int_variable_entry.pack(side=tk.LEFT, padx=10, pady=10)

# 创建按钮用于传递变量
pass_int_variable_button = tk.Button(root, text="SET STEP", command=lambda: pass_int_variable())
pass_int_variable_button.pack(side=tk.LEFT, padx=10, pady=10)

# 创建按钮用于显示选中列的数据
show_button = tk.Button(root, text="Show Column", command=lambda: show_selected_column())
show_button.pack(side=tk.RIGHT, padx=10, pady=10)


def load_csv():

    global file_path  # 声明为全局变量，以便在其他函数中使用
    global df
    # 打开文件选择对话框
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return
    try:
        # 读取CSV文件，指定编码为gbk
        df = pd.read_csv(file_path, encoding='gbk')
        # 去除列名中的空格
        df.columns = df.columns.str.strip()
        # 更新列选择下拉菜单
        column_var.set('')  # 清空当前选择
        column_menu['values'] = ()  # 清空下拉菜单选项
        column_menu['values'] = df.columns.tolist()  # 添加新的列名选项
        # 显示原始数据
        text_widget.delete('1.0', tk.END)  # 清空文本框
        text_widget.insert(tk.END, df.to_string())
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read the CSV file: {e}")


def pass_int_variable():

    try:
        int_variable_value = int(int_variable_entry.get())
        print(f"Integer variable value: {int_variable_value}")  # 打印整数值，你可以在这里将其传递到其他函数或处理逻辑中
        # 例如，你可以将整数值存储为全局变量或传递给其他函数
        global int_variable
        int_variable = int_variable_value
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid integer.")


def show_selected_column():

    global upper_limit
    global nominal_value
    global lower_limit
    global USL
    global LSL
    selected_column = column_var.get()
    if not selected_column:
        messagebox.showwarning("Warning", "Please select a column first.")
        return
    try:
        df1 = df.iloc[:16]
        df2 = df.iloc[16:]
        data = df2.iloc[::int_variable]
        y = data[selected_column].values.astype(float)

        nominal_value = float(df1.loc[0, selected_column])
        LSL = float(df1.loc[1, selected_column])
        USL = float(df1.loc[2, selected_column])
        nominal_value = round(nominal_value, 3)
        LSL = round(LSL, 3)
        USL = round(USL, 3)
        upper_limit = nominal_value + USL
        lower_limit = nominal_value + LSL
        lower_limit = round(lower_limit, 3)
        upper_limit = round(upper_limit, 3)
        print(nominal_value)
        print(LSL)
        print(lower_limit)

        ax2.cla()  # 清空ax2轴
        file_name = os.path.basename(file_path)

        ax2.set_title(f'{file_name}', color='red')  # 设置标题为文件名，并设置颜色为红色
        ax2.set_xlabel('Index')
        ax2.set_ylabel(selected_column)

        ax2.axhline(y=upper_limit, color='r', linestyle='--')
        ax2.text(-1, upper_limit, f'USL: {upper_limit}', color='red', verticalalignment='bottom',
                 horizontalalignment='right')
        ax2.axhline(y=nominal_value, color='k', linestyle='-')
        ax2.text(-1, nominal_value, f'Nominal: {nominal_value}', color='red', verticalalignment='bottom',
                 horizontalalignment='right')
        ax2.axhline(y=lower_limit, color='r', linestyle='--')
        ax2.text(-1, lower_limit, f'LSL: {lower_limit}', color='red', verticalalignment='bottom',
                 horizontalalignment='right')

        ax2.plot(y, 'g*', label=selected_column)  # 绘制散点图

        legend = ax2.legend(loc='upper right')
        for text in legend.get_texts():
            text.set_color('red')  # 设置图例文本颜色为红色
            text.set_fontsize(16)  # 设置图例文本字体大小为16

        canvas2.draw()  # 重新绘制画布
    except Exception as e:
        messagebox.showerror("Error", f"Failed to show the selected column: {e}")


# 运行主循环
root.mainloop()