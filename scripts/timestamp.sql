/***

Functions and triggers to insert automatically creation date and modifaction date
Can be called from CI/migrations:
select "hello" from __set_all_created_triggers()
select "hello" from __set_all_modified_triggers()
*/

CREATE OR REPLACE FUNCTION __set_creation_date() RETURNS TRIGGER AS $$
BEGIN
  NEW.creation_date = NOW();
RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- CREATION_DATE: Set for all tables that have the creation_date column:
CREATE OR REPLACE FUNCTION __set_all_created_triggers() returns void as $$
DECLARE
    t text;
BEGIN
    FOR t IN
    SELECT table_name
    FROM information_schema.columns
    WHERE column_name = 'created'
        AND table_schema = 'public'
    LOOP
    EXECUTE format
    ('
        DROP TRIGGER IF EXISTS __set_creation_date ON %I;
        CREATE TRIGGER __set_creation_date
        BEFORE INSERT ON %I
        FOR EACH ROW
        EXECUTE PROCEDURE __set_creation_date();', t, t);
END
LOOP;
END;
$$ LANGUAGE plpgsql;

-- LAST_MODIFIED_DATE:

CREATE OR REPLACE FUNCTION __set_modified_date() RETURNS TRIGGER AS $$
BEGIN
  NEW.last_modified_date = NOW();
RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- CREATION_DATE: Set for all tables that have the creation_date column:
CREATE OR REPLACE FUNCTION __set_all_modified_triggers() returns void as $$
DECLARE
    t text;
BEGIN
    FOR t IN
    SELECT cl.table_name
    FROM information_schema.columns cl
    JOIN information_schema."tables" tbl ON cl.table_name = tbl.table_name
    WHERE tbl.table_type = 'BASE TABLE'
    AND cl.column_name = 'updated'
        AND cl.table_schema = 'public'
    LOOP
    EXECUTE format
    ('
        DROP TRIGGER IF EXISTS __set_modified_date ON %I;
        CREATE TRIGGER __set_modified_date
        BEFORE UPDATE ON %I
        FOR EACH ROW
        EXECUTE PROCEDURE __set_modified_date();', t, t);
END
LOOP;
END;
$$ LANGUAGE plpgsql;