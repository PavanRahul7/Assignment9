-- =============================================================
-- D_update_record.sql
-- Step D: Update the result of calculation id=1.
-- =============================================================

UPDATE calculations
SET    result = 6
WHERE  id = 1;

-- Verify the update
SELECT * FROM calculations WHERE id = 1;
