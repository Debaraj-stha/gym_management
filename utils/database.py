import sqlite3
from datetime import datetime, timedelta
from venv import logger


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("my_db.db")
        self.cursor = self.conn.cursor()
        self._create_db()

    def _create_db(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS customers (
                            id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            email TEXT UNIQUE NOT NULL,
                            phone TEXT NOT NULL,
                            subscription_type TEXT NOT NULL,
                            subscription_date DATE DEFAULT(datetime('now', 'utc')),
                            membership_expiry DATE NOT NULL,
                            subscription_price REAL NOT NULL,
                            total_amount_paid REAL DEFAULT 0,
                            last_payment_date DATE DEFAULT NULL
                            
                        )"""
        )
        self.conn.commit()

    def close(self):
        self.conn.close()

    def insert(self, customer):
        """
        Add a new customer to the database.

        Args:
            customer (tuple): A tuple containing the customer's details: (name, email, phone, subscription_type, membership_expiry, subscription_price,total_amount_paid).
        Returns:
            int: The ID of the inserted customer if successful, None otherwise.
        """
        try:
            self.cursor.execute(
                """INSERT INTO customers (name, email, phone, subscription_type, membership_expiry, subscription_price,total_amount_paid) VALUES (?,?,?,?,?,?,?)""",
                customer,
            )
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            logger.info(f"An error occurred: {e}")

    def total_customers(self):
        """
        Count the number of customers
        Returns:
            int: total customers
        """
        try:
            self.cursor.execute("SELECT COUNT(*) FROM customers")
            return self.cursor.fetchone()[0]
        except sqlite3.Error as e:
            logger.info(f"An error occurred: {e}")

    def get_customer(self, customer_id: int):
        """
        Returns the customer with the given ID.

        Args:
            customer_id (int): The ID of the customer to retrieve.

        Returns all customers in the database.


        """

        try:
            self.cursor.execute(
                "SELECT * FROM customers WHERE customer_id=?", (customer_id,)
            )
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logger.info(f"An error occurred: {e}")

    def get_customers(self, limit: int = 10, offset: int = 1, **kwargs):
        """
        Returns all customers in the database, limited by the specified limit and offset.

        Args:
            limit (int, optional): The maximum number of customers to return. Defaults to 10.
            offset (int, optional): The starting index of the customers to return. Defaults to 1.

        Returns:
            list: A list of customers.
        """
        try:
            if "between" in kwargs:
                column_name, from_date, to_date = kwargs["between"]
                logger.info(kwargs["between"])

                # Split the date strings to detect their format
                from_day_list = from_date.split("-")
                to_date_list = to_date.split("-")
                f_len = len(from_day_list)
                t_len = len(to_date_list)

                # Convert to year if a full date is given in from_date and only year is provided in to_date
                if f_len > 1 and t_len == 1:
                    # Extract only the year from from_date
                    from_year = from_day_list[0]
                    # Use only the year for comparison
                    self.cursor.execute(
                        f"SELECT * FROM customers WHERE strftime('%Y', {column_name}) BETWEEN ? AND ? LIMIT ? OFFSET ?",
                        (
                            from_year,
                            to_date,
                            limit,
                            offset,
                        ),  # Compare only the year parts
                    )
                elif f_len == 1 and t_len > 1:
                    # Extract only the year from to_date
                    to_year = to_date_list[0]
                    # Use only the year for comparison
                    self.cursor.execute(
                        f"SELECT * FROM customers WHERE strftime('%Y', {column_name}) BETWEEN ? AND ? LIMIT ? OFFSET ?",
                        (
                            from_date,
                            to_year,
                            limit,
                            offset,
                        ),  # Compare only the year parts
                    )
                elif f_len == 1 or t_len == 1:
                    # Both are year only
                    self.cursor.execute(
                        f"SELECT * FROM customers WHERE strftime('%Y', {column_name}) BETWEEN ? AND ? LIMIT ? OFFSET ?",
                        (from_date, to_date, limit, offset),
                    )
                elif f_len == 2 or t_len == 2:
                    # Year and month comparison
                    self.cursor.execute(
                        f"SELECT * FROM customers WHERE strftime('%Y-%m', {column_name}) BETWEEN ? AND ?",
                        (from_date, to_date),
                    )
                else:
                    # Full date comparison
                    self.cursor.execute(
                        f"SELECT * FROM customers WHERE {column_name} BETWEEN ? AND ? LIMIT ? OFFSET ?",
                        (from_date, to_date, limit, offset),
                    )

                res = self.cursor.fetchall()
                logger.info(res)
                return res

            # Fallback for fetching customers without a date filter
            self.cursor.execute(
                "SELECT * FROM customers LIMIT ? OFFSET ?", (limit, offset)
            )
            return self.cursor.fetchall()

        except sqlite3.Error as e:
            logger.info(f"An error occurred: {e}")
            return []

    def update_last_payment_date(self, customer_id: id, last_payment_date: datetime):
        """
        Update the last payment date of a customer.

        Args:
            customer_id (int): The ID of the customer to update.
            last_payment_date (datetime): The new last payment date.
        """
        try:
            self.cursor.execute(
                "UPDATE customers SET last_payment_date=? WHERE id=?",
                (last_payment_date, customer_id),
            )
            self.conn.commit()
        except sqlite3.Error as e:
            logger.info(f"An error occurred: {e}")

    def get_customers_by_membership_expiry(self, days_before_expiry: int):
        """
        Returns all customers whose membership expires in the specified number of days.

        Args:
            days_before_expiry (int): The number of days before the membership expires.

        Returns:
            list: A list of customers whose membership expires in the specified number of days.
        """
        try:
            today = datetime.now().date()
            expiry_date = today + timedelta(days=days_before_expiry)
            fetch_total_expiring_customer = self.cursor.execute(
                "SELECT COUNT(*) FROM customers WHERE membership_expiry<=",
                (expiry_date),
            )
            total_expiring_customer = fetch_total_expiring_customer.fetchone()[0]

            self.cursor.execute(
                "SELECT * FROM customers WHERE membership_expiry <=?", (expiry_date,)
            )
            return self.cursor.fetchall(), total_expiring_customer
        except sqlite3.Error as e:
            logger.info(f"An error occurred: {e}")

    def update_membership_expiry(self, customer_id: int, new_expiry_date: datetime):
        """
        Update the membership expiry date of a customer.

        Args:
            customer_id (int): The ID of the customer to update.
            new_expiry_date (datetime): The new membership expiry date.
        """
        try:
            self.cursor.execute(
                "UPDATE customers SET membership_expiry=? WHERE id=?",
                (new_expiry_date, customer_id),
            )
            self.conn.commit()
        except sqlite3.Error as e:
            logger.info(f"An error occurred: {e}")

    def update_total_amount_paid(self, customer_id: int, new_total_amount_paid: float):
        """
        Update the total amount paid of a customer.

        Args:
            customer_id (int): The ID of the customer to update.
            new_total_amount_paid (float): The new total amount paid.
        """
        try:
            self.cursor.execute(
                "UPDATE customers SET total_amount_paid=? WHERE id=?",
                (new_total_amount_paid, customer_id),
            )
            self.conn.commit()
        except sqlite3.Error as e:
            logger.info(f"An error occurred: {e}")

    def get_customer_by_email(self, email):
        """
        Returns the customer with the given email.

        Args:
            email (str): The email of the customer to retrieve.

        Returns:
            tuple: The customer's details if found, None otherwise.
        """
        try:
            self.cursor.execute("SELECT * FROM customers WHERE email=?", (email,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            logger.info(f"An error occurred: {e}")

    def update_subscription_type(self, customer_id: int, new_subscription_type: str):
        """
        Update the subscription type of a customer.

        Args:
            customer_id (int): The ID of the customer to update.
            new_subscription_type (str): The new subscription type.
        """
        try:
            self.cursor.execute(
                "UPDATE customers SET subscription_type=? WHERE id=?",
                (new_subscription_type, customer_id),
            )
            self.conn.commit()
        except sqlite3.Error as e:
            logger.info(f"An error occurred: {e}")

    def update_subscription_price(
        self, customer_id: int, new_subscription_price: float
    ):
        """
        Update the subscription price of a customer.

        Args:
            customer_id (int): The ID of the customer to update.
            new_subscription_price (float): The new subscription price.
        """
        try:
            self.cursor.execute(
                "UPDATE customers SET subscription_price=? WHERE id=?",
                (new_subscription_price, customer_id),
            )
            self.conn.commit()
        except sqlite3.Error as e:
            logger.info(f"An error occurred: {e}")

    def update_subscription_date(
        self, customer_id: int, new_subscription_date: datetime
    ):
        """
        Update the subscription date of a customer.

        Args:
            customer_id (int): The ID of the customer to update.
            new_subscription_date (datetime): The new subscription date.
        """
        try:
            self.cursor.execute(
                "UPDATE customers SET subscription_date=? WHERE id=?",
                (new_subscription_date, customer_id),
            )
            self.conn.commit()
        except sqlite3.Error as e:
            logger.info(f"An error occurred: {e}")

    def delete_customer(self, customer_id: int):
        """
        Delete the customer with the given ID.

        Args:
            customer_id (int): The ID of the customer to delete.
        """
        try:
            self.cursor.execute("DELETE FROM customers WHERE id=?", (customer_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            logger.info(f"An error occurred: {e}")

    def search_customers(
        self,
        search_term: str,
        search_column: list = ["name", "email", "phone", "subscription_type"],
    ):
        """
        Search for customers whose names or emails contain the given search term.

        Args:
            search_term (str): The search term to match.
            search_column (list, optional): The columns to search in. Defaults to ["name", "email", "phone", "subscription_type"].

        Returns:
            list: A list of customers whose names or emails contain the search term.
        """
        try:
            like_query = [f"{col} LIKE ?" for col in search_column]
            like_clause = " OR ".join(like_query)
            self.cursor.execute(
                f"SELECT * FROM customers WHERE {like_clause}",
                [f"%{search_term}%"] * len(search_column),
            )
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logger.info(f"An error occurred: {e}")

    def get_customers_by_subscription_type(self, subscription_type: str):
        """
        Returns all customers with the given subscription type.

        Args:
            subscription_type (str): The subscription type to retrieve.

        Returns:
            list: A list of customers with the given subscription type.
        """
        try:
            self.cursor.execute(
                "SELECT * FROM customers WHERE subscription_type=?",
                (subscription_type,),
            )
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logger.info(f"An error occurred: {e}")

    def get_customers_by_total_amount_paid(self, min_amount: float, max_amount: float):
        """
        Returns all customers whose total amount paid falls within the given range.

        Args:
            min_amount (float): The minimum total amount paid.
            max_amount (float): The maximum total amount paid.

        Returns:
            list: A list of customers whose total amount paid falls within the given range.
        """
        try:
            self.cursor.execute(
                "SELECT * FROM customers WHERE total_amount_paid BETWEEN? AND?",
                (min_amount, max_amount),
            )
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logger.info(f"An error occurred: {e}")

    def insert_multiple_amounts(self, customers: list):
        """
        Inserts multiple customer records into the database.

        Args:
            customers (list): A list of customer tuple, where each tuple contains customer details.
        """
        try:
            self.cursor.executemany(
                "INSERT INTO customers (name, email, membership_expiry, last_payment_date, total_amount_paid, subscription_type, subscription_price, subscription_date) VALUES (?,?,?,?,?,?,?,?)",
                customers,
            )
            self.conn.commit()
        except sqlite3.Error as e:
            logger.info(f"An error occurred: {e}")

    def get_customer_by_pending_payment(self, limit, offset):
        """
        Returns all customers whose total amount paid is less than their subscription price.

        Returns:
            list: A list of customers whose total amount paid is less than their subscription price.
        """
        try:
            self.cursor.execute(
                "SELECT * FROM customers WHERE total_amount_paid < subscription_price LIMIT ? OFFSET ?",
                (limit, offset),
            )
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logger.info(f"An error occurred: {e}")
            logger.info(f"An error occurred while querying the database: {e}")

    def count_pending_payment_customers(self):
        """
        Returns the total number of customers whose total amount paid is less than their subscription price.
        """
        try:
            self.cursor.execute(
                "SELECT COUNT(*) FROM customers WHERE total_amount_paid < subscription_price"
            )
            return self.cursor.fetchone()[0]
        except sqlite3.Error as e:
            logger.info(f"An error occurred: {e}")
            logger.info(f"An error occurred while querying the database: {e}")
