-- =============================================================
-- E_delete_record.sql
-- Step E: Delete calculation id=2.
-- =============================================================

DELETE FROM calculations
WHERE  id = 2;

-- Verify deletion
SELECT * FROM calculations;
