class Author:
    all = []

    def __init__(self, name):
        self.name = name
        Author.all.append(self)
    
    def contracts(self):
        # Get all contracts related to this author
        return [contract for contract in Contract.all if contract.author == self]
    
    def books(self):
        # Get all books associated with this author through contracts
        return [contract.book for contract in self.contracts()]
    
    def sign_contract(self, book, date, royalties):
        # Ensure the book is a valid instance of the Book class
        if not isinstance(book, Book):
            raise Exception("The contract must be signed with a Book instance.")
        
        # Ensure the royalties are a valid integer (no upper limit for royalties)
        if not isinstance(royalties, int):
            raise Exception("Royalties must be an integer.")
        
        # Ensure the date is a valid string
        if not isinstance(date, str):
            raise Exception("Date must be a string.")

        # Ensure the author hasn't already signed a contract for this book
        existing_contracts = [contract for contract in Contract.all if contract.book == book and contract.author == self]
        if existing_contracts:
            raise Exception(f"{self.name} has already signed a contract for the book '{book.title}'.")

        # Create and return a new Contract object
        return Contract(self, book, date, royalties)
    
    def total_royalties(self):
        # Calculate the total royalties from all contracts this author has signed
        return sum(contract.royalties for contract in self.contracts())



class Book:
    all = []
    
    def __init__(self, title):
        self.title = title
        Book.all.append(self)

    def contracts(self):
        # Get all contracts related to this book
        return [contract for contract in Contract.all if contract.book == self]
    
    def authors(self):
        # Get all authors associated with this book through contracts
        return [contract.author for contract in self.contracts()]    


class Contract:
    all = []
    
    def __init__(self, author, book, date, royalties):
        # Validate the author and book objects
        if not isinstance(author, Author):
            raise Exception("Contract must be associated with an Author instance.")
        if not isinstance(book, Book):
            raise Exception("Contract must be associated with a Book instance.")
        if not isinstance(royalties, int):
            raise Exception("Royalties must be an integer.")
        if not isinstance(date, str):
            raise Exception("Date must be a string.")
        
        self._author = author
        self._book = book
        self._date = date
        self._royalties = royalties
        
        # Add the contract to the class-level 'all' list
        Contract.all.append(self)
    
    # Properties for each field (author, book, date, royalties)
    @property
    def author(self):
        return self._author

    @property
    def book(self):
        return self._book

    @property
    def date(self):
        return self._date

    @property
    def royalties(self):
        return self._royalties
    
    @classmethod
    def contracts_by_date(cls, date):
        # Return all contracts with the same date as the one passed in
        return [contract for contract in cls.all if contract.date == date]


# Example usage for testing:
if __name__ == "__main__":
    # Creating authors and books
    author_1 = Author("Jane Austen")
    author_2 = Author("Mark Twain")
    book_1 = Book("Pride and Prejudice")
    book_2 = Book("The Adventures of Huckleberry Finn")

    # Author signing contracts with royalties and dates
    contract_1 = author_1.sign_contract(book_1, "2024-11-09", 10)  # Signed on 2024-11-09
    contract_2 = author_1.sign_contract(book_2, "2024-11-10", 12)  # Signed on 2024-11-10
    contract_3 = author_2.sign_contract(book_2, "2024-11-09", 15)  # Signed on 2024-11-09

    # Using contracts_by_date to get all contracts signed on a specific date
    contracts_on_nov_9 = Contract.contracts_by_date("2024-11-09")
    print(f"Contracts signed on 2024-11-09:")
    for contract in contracts_on_nov_9:
        print(f"- {contract.author.name} for '{contract.book.title}'")

    # Total royalties for each author
    print(f"Total royalties for {author_1.name}: {author_1.total_royalties()}%")  # Output: 22%
    print(f"Total royalties for {author_2.name}: {author_2.total_royalties()}%")  # Output: 15%

    # Books and their authors
    print(f"Authors of '{book_2.title}': {[author.name for author in book_2.authors()]}")  # Output: ['Jane Austen', 'Mark Twain']
