import tkinter as tk
from tkinter import ttk, messagebox
import locale
from datetime import datetime, timedelta

class LoanCalculator:
    def __init__(self):
        # Set up the main window
        self.window = tk.Tk()
        self.window.title("Enhanced Loan Calculator")
        self.window.geometry("600x500")
        self.window.resizable(True, True)
        self.window.configure(padx=10, pady=10)
        
        # Set locale for currency formatting
        locale.setlocale(locale.LC_ALL, '')
        
        # Create tabbed interface
        self.tab_control = ttk.Notebook(self.window)
        
        # Create tabs
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)
        self.tab3 = ttk.Frame(self.tab_control)
        
        self.tab_control.add(self.tab1, text='Loan Calculator')
        self.tab_control.add(self.tab2, text='Amortization Schedule')
        self.tab_control.add(self.tab3, text='Comparison')
        self.tab_control.pack(expand=1, fill="both")
        
        # Create variables
        self.annualInterestRateVar = tk.StringVar(value="5.0")
        self.numberOfYearsVar = tk.StringVar(value="30")
        self.loanAmountVar = tk.StringVar(value="250000")
        self.monthlyPaymentVar = tk.StringVar()
        self.totalPaymentVar = tk.StringVar()
        self.totalInterestVar = tk.StringVar()
        self.startDateVar = tk.StringVar(value=datetime.now().strftime("%m/%d/%Y"))
        
        # Create main calculator tab
        self.create_calculator_tab()
        
        # Create amortization schedule tab
        self.create_amortization_tab()
        
        # Create comparison tab
        self.create_comparison_tab()
        
        # Calculate initial values
        self.computePayment()
        
        # Start the main loop
        self.window.mainloop()

    def create_calculator_tab(self):
        # Create frames
        input_frame = ttk.LabelFrame(self.tab1, text="Loan Information")
        input_frame.pack(padx=10, pady=10, fill="both")
        
        result_frame = ttk.LabelFrame(self.tab1, text="Loan Results")
        result_frame.pack(padx=10, pady=10, fill="both")
        
        # Create a style for input fields
        style = ttk.Style()
        style.configure('TEntry', padding=5)
        
        # Input fields
        ttk.Label(input_frame, text="Loan Amount ($):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(input_frame, textvariable=self.loanAmountVar, width=20, justify="right").grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Annual Interest Rate (%):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(input_frame, textvariable=self.annualInterestRateVar, width=20, justify="right").grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Loan Term (Years):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(input_frame, textvariable=self.numberOfYearsVar, width=20, justify="right").grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Start Date (MM/DD/YYYY):").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(input_frame, textvariable=self.startDateVar, width=20, justify="right").grid(row=3, column=1, padx=5, pady=5)
        
        # Result fields
        ttk.Label(result_frame, text="Monthly Payment:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Label(result_frame, textvariable=self.monthlyPaymentVar, width=20, borderwidth=2, relief="sunken").grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(result_frame, text="Total Payment:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Label(result_frame, textvariable=self.totalPaymentVar, width=20, borderwidth=2, relief="sunken").grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(result_frame, text="Total Interest:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        ttk.Label(result_frame, textvariable=self.totalInterestVar, width=20, borderwidth=2, relief="sunken").grid(row=2, column=1, padx=5, pady=5)
        
        # Buttons frame
        button_frame = ttk.Frame(self.tab1)
        button_frame.pack(padx=10, pady=10, fill="x")
        
        ttk.Button(button_frame, text="Calculate", command=self.computePayment, width=15).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Reset", command=self.reset, width=15).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Exit", command=self.window.destroy, width=15).pack(side="right", padx=5)

    def create_amortization_tab(self):
        # Create control frame
        control_frame = ttk.Frame(self.tab2)
        control_frame.pack(pady=10, fill="x")
        
        ttk.Button(control_frame, text="Generate Schedule", command=self.generate_amortization).pack(side="left", padx=5)
        
        # Create treeview for amortization schedule
        columns = ("payment_num", "payment_date", "payment", "principal", "interest", "balance")
        self.tree = ttk.Treeview(self.tab2, columns=columns, show="headings", height=15)
        
        # Define column headings
        self.tree.heading("payment_num", text="Payment #")
        self.tree.heading("payment_date", text="Payment Date")
        self.tree.heading("payment", text="Payment")
        self.tree.heading("principal", text="Principal")
        self.tree.heading("interest", text="Interest")
        self.tree.heading("balance", text="Remaining Balance")
        
        # Define column widths
        self.tree.column("payment_num", width=70, anchor="center")
        self.tree.column("payment_date", width=100, anchor="center")
        self.tree.column("payment", width=100, anchor="e")
        self.tree.column("principal", width=100, anchor="e")
        self.tree.column("interest", width=100, anchor="e")
        self.tree.column("balance", width=120, anchor="e")
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(self.tab2, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_comparison_tab(self):
        # Create frames
        input_frame = ttk.LabelFrame(self.tab3, text="Compare Loan Options")
        input_frame.pack(padx=10, pady=10, fill="both")
        
        # Current loan info (read-only)
        ttk.Label(input_frame, text="Current Loan:").grid(row=0, column=0, columnspan=2, sticky="w", padx=5, pady=5)
        
        ttk.Label(input_frame, text="Amount:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.curr_amount_label = ttk.Label(input_frame, text="")
        self.curr_amount_label.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        ttk.Label(input_frame, text="Interest Rate:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.curr_rate_label = ttk.Label(input_frame, text="")
        self.curr_rate_label.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        ttk.Label(input_frame, text="Term (Years):").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.curr_term_label = ttk.Label(input_frame, text="")
        self.curr_term_label.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        
        ttk.Label(input_frame, text="Monthly Payment:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.curr_payment_label = ttk.Label(input_frame, text="")
        self.curr_payment_label.grid(row=4, column=1, sticky="w", padx=5, pady=5)
        
        # Alternative loan info
        ttk.Label(input_frame, text="Alternative Loan:").grid(row=0, column=2, columnspan=2, sticky="w", padx=5, pady=5)
        
        ttk.Label(input_frame, text="Amount:").grid(row=1, column=2, sticky="e", padx=5, pady=5)
        self.alt_amount_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.alt_amount_var, width=15).grid(row=1, column=3, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Interest Rate (%):").grid(row=2, column=2, sticky="e", padx=5, pady=5)
        self.alt_rate_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.alt_rate_var, width=15).grid(row=2, column=3, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Term (Years):").grid(row=3, column=2, sticky="e", padx=5, pady=5)
        self.alt_term_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.alt_term_var, width=15).grid(row=3, column=3, padx=5, pady=5)
        
        # Results frame
        result_frame = ttk.LabelFrame(self.tab3, text="Comparison Results")
        result_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.comparison_result = ttk.Label(result_frame, text="Enter alternative loan details and click Compare")
        self.comparison_result.pack(padx=10, pady=10)
        
        # Button
        ttk.Button(self.tab3, text="Compare Loans", command=self.compare_loans).pack(pady=10)

    def computePayment(self):
        try:
            # Get input values
            loan_amount = float(self.loanAmountVar.get())
            annual_interest_rate = float(self.annualInterestRateVar.get())
            years = int(self.numberOfYearsVar.get())
            
            # Validate inputs
            if loan_amount <= 0:
                messagebox.showerror("Input Error", "Loan amount must be greater than zero")
                return
                
            if annual_interest_rate < 0:
                messagebox.showerror("Input Error", "Interest rate cannot be negative")
                return
                
            if years <= 0:
                messagebox.showerror("Input Error", "Loan term must be greater than zero")
                return
            
            # Calculate monthly interest rate
            monthly_interest_rate = annual_interest_rate / 1200
            
            # Calculate monthly payment
            if monthly_interest_rate > 0:
                monthly_payment = loan_amount * monthly_interest_rate / (1 - 1 / (1 + monthly_interest_rate) ** (years * 12))
            else:
                # Handle 0% interest case
                monthly_payment = loan_amount / (years * 12)
            
            # Calculate total payment and interest
            total_payment = monthly_payment * years * 12
            total_interest = total_payment - loan_amount
            
            # Update display
            self.monthlyPaymentVar.set(locale.currency(monthly_payment, grouping=True))
            self.totalPaymentVar.set(locale.currency(total_payment, grouping=True))
            self.totalInterestVar.set(locale.currency(total_interest, grouping=True))
            
            # Update comparison tab
            self.curr_amount_label.config(text=locale.currency(loan_amount, grouping=True))
            self.curr_rate_label.config(text=f"{annual_interest_rate}%")
            self.curr_term_label.config(text=f"{years} years")
            self.curr_payment_label.config(text=locale.currency(monthly_payment, grouping=True))
            
            return monthly_payment
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values")
            return None

    def reset(self):
        self.loanAmountVar.set("250000")
        self.annualInterestRateVar.set("5.0")
        self.numberOfYearsVar.set("30")
        self.startDateVar.set(datetime.now().strftime("%m/%d/%Y"))
        self.computePayment()

    def generate_amortization(self):
        monthly_payment = self.computePayment()
        if monthly_payment is None:
            return
            
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            # Get data
            loan_amount = float(self.loanAmountVar.get())
            annual_interest_rate = float(self.annualInterestRateVar.get())
            years = int(self.numberOfYearsVar.get())
            start_date = datetime.strptime(self.startDateVar.get(), "%m/%d/%Y")
            
            # Calculate monthly interest rate
            monthly_interest_rate = annual_interest_rate / 1200
            
            # Generate amortization schedule
            balance = loan_amount
            payment_date = start_date
            
            for payment_num in range(1, years * 12 + 1):
                # Calculate interest for this period
                interest_payment = balance * monthly_interest_rate
                
                # Calculate principal for this period
                principal_payment = monthly_payment - interest_payment
                
                # Update balance
                balance -= principal_payment
                if balance < 0:  # Fix for rounding errors
                    balance = 0
                    
                # Format values for display
                payment_date_str = payment_date.strftime("%m/%d/%Y")
                monthly_payment_str = locale.currency(monthly_payment, grouping=True)
                principal_payment_str = locale.currency(principal_payment, grouping=True)
                interest_payment_str = locale.currency(interest_payment, grouping=True)
                balance_str = locale.currency(balance, grouping=True)
                
                # Add to treeview
                self.tree.insert("", "end", values=(
                    payment_num, 
                    payment_date_str, 
                    monthly_payment_str, 
                    principal_payment_str, 
                    interest_payment_str, 
                    balance_str
                ))
                
                # Move to next month
                payment_date = payment_date + timedelta(days=30)
                
        except ValueError as e:
            messagebox.showerror("Input Error", f"Please enter valid values: {str(e)}")

    def compare_loans(self):
        try:
            # Get current loan data
            current_amount = float(self.loanAmountVar.get())
            current_rate = float(self.annualInterestRateVar.get())
            current_years = int(self.numberOfYearsVar.get())
            
            # Calculate current monthly payment
            current_monthly_rate = current_rate / 1200
            if current_monthly_rate > 0:
                current_payment = current_amount * current_monthly_rate / (1 - 1 / (1 + current_monthly_rate) ** (current_years * 12))
            else:
                current_payment = current_amount / (current_years * 12)
                
            current_total = current_payment * current_years * 12
            
            # Get alternative loan data
            if not self.alt_amount_var.get().strip():
                self.alt_amount_var.set(str(current_amount))
            if not self.alt_rate_var.get().strip():
                self.alt_rate_var.set(str(current_rate))
            if not self.alt_term_var.get().strip():
                self.alt_term_var.set(str(current_years))
                
            alt_amount = float(self.alt_amount_var.get())
            alt_rate = float(self.alt_rate_var.get())
            alt_years = int(self.alt_term_var.get())
            
            # Calculate alternative monthly payment
            alt_monthly_rate = alt_rate / 1200
            if alt_monthly_rate > 0:
                alt_payment = alt_amount * alt_monthly_rate / (1 - 1 / (1 + alt_monthly_rate) ** (alt_years * 12))
            else:
                alt_payment = alt_amount / (alt_years * 12)
                
            alt_total = alt_payment * alt_years * 12
            
            # Generate comparison report
            comparison_text = f"""Comparison Results:

Current Loan:
  - Monthly Payment: {locale.currency(current_payment, grouping=True)}
  - Total Payment: {locale.currency(current_total, grouping=True)}
  - Total Interest: {locale.currency(current_total - current_amount, grouping=True)}

Alternative Loan:
  - Monthly Payment: {locale.currency(alt_payment, grouping=True)}
  - Total Payment: {locale.currency(alt_total, grouping=True)}
  - Total Interest: {locale.currency(alt_total - alt_amount, grouping=True)}

Difference:
  - Monthly Payment: {locale.currency(alt_payment - current_payment, grouping=True)}
  - Total Payment: {locale.currency(alt_total - current_total, grouping=True)}
  - Total Interest: {locale.currency((alt_total - alt_amount) - (current_total - current_amount), grouping=True)}
"""
            
            self.comparison_result.config(text=comparison_text)
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values for all fields")

if __name__ == "__main__":
    LoanCalculator()