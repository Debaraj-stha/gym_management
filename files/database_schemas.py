from utils.constraints import DURATIONS, SHIFTS, STATUS, TABLENAME


CUSTOMER_SCHEMA = """id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phone TEXT NOT NULL,
                    subscription_type TEXT NOT NULL,
                    subscription_date DATE DEFAULT(datetime('now', 'utc')),
                    membership_expiry DATE NOT NULL,
                    subscription_price REAL NOT NULL,
                    total_amount_paid REAL DEFAULT 0,
                    last_payment_date DATE DEFAULT NULL
                    """
ATTENDANCE_SCHEMA = """ id INTEGER PRIMARY KEY,
                    check_in DATE DEFAULT(datetime('now', 'utc')),
                    checkout DATE DEFAULT NULL,
                    customer_id INTEGER,
                    FOREIGN KEY (customer_id) REFERENCES customers(id)"""
INSTRUCTOR_SCHEMA = """  id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        phone TEXT NOT NULL,
                        joined_at DATE DEFAULT(datetime('now', 'utc')),
                        rate REAL DEFAULT 7000
                    """

CLASS_SCHEDULE_SCHEMA = f""" 
                        id INTEGER PRIMARY KEY,
                        date DATE DEFAULT (datetime('now', 'utc')),
                        duration TEXT CHECK (duration IN {DURATIONS}) DEFAULT '1 hour',
                        shift TEXT CHECK (shift IN {SHIFTS}) DEFAULT 'morning',
                        status TEXT CHECK (status IN {STATUS}) DEFAULT 'available',
                        available_spots INTEGER DEFAULT 30
                    """

CLASS_SCHEDULE_INSTRUCTOR_SCHEMA = """class_schedule_id INTEGER,
                instructor_id INTEGER,
                FOREIGN KEY (class_schedule_id) REFERENCES class_schedule(id),
                FOREIGN KEY (instructor_id) REFERENCES instructors(id),
                PRIMARY KEY (class_schedule_id, instructor_id)"""
INVOICE_SCHEMA = f"""
                invoice_id INTEGER PRIMARY KEY,
                date DATE DEFAULT (datetime('now', 'utc')),
                amount_to_pay REAL CHECK( amount_to_pay >0) DEFAULT 0.0,
                amount_paid REAL CHECK( amount_to_pay >0) DEFAULT 0.0,
                remaining_amount REAL CHECK( amount_to_pay >0)  DEFAULT 0.0,
                last_paid_amount REAL DEFAULT 0.0,
                last_paid_date DATE DEFAULT (datetime('now', 'utc')),
                customer_id INTEGER,
                FOREIGN KEY (customer_id) REFERENCES {TABLENAME.CUSTOMERS.value}(id)
                """
