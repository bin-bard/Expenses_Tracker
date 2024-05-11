import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.filedialog
from PIL import Image, ImageTk
import customtkinter as ck
from tkinter import PhotoImage

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import os
import datetime
import calendar
import db
import time

import pandas as pd
import sqlite3
# Delete the file and move it to the computer's recycle bin instead of permanently deleting it
import send2trash

ck.set_appearance_mode("dark")
ck.set_default_color_theme("dark-blue")


class App(ck.CTk):
	WIDTH = 1200
	HEIGHT = 600

	def __init__(self):
		super().__init__()

		self.title("Expenses Tracker")
		self.resizable(0, 0)
		self.geometry(f"{self.WIDTH}x{self.HEIGHT}+70+30")

		self.input_balance = db.select_balance()
		print("Input Balance from database:", self.input_balance)

		self.balance = 0.0

		self.total_expenses = db.sum_all()
		print("Total Expenses from database:", self.total_expenses)

		# Sidebar
		self.sidebar_frame = ck.CTkFrame(self, fg_color="#725373", width=176, height=650, corner_radius=0)
		self.sidebar_frame.pack_propagate(0)
		self.sidebar_frame.pack(fill="y", anchor="w", side="left")

		# Logo
		logo_img_data = Image.open("image/logo.png")
		self.logo_img = ck.CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(77.68, 85.42))
		self.logo_label = ck.CTkLabel(master=self.sidebar_frame, text="", image=self.logo_img).pack(pady=(38, 0),
																									anchor="center")

		# Main View
		self.main_view = ck.CTkFrame(self, fg_color="#1a1e24", width=1400, height=1000, corner_radius=0)
		self.main_view.pack_propagate(0)
		self.main_view.pack(side="left")

		# Define function to clear the main_view frame
		def clear_main_view():
			for widget in self.main_view.winfo_children():
				widget.destroy()

		def switch_to_Dashboard():
			clear_main_view()
			# Insert button
			self.InsertButton = ck.CTkButton(
				self.main_view,
				text=None,
				fg_color="#654a64",
				corner_radius=50,
				width=50,
				height=50,
				hover=False,
				command=self.toggleEntryForm,
			)

			self.InsertButton.place(x=460, y=530)

			self.PlusLabel = ck.CTkLabel(
				self.InsertButton,
				bg_color="#654a64",
				text="+",
			)

			self.PlusLabel.place(
				relx=0.5, rely=0.5, anchor="center"
			)

			# cardBalance
			self.CardBalance = ck.CTkFrame(
				self.main_view,
				fg_color="#654a64",
				corner_radius=10,
				width=400,
				height=120
			)
			self.CardBalance.place(x=30, y=30)

			self.BalanceButton = ck.CTkButton(
				self.main_view,
				text="Add Balance",
				fg_color="#654a64",
				width=100,
				height=30,
				hover=False,
				font=("Cascadia Code", 12),
				command=self.buttonBalance,
			)

			self.BalanceButton.place(x=320, y=40)

			# cardExpenses
			self.CardExpenses = ck.CTkFrame(
				self.main_view,
				fg_color="#654a64",
				corner_radius=10,
				width=400,
				height=120
			)
			self.CardExpenses.place(x=500, y=30)

			# lable
			self.TitleBalance = ck.CTkLabel(
				self.main_view, text="BALANCE",
				fg_color="#654a64",
				font=("Franklin Gothic Medium", 22),
				width=20,
				height=10
			)
			self.TitleBalance.place(x=60, y=40)

			self.TitleExpenses = ck.CTkLabel(
				self.main_view, text="EXPENSES",
				fg_color="#654a64",
				font=("Franklin Gothic Medium", 22),
				width=20,
				height=10
			)
			self.TitleExpenses.place(x=520, y=40)

			self.BALANCE = ck.CTkLabel(
				self.main_view,
				text=f"$ {self.balance}",
				fg_color="#654a64",
				width=20,
				height=10,
				font=("Cascadia Code", 55)
			)
			self.BALANCE.place(x=65, y=70)

			self.Expenses = ck.CTkLabel(
				self.main_view,
				text=f"-$ {self.total_expenses}",
				fg_color="#654a64",
				width=20,
				height=10,
				font=("Cascadia Code", 55)
			)
			self.Expenses.place(x=530, y=70)

			self.ExpensesHistory = ck.CTkLabel(
				self.main_view,
				text="Expenses History",
				fg_color="#1a1e24",
				width=20,
				height=10,
				font=("Cascadia Code", 18)
			)
			self.ExpensesHistory.place(x=30, y=170)

			## EntryForm

			self.entryForm = ck.CTkFrame(self.main_view, fg_color="#482f47", width=400, height=360, corner_radius=40)
			self.entryForm.grid_columnconfigure((0, 3), minsize=200)

			# Description
			self.DescriptionLabel = ck.CTkLabel(self.entryForm,
												text="Description",
												fg_color="#482f47",
												font=("Arial Bold", 18),
												justify="left")

			self.DescriptionLabel.place(x=30, y=30)

			self.DescriptionEntry = ck.CTkEntry(self.entryForm, fg_color="#482f47", font=("Arial Bold", 18),
												border_width=0, width=300)
			self.DescriptionEntry.place(x=30, y=60)

			self.UnderLineEntry = ck.CTkFrame(self.entryForm, fg_color="white", height=3, width=300)
			self.UnderLineEntry.place(x=30, y=90)

			# Cost
			self.CostLabel = ck.CTkLabel(self.entryForm,
										 text="Cost",
										 fg_color="#482f47",
										 font=("Arial Bold", 18),
										 justify="left")

			self.CostLabel.place(x=30, y=120)

			self.CostEntry = ck.CTkEntry(self.entryForm, fg_color="#482f47", font=("Arial Bold", 18), border_width=0,
										 width=300)
			self.CostEntry.place(x=30, y=150)

			self.UnderLineCostEntry = ck.CTkFrame(self.entryForm, fg_color="white", height=3, width=300)
			self.UnderLineCostEntry.place(x=30, y=180)

			# menu category

			self.Category = ck.CTkOptionMenu(self.entryForm,
											 state="readonly",
											 fg_color="#2b1c2a",
											 button_color="#ada2ad",
											 values=["Food",
													 "Transport",
													 "Entertainment",
													 "Health",
													 "Education",
													 "Others"],
											 font=("Arial Bold", 18),
											 width=250
											 )
			self.Category.set("Select Category")
			self.Category.place(x=30, y=210)

			# Button submit and cancel
			self.SubmitButton = ck.CTkButton(self.entryForm,
											 text="Submit",
											 fg_color="#2b1c2a",
											 corner_radius=10,
											 width=0,
											 font=("Arial Bold", 18),
											 hover_color="#1c2026",
											 command=self.submitExpense
											 )
			self.SubmitButton.place(x=100, y=300)

			self.CancelButton = ck.CTkButton(self.entryForm,
											 text="Cancel",
											 fg_color="#2b1c2a",
											 corner_radius=10,
											 width=0,
											 font=("Arial Bold", 18),
											 command=self.clearEntry,
											 hover_color="#1c2026",

											 )
			self.CancelButton.place(x=180, y=300)

			# Table

			table_data = self.getData()
			header = ["ID", "Expense_Name", "Category", "Cost", "Time"]

			self.table_frame = tk.Frame(self.main_view)
			self.table_frame.place(x=100, y=270)

			# add style
			style = ttk.Style()
			style.theme_use("clam")
			style.configure("Treeview",
							background="#1a1e24",
							foreground="white",
							rowheight=25,
							fieldbackground="#1a1e24",
							font=("Arial Bold", 14)

							)

			style.map("Treeview", background=[('selected', '#482f47')])

			self.table = ttk.Treeview(self.table_frame, columns=header, show='headings', style="Treeview", height=14)

			for column in header:
				self.table.heading(column, text=column)

			for row in table_data:
				self.table.insert('', 'end', values=row)

			self.table.pack(expand=True)
			self.table.bind("<Double-Button-1>", self.deleteRow)

			self.button_save = ck.CTkButton(master=self.main_view,
											text="Save Expenses in excel",
											command=self.save_expenses
											)
			self.button_save.place(x=100, y=525)

			self.update_balance()

		def switch_to_Analytics():
			clear_main_view()
			# Default chart: Bar chart and default time: This Year
			self.selected_chart = "Bar Chart"
			self.selected_time = "This Year"

			self.start_of_time = None
			self.end_of_time = None

			# Hàm để kết nối và truy vấn dữ liệu từ cơ sở dữ liệu
			def query_data():
				conn = sqlite3.connect('expense.db')

				end_of_time_query = "SELECT MAX(datetime(Time)) FROM expenses"
				end_of_time_result = conn.execute(end_of_time_query).fetchone()[0]
				self.end_of_time = datetime.datetime.strptime(end_of_time_result, "%Y-%m-%d %H:%M:%S")
				if self.selected_time == "This Year":
					self.start_of_time = datetime.datetime(datetime.datetime.now().year, 1, 1)
				elif self.selected_time == "This Month":
					self.start_of_time = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month,
														   1)
				else:  # All Time
					self.start_of_time = None  # Không cần thiết đặt ngày bắt đầu cho All Time

				if self.start_of_time:
					query = "SELECT Category, Cost, Time FROM expenses WHERE Time BETWEEN ? AND ?"
					df_category = pd.read_sql_query(query, conn, params=[self.start_of_time, self.end_of_time])
				else:
					query = "SELECT Category, Cost, Time FROM expenses"
					df_category = pd.read_sql_query(query, conn)

				conn.close()

				return df_category

			# Line_Chart: Income Line Query
			def query_income_data():
				conn = sqlite3.connect('expense.db')

				end_of_time_query = "SELECT MAX(datetime(Balance_time)) FROM balance"
				end_of_time_result = conn.execute(end_of_time_query).fetchone()[0]
				self.end_of_time = datetime.datetime.strptime(end_of_time_result, "%Y-%m-%d %H:%M:%S")
				if self.selected_time == "This Year":
					self.start_of_time = datetime.datetime(datetime.datetime.now().year, 1, 1)
				elif self.selected_time == "This Month":
					self.start_of_time = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month,
														   1)
				else:  # All Time
					self.start_of_time = None  # Không cần thiết đặt ngày bắt đầu cho All Time

				if self.start_of_time:
					query = "SELECT Balance, Balance_time FROM balance WHERE Balance_time BETWEEN ? AND ?"
					df_income = pd.read_sql_query(query, conn, params=[self.start_of_time, self.end_of_time])
				else:
					query = "SELECT Balance, Balance_time FROM balance"
					df_income = pd.read_sql_query(query, conn)

				conn.close()

				return df_income

			# Hàm update_chart sử dụng hàm query_data
			def update_chart():
				df_category = query_data()
				if self.selected_chart == "Bar Chart" or self.selected_chart == "Pie Chart":
					grouped = df_category.groupby('Category').sum()
					grouped = grouped.sort_values('Cost', ascending=True)
				else:  # Line Chart
					grouped = df_category.sort_values('Time', ascending=True)
					grouped['Time'] = pd.to_datetime(df_category['Time'])
				return grouped

			def show_selected_chart():
				self.selected_chart = self.chart_selection.get()
				self.selected_time = self.time_selection.get()
				if self.selected_chart == "Bar Chart":
					plot_bar_chart()
				elif self.selected_chart == "Pie Chart":
					plot_pie_chart()
				elif self.selected_chart == "Line Chart":
					plot_line_chart()

			def plot_bar_chart():
				grouped = update_chart()

				self.fig = Figure(figsize=(12, 6), facecolor="#b8d3ff")
				ax_1 = self.fig.add_subplot()

				# Danh sách các màu sử dụng cho từng cột
				colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#C70039', '#9467bd', '#8c564b']

				# Vẽ biểu đồ cột với màu tùy chỉnh và hiển thị số liệu lên đầu cột
				bars = ax_1.bar(grouped.index, grouped['Cost'], width=0.7, color=colors)
				for bar in bars:
					height = bar.get_height()
					ax_1.text(bar.get_x() + bar.get_width() / 2, height, '{:.2f}'.format(height),
							  ha='center', va='bottom', color='black')  # Chỉnh màu số liệu

				ax_1.set_xlabel('Category', fontsize=14, fontweight='bold', color='#2ba8ff')
				ax_1.set_ylabel('Total Cost', fontsize=14, fontweight='bold', color='#2ba8ff')
				ax_1.set_title('Expenses By Category', fontsize=16, fontweight='bold', color='#C70039')

				canvas = FigureCanvasTkAgg(figure=self.fig, master=app.main_view)
				canvas.draw()
				canvas.get_tk_widget().place(x=70, y=200)

			def plot_pie_chart():
				grouped = update_chart()

				self.fig = Figure(figsize=(12, 6), facecolor="#b8d3ff")
				ax2 = self.fig.add_subplot()

				# Define colors for each wedge in the pie chart
				colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#C70039', '#9467bd', '#8c564b']

				# Draw the pie chart with custom colors for wedges
				wedges, texts, autotexts = ax2.pie(grouped['Cost'], labels=grouped.index, autopct='%1.1f%%',
												   colors=colors)

				# Customize font properties of the labels
				for i, text in enumerate(texts):
					text.set_fontsize(16)
					text.set_fontweight('bold')
					text.set_color(colors[i])  # Set label color to match corresponding wedge color

				# Customize font properties of the percentage values
				for autotext in autotexts:
					autotext.set_fontsize(14)  # Set font size
					# autotext.set_fontweight('bold')  # Set font weight to bold
					autotext.set_color('black')  # Set autotext color to black

				ax2.set_title('Expenses By Category', fontsize=16, fontweight='bold', color='#21b3cc')

				canvas = FigureCanvasTkAgg(figure=self.fig, master=self.main_view)
				canvas.draw()
				canvas.get_tk_widget().place(x=70, y=200)

			def plot_line_chart():
				df_category = update_chart()

				df_income = query_income_data()
				df_income['Balance_time'] = pd.to_datetime(df_income['Balance_time'])

				self.fig = plt.figure(figsize=(12, 6), facecolor="#b8d3ff")
				ax = self.fig.add_subplot()

				if self.selected_time == "This Year":
					frequency = 'M'
					xlabel = "Months"
					# Group by month and use the start of each month as the marker MS
					grouped = df_category.groupby(pd.Grouper(key='Time', freq='MS')).sum()
					income_grouped = df_income.groupby(pd.Grouper(key='Balance_time', freq='MS')).sum()
					# Định dạng lại nhãn trục x để hiển thị theo dạng 'Year-Month'
					ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
					# Chỉ định các điểm dữ liệu hàng tháng mà không có khoảng trống giữa chúng
					ax.xaxis.set_major_locator(mdates.MonthLocator())

				elif self.selected_time == "This Month":
					frequency = 'D'
					xlabel = "Days"
					grouped = df_category.groupby(pd.Grouper(key='Time', freq='D')).sum()
					income_grouped = df_income.groupby(pd.Grouper(key='Balance_time', freq='D')).sum()
					# Định dạng lại nhãn trục x để hiển thị theo dạng 'Month-Day'
					ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
					# Chỉ định các điểm dữ liệu hàng ngày mà không có khoảng trống giữa chúng
					ax.xaxis.set_major_locator(mdates.DayLocator())

				else:  # All Time
					frequency = 'Y'
					xlabel = "Years"
					grouped = df_category.groupby(pd.Grouper(key='Time', freq='YS')).sum()
					income_grouped = df_income.groupby(pd.Grouper(key='Balance_time', freq='YS')).sum()
					ax.xaxis.set_major_locator(mdates.YearLocator())

				# Đường 1
				ax.plot(grouped.index, grouped['Cost'], marker='o', linestyle='-', color='#32d2bf', label='Expenses')
				# Đường 2
				ax.plot(income_grouped.index, income_grouped['Balance'], marker='o', linestyle='-', color='#ff7f0e',
						label='Income')
				ax.legend()  # Chú thích cho 2 đường

				# Đặt số trên mỗi điểm của đường thu nhập
				for i in range(len(income_grouped)):
					rounded_balance = round(income_grouped['Balance'].iloc[i], 2)  # làm tròn đến 2 chữ số thập phân
					ax.annotate(f"{rounded_balance}", (income_grouped.index[i], income_grouped['Balance'].iloc[i]),
								textcoords="offset points",
								xytext=(0, 10), ha='center',
								color='#ff7f0e')  # Màu cho số liệu của đường thu nhập

				# Đặt số trên mỗi điểm của đường chi tiêu
				for i in range(len(grouped)):
					rounded_cost = round(grouped['Cost'].iloc[i], 2)  # làm tròn đến 2 chữ số thập phân
					ax.annotate(f"{rounded_cost}", (grouped.index[i], grouped['Cost'].iloc[i]),
								textcoords="offset points",
								xytext=(0, 10), ha='center',
								color='#32d2bf')  # Màu cho số liệu của đường chi tiêu

				ax.set_xlabel(xlabel, fontsize=16, fontweight='bold', color='#2ba8ff')
				ax.set_ylabel('Total Cost', fontsize=16, fontweight='bold', color='#2ba8ff')
				ax.set_title('Overview Chart of Expenses and Income over Time', fontsize=16, fontweight='bold',
							 color='#C70039')

				canvas = FigureCanvasTkAgg(self.fig, master=app.main_view)
				canvas.draw()
				canvas.get_tk_widget().place(x=70, y=200)

			def save_chart():
				selected_chart = self.chart_selection.get()
				if selected_chart == "Bar Chart":
					default_filename = "bar_chart.png"
					fig = self.fig
				elif selected_chart == "Pie Chart":
					default_filename = "pie_chart.png"
					fig = self.fig
				elif selected_chart == "Line Chart":
					default_filename = "line_chart.png"
					fig = self.fig

				# Open a file dialog for saving the chart
				file_path = tkinter.filedialog.asksaveasfilename(
					initialdir="chart_images",
					initialfile=default_filename,
					defaultextension=".png",
					filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
				)

				# Save the chart if a file path is chosen
				if file_path:
					fig.savefig(file_path)
					tk.messagebox.showinfo("Success", f"Chart saved as {file_path}")
				else:
					tk.messagebox.showinfo("Information", "Saving cancelled.")

			self.fig = None
			# Create a Label for chart selection
			self.chart_selection_label = ck.CTkLabel(self.main_view, text="CHART TYPE:", font=("Arial Bold", 24),
													 fg_color="#6c4b8a")
			self.chart_selection_label.place(x=50, y=50)

			# Create OptionMenu for chart selection
			self.chart_selection = ck.CTkOptionMenu(self.main_view,
													fg_color="#2b1c2a",
													button_color="#ada2ad",
													values=["Bar Chart", "Pie Chart", "Line Chart"],
													font=("Arial Bold", 24),
													width=180)
			self.chart_selection.set("Bar Chart")
			self.chart_selection.place(x=230, y=50)

			# Create OptionMenu for time selection
			self.time_selection = ck.CTkOptionMenu(self.main_view,
												   fg_color="#2b1c2a",
												   button_color="#ada2ad",
												   values=["This Year", "This Month", "All Time"],
												   font=("Arial Bold", 24),
												   width=180)
			self.time_selection.set("This Year")
			self.time_selection.place(x=800, y=50)

			# Create a button to show selected chart
			show_img_data = Image.open("image/data-report.png")
			show_img = ck.CTkImage(light_image=show_img_data, dark_image=show_img_data, size=(70, 70))
			self.show_button = ck.CTkButton(master=self.main_view,
											image=show_img,
											text="",
											fg_color="#292d3e",
											hover_color="#4d3461",
											width=30,
											command=show_selected_chart)
			self.show_button.place(x=890, y=100)

			# Create a button to save chart
			save_img_data = Image.open("image/save_chart.png")
			save_img = ck.CTkImage(light_image=save_img_data, dark_image=save_img_data, size=(70, 70))
			self.save_button = ck.CTkButton(master=self.main_view,
											image=save_img,
											text="",
											fg_color="#292d3e",
											hover_color="#4d3461",
											width=30,
											command=save_chart)
			self.save_button.place(x=890, y=200)
			plot_bar_chart()

		def switch_to_Save():
			clear_main_view()
			self.tree_2 = None
			self.tree_1 = None

			# Add style
			style = ttk.Style()
			style.theme_use("clam")

			# Configure column headings
			style.configure("Treeview.Heading",
							font=('Arial Bold', 14),
							background="#515d70",
							foreground="white")

			style.configure("Treeview",
							background="#1a1e24",
							foreground="white",
							rowheight=25,
							fieldbackground="#1a1e24",
							font=("Arial Bold", 14)
							)

			style.map('Treeview',
					  foreground=[('selected', 'black')],
					  background=[('selected', '#e5f3ff')])

			def populate_treeview(tree, directory):
				for item in os.listdir(directory):
					item_path = os.path.join(directory, item)
					if os.path.isfile(item_path):
						file_info = get_file_info(item_path)
						tree.insert("", "end", text=item, values=file_info)

			def get_file_info(file_path):
				file_name = os.path.basename(file_path)
				date_modified = os.path.getmtime(file_path)
				file_type = "File"
				size_kb = round(os.path.getsize(file_path) / 1024, 2)
				return (file_name, format_timestamp(date_modified), file_type, size_kb)

			def format_timestamp(timestamp):
				return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))

			def delete_file_confirm(file_path):
				confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{file_path}'?")
				if confirm:
					try:
						send2trash.send2trash(file_path)  # Xoá tập tin và đưa vào thùng rác
						messagebox.showinfo("Success", f"Successfully deleted '{file_path}'!")
						# Sau khi xoá tập tin thành công, làm mới lại Treeview
						refresh_treeview()
					except Exception as e:
						messagebox.showerror("Error", f"An error occurred while deleting '{file_path}': {str(e)}")

			def on_treeview_double_click(event):
				selected_tree = event.widget
				if selected_tree == self.tree_1:
					directory = "chart_images"
				elif selected_tree == self.tree_2:
					directory = "excel_saved"
				else:
					return

				item = selected_tree.selection()[0]
				file_path = os.path.join(directory, selected_tree.item(item, "text"))
				delete_file_confirm(file_path)

			def refresh_treeview():
				# Delete all current items in the Treeview and reload
				self.tree_1.delete(*self.tree_1.get_children())
				self.tree_2.delete(*self.tree_2.get_children())
				populate_treeview(self.tree_1, "chart_images")
				populate_treeview(self.tree_2, "excel_saved")

			def show_xlsx_treeview():
				# First Treeview for "excel_saved" folder
				tree_frame_2 = ck.CTkFrame(self.main_view, fg_color="#1a1e24", width=500, height=500)
				tree_frame_2.place(x=250, y=120)
				self.tree_2 = ttk.Treeview(tree_frame_2,
										   height=10,
										   columns=("Name",
													"Date Modified",
													"Type",
													"Size (KB)"),
										   show='headings')
				self.tree_2.column("Name", width=300, anchor="w")
				self.tree_2.column("Date Modified", width=300, anchor="w")
				self.tree_2.column("Type", width=200, anchor="w")
				self.tree_2.column("Size (KB)", width=200, anchor="e")

				self.tree_2.heading("Name", text="Name", anchor="w")
				self.tree_2.heading("Date Modified", text="Date Modified", anchor="w")
				self.tree_2.heading("Type", text="Type", anchor="w")
				self.tree_2.heading("Size (KB)", text="Size (KB)", anchor="w")
				self.tree_2.pack(fill="both", expand=True)
				self.tree_2.bind("<Double-1>", on_treeview_double_click)
				populate_treeview(self.tree_2, "excel_saved")

			def show_png_treeview():
				# Second Treeview for "chart_images" folder
				tree_frame_1 = ck.CTkFrame(self.main_view, fg_color="#1a1e24", width=500, height=500)
				tree_frame_1.place(x=250, y=320)
				self.tree_1 = ttk.Treeview(tree_frame_1,
										   height=10,
										   columns=("Name",
													"Date Modified",
													"Type", "Size (KB)"),
										   show='headings')
				self.tree_1.column("Name", width=300, anchor="w")
				self.tree_1.column("Date Modified", width=300, anchor="w")
				self.tree_1.column("Type", width=200, anchor="w")
				self.tree_1.column("Size (KB)", width=200, anchor="e")
				self.tree_1.heading("#0", text="Name", anchor="w")
				self.tree_1.heading("Name", text="Name", anchor="w")
				self.tree_1.heading("Date Modified", text="Date Modified", anchor="w")
				self.tree_1.heading("Type", text="Type", anchor="w")
				self.tree_1.heading("Size (KB)", text="Size (KB)", anchor="w")
				self.tree_1.pack(fill="both", expand=True)
				self.tree_1.bind("<Double-1>", on_treeview_double_click)
				populate_treeview(self.tree_1, "chart_images")

			self.save_label = ck.CTkLabel(self.main_view, text="MANAGE FILES:", font=("Arial Bold", 24),
										  fg_color="#6c4b8a")
			self.save_label.place(x=50, y=50)

			pngfile_img_data = Image.open("image/png-file.png")
			pngfile_img = ck.CTkImage(light_image=pngfile_img_data, dark_image=pngfile_img_data, size=(70, 70))
			self.pngfile_button = ck.CTkButton(master=self.main_view,
											   image=pngfile_img,
											   text="",
											   fg_color="#292d3e",
											   hover_color="#4d3461",
											   width=30,
											   command=show_png_treeview)
			self.pngfile_button.place(x=100, y=320)

			xlsxfile_img_data = Image.open("image/xlsx.png")
			xlsxfile_img = ck.CTkImage(light_image=xlsxfile_img_data, dark_image=xlsxfile_img_data, size=(70, 70))
			self.xlsxfile_button = ck.CTkButton(master=self.main_view,
												image=xlsxfile_img,
												text="",
												fg_color="#292d3e",
												hover_color="#4d3461",
												width=30,
												command=show_xlsx_treeview)
			self.xlsxfile_button.place(x=100, y=120)

			show_xlsx_treeview()
			show_png_treeview()

		# Buttons
		expen_img_data = Image.open("image/home.png")
		self.expen_img = ck.CTkImage(light_image=expen_img_data, dark_image=expen_img_data, size=(43, 43))
		self.btnExpen = ck.CTkButton(master=self.sidebar_frame,
									 image=self.expen_img,
									 text="Dashboard",
									 fg_color="#725373",
									 font=("Arial Bold", 14),
									 text_color="#efe5ef",
									 hover_color="#1c2026",
									 anchor="w",
									 command=switch_to_Dashboard).pack(anchor="center", ipady=5, pady=(60, 0))

		analytic_img_data = Image.open("image/analytics.png")
		self.analytic_img = ck.CTkImage(light_image=analytic_img_data, dark_image=analytic_img_data, size=(43, 43))
		self.btnAnalytic = ck.CTkButton(master=self.sidebar_frame,
										image=self.analytic_img,
										text="Analytics",
										fg_color="#725373",
										font=("Arial Bold", 14),
										text_color="#efe5ef",
										hover_color="#1c2026",
										anchor="w",
										command=switch_to_Analytics).pack(anchor="center", ipady=5, pady=(16, 0))

		save_img_data = Image.open("image/managefile.png")
		self.save_img = ck.CTkImage(light_image=save_img_data, dark_image=save_img_data, size=(43, 43))
		self.Save = ck.CTkButton(master=self.sidebar_frame,
								 image=self.save_img,
								 text="Files",
								 fg_color="#725373",
								 font=("Arial Bold", 14),
								 text_color="#efe5ef",
								 hover_color="#1c2026",
								 anchor="w",
								 command=switch_to_Save).pack(anchor="center", ipady=5, pady=(16, 0))

		switch_to_Dashboard()

	# entry animation when the button is clicked
	def entryAnimation(self):
		self.entryForm.update()
		self.entryForm.place(relx=0.5, y=360, anchor="center")
		self.entryForm.lift()

	def toggleEntryForm(self):
		if self.entryForm.winfo_viewable():
			self.entryForm.place_forget()
		else:
			self.entryAnimation()

	def buttonBalance(self):
		dialog = ck.CTkInputDialog(text="Type in your balance:", title="Add Balance")
		self.input_balance = dialog.get_input()
		print("Balance:", self.input_balance)

		time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		db.insert_balance(self.input_balance, time)

		# Update expenses
		self.updateExpenses()
		# Update balance
		self.update_balance()

	def clearEntry(self):
		self.Category.set('Select Category')  # Assuming self.Category is a StringVar
		self.DescriptionEntry.delete(0, 'end')
		self.CostEntry.delete(0, 'end')

	def submitExpense(self):
		# Retrieve information
		expense_name = self.DescriptionEntry.get()
		category = self.Category.get()
		cost = self.CostEntry.get()

		if not expense_name or not cost or category == "Select Category":
			tk.messagebox.showinfo("Error", "Please fill in all fields!")
			return

		time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		# Insert into database
		db.insert_groceries(expense_name, category, cost, time)
		tk.messagebox.showinfo("Success", "Expense submitted successfully!")

		# Update total_expenses
		self.total_expenses = db.sum_all()
		# Update the Expenses label
		self.updateExpenses()
		# Update balance
		self.update_balance()
		# Refresh the table
		self.refresh_table()

	def getData(self):
		data = db.select_all()
		return data

	def deleteRow(self, event):
		# Get the clicked row
		clicked_row = self.table.identify_row(event.y)
		# Get the data for the clicked row
		clicked_row_data = self.table.item(clicked_row, 'values')
		id = clicked_row_data[0]

		if tk.messagebox.askyesno("Confirmation", f"Do you want to delete the expense with ID {id}?"):
			# Delete from database
			db.delete_one(id)

			# Update total_expenses
			self.total_expenses = db.sum_all()
			# Update balance
			self.update_balance()
			# Update the Expenses label
			self.updateExpenses()
			# Delete from table
			self.table.delete(clicked_row)
			# Refresh the table
			self.refresh_table()

	def refresh_table(self):
		# Clear the table
		for row in self.table.get_children():
			self.table.delete(row)

		# Get the new data
		table_data = self.getData()

		# Insert the new data into the table
		for row in table_data:
			self.table.insert('', 'end', values=row)

	def updateExpenses(self):
		self.Expenses.configure(text=f"-$ {self.total_expenses}")
		self.Expenses.update_idletasks()

	def update_balance(self):
		if self.input_balance is None:
			print("Input balance is not set.")
			return
		expenses = db.sum_all()
		self.balance = float(self.input_balance) - expenses
		print("Balance:", self.balance)

		self.BALANCE.configure(text=f"$ {self.balance}")
		self.BALANCE.update_idletasks()

	def save_expenses(self):
		# Get data from the database
		data = db.select_all()
		# Create a DataFrame from the data
		df = pd.DataFrame(data, columns=['ID', 'Expense_Name', 'Category', 'Cost', 'Time'])

		# Open a file dialog for saving the Excel file
		file_path = tkinter.filedialog.asksaveasfilename(
			initialdir="excel_saved",
			defaultextension=".xlsx",
			filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
		)

		# Save the Excel file if a file path is chosen
		if file_path:
			df.to_excel(file_path, index=False)
			tk.messagebox.showinfo("Success", "Excel file saved successfully!")
		else:
			tk.messagebox.showinfo("Information", "Saving cancelled.")

	def show_expenses_plot(self):
		# Create a new Tk window
		new_window = tk.Toplevel(self)

		# Rest of your code...
		conn = sqlite3.connect('expense.db')
		query = "SELECT Time, Cost FROM expenses LIMIT 30"
		df = pd.read_sql_query(query, conn)
		conn.close()
		df['Time'] = pd.to_datetime(df['Time']).dt.strftime('%m-%d')
		grouped = df.groupby('Time').sum()
		grouped = grouped.sort_values('Time')

		fig_1 = Figure(figsize=(15, 7), facecolor="#725373")
		ax_1 = fig_1.add_subplot()
		ax_1.plot(grouped.index, grouped['Cost'])
		ax_1.set_xlabel('Time')
		ax_1.set_xticklabels(grouped.index, rotation=45, ha='right')
		ax_1.set_xlabel('Cost')
		ax_1.grid(visible=True)

		ax_1.xaxis.set_label_position('top')
		ax_1.set_xlabel('Expenses Over Time', fontsize=15, labelpad=10)

		# Draw the plot on the new Tkinter canvas
		canvas = FigureCanvasTkAgg(figure=fig_1, master=new_window)
		canvas.draw()
		canvas.get_tk_widget().pack()


if __name__ == "__main__":
	app = App()
	app.mainloop()
