"""Hostel Room Booking and Fees Management System.

A simple, beginner-friendly menu-driven programme for a university hostel warden
to manage room allocations, fee payments, student searches, and occupancy reports.
"""

import copy
import datetime
import json
import os
from data import hostel_blocks as default_blocks
from data import payments as default_payments
from data import students as default_students

# Filename used for saving and loading system records
DATA_FILE = "hostel_data.json"

# In-memory working data lists
hostel_blocks = []
students = []
payments = []



# FILE PERSISTENCE FUNCTIONS
def load_data():
    """Loads hostel, student, and payment records from a JSON file.

    If the file does not exist or contains invalid/corrupted data, the programme
    catches the exception gracefully and falls back to default initial data from data.py.

    Returns:
        None
    """
    global hostel_blocks, students, payments

    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                saved_data = json.load(file)
                hostel_blocks = saved_data.get("hostel_blocks", default_blocks)
                students = saved_data.get("students", default_students)
                payments = saved_data.get("payments", default_payments)
                print("[System] Saved records loaded successfully from file.")
                return
        except (json.JSONDecodeError, IOError, Exception) as error:
            # Handle missing or corrupted file gracefully
            print(f"[Warning] Could not read '{DATA_FILE}' ({error}).")
            print("[System] Loading default data from data.py instead.")

    # Initialize from data.py using deepcopy so originals are not mutated
    hostel_blocks = copy.deepcopy(default_blocks)
    students = copy.deepcopy(default_students)
    payments = copy.deepcopy(default_payments)


def save_data():
    """Saves student, room, and payment records to the JSON data file.

    Returns:
        None
    """
    try:
        data_to_save = {
            "hostel_blocks": hostel_blocks,
            "students": students,
            "payments": payments
        }
        with open(DATA_FILE, "w") as file:
            json.dump(data_to_save, file, indent=2)
    except IOError as error:
        print(f"[Error] Failed to save data to file: {error}")



# INPUT VALIDATION HELPERS
def prompt_string(message):
    """Prompts the user until a non-empty string is provided.

    Args:
        message (str): The prompt text shown to the user.

    Returns:
        str: Trimmed non-empty string entered by the user.
    """
    while True:
        value = input(message).strip()
        if value: # if True
            return value
        print("Invalid input: This field cannot be empty. Please try again.")


def prompt_float(message, min_val=0.0):
    """Prompts the user for a valid floating-point number >= min_val.

    Args:
        message (str): The prompt text shown to the user.
        min_val (float): The minimum acceptable numerical value.

    Returns:
        float: Validated float value entered by the user.
    """
    while True:
        raw = input(message).strip()
        try:
            val = float(raw)
            if val < min_val:
                print(f"Invalid input: Value must be at least {min_val}.")
                continue
            return val
        except ValueError:
            print("Invalid input: Please enter a valid number.")


def pause():
    """Prompts the user to press Enter to continue."""
    input("\nPress [Enter] to return to the menu...")



# BLOCK & CAPACITY HELPER FUNCTIONS
def get_block_index(block_name):
    """Returns the index of a block within the hostel_blocks list.

    Args:
        block_name (str): Block identifier ("A", "B", or "C").

    Returns:
        int: Index of the block, or -1 if not found.
    """
    block_upper = block_name.strip().upper()
    if block_upper == "A":
        return 0
    elif block_upper == "B":
        return 1
    elif block_upper == "C":
        return 2
    return -1


def get_total_capacity(block):
    """Returns the total capacity of students across all rooms in a block.

    Args:
        block (dict): The block dictionary containing rooms.

    Returns:
        int: Total capacity of all rooms in the block.
    """
    rooms = block["rooms"]
    total_capacity = 0
    for room in rooms:
        total_capacity += room["capacity"]
    return total_capacity


def get_occupants(block):
    """Returns the total student occupants living in a block.

    Args:
        block (dict): The block dictionary containing rooms.

    Returns:
        int: Total number of occupants currently in the block.
    """
    rooms = block["rooms"]
    total_occupants = 0
    for room in rooms:
        total_occupants += room["occupants"]
    return total_occupants


def find_block(block_name):
    """Searches for a block dictionary by block name.

    Args:
        block_name (str): The name of the block (e.g. "A", "B", "C").

    Returns:
        dict or None: The block dictionary if found, else None.
    """
    target = block_name.strip().upper()
    for block in hostel_blocks:
        if block["block_name"].upper() == target:
            return block
    return None


def find_room(block, room_name):
    """Searches for a room dictionary within a given block.

    Args:
        block (dict): The block dictionary to search in.
        room_name (str): The room identifier (e.g. "A1", "B2").

    Returns:
        dict or None: The room dictionary if found, else None.
    """
    target = room_name.strip().upper()
    for room in block["rooms"]:
        if room["room_name"].upper() == target:
            return room
    return None


def find_students(query):
    """Searches for students whose name or registration number matches the query.

    Args:
        query (str): The name or registration number to search.

    Returns:
        list: A list of matching student dictionaries.
    """
    clean_query = query.strip().lower()
    matches = []
    for s in students:
        name_match = clean_query in s["name"].lower()
        reg_match = clean_query in s.get("reg_no", "").lower()
        if name_match or reg_match:
            matches.append(s)
    return matches



# SYSTEM FEATURES
def display_occupancy_overview():
    """Prints a brief overview of hostel capacity and occupancy at startup and on demand."""
    print("\n" + "=" * 65)
    print("           HOSTEL OCCUPANCY OVERVIEW           ".center(65))
    print("=" * 65)
    print(f"{'Block':<10} {'Total Capacity':<18} {'Occupants':<15} {'Available Space':<15}")
    print("-" * 65)

    grand_capacity = 0
    grand_occupants = 0

    for block in hostel_blocks:
        b_name = block.get("block_name")
        cap = get_total_capacity(block)
        occ = get_occupants(block)
        avail = cap - occ

        grand_capacity += cap
        grand_occupants += occ

        print(f"Block {b_name:<4} {cap:<18} {occ:<15} {avail:<15}")

    print("-" * 65)
    total_avail = grand_capacity - grand_occupants
    print(f"{'TOTAL':<10} {grand_capacity:<18} {grand_occupants:<15} {total_avail:<15}")
    print("=" * 65)


def register_and_allocate_student():
    """Handles new student registration and allocates a room if space is available.

    Validates that the room exists and has remaining capacity. Rejects allocation
    with a clear explanation if the room is already full.
    """
    print("\n--- STUDENT REGISTRATION AND ROOM ALLOCATION ---")

    # Step 1: Input student registration number and validate uniqueness
    reg_no = prompt_string("Enter Student Registration Number (e.g., VU003): ")
    for s in students:
        if s.get("reg_no", "").upper() == reg_no.upper():
            print(f"\n[Error] A student with Registration Number '{reg_no}' already exists ({s['name']}).")
            pause()
            return

    # Step 2: Input student name
    name = prompt_string("Enter Student Full Name: ")

    # Step 3: Select hostel block
    print("\nAvailable Blocks: A, B, C")
    block_input = prompt_string("Enter Block Name (A / B / C): ")
    block = find_block(block_input)
    if not block:
        print(f"\n[Error] Block '{block_input}' does not exist.")
        pause()
        return

    # Step 4: Show rooms in selected block with current occupancy
    print(f"\nRooms in Block {block['block_name']}:")
    print(f"{'Room':<8} {'Capacity':<10} {'Occupants':<12} {'Rate':<10} {'Status':<12}")
    print("-" * 52)
    for r in block["rooms"]:
        is_full = r["occupants"] >= r["capacity"]
        status = "FULL" if is_full else f"{r['capacity'] - r['occupants']} space(s)"
        print(f"{r['room_name']:<8} {r['capacity']:<10} {r['occupants']:<12} {r['rate']:<10} {status:<12}")

    # Step 5: Input target room
    room_input = prompt_string("\nEnter Room Name to allocate (e.g., A1, A2): ")
    room = find_room(block, room_input)
    if not room:
        print(f"\n[Error] Room '{room_input}' does not exist in Block {block['block_name']}.")
        pause()
        return

    # Step 6: Check room space - Reject if full
    if room["occupants"] >= room["capacity"]:
        print(f"\n[Allocation Rejected] Room '{room['room_name']}' in Block '{block['block_name']}' is full!")
        print(f"Current occupancy: {room['occupants']}/{room['capacity']}. No space remaining.")
        pause()
        return

    # Step 7: Allocate room, update occupancy, and record fee balance
    room["occupants"] += 1
    new_student = {
        "name": name,
        "reg_no": reg_no,
        "block_name": block["block_name"],
        "room_name": room["room_name"],
        "balance": room["rate"]
    }
    students.append(new_student)
    save_data()

    print(f"\n[Success] Student '{name}' ({reg_no}) allocated to Room {room['room_name']} in Block {block['block_name']}.")
    print(f"Room fee of {room['rate']} has been added to their outstanding balance.")
    print(f"Updated room occupancy: {room['occupants']}/{room['capacity']}.")
    pause()


def record_fee_payment():
    """Records full or partial fee payments against a student's account.

    Updates the student's outstanding balance and logs the payment transaction.
    """
    print("\n--- RECORD FEE PAYMENT ---")

    search_term = prompt_string("Enter Student Name or Registration Number: ")
    matches = find_students(search_term)

    if not matches:
        print(f"\n[Error] No student found matching '{search_term}'.")
        pause()
        return

    # If multiple students match, let the warden choose one
    if len(matches) == 1:
        target_student = matches[0]
    else:
        print(f"\nMultiple students found:")
        for idx, s in enumerate(matches, 1):
            print(f"  [{idx}] {s['name']} (Reg: {s.get('reg_no', 'N/A')}, Room: {s['block_name']}{s['room_name']}, Balance: {s['balance']})")
        while True:
            choice = input(f"Select student number (1-{len(matches)}): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(matches):
                target_student = matches[int(choice) - 1]
                break
            print("Invalid choice. Please try again.")

    # Show current student details
    print("\nStudent Account Details:")
    print(f"  Name:                {target_student['name']}")
    print(f"  Registration No:     {target_student.get('reg_no', 'N/A')}")
    print(f"  Allocated Room:      Block {target_student['block_name']}, Room {target_student['room_name']}")
    print(f"  Outstanding Balance: {target_student['balance']}")

    if target_student["balance"] <= 0:
        print("\n[Notice] This student has cleared all fees (Outstanding balance is 0).")
        proceed = input("Do you still want to record an advance payment? (y/n): ").strip().lower()
        if proceed != "y":
            pause()
            return

    # Enter payment amount (can be full or partial)
    amount = prompt_float("Enter payment amount: ", min_val=1.0)

    # Update balance and record payment
    old_balance = target_student["balance"]
    target_student["balance"] -= amount

    payment_record = {
        "reg_no": target_student.get("reg_no", "N/A"),
        "name": target_student["name"],
        "amount": amount,
        "date": str(datetime.date.today())
    }
    payments.append(payment_record)
    save_data()

    print("\n[Payment Recorded Successfully]")
    print(f"  Previous Balance:    {old_balance}")
    print(f"  Amount Paid:         {amount}")
    print(f"  New Balance:         {target_student['balance']}")
    pause()


def search_student():
    """Searches for a student by full or partial name or registration number.

    Displays student room allocation, fee balance, and payment history.
    """
    print("\n--- SEARCH STUDENT RECORDS ---")
    query = prompt_string("Enter Student Name or Registration Number to search: ")

    matches = find_students(query)

    if not matches:
        print(f"\n[Result] No student found matching '{query}'.")
    else:
        print(f"\nFound {len(matches)} matching student record(s):\n")
        for idx, s in enumerate(matches, 1):
            print(f"[{idx}] Student Name:       {s['name']}")
            print(f"    Registration No:    {s.get('reg_no', 'N/A')}")
            print(f"    Room Assignment:    Block {s['block_name']}, Room {s['room_name']}")
            print(f"    Outstanding Balance:{s['balance']}")

            # Find payment history for this student
            history = [p for p in payments if (s.get("reg_no") and p.get("reg_no") == s.get("reg_no")) or p.get("name", "").lower() == s["name"].lower()]
            if history:
                print("    Payment History:")
                for p in history:
                    print(f"      - Date: {p.get('date', 'N/A')} | Paid: {p.get('amount')} ")
            else:
                print("    Payment History:    No payments recorded yet.")
            print("-" * 50)

    pause()


def display_full_occupancy_report():
    """Generates a detailed occupancy report for each hostel block.

    Displays room capacities, occupants, available spaces, room rate,
    and lists students currently residing in each room.
    """
    print("\n" + "=" * 74)
    print("            FULL HOSTEL OCCUPANCY & RESIDENTS REPORT            ".center(74))
    print("=" * 74)

    for block in hostel_blocks:
        b_name = block["block_name"]
        total_cap = get_total_capacity(block)
        total_occ = get_occupants(block)
        vacant_spaces = total_cap - total_occ

        print(f"\n>>> HOSTEL BLOCK {b_name} <<<")
        print(f"Total Capacity: {total_cap} | Total Occupants: {total_occ} | Available Spaces: {vacant_spaces}")
        print("-" * 74)
        print(f"{'Room':<8} {'Capacity':<10} {'Occupants':<12} {'Available':<12} {'Rate':<10} {'Status':<10}")
        print("-" * 74)

        for room in block["rooms"]:
            r_name = room["room_name"]
            cap = room["capacity"]
            occ = room["occupants"]
            avail = cap - occ
            rate = room["rate"]
            status = "FULL" if occ >= cap else "AVAILABLE"

            print(f"{r_name:<8} {cap:<10} {occ:<12} {avail:<12} {rate:<10} {status:<10}")

            # Find all students assigned to this room
            residents = [
                f"{s['name']} ({s.get('reg_no', 'N/A')})"
                for s in students
                if s.get("block_name") == b_name and s.get("room_name") == r_name
            ]
            if residents:
                print(f"   Residents: {', '.join(residents)}")
            else:
                print("   Residents: (Vacant)")

        print("-" * 74)

    pause()


def display_fee_defaulters():
    """Generates a list of fee defaulters whose balance is above a user-specified threshold.

    Displays student registration number, name, room, and outstanding amount.
    """
    print("\n--- FEE DEFAULTERS REPORT ---")
    print("Specify a threshold amount to find students owing more than that amount.")
    threshold = prompt_float("Enter balance threshold (e.g. 0 for all owing students): ", min_val=0.0)

    # Filter students with balance greater than threshold
    defaulters = [s for s in students if s["balance"] > threshold]

    if not defaulters:
        print(f"\n[Result] No fee defaulters found with an outstanding balance above {threshold}.")
    else:
        print(f"\nFound {len(defaulters)} student(s) owing more than {threshold}:\n")
        print("-" * 65)
        print(f"{'Reg No':<14} {'Student Name':<20} {'Room':<12} {'Balance Owed':<15}")
        print("-" * 65)

        total_debt = 0.0
        for s in defaulters:
            total_debt += s["balance"]
            room_loc = f"{s['block_name']}-{s['room_name']}"
            print(f"{s.get('reg_no', 'N/A'):<14} {s['name'][:18]:<20} {room_loc:<12} {s['balance']:<15}")

        print("-" * 65)
        print(f"Total Outstanding Amount for Defaulters: {total_debt}")
        print("-" * 65)

    pause()



# MAIN DRIVER MENU
def main_menu():
    """Runs the primary menu-driven execution loop for the hostel management system."""
    # 1. Load persistent data from file (or defaults from data.py if file missing)
    load_data() # dataetup & persistence done by Joyce & David

    # 2. Print initial occupancy overview as required by coursework specification
    display_occupancy_overview() # done by Henry

    # 3. Looping menu driven interface
    while True:
        print("\n" + "=" * 55)
        print("   HOSTEL ROOM BOOKING AND FEES MANAGEMENT SYSTEM   ".center(55))
        print("=" * 55)
        print("  [1] View Hostel Occupancy Overview")
        print("  [2] Register Student & Allocate Room")
        print("  [3] Record Student Fee Payment")
        print("  [4] Search Student (by Name or Reg Number)")
        print("  [5] Generate Full Occupancy Report")
        print("  [6] Generate Fee Defaulters Report")
        print("  [7] Save and Exit")
        print("=" * 55)

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            display_occupancy_overview()
            pause()
        elif choice == "2":
            register_and_allocate_student() # done by Rinidh
        elif choice == "3":
            record_fee_payment() # done by Rinidh
        elif choice == "4":
            search_student() # done by Rinidh + Mugisha
        elif choice == "5":
            display_full_occupancy_report()
        elif choice == "6":
            display_fee_defaulters()
        elif choice == "7":
            save_data()
            print("\n[System] All records have been saved successfully to 'hostel_data.json'.")
            print("Thank you for using the Hostel Management System. Goodbye!\n")
            break
        else:
            print("\n[Invalid Choice] Please enter a valid number between 1 and 7.")


if __name__ == "__main__":
    main_menu()