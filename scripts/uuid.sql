/**

    Queries the db catalog and sets the default gen_random_uuid() for each column found with PK uuid
    Execute with:
    select 'hello world' from __alter_uuid_default();
*/
CREATE OR REPLACE FUNCTION __alter_uuid_default()
returns void as $$
DECLARE
    t text;
BEGIN
    FOR t IN
    SELECT table_name
    FROM information_schema.columns
    WHERE 
    column_name = 'id' 
    AND data_type = 'uuid' 
    AND table_schema = 'public'
    LOOP
    EXECUTE format('ALTER TABLE %I ALTER COLUMN id SET DEFAULT gen_random_uuid();', t);
end LOOP;
END;
$$ LANGUAGE plpgsql;