
## Contribution Rules

1. Each member contributes GHS 50.00 per week.
2. Partial payments are allowed.
3. A payment cannot exceed the outstanding balance.
4. Every member must complete the contribution before a payout.
5. A cancelled payout must not change the queue or week.
6. A successful payout advances the contribution week.
7. Previous contribution records must be preserved.
8. The payout recipient rotates after a successful payout.

##  Payout Calculation

The payout is calculated by adding the contributions
collected from all registered members.

For example, if four members each contribute GHS 50.00:

    Total payout = 4 * GHS 50.00
                 = GHS 200.00

The payout cannot proceed if any member has an incomplete
contribution.



## Data Storage and Safety

Back up list.json and susu_storage.json before manually
editing the files or making significant changes.

The application should report malformed JSON rather than
silently replacing existing records with empty data.

Saving two separate JSON files is not a fully atomic
transaction. A failure during saving can leave the files
inconsistent.

A relational database with transactions would provide
stronger consistency for a larger deployment.

##  Limitations

- The application runs in a command-line terminal.
- Data is stored locally in JSON files.
- The application does not transfer money to a bank
  account or mobile-money wallet.
- Payout records do not independently prove that money
  was physically transferred.
- The application does not yet provide user authentication
  or administrator permissions.
- It does not yet provide automated payment reminders.

## Future Improvements

Possible improvements include:

- A graphical user interface
- A web application
- MySQL integration
- Authentication and authorization
- Exportable reports
- Automated contribution reminders
- Audit logging
- Transaction-safe payout processing

## Conclusion

The Susu Contribution Management System demonstrates
member management, monetary calculations, JSON persistence,
input validation, payout eligibility, queue rotation,
and automated testing using Python.