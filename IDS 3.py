class Account:
    def __init__(self, name, balance=0):
        self.name = name
        self.balance = balance

    def __str__(self):
        return f"{self.name}: {self.balance} tokens"

    def transfer(self, amount, recipient):
        if amount <= self.balance:
            self.balance -= amount
            recipient.balance += amount
            print(f"Transferred {amount} tokens from {self.name} to {recipient.name}")
        else:
            print(f"Insufficient balance for transfer from {self.name}")

class Token:
    def __init__(self, name, symbol, total_supply):
        self.name = name
        self.symbol = symbol
        self.total_supply = total_supply
        self.accounts = {}

    def create_account(self, name, initial_balance=0):
        if name not in self.accounts:
            self.accounts[name] = Account(name, initial_balance)
            print(f"Account {name} created with {initial_balance} tokens.")
        else:
            print(f"Account {name} already exists.")
    
    def transfer_tokens(self, from_account_name, to_account_name, amount):
        if from_account_name in self.accounts and to_account_name in self.accounts:
            from_account = self.accounts[from_account_name]
            to_account = self.accounts[to_account_name]
            from_account.transfer(amount, to_account)
        else:
            print("One or both accounts do not exist.")
    
    def mint_tokens(self, amount):
        self.total_supply += amount
        print(f"Minted {amount} tokens. New total supply: {self.total_supply}")

    def distribute_tokens(self, amount, account_names):
        # Distribute tokens equally among the listed accounts
        if len(account_names) == 0:
            print("No accounts to distribute tokens to.")
            return

        tokens_per_account = amount // len(account_names)
        for name in account_names:
            if name in self.accounts:
                self.accounts[name].balance += tokens_per_account
                print(f"Distributed {tokens_per_account} tokens to {name}.")
            else:
                print(f"Account {name} not found.")

    def display_account_balances(self):
        print("Account Balances:")
        for account in self.accounts.values():
            print(account)

my_token = Token("MyToken", "MTK", total_supply=1000)

my_token.create_account("Treasury", 950)
my_token.create_account("Recipient", 50)

my_token.display_account_balances()

my_token.transfer_tokens("Treasury", "Recipient", 100)

my_token.display_account_balances()

my_token.mint_tokens(500)

my_token.distribute_tokens(400, ["Treasury", "Recipient"])

my_token.display_account_balances()
