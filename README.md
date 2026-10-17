# Susu Contribution Management System

## 1. Project Overview

The Susu Contribution Management System is a Python command-line
application for managing members of a weekly contribution group.

Each member is expected to contribute GHS 50.00 per week.

The application supports member registration, partial contributions,
outstanding-balance calculations, payout reports, payout rotation,
and contribution history.

Member information and system records are stored in JSON files.

## 2. Technologies Used

- Python 3
- JSON
- Decimal for monetary calculations
- Python standard library
- unittest for automated testing

No external packages are required.

## 3. Project Structure

The project uses the following files:

    susu-project/
    |
    |-- implement.py
    |-- test.py
    |-- README.md
    |-- list.json
    |-- susu_storage.json
    |-- main.py
    |-- members.py
    |-- member_id.py
    |-- metadata.py
    |-- money.py
    |-- saved_data.py

### main.py

Contains the main application, menu, member registration,
contribution processing, reports, and payout management.

### implement.py
Contains the filename,metadata_file and the constant amount

### members.py
Contains the load_members method which contains weekly_contributions and the payouts received by the member which is then stored in the json file

### member_id.py
This file contains the code which randomly generates a unique member ID 

### metadata.py
Contains the weekly payout reports

### money.py
Contains the code that prevents rounding errors and also accepts a real value/amount

### saved_data.py
Contains the program for saving members information, their contributions,payouts and their weekly contributions report in a file

### test.py

Contains automated tests for contribution calculations,
payout eligibility, rotation, persistence, and menu behavior.

### list.json

Stores member information, including:

- Member ID
- Member name
- Current contribution
- Weekly contribution history
- Cumulative payouts received

### susu_storage.json

Stores system-level information, including:

- Current contribution week
- Payout history

The JSON files are created when the application saves data.

## 4. Installation and Execution

### Requirements

Install Python 3.

Check the installation:

    python3 --version
-Git
### Run the application

Open a terminal and navigate to the project directory.

Run:

    python3 implement.py

## 5. Application Menu

The application provides five options:

1. Add member
2. List Members
3. Update Amount
4. Show Payout Report
5. Exit

### Option 1: Add Member

Registers a new member, generates a unique 10-digit ID,
and records the initial contribution.

Duplicate names are rejected.

### Option 2: List Members

Displays registered members, their current contributions,
and outstanding balances.

The report can also display weekly contribution history
and cumulative payouts received.

### Option 3: Update Amount

Records a contribution payment.

Members may pay in installments, but the total contribution
for the week cannot exceed GHS 50.00.

Zero, negative, invalid, and excessive payments are rejected.

### Option 4: Show Payout Report

Displays current contributions, the total collected,
payout eligibility, and payout history.

A payout is blocked if any member has not contributed
the full GHS 50.00.

When everyone has paid, the program identifies the next
recipient and requests confirmation.

After a successful payout, the application records the payout,
resets current balances, advances the week, and rotates
the payout queue.

### Option 5: Exit

Terminates the application.

## 8. Running the Tests

The project uses Python's built-in unittest framework.

No external testing package is required.

Run:

    python3 -m unittest -v test.py

The tests use temporary files to avoid overwriting the
project's real JSON data.

The test suite checks:

- Money calculations
- Incomplete contributions
- Cancelled payouts
- Successful payouts
- Recipient rotation
- Weekly balance resets
- Contribution history
- JSON persistence
- Invalid menu options
