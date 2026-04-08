-- =============================================================
-- C_query_data.sql
-- Step C: Query data from users and calculations tables.
-- =============================================================

-- Retrieve all users
SELECT * FROM users;

-- Retrieve all calculations
SELECT * FROM calculations;

-- Join users and calculations to show who performed each operation
SELECT u.username,
       c.operation,
       c.operand_a,
       c.operand_b,
       c.result
FROM   calculations c
JOIN   users u ON c.user_id = u.id;
