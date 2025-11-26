DROP TRIGGER IF EXISTS trg_update_checkin_count ON attendance;
DROP FUNCTION IF EXISTS update_checkin_count;

CREATE OR REPLACE FUNCTION update_checkin_count()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE members
    SET total_check_ins = total_check_ins + 1
    WHERE id = NEW.member_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_checkin_count
AFTER INSERT ON attendance
FOR EACH ROW
EXECUTE FUNCTION update_checkin_count();
