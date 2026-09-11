# HOSTEL ROOM BOOKING AND FEES MANAGEMENT SYSTEM

## Overview

Your university’s hostel warden currently tracks room bookings and fee payments using a paper ledger, which is slow and error-prone. Your group has been asked to build a Python system to replace it.

## Requirements

### Data setup

The data file has been predefined in data.py and you are required to follow it. It has three hostel blocks, each with a fixed number of rooms and a maximum capacity per room. When the programme starts, print a brief occupancy overview.

### Student registration and room allocation

Allow a new student to be allocated to a specified room only if space remains in it. Reject the allocation with a clear explanation if the room is already full and correctly update the room’s current occupancy when an allocation succeeds.

### Fee payment recording

Allow full or partial fee payments to be recorded against a student’s account. Track and correctly update the outstanding balance across multiple payments made over time for the same student.

### Search and reporting

Allow a student to be searched for by name or registration number. Generate a full occupancy report for each hostel block and generate a list of “fee defaulters”, meaning students whose outstanding balance is above a given threshold.

### File persistence

Save student, room and payment records to file so that data survives between runs and reload this data automatically when the programme starts. Handle a missing or damaged file gracefully rather than crashing.

### Menu-driven driver programme

Bring every module above together behind one well-organised, looping menu that a hostel warden with no programming background could realistically operate, with input validated throughout.

### Code quality and structure

- Organise your solution into simple and well-named functions rather than one long block of code, but may skip writing separate functions for small functionality.
- Add few concise and clear inline comments explaining any non-obvious logic
- Add dosctrings at the beginning of blocks of complex function explaining the purpose, arguments, return values and raises (exceptions).
- use snake case (eg. my_variable_name) for naming all variables and functions
