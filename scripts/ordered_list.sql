/***

A ordered list implementation via triggers and Dynamic SQL
Limitations:
	1) Supports only one "ordered list" per table
	2) Currently REQUIRES a table with a self-reference (such as component, comment...) --> Will add logic later on for this..
	3) Needs an "id" column to prevent infinite loops. Need to "parametrize" this...
*/

/**
Depending on the mutation (insert, upd, delete), 

*/
CREATE OR REPLACE FUNCTION __reorder_ordered_list() RETURNS TRIGGER AS $$
declare
  _column_name text;
  _self_ref_column_name text;
  _self_ref_belongs_to text;
  _old_order int;
  _new_order int;
  _is_lowered_in_order bool;
BEGIN    
    -- Even though no declared params are allowed in postgres functions that are called by trigger functions, trigger functions can pass arguments that are then
    -- available in the automatic variable "TG_ARGV[]" and the number of arguments passed is in "TG_NARGS".
    IF TG_NARGS < 1 THEN
      RAISE EXCEPTION 'Must provide the column name as argument in the trigger function calling this function!';
    END IF;
   _column_name := TG_ARGV[0];
   _self_ref_column_name := TG_ARGV[1];
   _self_ref_belongs_to := TG_ARGV[2];
     
    -- INSERT
    IF  (TG_OP = 'INSERT') THEN
        -- Note the usage of the automatic variables "TG_*", which are available in the top level block:
        -- https://www.postgresql.org/docs/current/plpgsql-trigger.html
        
        EXECUTE format('
        UPDATE %1$I.%2$I SET %3$I = %3$I + 1 
        WHERE %3$I >= $1.%3$I
		AND %4$I IS NOT DISTINCT FROM $1.%4$I
        AND %5$I = $1.%5$I
		AND id <> $1.id 
        ', TG_TABLE_SCHEMA, TG_TABLE_NAME, _column_name, _self_ref_column_name, _self_ref_belongs_to) USING new;
    END IF;

    -- UPDATE
    IF  (TG_OP = 'UPDATE') THEN
        -- TODO(df): Changing of the "level", i.e. changing a self-reference is not supported!
        -- IF NEW._self_ref_column_name IS DISTINCT FROM OLD._self_ref_column_name -- NULL!
    	
        
        -- Since column names (or identifiers more generally) can't be used dynamically in SQL/plpgsql, need to use the (injection save) formatting method:
    	EXECUTE format('SELECT $1.%1$I', _column_name) using old into _old_order;
    	EXECUTE format('SELECT $1.%1$I', _column_name) using new into _new_order;
    	IF _new_order < _old_order then
            EXECUTE format('UPDATE %1$I.%2$I SET %3$I = %3$I + 1 WHERE id <> $1.id AND %3$I >= $1.%3$I AND %3$I < $2.%3$I AND %4$I IS NOT DISTINCT FROM $2.%4$I AND %5$I = $1.%5$I', TG_TABLE_SCHEMA, TG_TABLE_NAME, _column_name, _self_ref_column_name, _self_ref_belongs_to) using new, old, TG_RELID;
        -- We don't need to do anything if the order stays the same!
        ELSIF _new_order > _old_order then
            EXECUTE format('UPDATE %1$I.%2$I SET %3$I = %3$I - 1 WHERE id <> $1.id AND %3$I <= $1.%3$I AND %3$I > $2.%3$I AND %4$I IS NOT DISTINCT FROM $2.%4$I AND %5$I = $1.%5$I', TG_TABLE_SCHEMA, TG_TABLE_NAME, _column_name, _self_ref_column_name, _self_ref_belongs_to) using new, old, TG_RELID;
        END IF;
    END IF;

    -- DELETE
    IF  (TG_OP = 'DELETE') THEN
        EXECUTE format('UPDATE %1$I.%2$I SET %3$I = %3$I - 1 WHERE %3$I > $1.%3$I AND %4$I IS NOT DISTINCT FROM $1.%4$I AND %5$I = $1.%5$I', TG_TABLE_SCHEMA, TG_TABLE_NAME, _column_name, _self_ref_column_name, _self_ref_belongs_to) using OLD;
        RETURN OLD;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

/**
For all columns defined here in the variables "tables", this function sets up all the necessary triggers for ordered lists
*/
CREATE OR REPLACE FUNCTION __set_all_ordered_list_triggers() returns void as $$
DECLARE
    -- New tables with an "ordered_list" property should be addded here.
    -- 1. table_name, 2. column_name, 3. FK column name of parent of ordered list, 4. self-reference-column TODO(df): Make optional: In case of no self-ref
    -- Example: ['api_component','order_in_chapter', 'fk_chapter_id', 'fk_component_id']
    -- Note: this placeholder can be replaced with above or via migration script
    tables text[] := array__PLACEHOLDER_ORDERED_COLUMN_ARRAY__;
    t text[];
BEGIN
    FOREACH t SLICE 1 in ARRAY tables
    LOOP
    EXECUTE format
    ('
        -- Ensure that each components position is unique. Deferr the unique constraint to allow shuffling
        ALTER TABLE %1$I DROP CONSTRAINT IF EXISTS "ordered_list_null";
		-- TODO(df): Problem: Null values! Since in SQL NULL = NULL --> undefined!
		-- ALTER TABLE %1$I ADD CONSTRAINT "ordered_list_null" UNIQUE (%3$I,%4$I, %2$I) deferrable initially deferred;
        DROP TRIGGER IF EXISTS __reorder_ordered_list ON %1$I;
        CREATE TRIGGER __reorder_ordered_list
        AFTER INSERT OR DELETE OR UPDATE OF %2$I ON %1$I
        FOR EACH ROW
        EXECUTE PROCEDURE __reorder_ordered_list(%2$I, %4$I, %3$I);
        ', t[1], t[2], t[3], t[4]);
END
LOOP;
END;
$$ LANGUAGE plpgsql;