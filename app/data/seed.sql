INSERT INTO users (username, password, first_name, last_name, role, is_active)
VALUES
    ('tomer_admin', 'Admin123', 'Tomer', 'Gil-Or', 'admin', 1),
    ('dana_user', 'Dana123', 'Dana', 'Levi', 'customer', 1),
    ('ron_guest', 'Ron123', 'Ron', 'Cohen', 'customer', 0);

INSERT INTO accounts (user_id, account_number, account_type, balance, currency)
VALUES
    (1, '100200300', 'checking', 15420.75, 'ILS'),
    (2, '200300400', 'savings', 9800.00, 'ILS'),
    (2, '200300401', 'checking', 1250.50, 'USD');

INSERT INTO transactions (account_id, transaction_type, amount, description, created_at)
VALUES
    (1, 'deposit', 3000.00, 'Salary deposit', '2026-05-01 09:00:00'),
    (1, 'withdrawal', 250.00, 'ATM withdrawal', '2026-05-03 18:20:00'),
    (2, 'deposit', 500.00, 'Monthly savings', '2026-05-04 10:30:00'),
    (3, 'payment', 120.00, 'Card payment', '2026-05-05 14:15:00');
