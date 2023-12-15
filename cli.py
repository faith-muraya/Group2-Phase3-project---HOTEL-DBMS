import click
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import Base, Booking, Customer, Employee, Expense, Item, Order, Payment, Room, RoomType

# Set the database URI
DATABASE_URI = "sqlite:///mydb.db"

engine = create_engine(DATABASE_URI, echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


@click.group()
def cli():
    pass


@cli.command()
def initdb():

    Base.metadata.create_all(engine)
    click.echo("Database initialized.")


@cli.command()
@click.option("--customername", prompt="Customer Name", help="Customer's name")
@click.option("--address", prompt="Address", help="Customer's address")
@click.option("--phoneno", prompt="Phone Number", help="Customer's phone number")
@click.option("--gender", prompt="Gender", help="Customer's gender")
@click.option("--status", default="active", help="Customer's status (default: active)")
def add_customer(customername, address, phoneno, gender, status):
    customer = Customer(
        Customername=customername,
        address=address,
        phoneno=phoneno,
        gender=gender,
        status=status
    )
    session.add(customer)
    session.commit()
    click.echo("Customer added successfully.")


@cli.command()
@click.option("--employeename", prompt="Employee Name", help="Employee's name")
@click.option("--loginid", prompt="Login ID", help="Employee's login ID")
@click.option("--emptype", prompt="Employee Type", help="Employee's type")
@click.option("--status", default="active", help="Employee's status (default: active)")
def add_employee(employeename, loginid, emptype, status):
    employee = Employee(
        employeename=employeename,
        loginid=loginid,
        emptype=emptype,
        status=status
    )
    session.add(employee)
    session.commit()
    click.echo("Employee added successfully.")


@cli.command()
@click.option("--employeeid", prompt="Employee ID", type=int, help="Employee ID")
@click.option("--expensetype", prompt="Expense Type", help="Expense Type")
@click.option("--expensemat", prompt="Expense Amount", help="Expense Amount")
@click.option("--expensedate", prompt="Expense Date", help="Expense Date")
@click.option("--status", default="pending", help="Expense Status (default: pending)")
def add_expense(employeeid, expensetype, expensemat, expensedate, status):

    try:
        # Convert expensedate string to a datetime object
        expensedate = datetime.strptime(expensedate, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        click.echo("Invalid date format. Please use YYYY-MM-DD HH:MM:SS.")
        return

    expense = Expense(
        employeeid=employeeid,
        expensetype=expensetype,
        expensemat=expensemat,
        expensedate=expensedate,
        status=status
    )

    session.add(expense)
    session.commit()
    click.echo("Expense added successfully.")


@cli.command()
@click.option("--roomid", prompt="Room ID", type=int, help="Room ID")
@click.option("--customerid", prompt="Customer ID", type=int, help="Customer ID")
@click.option("--bookdate", prompt="Booking Date", type=str, help="Booking Date")
@click.option("--checkin", prompt="Check-in Date", type=str, help="Check-in Date")
@click.option("--checkout", prompt="Check-out Date", type=str, help="Check-out Date")
@click.option("--status", default="active", help="Booking Status (default: active)")
def add_booking(roomid, customerid, bookdate, checkin, checkout, status):
    try:
        bookdate = datetime.strptime(bookdate, "%Y-%m-%d %H:%M:%S")
        checkin = datetime.strptime(checkin, "%Y-%m-%d %H:%M:%S")
        checkout = datetime.strptime(checkout, "%Y-%m-%d %H:%M:%S")

        booking = Booking(
            Roomid=roomid,
            Customerid=customerid,
            Bookdate=bookdate,
            Checkin=checkin,
            Checkout=checkout,
            status=status
        )

        session.add(booking)
        session.commit()
        print("Booking added successfully!")
    except Exception as e:
        print(f"Error: {e}")
        session.rollback()

@cli.command()
@click.option("--roomtype", prompt="Room Type", help="Room Type")
@click.option("--roomnumber", prompt="Room number", help="Room Price")
@click.option("--status", default="active", help="Room Status (default: active)")
def add_room( Roomtype, Roomnumber, status):
    room = Room(
        Roomtype=Roomtype,
        Roomnumber=Roomnumber,
        status=status
    )
    session.add(room)
    session.commit()
    click.echo("Room added successfully.")

@cli.command()
@click.option("--roomtype", prompt="Room Type", help="Room Type")
@click.option("--roomprice", prompt="Room Price", help="Room Price")
@click.option("--status", default="active", help="Room Status (default: active)")
def add_roomtype(Roomtype, Roomprice, status):
    roomtype = RoomType(
        Roomtype=Roomtype,
        Roomprice=Roomprice,
        status=status
    )
    session.add(roomtype)
    session.commit()
    click.echo("Room Type added successfully.")


@cli.command()
@click.option("--orderid", prompt="Order Id", help="Order Id")
@click.option("--itemid", prompt="Item Id", help="Item Id")
@click.option("--bookid", prompt="Book Id", help="Book Id")
@click.option("--orderdate", prompt="Order Date", help="Order Date")
@click.option("--quantity", prompt="Quantity", help="Quantity")
@click.option("--cost", prompt="Cost", help="Cost")
@click.option("--status", default="active", help="Order's Status (default: active)")
def add_customer(orderid, itemid, bookid, orderdate, quantity, cost, status):
    try:
        # Remove leading and trailing spaces from orderdate
        orderdate = orderdate.strip()
        
        orderdate = datetime.strptime(orderdate, "%Y-%m-%d %H:%M:%S")
        quantity = int(quantity)
        cost = float(cost)
    except ValueError as e:
        click.echo(f"Error: {e}")
        return

    order = Order(
        orderid=orderid,
        itemid=itemid,
        bookid=bookid,
        orderdate=orderdate,
        quantity=quantity,
        cost=cost,
        status=status
    )
    session.add(order)
    session.commit()
    click.echo("Order added successfully.")


if __name__ == "__main__":
    cli()
