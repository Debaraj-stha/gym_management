import sqlite3
from datetime import datetime, timedelta
from utils.constraints import DURATIONS, SHIFTS, TABLENAME
from utils.logger import logger

from utils.helper import send_email


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("my_db.db", timeout=5)

        self.cursor = self.conn.cursor()

        self._create_db()

    def _create_db(self):
        try:
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

            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY,
                    check_in DATE DEFAULT(datetime('now', 'utc')),
                    checkout DATE DEFAULT NULL,
                    customer_id INTEGER,
                    FOREIGN KEY (customer_id) REFERENCES customers(id)
                )"""
            )

            self.conn.commit()
            self.cursor.execute(
                """
                                CREATE TABLE IF NOT EXISTS instructors(
                                    id INTEGER PRIMARY KEY,
                                    name TEXT NOT NULL,
                                    email TEXT UNIQUE NOT NULL,
                                    phone TEXT NOT NULL,
                                    joined_at DATE DEFAULT(datetime('now', 'utc')),
                                    rate REAL DEFAULT 7000

                                )
                                """
            )
            self.conn.commit()
            self.cursor.execute(
                f"""
            CREATE TABLE IF NOT EXISTS class_schedule (
                id INTEGER PRIMARY KEY,
                date DATE DEFAULT (datetime('now', 'utc')),
                duration TEXT CHECK(duration IN {DURATIONS}) DEFAULT '1 hour',
                shift TEXT CHECK(shift IN {SHIFTS}) DEFAULT 'morning',
                status TEXT CHECK(status IN ) DEFAULT 'available',
                available_spots INTEGER DEFAULT 30
      
            )
            """
            )
            self.conn.commit()
            self.cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS class_schedule_instructors (
                class_schedule_id INTEGER,
                instructor_id INTEGER,
                FOREIGN KEY (class_schedule_id) REFERENCES class_schedule(id),
                FOREIGN KEY (instructor_id) REFERENCES instructors(id),
                PRIMARY KEY (class_schedule_id, instructor_id)
            )
            """
            )
            self.conn.commit()

        except Exception as e:
            logger.info(f"An error occurred while creating database: {e}")

    def close(self):
        self.conn.close()

    def insert(
        self, values: tuple, columns_name: list, table_name: str = "customers", **kwargs
    ):
        """
        Add a new customer to the database.

        Args:
            values (tuple): A tuple containing the customer's details: (name, email, phone, subscription_type, membership_expiry, subscription_price,total_amount_paid).
            columns_name (list): A list of column names in the database.
            table_name (str): The name of the table.Default is customers.


        Returns:
            int: The ID of the inserted customer if successful, None otherwise.
            str: An error message if any occurred.
        """
        try:
            col = ",".join(columns_name)
            placeholder = ",".join(["?"] * len(columns_name))
            query = f"""INSERT INTO {table_name} ({col}) VALUES ({placeholder})"""
            print(query)

            self.cursor.execute(
                query,
                values,
            )
            self.conn.commit()
            schedule_id = self.cursor.lastrowid
            if "instructors_id" in kwargs:
                values = [(schedule_id, id) for id in kwargs["instructors_id"]]
                print(values)
                query = f"""INSERT INTO class_schedule_instructors (class_schedule_id, instructor_id) VALUES (?,?)"""
                self.cursor.executemany(query, values)
                self.conn.commit()

            return schedule_id
        except sqlite3.Error as e:

            logger.info(f"An error occurred: {e}")
            return str(e)

    def total_records(
        self,
        where_condition: tuple = None,
        where_value: tuple = None,
        table_name="customers",
    ):
        """
        ## Count the number of customers
        Args:
            where_condition (tuple): A tuple containing column names to use in the WHERE clause.
            where_value (tuple): Values to use with the WHERE clause.
            table_name (str): The name of the table. Default is customers.
        Returns:
            int: total customers
        """
        try:
            if where_condition is not None and where_value is not None:
                where_clause = " AND ".join(f"{col}=?" for col in where_condition)
                self.cursor.execute(
                    f"SELECT COUNT(*) FROM {table_name} WHERE {where_clause}",
                    where_value,
                )
                return self.cursor.fetchone()[0]
            self.cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            return self.cursor.fetchone()[0]
        except sqlite3.Error as e:
            logger.info(f"An error occurred: {e}")

    def get_specific(
        self,
        where: tuple,
        value: tuple,
        columns_name: tuple = "*",
        limit=10,
        offset=0,
        table_name="customers",
        is_date_field=True,
    ):
        """
        Returns specific rows from the given table based on provided conditions.

        Args:
            where (tuple): Column names to use in the WHERE clause.
            value (tuple): Values to match for the WHERE clause.
            columns_name (tuple): Columns to retrieve from the table.
            table_name (str): Name of the table to query.
            is_date_field (bool): Placeholder, not used in this query.

        Returns:
            list: The rows that match the query.
        """

        try:

            col = ",".join(columns_name) if columns_name != ("*",) else "*"

            where_clause = " AND ".join(f"{col}=?" for col in where)

            query = (
                f"SELECT {col} FROM {table_name} WHERE {where_clause} LIMIT ? OFFSET ?"
            )

            # Execute the query
            self.cursor.execute(query, value + (limit, offset))
            return self.cursor.fetchall()

        except sqlite3.Error as e:
            logger.info(f"An error occurred: {e}")
            print(e)
            return []

    def get_customers(
        self,
        columns: tuple = "*",
        limit: int = 10,
        offset: int = 0,
        table_name="customers",
        **kwargs,
    ):
        """


        Args:
            columns (str,optional): The columns to retrieve customers from. If not provided, all customers will be returned from the database.
            limit (int, optional): The maximum number of customers to return. Defaults to 10.
            offset (int, optional): The starting index of the customers to return. Defaults to 1.
            **kwargs: (optional): Additional keyword like between ,sort order,order_by for filtering and sorting customers.

        Returns:
            list: A list of customers.
        """
        try:

            order_clause = ""
            columns_name = ",".join(columns) if columns != ("*",) else "*"
            if "order_by" in kwargs and "sort_order" in kwargs:
                order_by = kwargs["order_by"]
                sort_order = kwargs["sort_order"]
                order_clause = f"ORDER BY {order_by} {sort_order}"

            if "between" in kwargs:
                column_name, from_date, to_date = kwargs["between"]

                from_day_list = from_date.split("-")
                to_date_list = to_date.split("-")
                f_len = len(from_day_list)
                t_len = len(to_date_list)

                if f_len > 1 and t_len == 1:
                    from_year = from_day_list[0]
                    query = f"""
                        SELECT {columns} FROM {table_name} 
                        WHERE strftime('%Y', {column_name}) BETWEEN ? AND ? 
                        {order_clause} LIMIT ? OFFSET ?
                    """
                    self.cursor.execute(query, (from_year, to_date, limit, offset))
                elif f_len == 1 and t_len > 1:
                    to_year = to_date_list[0]
                    query = f"""
                        SELECT {columns} FROM {table_name} 
                        WHERE strftime('%Y', {column_name}) BETWEEN ? AND ? 
                        {order_clause} LIMIT ? OFFSET ?
                    """
                    self.cursor.execute(query, (from_date, to_year, limit, offset))
                elif f_len == 1 or t_len == 1:
                    query = f"""
                        SELECT {columns} FROM {table_name} 
                        WHERE strftime('%Y', {column_name}) BETWEEN ? AND ? 
                        {order_clause} LIMIT ? OFFSET ?
                    """
                    self.cursor.execute(query, (from_date, to_date, limit, offset))
                elif f_len == 2 or t_len == 2:
                    query = f"""
                        SELECT {columns} FROM {table_name} 
                        WHERE strftime('%Y-%m', {column_name}) BETWEEN ? AND ? 
                        {order_clause} LIMIT ? OFFSET ?
                    """
                    self.cursor.execute(query, (from_date, to_date, limit, offset))
                else:
                    query = f"""
                        SELECT {columns} FROM {table_name} 
                        WHERE {column_name} BETWEEN ? AND ? 
                        {order_clause} LIMIT ? OFFSET ?
                    """
                    self.cursor.execute(query, (from_date, to_date, limit, offset))

                return self.cursor.fetchall()

            columns_name = "*"
            if "*" not in columns:
                columns_name = ",".join(columns)
            query = f"SELECT {columns_name} FROM {table_name} {order_clause} LIMIT ? OFFSET ?"
            self.cursor.execute(query, (limit, offset))
            res = self.cursor.fetchall()
            return res

        except sqlite3.Error as e:
            logger.info(f"An error occurred: {e}")
            print(e)
            return []

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

    def search(
        self,
        search_term: str,
        column_names: list = "*",
        search_column: list = ["name", "email", "phone", "subscription_type"],
        table_name: str = "customers",
        **kwargs,
    ):
        """
        Search for customers whose names, emails, or other fields contain the given search term.

        Args:
            search_term (str): The search term to match.
            column_names (str or list): The columns to retrieve. Defaults to "*" for all columns.
            search_column (list): The columns to search in. Defaults to ["name", "email", "phone", "subscription_type"].
            table_name (str): The table name to search in. Defaults to "customers".
            join_with (str, optional): The table to join with. Defaults to None.
            join_column (list, optional): The columns to join with. Defaults to None.

        Returns:
            list: A list of matching records.
        """
        try:
            # Handle column names for select statement
            if isinstance(column_names, list):
                column_names = ", ".join(
                    [
                        f"t1.{col}" if isinstance(col, str) else f"{col[0]}.{col[1]}"
                        for col in column_names
                    ]
                )

            # Build the LIKE clause
            like_query = [f"{col} LIKE ?" for col in search_column]
            like_clause = " OR ".join(like_query)

            # Join table if specified
            if "join_with" in kwargs:
                join_with = kwargs.get("join_with")
                join_column = kwargs.get("join_column")
                query = f"""
                    SELECT {column_names} FROM {table_name} as t1
                    INNER JOIN {join_with} as t2 ON t1.{join_column[0]} = t2.{join_column[1]}
                    WHERE {like_clause}
                """
            else:
                query = f"SELECT {column_names} FROM {table_name} WHERE {like_clause}"

            # Execute query with search term applied to each search column
            self.cursor.execute(query, [f"%{search_term}%"] * len(search_column))
            return self.cursor.fetchall()

        except sqlite3.Error as e:
            logger.info(f"An error occurred: {e}")
            return []

    def insert_multiple(
        self, records: list, columns_name: list, table_name: str = "customers"
    ):
        """
        Inserts multiple customer records into the database.

        Args:
            rescords (list): A list of records tuple, where each tuple contains records details.
        """
        try:
            col = ",".join(columns_name)
            placeholders = ",".join(["?"] * len(columns_name))

            query = f"INSERT INTO {table_name} ({col}) VALUES ({placeholders})"

            self.cursor.executemany(
                query,
                records,
            )
            self.conn.commit()
        except sqlite3.Error as e:
            logger.info(f"An error occurred: {e}")
            print(e)

    def get_customer_by_pending_payment(
        self,
        limit,
        offset,
        order_by="name",
        sort_order="asc",
    ):
        """
        Returns all customers whose total amount paid is less than their subscription price.
        Args:
        limit (int): The maximum number of customers to return.
        offset (int): The number of customers to skip before returning the results.
        order_by (str, optional): The column to order the results by. Defaults to "name".
        sort_order (str, optional): The order of sorting (asc or desc). Defaults to "asc".

        Returns:
            list: A list of customers whose total amount paid is less than their subscription price.
        """
        try:
            self.cursor.execute(
                "SELECT * FROM customers WHERE total_amount_paid < subscription_price LIMIT ? OFFSET ? ORDER BY ? ?",
                (limit, offset, order_by, sort_order),
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

    def update_email_sent(self, new_status: list, id: list, previous_status: list):
        """

        Args:
            new_status (list): New status of email sent.
            id (list): ID of the customer to update.
            previous_status (list): Previous status of email sent.
        Returns:
        bool: True if update is successful, False otherwise.
        """
        try:
            date_to_update = [
                (new_status[i], id[i], previous_status[i])
                for i in range(len(new_status))
            ]
            self.cursor.executemany(
                "UPDATE customers SET is_email_sent =? WHERE id =? AND is_email_sent=?",
                (date_to_update),
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            logger.info(f"An error occurred: {e}")
            return False

    def send_membership_expiring_message(self, daye_before: int):
        try:
            expiring_customers = self.get_customers_by_membership_expiry(daye_before)
            to = []
            id = []
            if expiring_customers is None:
                return
            for customer in expiring_customers:
                to.append(customer[2])
                id.append(customer[0])
            subject = "Membership expiring"
            body = f"""Membership of {customer[1]} is expiring in {daye_before} days.
            Please renew  your membership before expiring.Thank you for your membership.
            """
            send_email(to, subject, body)
            new_status = [1] * len(to)
            previous_status = [0] * len(to)

            self.update_email_sent(new_status, id, previous_status)

        except sqlite3.Error as e:
            logger.info(f"An error occurred while querying the database: {e}")

    def update(
        self,
        columns_name: list,
        values: tuple,
        where_value: tuple,
        table_name="customers",
        where_col=tuple,
    ):
        try:

            set_clause = ", ".join(f"{col} = ?" for col in columns_name)
            where_clause = " AND ".join(f"{where} = ?" for where in where_col)

            query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"

            self.cursor.execute(query, values + (where_value))
            self.conn.commit()
            return True

        except Exception as e:
            logger.info(f"An error occurred while querying the database: {e}")
            print(e)
            return False

    def delete(
        self,
        where: tuple = (None,),
        where_value: tuple = (None,),
        table_name="customers",
    ):
        try:

            if where != (None,) and where_value != (None,):
                where_clause = " AND ".join(f"{col}=?" for col in where)
                query = f"DELETE FROM {table_name} WHERE {where_clause}"
                self.cursor.execute(query, where_value)
            else:
                query = f"DELETE FROM {table_name}"
                self.cursor.execute(query)

            self.conn.commit()
            return True
        except Exception as e:
            logger.info(f"An error occurred while querying the database: {e}")
            print(e)
            return False

    def join(
        self,
        table_names: list,
        limit=10,
        offset=0,
        where: list = None,
    ):
        try:
            # Get today's date in 'YYYY-MM-DD' format
            today = datetime.now().date()

            query = f"""
                SELECT c.id AS customer_id, c.name, 
                    MAX(CASE WHEN DATE(a.check_in) = ? THEN a.check_in END) AS check_in,
                    MAX(CASE WHEN DATE(a.checkout) = ? THEN a.checkout END) AS checkout
                FROM {table_names[0]} AS c
                LEFT JOIN {table_names[1]} AS a ON c.id = a.customer_id
                GROUP BY c.id
            """

            if where:
                query += f" HAVING {where[0]} = ?"
                parameters = (today, today, where[1], limit, offset)
            else:
                parameters = (today, today, limit, offset)

            query += " LIMIT ? OFFSET ?"

            self.cursor.execute(query, parameters)
            results = self.cursor.fetchall()

            return results

        except sqlite3.Error as e:
            logger.info(f"An error occurred while querying the database: {e}")
            print(e)
            return None

    def get_all(self, columns_name: tuple = "*", table_name="customers"):
        try:
            col = ",".join(columns_name) if columns_name != ("*",) else "*"
            query = f"SELECT {col} FROM {table_name}"
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return results
        except sqlite3.Error as e:
            logger.info(f"An error occurred while querying the database: {e}")
            print(e)
            return None

    from datetime import datetime

    def get_schedule(self, limit, offset):
        today = datetime.now().date()
        try:
            query = f"""
            SELECT 
                t1.id as schedule_id,
                t1.date,
                t1.duration,
                t1.shift,
                t1.status,
                t1.available_spots,
                t3.name as instructor_name,
                t3.id as instructor_id
            FROM 
                {TABLENAME.CLASS_SCHEDULE.value} as t1
            LEFT JOIN 
                {TABLENAME.CLASS_SCHEDULE_INSTRUCTORS.value} as t2 ON t1.id = t2.class_schedule_id
            LEFT JOIN 
                {TABLENAME.INSTRUCTORS.value} as t3 ON t2.instructor_id = t3.id
            WHERE 
                DATE(t1.date) = ?
            LIMIT ? OFFSET ?
            """

            params = (today, limit, offset)
            self.cursor.execute(query, params)
            results = self.cursor.fetchall()
            return results
        except sqlite3.Error as e:
            logger.info(f"An error occurred while querying the database: {e}")
            print(e)
            return None
