CREATE FUNCTION public.__alter_uuid_default() RETURNS void
    LANGUAGE plpgsql
    AS $$
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
$$;
CREATE FUNCTION public.__reorder_ordered_list() RETURNS trigger
    LANGUAGE plpgsql
    AS $_$
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
$_$;
CREATE FUNCTION public.__set_all_created_triggers() RETURNS void
    LANGUAGE plpgsql
    AS $$
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
$$;
CREATE FUNCTION public.__set_all_modified_triggers() RETURNS void
    LANGUAGE plpgsql
    AS $$
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
$$;
CREATE FUNCTION public.__set_all_ordered_list_triggers() RETURNS void
    LANGUAGE plpgsql
    AS $_$
DECLARE
    -- New tables with an "ordered_list" property should be addded here.
    -- 1. table_name, 2. column_name, 3. FK column name of parent of ordered list, 4. self-reference-column TODO(df): Make optional: In case of no self-ref
    -- Example: ['api_component','order_in_chapter', 'fk_chapter_id', 'fk_component_id']
    -- Note: this placeholder can be replaced with above or via migration script
    tables text[] := array[['api_component', 'order_in_chapter', 'fk_chapter_id', 'fk_component_id']];
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
$_$;
CREATE FUNCTION public.__set_creation_date() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  NEW.created = NOW();
  NEW.updated = NOW();
RETURN NEW;
END;
$$;
CREATE FUNCTION public.__set_modified_date() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  NEW.updated = NOW();
RETURN NEW;
END;
$$;
CREATE TABLE public.api_book (
    id uuid DEFAULT public.gen_random_uuid() NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    number integer NOT NULL
);
CREATE TABLE public.api_chapter (
    id uuid DEFAULT public.gen_random_uuid() NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    description character varying(500) NOT NULL,
    number integer NOT NULL,
    fk_belongs_to_id uuid,
    fk_book_id uuid,
    disable_children boolean NOT NULL
);
CREATE TABLE public.api_chaptertitle (
    id uuid DEFAULT public.gen_random_uuid() NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    title character varying(200) NOT NULL,
    chapter_id uuid NOT NULL,
    language_id character varying(20) NOT NULL
);
CREATE TABLE public.api_character (
    id uuid DEFAULT public.gen_random_uuid() NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    formal_name character varying(45) NOT NULL,
    informal_name character varying(45) NOT NULL,
    gender character varying(1),
    title character varying(45),
    speaker character varying(45),
    fk_book_id uuid
);
CREATE TABLE public.api_comment (
    id uuid DEFAULT public.gen_random_uuid() NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    text character varying(500) NOT NULL,
    active boolean NOT NULL,
    context character varying(1),
    written timestamp with time zone,
    fk_author_id uuid,
    fk_chapter_id uuid,
    fk_component_id uuid NOT NULL,
    fk_parent_comment_id uuid
);
CREATE TABLE public.api_component (
    id uuid DEFAULT public.gen_random_uuid() NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    data jsonb NOT NULL,
    state character varying(1) NOT NULL,
    locked_ts timestamp with time zone NOT NULL,
    fk_chapter_id uuid NOT NULL,
    fk_component_id uuid,
    fk_component_type_id uuid NOT NULL,
    fk_locked_by_id uuid,
    order_in_chapter integer NOT NULL,
    CONSTRAINT api_component_order_in_chapter_check CHECK ((order_in_chapter >= 0))
);
CREATE TABLE public.api_componenttype (
    id uuid DEFAULT public.gen_random_uuid() NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    name character varying(45) NOT NULL,
    schema jsonb NOT NULL,
    base boolean NOT NULL,
    icon character varying(100) NOT NULL,
    label character varying(45) NOT NULL,
    fk_frontend_widget_id uuid,
    fk_parent_type_id uuid
);
CREATE TABLE public.api_language (
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    id character varying(20) NOT NULL,
    name character varying(100) NOT NULL
);
CREATE TABLE public.api_media (
    id uuid DEFAULT public.gen_random_uuid() NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    type character varying(45) NOT NULL,
    url character varying(255) NOT NULL,
    fk_component_id uuid
);
CREATE TABLE public.api_profile (
    id uuid DEFAULT public.gen_random_uuid() NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    firstname character varying(100) NOT NULL,
    lastname character varying(100) NOT NULL,
    roles character varying(120) NOT NULL,
    "current_role" character varying(30) NOT NULL,
    event_notifications boolean NOT NULL,
    setup_completed boolean NOT NULL,
    fk_language_id character varying(20),
    user_id integer NOT NULL
);
CREATE TABLE public.api_profile_translator_languages (
    id integer NOT NULL,
    profile_id uuid NOT NULL,
    language_id character varying(20) NOT NULL
);
CREATE SEQUENCE public.api_profile_translator_languages_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.api_profile_translator_languages_id_seq OWNED BY public.api_profile_translator_languages.id;
CREATE TABLE public.api_text (
    id uuid DEFAULT public.gen_random_uuid() NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    translatable boolean NOT NULL,
    fk_component_id uuid NOT NULL,
    placeholder text
);
CREATE TABLE public.api_translation (
    id uuid DEFAULT public.gen_random_uuid() NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    text_field text,
    valid boolean NOT NULL,
    fk_language_id character varying(20) NOT NULL,
    fk_text_id uuid NOT NULL
);
CREATE TABLE public.api_word (
    id uuid DEFAULT public.gen_random_uuid() NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL
);
CREATE TABLE public.api_wordgroup (
    id uuid DEFAULT public.gen_random_uuid() NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    fk_chapter_id uuid
);
CREATE TABLE public.api_wordgroup_words (
    id integer NOT NULL,
    wordgroup_id uuid NOT NULL,
    word_id uuid NOT NULL
);
CREATE SEQUENCE public.api_wordgroup_words_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.api_wordgroup_words_id_seq OWNED BY public.api_wordgroup_words.id;
CREATE TABLE public.api_wordgrouptitle (
    id uuid DEFAULT public.gen_random_uuid() NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    title character varying(200) NOT NULL,
    language_id character varying(20) NOT NULL,
    "wordGroup_id" uuid NOT NULL
);
CREATE TABLE public.api_wordtranslation (
    id uuid DEFAULT public.gen_random_uuid() NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    text character varying(40) NOT NULL,
    audio character varying(255),
    example_sentence character varying(500),
    fk_language_id character varying(20) NOT NULL,
    word_id uuid NOT NULL
);
CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);
CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;
CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);
CREATE SEQUENCE public.auth_group_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;
CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);
CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;
CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);
CREATE TABLE public.auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);
CREATE SEQUENCE public.auth_user_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.auth_user_groups_id_seq OWNED BY public.auth_user_groups.id;
CREATE SEQUENCE public.auth_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.auth_user_id_seq OWNED BY public.auth_user.id;
CREATE TABLE public.auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);
CREATE SEQUENCE public.auth_user_user_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.auth_user_user_permissions_id_seq OWNED BY public.auth_user_user_permissions.id;
CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);
CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;
CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);
CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;
CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);
CREATE SEQUENCE public.django_migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;
CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);
ALTER TABLE ONLY public.api_profile_translator_languages ALTER COLUMN id SET DEFAULT nextval('public.api_profile_translator_languages_id_seq'::regclass);
ALTER TABLE ONLY public.api_wordgroup_words ALTER COLUMN id SET DEFAULT nextval('public.api_wordgroup_words_id_seq'::regclass);
ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);
ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);
ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);
ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq'::regclass);
ALTER TABLE ONLY public.auth_user_groups ALTER COLUMN id SET DEFAULT nextval('public.auth_user_groups_id_seq'::regclass);
ALTER TABLE ONLY public.auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_user_user_permissions_id_seq'::regclass);
ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);
ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);
ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);
ALTER TABLE ONLY public.api_book
    ADD CONSTRAINT api_book_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.api_chapter
    ADD CONSTRAINT api_chapter_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.api_chaptertitle
    ADD CONSTRAINT api_chaptertitle_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.api_character
    ADD CONSTRAINT api_character_formal_name_fk_book_id_01f452af_uniq UNIQUE (formal_name, fk_book_id);
ALTER TABLE ONLY public.api_character
    ADD CONSTRAINT api_character_informal_name_fk_book_id_4ca7aa6d_uniq UNIQUE (informal_name, fk_book_id);
ALTER TABLE ONLY public.api_character
    ADD CONSTRAINT api_character_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.api_comment
    ADD CONSTRAINT api_comment_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.api_component
    ADD CONSTRAINT api_component_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.api_componenttype
    ADD CONSTRAINT api_componenttype_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.api_language
    ADD CONSTRAINT api_language_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.api_media
    ADD CONSTRAINT api_media_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.api_profile
    ADD CONSTRAINT api_profile_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.api_profile_translator_languages
    ADD CONSTRAINT api_profile_translator_l_profile_id_language_id_54b48cc3_uniq UNIQUE (profile_id, language_id);
ALTER TABLE ONLY public.api_profile_translator_languages
    ADD CONSTRAINT api_profile_translator_languages_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.api_profile
    ADD CONSTRAINT api_profile_user_id_key UNIQUE (user_id);
ALTER TABLE ONLY public.api_text
    ADD CONSTRAINT api_text_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.api_translation
    ADD CONSTRAINT api_translation_fk_language_id_fk_text_id_807318e5_uniq UNIQUE (fk_language_id, fk_text_id);
ALTER TABLE ONLY public.api_translation
    ADD CONSTRAINT api_translation_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.api_word
    ADD CONSTRAINT api_word_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.api_wordgroup
    ADD CONSTRAINT api_wordgroup_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.api_wordgroup_words
    ADD CONSTRAINT api_wordgroup_words_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.api_wordgroup_words
    ADD CONSTRAINT api_wordgroup_words_wordgroup_id_word_id_aebfaecb_uniq UNIQUE (wordgroup_id, word_id);
ALTER TABLE ONLY public.api_wordgrouptitle
    ADD CONSTRAINT api_wordgrouptitle_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.api_wordtranslation
    ADD CONSTRAINT api_wordtranslation_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);
ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);
ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);
ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);
ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);
ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);
ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);
ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);
CREATE INDEX api_chapter_fk_belongs_to_id_576cd489 ON public.api_chapter USING btree (fk_belongs_to_id);
CREATE INDEX api_chapter_fk_book_id_46668b75 ON public.api_chapter USING btree (fk_book_id);
CREATE INDEX api_chaptertitle_chapter_id_6db27968 ON public.api_chaptertitle USING btree (chapter_id);
CREATE INDEX api_chaptertitle_language_id_6c27a0a9 ON public.api_chaptertitle USING btree (language_id);
CREATE INDEX api_chaptertitle_language_id_6c27a0a9_like ON public.api_chaptertitle USING btree (language_id varchar_pattern_ops);
CREATE INDEX api_character_fk_book_id_ca20a75b ON public.api_character USING btree (fk_book_id);
CREATE INDEX api_comment_fk_author_id_91cc0cf9 ON public.api_comment USING btree (fk_author_id);
CREATE INDEX api_comment_fk_chapter_id_39183f79 ON public.api_comment USING btree (fk_chapter_id);
CREATE INDEX api_comment_fk_component_id_79fe320e ON public.api_comment USING btree (fk_component_id);
CREATE INDEX api_comment_fk_parent_comment_id_68b52553 ON public.api_comment USING btree (fk_parent_comment_id);
CREATE INDEX api_component_fk_chapter_id_8111705c ON public.api_component USING btree (fk_chapter_id);
CREATE INDEX api_component_fk_component_id_6b3b3166 ON public.api_component USING btree (fk_component_id);
CREATE INDEX api_component_fk_component_type_id_7257d108 ON public.api_component USING btree (fk_component_type_id);
CREATE INDEX api_component_fk_locked_by_id_42c14e1c ON public.api_component USING btree (fk_locked_by_id);
CREATE INDEX api_componenttype_fk_frontend_widget_id_b6515b7e ON public.api_componenttype USING btree (fk_frontend_widget_id);
CREATE INDEX api_componenttype_fk_parent_type_id_17f082de ON public.api_componenttype USING btree (fk_parent_type_id);
CREATE INDEX api_language_id_05fbbec3_like ON public.api_language USING btree (id varchar_pattern_ops);
CREATE INDEX api_media_fk_component_id_73a6dada ON public.api_media USING btree (fk_component_id);
CREATE INDEX api_profile_fk_language_id_7e07e756 ON public.api_profile USING btree (fk_language_id);
CREATE INDEX api_profile_fk_language_id_7e07e756_like ON public.api_profile USING btree (fk_language_id varchar_pattern_ops);
CREATE INDEX api_profile_translator_languages_language_id_b4512bc9 ON public.api_profile_translator_languages USING btree (language_id);
CREATE INDEX api_profile_translator_languages_language_id_b4512bc9_like ON public.api_profile_translator_languages USING btree (language_id varchar_pattern_ops);
CREATE INDEX api_profile_translator_languages_profile_id_04827fb9 ON public.api_profile_translator_languages USING btree (profile_id);
CREATE INDEX api_text_fk_component_id_3460180b ON public.api_text USING btree (fk_component_id);
CREATE INDEX api_translation_fk_language_id_1d2ccd51 ON public.api_translation USING btree (fk_language_id);
CREATE INDEX api_translation_fk_language_id_1d2ccd51_like ON public.api_translation USING btree (fk_language_id varchar_pattern_ops);
CREATE INDEX api_translation_fk_text_id_005e71dc ON public.api_translation USING btree (fk_text_id);
CREATE INDEX api_wordgroup_fk_chapter_id_6116571e ON public.api_wordgroup USING btree (fk_chapter_id);
CREATE INDEX api_wordgroup_words_word_id_4d17b2ab ON public.api_wordgroup_words USING btree (word_id);
CREATE INDEX api_wordgroup_words_wordgroup_id_14408e3a ON public.api_wordgroup_words USING btree (wordgroup_id);
CREATE INDEX api_wordgrouptitle_language_id_1d5652fe ON public.api_wordgrouptitle USING btree (language_id);
CREATE INDEX api_wordgrouptitle_language_id_1d5652fe_like ON public.api_wordgrouptitle USING btree (language_id varchar_pattern_ops);
CREATE INDEX "api_wordgrouptitle_wordGroup_id_e3edc932" ON public.api_wordgrouptitle USING btree ("wordGroup_id");
CREATE INDEX api_wordtranslation_fk_language_id_bfc057ff ON public.api_wordtranslation USING btree (fk_language_id);
CREATE INDEX api_wordtranslation_fk_language_id_bfc057ff_like ON public.api_wordtranslation USING btree (fk_language_id varchar_pattern_ops);
CREATE INDEX api_wordtranslation_word_id_3a712d3e ON public.api_wordtranslation USING btree (word_id);
CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);
CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);
CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);
CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);
CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);
CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);
CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);
CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);
CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);
CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);
CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);
CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);
CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);
CREATE TRIGGER __reorder_ordered_list AFTER INSERT OR DELETE OR UPDATE OF order_in_chapter ON public.api_component FOR EACH ROW EXECUTE FUNCTION public.__reorder_ordered_list('order_in_chapter', 'fk_component_id', 'fk_chapter_id');
CREATE TRIGGER __set_creation_date BEFORE INSERT ON public.api_book FOR EACH ROW EXECUTE FUNCTION public.__set_creation_date();
CREATE TRIGGER __set_creation_date BEFORE INSERT ON public.api_chapter FOR EACH ROW EXECUTE FUNCTION public.__set_creation_date();
CREATE TRIGGER __set_creation_date BEFORE INSERT ON public.api_chaptertitle FOR EACH ROW EXECUTE FUNCTION public.__set_creation_date();
CREATE TRIGGER __set_creation_date BEFORE INSERT ON public.api_character FOR EACH ROW EXECUTE FUNCTION public.__set_creation_date();
CREATE TRIGGER __set_creation_date BEFORE INSERT ON public.api_comment FOR EACH ROW EXECUTE FUNCTION public.__set_creation_date();
CREATE TRIGGER __set_creation_date BEFORE INSERT ON public.api_component FOR EACH ROW EXECUTE FUNCTION public.__set_creation_date();
CREATE TRIGGER __set_creation_date BEFORE INSERT ON public.api_componenttype FOR EACH ROW EXECUTE FUNCTION public.__set_creation_date();
CREATE TRIGGER __set_creation_date BEFORE INSERT ON public.api_language FOR EACH ROW EXECUTE FUNCTION public.__set_creation_date();
CREATE TRIGGER __set_creation_date BEFORE INSERT ON public.api_media FOR EACH ROW EXECUTE FUNCTION public.__set_creation_date();
CREATE TRIGGER __set_creation_date BEFORE INSERT ON public.api_profile FOR EACH ROW EXECUTE FUNCTION public.__set_creation_date();
CREATE TRIGGER __set_creation_date BEFORE INSERT ON public.api_text FOR EACH ROW EXECUTE FUNCTION public.__set_creation_date();
CREATE TRIGGER __set_creation_date BEFORE INSERT ON public.api_translation FOR EACH ROW EXECUTE FUNCTION public.__set_creation_date();
CREATE TRIGGER __set_creation_date BEFORE INSERT ON public.api_word FOR EACH ROW EXECUTE FUNCTION public.__set_creation_date();
CREATE TRIGGER __set_creation_date BEFORE INSERT ON public.api_wordgroup FOR EACH ROW EXECUTE FUNCTION public.__set_creation_date();
CREATE TRIGGER __set_creation_date BEFORE INSERT ON public.api_wordgrouptitle FOR EACH ROW EXECUTE FUNCTION public.__set_creation_date();
CREATE TRIGGER __set_creation_date BEFORE INSERT ON public.api_wordtranslation FOR EACH ROW EXECUTE FUNCTION public.__set_creation_date();
CREATE TRIGGER __set_modified_date BEFORE UPDATE ON public.api_book FOR EACH ROW EXECUTE FUNCTION public.__set_modified_date();
CREATE TRIGGER __set_modified_date BEFORE UPDATE ON public.api_chapter FOR EACH ROW EXECUTE FUNCTION public.__set_modified_date();
CREATE TRIGGER __set_modified_date BEFORE UPDATE ON public.api_chaptertitle FOR EACH ROW EXECUTE FUNCTION public.__set_modified_date();
CREATE TRIGGER __set_modified_date BEFORE UPDATE ON public.api_character FOR EACH ROW EXECUTE FUNCTION public.__set_modified_date();
CREATE TRIGGER __set_modified_date BEFORE UPDATE ON public.api_comment FOR EACH ROW EXECUTE FUNCTION public.__set_modified_date();
CREATE TRIGGER __set_modified_date BEFORE UPDATE ON public.api_component FOR EACH ROW EXECUTE FUNCTION public.__set_modified_date();
CREATE TRIGGER __set_modified_date BEFORE UPDATE ON public.api_componenttype FOR EACH ROW EXECUTE FUNCTION public.__set_modified_date();
CREATE TRIGGER __set_modified_date BEFORE UPDATE ON public.api_language FOR EACH ROW EXECUTE FUNCTION public.__set_modified_date();
CREATE TRIGGER __set_modified_date BEFORE UPDATE ON public.api_media FOR EACH ROW EXECUTE FUNCTION public.__set_modified_date();
CREATE TRIGGER __set_modified_date BEFORE UPDATE ON public.api_profile FOR EACH ROW EXECUTE FUNCTION public.__set_modified_date();
CREATE TRIGGER __set_modified_date BEFORE UPDATE ON public.api_text FOR EACH ROW EXECUTE FUNCTION public.__set_modified_date();
CREATE TRIGGER __set_modified_date BEFORE UPDATE ON public.api_translation FOR EACH ROW EXECUTE FUNCTION public.__set_modified_date();
CREATE TRIGGER __set_modified_date BEFORE UPDATE ON public.api_word FOR EACH ROW EXECUTE FUNCTION public.__set_modified_date();
CREATE TRIGGER __set_modified_date BEFORE UPDATE ON public.api_wordgroup FOR EACH ROW EXECUTE FUNCTION public.__set_modified_date();
CREATE TRIGGER __set_modified_date BEFORE UPDATE ON public.api_wordgrouptitle FOR EACH ROW EXECUTE FUNCTION public.__set_modified_date();
CREATE TRIGGER __set_modified_date BEFORE UPDATE ON public.api_wordtranslation FOR EACH ROW EXECUTE FUNCTION public.__set_modified_date();
ALTER TABLE ONLY public.api_chapter
    ADD CONSTRAINT api_chapter_fk_belongs_to_id_576cd489_fk_api_chapter_id FOREIGN KEY (fk_belongs_to_id) REFERENCES public.api_chapter(id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.api_chapter
    ADD CONSTRAINT api_chapter_fk_book_id_46668b75_fk_api_book_id FOREIGN KEY (fk_book_id) REFERENCES public.api_book(id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.api_chaptertitle
    ADD CONSTRAINT api_chaptertitle_chapter_id_6db27968_fk_api_chapter_id FOREIGN KEY (chapter_id) REFERENCES public.api_chapter(id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.api_chaptertitle
    ADD CONSTRAINT api_chaptertitle_language_id_6c27a0a9_fk_api_language_id FOREIGN KEY (language_id) REFERENCES public.api_language(id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.api_character
    ADD CONSTRAINT api_character_fk_book_id_ca20a75b_fk_api_book_id FOREIGN KEY (fk_book_id) REFERENCES public.api_book(id) ON UPDATE CASCADE ON DELETE SET NULL DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.api_comment
    ADD CONSTRAINT api_comment_fk_author_id_91cc0cf9_fk_api_profile_id FOREIGN KEY (fk_author_id) REFERENCES public.api_profile(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.api_comment
    ADD CONSTRAINT api_comment_fk_chapter_id_39183f79_fk_api_chapter_id FOREIGN KEY (fk_chapter_id) REFERENCES public.api_chapter(id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.api_comment
    ADD CONSTRAINT api_comment_fk_component_id_79fe320e_fk_api_component_id FOREIGN KEY (fk_component_id) REFERENCES public.api_component(id) ON UPDATE CASCADE ON DELETE SET NULL DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.api_comment
    ADD CONSTRAINT api_comment_fk_parent_comment_id_68b52553_fk_api_comment_id FOREIGN KEY (fk_parent_comment_id) REFERENCES public.api_comment(id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.api_component
    ADD CONSTRAINT api_component_fk_chapter_id_8111705c_fk_api_chapter_id FOREIGN KEY (fk_chapter_id) REFERENCES public.api_chapter(id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.api_component
    ADD CONSTRAINT api_component_fk_component_id_6b3b3166_fk_api_component_id FOREIGN KEY (fk_component_id) REFERENCES public.api_component(id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.api_component
    ADD CONSTRAINT api_component_fk_component_type_id_7257d108_fk_api_compo FOREIGN KEY (fk_component_type_id) REFERENCES public.api_componenttype(id) ON UPDATE CASCADE ON DELETE RESTRICT DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.api_component
    ADD CONSTRAINT api_component_fk_locked_by_id_42c14e1c_fk_api_profile_id FOREIGN KEY (fk_locked_by_id) REFERENCES public.api_profile(id) ON UPDATE CASCADE ON DELETE SET NULL DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.api_componenttype
    ADD CONSTRAINT api_componenttype_fk_frontend_widget_i_b6515b7e_fk_api_compo FOREIGN KEY (fk_frontend_widget_id) REFERENCES public.api_componenttype(id) ON UPDATE CASCADE ON DELETE SET NULL DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.api_componenttype
    ADD CONSTRAINT api_componenttype_fk_parent_type_id_17f082de_fk_api_compo FOREIGN KEY (fk_parent_type_id) REFERENCES public.api_componenttype(id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.api_media
    ADD CONSTRAINT api_media_fk_component_id_73a6dada_fk_api_component_id FOREIGN KEY (fk_component_id) REFERENCES public.api_component(id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.api_profile
    ADD CONSTRAINT api_profile_fk_language_id_7e07e756_fk_api_language_id FOREIGN KEY (fk_language_id) REFERENCES public.api_language(id) ON UPDATE CASCADE ON DELETE SET NULL DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.api_profile_translator_languages
    ADD CONSTRAINT api_profile_translat_language_id_b4512bc9_fk_api_langu FOREIGN KEY (language_id) REFERENCES public.api_language(id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.api_profile_translator_languages
    ADD CONSTRAINT api_profile_translat_profile_id_04827fb9_fk_api_profi FOREIGN KEY (profile_id) REFERENCES public.api_profile(id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.api_profile
    ADD CONSTRAINT api_profile_user_id_41309820_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.api_text
    ADD CONSTRAINT api_text_fk_component_id_3460180b_fk_api_component_id FOREIGN KEY (fk_component_id) REFERENCES public.api_component(id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.api_translation
    ADD CONSTRAINT api_translation_fk_language_id_1d2ccd51_fk_api_language_id FOREIGN KEY (fk_language_id) REFERENCES public.api_language(id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.api_translation
    ADD CONSTRAINT api_translation_fk_text_id_005e71dc_fk_api_text_id FOREIGN KEY (fk_text_id) REFERENCES public.api_text(id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.api_wordgroup
    ADD CONSTRAINT api_wordgroup_fk_chapter_id_6116571e_fk_api_chapter_id FOREIGN KEY (fk_chapter_id) REFERENCES public.api_chapter(id) ON UPDATE CASCADE ON DELETE SET NULL DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.api_wordgroup_words
    ADD CONSTRAINT api_wordgroup_words_word_id_4d17b2ab_fk_api_word_id FOREIGN KEY (word_id) REFERENCES public.api_word(id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.api_wordgroup_words
    ADD CONSTRAINT api_wordgroup_words_wordgroup_id_14408e3a_fk_api_wordgroup_id FOREIGN KEY (wordgroup_id) REFERENCES public.api_wordgroup(id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.api_wordgrouptitle
    ADD CONSTRAINT api_wordgrouptitle_language_id_1d5652fe_fk_api_language_id FOREIGN KEY (language_id) REFERENCES public.api_language(id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.api_wordgrouptitle
    ADD CONSTRAINT "api_wordgrouptitle_wordGroup_id_e3edc932_fk_api_wordgroup_id" FOREIGN KEY ("wordGroup_id") REFERENCES public.api_wordgroup(id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.api_wordtranslation
    ADD CONSTRAINT api_wordtranslation_fk_language_id_bfc057ff_fk_api_language_id FOREIGN KEY (fk_language_id) REFERENCES public.api_language(id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.api_wordtranslation
    ADD CONSTRAINT api_wordtranslation_word_id_3a712d3e_fk_api_word_id FOREIGN KEY (word_id) REFERENCES public.api_word(id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
