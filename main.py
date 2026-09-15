"""
ATM Transaction Simulator
Features: PIN authentication, Balance Check, Deposit, Withdrawal, and Transaction History.
"""

import sys
from datetime import datetime


class ATM:
    def __init__(self, card_number: str, pin: str, initial_balance: float = 1000.0):
        self.card_number = card_number
        self._pin = pin
        self.balance = initial_balance
        self.transaction_history = []
        self._log_transaction("Account Initialized", initial_balance)

    def verify_pin(self, input_pin: str) -> bool:
        """Authenticates the user's PIN."""
        return self._pin == input_pin

    def _log_transaction(self, tx_type: str, amount: float):
        """Records timestamped transaction entries."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        record = {
            "timestamp": timestamp,
            "type": tx_type,
            "amount": amount,
            "balance_after": self.balance,
        }
        self.transaction_history.append(record)

    def check_balance(self) -> float:
        """Returns the current account balance."""
        return self.balance

    def deposit(self, amount: float) -> tuple[bool, str]:
        """Deposits a positive amount into the account."""
        if amount <= 0:
            return False, "Deposit amount must be greater than $0.00."

        self.balance += amount
        self._log_transaction("Deposit", amount)
        return True, f"Successfully deposited ${amount:,.2f}."

    def withdraw(self, amount: float) -> tuple[bool, str]:
        """Withdraws funds if positive and within balance limits."""
        if amount <= 0:
            return False, "Withdrawal amount must be greater than $0.00."
        if amount > self.balance:
            return (
                False,
                f"Insufficient funds. Current balance: ${self.balance:,.2f}",
            )

        self.balance -= amount
        self._log_transaction("Withdrawal", amount)
        return True, f"Successfully withdrew ${amount:,.2f}."

    def get_statement(self) -> list[dict]:
        return self.transaction_history


def run_atm():
    # Setup demo account
    user_atm = ATM(card_number="4532-XXXX-XXXX-8901", pin="1234", initial_balance=500.00)

    print("========================================")
    print("       WELCOME TO PYTHON BANK ATM       ")
    print("========================================")

    # PIN Verification (Max 3 attempts)
    attempts = 3
    authenticated = False
    while attempts > 0:
        entered_pin = input("\nPlease enter your 4-digit PIN: ").strip()
        if user_atm.verify_pin(entered_pin):
            authenticated = True
            break
        else:
            attempts -= 1
            print(f"Incorrect PIN. Attempts remaining: {attempts}")

    if not authenticated:
        print("\nToo many incorrect attempts. Your card has been retained for security.")
        sys.exit()

    # Main ATM Menu Loop
    while True:
        print("\n----------------------------------------")
        print("MAIN MENU")
        print("1. Check Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Mini Statement (Transaction History)")
        print("5. Exit")
        print("----------------------------------------")

        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            print(f"\nYour current balance is: ${user_atm.check_balance():,.2f}")

        elif choice == "2":
            try:
                amt = float(input("\nEnter amount to deposit: $"))
                success, msg = user_atm.deposit(amt)
                print(f"[{'SUCCESS' if success else 'ERROR'}] {msg}")
                if success:
                    print(f"Updated Balance: ${user_atm.check_balance():,.2f}")
            except ValueError:
                print("[ERROR] Invalid numeric input. Transaction canceled.")

        elif choice == "3":
            try:
                amt = float(input("\nEnter amount to withdraw: $"))
                success, msg = user_atm.withdraw(amt)
                print(f"[{'SUCCESS' if success else 'ERROR'}] {msg}")
                if success:
                    print(f"Updated Balance: ${user_atm.check_balance():,.2f}")
            except ValueError:
                print("[ERROR] Invalid numeric input. Transaction canceled.")

        elif choice == "4":
            print("\n--- MINI STATEMENT ---")
            history = user_atm.get_statement()
            print(f"{'Timestamp':<20} | {'Type':<12} | {'Amount':<10} | {'Balance':<10}")
            print("-" * 60)
            for tx in history:
                print(
                    f"{tx['timestamp']:<20} | {tx['type']:<12} | ${tx['amount']:<9,.2f} | ${tx['balance_after']:<9,.2f}"
                )

        elif choice == "5":
            print("\nThank you for banking with us. Please take your card!")
            break
        else:
            print("\nInvalid choice. Please select between 1 and 5.")


if __name__ == "__main__":
    run_atm()