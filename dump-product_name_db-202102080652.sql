PGDMP         4                y            product_name_db    13.1 (Debian 13.1-1.pgdg100+1)     13.1 (Ubuntu 13.1-1.pgdg20.04+1) �    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    16384    product_name_db    DATABASE     c   CREATE DATABASE product_name_db WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'en_US.utf8';
    DROP DATABASE product_name_db;
                product_name_db_user    false                        2615    18049    public    SCHEMA        CREATE SCHEMA public;
    DROP SCHEMA public;
                product_name_db_user    false            �           0    0    SCHEMA public    COMMENT     6   COMMENT ON SCHEMA public IS 'standard public schema';
                   product_name_db_user    false    5            �            1259    18050    account_emailaddress    TABLE     �   CREATE TABLE public.account_emailaddress (
    id integer NOT NULL,
    email character varying(254) NOT NULL,
    verified boolean NOT NULL,
    "primary" boolean NOT NULL,
    user_id integer NOT NULL
);
 (   DROP TABLE public.account_emailaddress;
       public         heap    product_name_db_user    false    5            �            1259    18053    account_emailaddress_id_seq    SEQUENCE     �   CREATE SEQUENCE public.account_emailaddress_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 2   DROP SEQUENCE public.account_emailaddress_id_seq;
       public          product_name_db_user    false    5    200            �           0    0    account_emailaddress_id_seq    SEQUENCE OWNED BY     [   ALTER SEQUENCE public.account_emailaddress_id_seq OWNED BY public.account_emailaddress.id;
          public          product_name_db_user    false    201            �            1259    18055    account_emailconfirmation    TABLE     �   CREATE TABLE public.account_emailconfirmation (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    sent timestamp with time zone,
    key character varying(64) NOT NULL,
    email_address_id integer NOT NULL
);
 -   DROP TABLE public.account_emailconfirmation;
       public         heap    product_name_db_user    false    5            �            1259    18058     account_emailconfirmation_id_seq    SEQUENCE     �   CREATE SEQUENCE public.account_emailconfirmation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 7   DROP SEQUENCE public.account_emailconfirmation_id_seq;
       public          product_name_db_user    false    202    5            �           0    0     account_emailconfirmation_id_seq    SEQUENCE OWNED BY     e   ALTER SEQUENCE public.account_emailconfirmation_id_seq OWNED BY public.account_emailconfirmation.id;
          public          product_name_db_user    false    203            �            1259    18060    accounts_balancetransaction    TABLE       CREATE TABLE public.accounts_balancetransaction (
    id integer NOT NULL,
    type_of_transaction character varying(1) NOT NULL,
    amount numeric(7,2) NOT NULL,
    verified boolean NOT NULL,
    created timestamp with time zone NOT NULL,
    user_id integer NOT NULL
);
 /   DROP TABLE public.accounts_balancetransaction;
       public         heap    product_name_db_user    false    5            �            1259    18063 "   accounts_balancetransaction_id_seq    SEQUENCE     �   CREATE SEQUENCE public.accounts_balancetransaction_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 9   DROP SEQUENCE public.accounts_balancetransaction_id_seq;
       public          product_name_db_user    false    5    204            �           0    0 "   accounts_balancetransaction_id_seq    SEQUENCE OWNED BY     i   ALTER SEQUENCE public.accounts_balancetransaction_id_seq OWNED BY public.accounts_balancetransaction.id;
          public          product_name_db_user    false    205            �            1259    18065    accounts_billingaddress    TABLE     �  CREATE TABLE public.accounts_billingaddress (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    address1 character varying(128) NOT NULL,
    address2 character varying(128) NOT NULL,
    zip_code character varying(12) NOT NULL,
    city character varying(128) NOT NULL,
    state character varying(128) NOT NULL,
    country character varying(3) NOT NULL,
    user_id integer NOT NULL
);
 +   DROP TABLE public.accounts_billingaddress;
       public         heap    product_name_db_user    false    5            �            1259    18071    accounts_billingaddress_id_seq    SEQUENCE     �   CREATE SEQUENCE public.accounts_billingaddress_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 5   DROP SEQUENCE public.accounts_billingaddress_id_seq;
       public          product_name_db_user    false    5    206            �           0    0    accounts_billingaddress_id_seq    SEQUENCE OWNED BY     a   ALTER SEQUENCE public.accounts_billingaddress_id_seq OWNED BY public.accounts_billingaddress.id;
          public          product_name_db_user    false    207            �            1259    18073    accounts_contactnumberotp    TABLE     �   CREATE TABLE public.accounts_contactnumberotp (
    id integer NOT NULL,
    username character varying(12) NOT NULL,
    created timestamp with time zone NOT NULL
);
 -   DROP TABLE public.accounts_contactnumberotp;
       public         heap    product_name_db_user    false    5            �            1259    18076     accounts_contactnumberotp_id_seq    SEQUENCE     �   CREATE SEQUENCE public.accounts_contactnumberotp_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 7   DROP SEQUENCE public.accounts_contactnumberotp_id_seq;
       public          product_name_db_user    false    5    208            �           0    0     accounts_contactnumberotp_id_seq    SEQUENCE OWNED BY     e   ALTER SEQUENCE public.accounts_contactnumberotp_id_seq OWNED BY public.accounts_contactnumberotp.id;
          public          product_name_db_user    false    209            �            1259    18078    accounts_customuser    TABLE     �  CREATE TABLE public.accounts_customuser (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    username character varying(12) NOT NULL,
    first_name character varying(26) NOT NULL,
    last_name character varying(26) NOT NULL,
    picture character varying(100) NOT NULL,
    aadhaar_number character varying(12) NOT NULL,
    pan_number character varying(10) NOT NULL,
    identity_proof character varying(100) NOT NULL,
    identity_verified boolean NOT NULL,
    identity_reject_reason character varying(250) NOT NULL,
    contact_secret character varying(16) NOT NULL,
    contact_verified boolean NOT NULL,
    is_willing_master boolean NOT NULL,
    balance_amount numeric(8,2) NOT NULL,
    investment_amount numeric(7,2) NOT NULL
);
 '   DROP TABLE public.accounts_customuser;
       public         heap    product_name_db_user    false    5            �            1259    18084    accounts_customuser_groups    TABLE     �   CREATE TABLE public.accounts_customuser_groups (
    id integer NOT NULL,
    customuser_id integer NOT NULL,
    group_id integer NOT NULL
);
 .   DROP TABLE public.accounts_customuser_groups;
       public         heap    product_name_db_user    false    5            �            1259    18087 !   accounts_customuser_groups_id_seq    SEQUENCE     �   CREATE SEQUENCE public.accounts_customuser_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 8   DROP SEQUENCE public.accounts_customuser_groups_id_seq;
       public          product_name_db_user    false    211    5            �           0    0 !   accounts_customuser_groups_id_seq    SEQUENCE OWNED BY     g   ALTER SEQUENCE public.accounts_customuser_groups_id_seq OWNED BY public.accounts_customuser_groups.id;
          public          product_name_db_user    false    212            �            1259    18089    accounts_customuser_id_seq    SEQUENCE     �   CREATE SEQUENCE public.accounts_customuser_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public.accounts_customuser_id_seq;
       public          product_name_db_user    false    210    5            �           0    0    accounts_customuser_id_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public.accounts_customuser_id_seq OWNED BY public.accounts_customuser.id;
          public          product_name_db_user    false    213            �            1259    18091 $   accounts_customuser_user_permissions    TABLE     �   CREATE TABLE public.accounts_customuser_user_permissions (
    id integer NOT NULL,
    customuser_id integer NOT NULL,
    permission_id integer NOT NULL
);
 8   DROP TABLE public.accounts_customuser_user_permissions;
       public         heap    product_name_db_user    false    5            �            1259    18094 +   accounts_customuser_user_permissions_id_seq    SEQUENCE     �   CREATE SEQUENCE public.accounts_customuser_user_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 B   DROP SEQUENCE public.accounts_customuser_user_permissions_id_seq;
       public          product_name_db_user    false    5    214            �           0    0 +   accounts_customuser_user_permissions_id_seq    SEQUENCE OWNED BY     {   ALTER SEQUENCE public.accounts_customuser_user_permissions_id_seq OWNED BY public.accounts_customuser_user_permissions.id;
          public          product_name_db_user    false    215            �            1259    18096    accounts_investmenttransaction    TABLE       CREATE TABLE public.accounts_investmenttransaction (
    id integer NOT NULL,
    type_of_transaction character varying(1) NOT NULL,
    amount numeric(7,2) NOT NULL,
    verified boolean NOT NULL,
    pool_id integer NOT NULL,
    user_id integer NOT NULL
);
 2   DROP TABLE public.accounts_investmenttransaction;
       public         heap    product_name_db_user    false    5            �            1259    18099 %   accounts_investmenttransaction_id_seq    SEQUENCE     �   CREATE SEQUENCE public.accounts_investmenttransaction_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 <   DROP SEQUENCE public.accounts_investmenttransaction_id_seq;
       public          product_name_db_user    false    5    216            �           0    0 %   accounts_investmenttransaction_id_seq    SEQUENCE OWNED BY     o   ALTER SEQUENCE public.accounts_investmenttransaction_id_seq OWNED BY public.accounts_investmenttransaction.id;
          public          product_name_db_user    false    217            �            1259    18101 
   auth_group    TABLE     f   CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);
    DROP TABLE public.auth_group;
       public         heap    product_name_db_user    false    5            �            1259    18104    auth_group_id_seq    SEQUENCE     �   CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.auth_group_id_seq;
       public          product_name_db_user    false    218    5            �           0    0    auth_group_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;
          public          product_name_db_user    false    219            �            1259    18106    auth_group_permissions    TABLE     �   CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);
 *   DROP TABLE public.auth_group_permissions;
       public         heap    product_name_db_user    false    5            �            1259    18109    auth_group_permissions_id_seq    SEQUENCE     �   CREATE SEQUENCE public.auth_group_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 4   DROP SEQUENCE public.auth_group_permissions_id_seq;
       public          product_name_db_user    false    5    220            �           0    0    auth_group_permissions_id_seq    SEQUENCE OWNED BY     _   ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;
          public          product_name_db_user    false    221            �            1259    18111    auth_permission    TABLE     �   CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);
 #   DROP TABLE public.auth_permission;
       public         heap    product_name_db_user    false    5            �            1259    18114    auth_permission_id_seq    SEQUENCE     �   CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.auth_permission_id_seq;
       public          product_name_db_user    false    222    5            �           0    0    auth_permission_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;
          public          product_name_db_user    false    223            �            1259    18116    captcha_captchastore    TABLE     �   CREATE TABLE public.captcha_captchastore (
    id integer NOT NULL,
    challenge character varying(32) NOT NULL,
    response character varying(32) NOT NULL,
    hashkey character varying(40) NOT NULL,
    expiration timestamp with time zone NOT NULL
);
 (   DROP TABLE public.captcha_captchastore;
       public         heap    product_name_db_user    false    5            �            1259    18119    captcha_captchastore_id_seq    SEQUENCE     �   CREATE SEQUENCE public.captcha_captchastore_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 2   DROP SEQUENCE public.captcha_captchastore_id_seq;
       public          product_name_db_user    false    5    224            �           0    0    captcha_captchastore_id_seq    SEQUENCE OWNED BY     [   ALTER SEQUENCE public.captcha_captchastore_id_seq OWNED BY public.captcha_captchastore.id;
          public          product_name_db_user    false    225            �            1259    18121    django_admin_log    TABLE     �  CREATE TABLE public.django_admin_log (
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
 $   DROP TABLE public.django_admin_log;
       public         heap    product_name_db_user    false    5            �            1259    18128    django_admin_log_id_seq    SEQUENCE     �   CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.django_admin_log_id_seq;
       public          product_name_db_user    false    5    226            �           0    0    django_admin_log_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;
          public          product_name_db_user    false    227            �            1259    18130    django_content_type    TABLE     �   CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);
 '   DROP TABLE public.django_content_type;
       public         heap    product_name_db_user    false    5            �            1259    18133    django_content_type_id_seq    SEQUENCE     �   CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public.django_content_type_id_seq;
       public          product_name_db_user    false    228    5            �           0    0    django_content_type_id_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;
          public          product_name_db_user    false    229            �            1259    18135    django_migrations    TABLE     �   CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);
 %   DROP TABLE public.django_migrations;
       public         heap    product_name_db_user    false    5            �            1259    18141    django_migrations_id_seq    SEQUENCE     �   CREATE SEQUENCE public.django_migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 /   DROP SEQUENCE public.django_migrations_id_seq;
       public          product_name_db_user    false    230    5            �           0    0    django_migrations_id_seq    SEQUENCE OWNED BY     U   ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;
          public          product_name_db_user    false    231            �            1259    18143    django_session    TABLE     �   CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);
 "   DROP TABLE public.django_session;
       public         heap    product_name_db_user    false    5            �            1259    18149    django_site    TABLE     �   CREATE TABLE public.django_site (
    id integer NOT NULL,
    domain character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);
    DROP TABLE public.django_site;
       public         heap    product_name_db_user    false    5            �            1259    18152    django_site_id_seq    SEQUENCE     �   CREATE SEQUENCE public.django_site_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public.django_site_id_seq;
       public          product_name_db_user    false    233    5            �           0    0    django_site_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public.django_site_id_seq OWNED BY public.django_site.id;
          public          product_name_db_user    false    234            �            1259    18154 
   pools_pool    TABLE     L  CREATE TABLE public.pools_pool (
    id integer NOT NULL,
    codename character varying(250) NOT NULL,
    name character varying(250) NOT NULL,
    size integer NOT NULL,
    investment numeric(7,2) NOT NULL,
    created timestamp with time zone NOT NULL,
    activated timestamp with time zone,
    master_id integer NOT NULL
);
    DROP TABLE public.pools_pool;
       public         heap    product_name_db_user    false    5            �            1259    18160    pools_pool_id_seq    SEQUENCE     �   CREATE SEQUENCE public.pools_pool_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.pools_pool_id_seq;
       public          product_name_db_user    false    235    5            �           0    0    pools_pool_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.pools_pool_id_seq OWNED BY public.pools_pool.id;
          public          product_name_db_user    false    236            �            1259    18162    pools_poolinvite    TABLE     �   CREATE TABLE public.pools_poolinvite (
    id integer NOT NULL,
    username character varying(12) NOT NULL,
    created timestamp with time zone NOT NULL,
    accepted boolean NOT NULL,
    pool_id integer NOT NULL
);
 $   DROP TABLE public.pools_poolinvite;
       public         heap    product_name_db_user    false    5            �            1259    18165    pools_poolinvite_id_seq    SEQUENCE     �   CREATE SEQUENCE public.pools_poolinvite_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.pools_poolinvite_id_seq;
       public          product_name_db_user    false    5    237            �           0    0    pools_poolinvite_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.pools_poolinvite_id_seq OWNED BY public.pools_poolinvite.id;
          public          product_name_db_user    false    238            �            1259    18167    pools_poolmember    TABLE     ~   CREATE TABLE public.pools_poolmember (
    id integer NOT NULL,
    pool_id integer NOT NULL,
    user_id integer NOT NULL
);
 $   DROP TABLE public.pools_poolmember;
       public         heap    product_name_db_user    false    5            �            1259    18170    pools_poolmember_id_seq    SEQUENCE     �   CREATE SEQUENCE public.pools_poolmember_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.pools_poolmember_id_seq;
       public          product_name_db_user    false    5    239            �           0    0    pools_poolmember_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.pools_poolmember_id_seq OWNED BY public.pools_poolmember.id;
          public          product_name_db_user    false    240            �            1259    18172    socialaccount_socialaccount    TABLE     D  CREATE TABLE public.socialaccount_socialaccount (
    id integer NOT NULL,
    provider character varying(30) NOT NULL,
    uid character varying(191) NOT NULL,
    last_login timestamp with time zone NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    extra_data text NOT NULL,
    user_id integer NOT NULL
);
 /   DROP TABLE public.socialaccount_socialaccount;
       public         heap    product_name_db_user    false    5            �            1259    18178 "   socialaccount_socialaccount_id_seq    SEQUENCE     �   CREATE SEQUENCE public.socialaccount_socialaccount_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 9   DROP SEQUENCE public.socialaccount_socialaccount_id_seq;
       public          product_name_db_user    false    5    241            �           0    0 "   socialaccount_socialaccount_id_seq    SEQUENCE OWNED BY     i   ALTER SEQUENCE public.socialaccount_socialaccount_id_seq OWNED BY public.socialaccount_socialaccount.id;
          public          product_name_db_user    false    242            �            1259    18180    socialaccount_socialapp    TABLE     #  CREATE TABLE public.socialaccount_socialapp (
    id integer NOT NULL,
    provider character varying(30) NOT NULL,
    name character varying(40) NOT NULL,
    client_id character varying(191) NOT NULL,
    secret character varying(191) NOT NULL,
    key character varying(191) NOT NULL
);
 +   DROP TABLE public.socialaccount_socialapp;
       public         heap    product_name_db_user    false    5            �            1259    18186    socialaccount_socialapp_id_seq    SEQUENCE     �   CREATE SEQUENCE public.socialaccount_socialapp_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 5   DROP SEQUENCE public.socialaccount_socialapp_id_seq;
       public          product_name_db_user    false    243    5            �           0    0    socialaccount_socialapp_id_seq    SEQUENCE OWNED BY     a   ALTER SEQUENCE public.socialaccount_socialapp_id_seq OWNED BY public.socialaccount_socialapp.id;
          public          product_name_db_user    false    244            �            1259    18188    socialaccount_socialapp_sites    TABLE     �   CREATE TABLE public.socialaccount_socialapp_sites (
    id integer NOT NULL,
    socialapp_id integer NOT NULL,
    site_id integer NOT NULL
);
 1   DROP TABLE public.socialaccount_socialapp_sites;
       public         heap    product_name_db_user    false    5            �            1259    18191 $   socialaccount_socialapp_sites_id_seq    SEQUENCE     �   CREATE SEQUENCE public.socialaccount_socialapp_sites_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ;   DROP SEQUENCE public.socialaccount_socialapp_sites_id_seq;
       public          product_name_db_user    false    5    245                        0    0 $   socialaccount_socialapp_sites_id_seq    SEQUENCE OWNED BY     m   ALTER SEQUENCE public.socialaccount_socialapp_sites_id_seq OWNED BY public.socialaccount_socialapp_sites.id;
          public          product_name_db_user    false    246            �            1259    18193    socialaccount_socialtoken    TABLE     �   CREATE TABLE public.socialaccount_socialtoken (
    id integer NOT NULL,
    token text NOT NULL,
    token_secret text NOT NULL,
    expires_at timestamp with time zone,
    account_id integer NOT NULL,
    app_id integer NOT NULL
);
 -   DROP TABLE public.socialaccount_socialtoken;
       public         heap    product_name_db_user    false    5            �            1259    18199     socialaccount_socialtoken_id_seq    SEQUENCE     �   CREATE SEQUENCE public.socialaccount_socialtoken_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 7   DROP SEQUENCE public.socialaccount_socialtoken_id_seq;
       public          product_name_db_user    false    247    5                       0    0     socialaccount_socialtoken_id_seq    SEQUENCE OWNED BY     e   ALTER SEQUENCE public.socialaccount_socialtoken_id_seq OWNED BY public.socialaccount_socialtoken.id;
          public          product_name_db_user    false    248            �           2604    18201    account_emailaddress id    DEFAULT     �   ALTER TABLE ONLY public.account_emailaddress ALTER COLUMN id SET DEFAULT nextval('public.account_emailaddress_id_seq'::regclass);
 F   ALTER TABLE public.account_emailaddress ALTER COLUMN id DROP DEFAULT;
       public          product_name_db_user    false    201    200            �           2604    18202    account_emailconfirmation id    DEFAULT     �   ALTER TABLE ONLY public.account_emailconfirmation ALTER COLUMN id SET DEFAULT nextval('public.account_emailconfirmation_id_seq'::regclass);
 K   ALTER TABLE public.account_emailconfirmation ALTER COLUMN id DROP DEFAULT;
       public          product_name_db_user    false    203    202            �           2604    18203    accounts_balancetransaction id    DEFAULT     �   ALTER TABLE ONLY public.accounts_balancetransaction ALTER COLUMN id SET DEFAULT nextval('public.accounts_balancetransaction_id_seq'::regclass);
 M   ALTER TABLE public.accounts_balancetransaction ALTER COLUMN id DROP DEFAULT;
       public          product_name_db_user    false    205    204            �           2604    18204    accounts_billingaddress id    DEFAULT     �   ALTER TABLE ONLY public.accounts_billingaddress ALTER COLUMN id SET DEFAULT nextval('public.accounts_billingaddress_id_seq'::regclass);
 I   ALTER TABLE public.accounts_billingaddress ALTER COLUMN id DROP DEFAULT;
       public          product_name_db_user    false    207    206            �           2604    18205    accounts_contactnumberotp id    DEFAULT     �   ALTER TABLE ONLY public.accounts_contactnumberotp ALTER COLUMN id SET DEFAULT nextval('public.accounts_contactnumberotp_id_seq'::regclass);
 K   ALTER TABLE public.accounts_contactnumberotp ALTER COLUMN id DROP DEFAULT;
       public          product_name_db_user    false    209    208            �           2604    18206    accounts_customuser id    DEFAULT     �   ALTER TABLE ONLY public.accounts_customuser ALTER COLUMN id SET DEFAULT nextval('public.accounts_customuser_id_seq'::regclass);
 E   ALTER TABLE public.accounts_customuser ALTER COLUMN id DROP DEFAULT;
       public          product_name_db_user    false    213    210            �           2604    18207    accounts_customuser_groups id    DEFAULT     �   ALTER TABLE ONLY public.accounts_customuser_groups ALTER COLUMN id SET DEFAULT nextval('public.accounts_customuser_groups_id_seq'::regclass);
 L   ALTER TABLE public.accounts_customuser_groups ALTER COLUMN id DROP DEFAULT;
       public          product_name_db_user    false    212    211            �           2604    18208 '   accounts_customuser_user_permissions id    DEFAULT     �   ALTER TABLE ONLY public.accounts_customuser_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.accounts_customuser_user_permissions_id_seq'::regclass);
 V   ALTER TABLE public.accounts_customuser_user_permissions ALTER COLUMN id DROP DEFAULT;
       public          product_name_db_user    false    215    214            �           2604    18209 !   accounts_investmenttransaction id    DEFAULT     �   ALTER TABLE ONLY public.accounts_investmenttransaction ALTER COLUMN id SET DEFAULT nextval('public.accounts_investmenttransaction_id_seq'::regclass);
 P   ALTER TABLE public.accounts_investmenttransaction ALTER COLUMN id DROP DEFAULT;
       public          product_name_db_user    false    217    216            �           2604    18210    auth_group id    DEFAULT     n   ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);
 <   ALTER TABLE public.auth_group ALTER COLUMN id DROP DEFAULT;
       public          product_name_db_user    false    219    218            �           2604    18211    auth_group_permissions id    DEFAULT     �   ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);
 H   ALTER TABLE public.auth_group_permissions ALTER COLUMN id DROP DEFAULT;
       public          product_name_db_user    false    221    220            �           2604    18212    auth_permission id    DEFAULT     x   ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);
 A   ALTER TABLE public.auth_permission ALTER COLUMN id DROP DEFAULT;
       public          product_name_db_user    false    223    222            �           2604    18213    captcha_captchastore id    DEFAULT     �   ALTER TABLE ONLY public.captcha_captchastore ALTER COLUMN id SET DEFAULT nextval('public.captcha_captchastore_id_seq'::regclass);
 F   ALTER TABLE public.captcha_captchastore ALTER COLUMN id DROP DEFAULT;
       public          product_name_db_user    false    225    224            �           2604    18214    django_admin_log id    DEFAULT     z   ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);
 B   ALTER TABLE public.django_admin_log ALTER COLUMN id DROP DEFAULT;
       public          product_name_db_user    false    227    226            �           2604    18215    django_content_type id    DEFAULT     �   ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);
 E   ALTER TABLE public.django_content_type ALTER COLUMN id DROP DEFAULT;
       public          product_name_db_user    false    229    228            �           2604    18216    django_migrations id    DEFAULT     |   ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);
 C   ALTER TABLE public.django_migrations ALTER COLUMN id DROP DEFAULT;
       public          product_name_db_user    false    231    230            �           2604    18217    django_site id    DEFAULT     p   ALTER TABLE ONLY public.django_site ALTER COLUMN id SET DEFAULT nextval('public.django_site_id_seq'::regclass);
 =   ALTER TABLE public.django_site ALTER COLUMN id DROP DEFAULT;
       public          product_name_db_user    false    234    233            �           2604    18218    pools_pool id    DEFAULT     n   ALTER TABLE ONLY public.pools_pool ALTER COLUMN id SET DEFAULT nextval('public.pools_pool_id_seq'::regclass);
 <   ALTER TABLE public.pools_pool ALTER COLUMN id DROP DEFAULT;
       public          product_name_db_user    false    236    235            �           2604    18219    pools_poolinvite id    DEFAULT     z   ALTER TABLE ONLY public.pools_poolinvite ALTER COLUMN id SET DEFAULT nextval('public.pools_poolinvite_id_seq'::regclass);
 B   ALTER TABLE public.pools_poolinvite ALTER COLUMN id DROP DEFAULT;
       public          product_name_db_user    false    238    237            �           2604    18220    pools_poolmember id    DEFAULT     z   ALTER TABLE ONLY public.pools_poolmember ALTER COLUMN id SET DEFAULT nextval('public.pools_poolmember_id_seq'::regclass);
 B   ALTER TABLE public.pools_poolmember ALTER COLUMN id DROP DEFAULT;
       public          product_name_db_user    false    240    239            �           2604    18221    socialaccount_socialaccount id    DEFAULT     �   ALTER TABLE ONLY public.socialaccount_socialaccount ALTER COLUMN id SET DEFAULT nextval('public.socialaccount_socialaccount_id_seq'::regclass);
 M   ALTER TABLE public.socialaccount_socialaccount ALTER COLUMN id DROP DEFAULT;
       public          product_name_db_user    false    242    241            �           2604    18222    socialaccount_socialapp id    DEFAULT     �   ALTER TABLE ONLY public.socialaccount_socialapp ALTER COLUMN id SET DEFAULT nextval('public.socialaccount_socialapp_id_seq'::regclass);
 I   ALTER TABLE public.socialaccount_socialapp ALTER COLUMN id DROP DEFAULT;
       public          product_name_db_user    false    244    243            �           2604    18223     socialaccount_socialapp_sites id    DEFAULT     �   ALTER TABLE ONLY public.socialaccount_socialapp_sites ALTER COLUMN id SET DEFAULT nextval('public.socialaccount_socialapp_sites_id_seq'::regclass);
 O   ALTER TABLE public.socialaccount_socialapp_sites ALTER COLUMN id DROP DEFAULT;
       public          product_name_db_user    false    246    245            �           2604    18224    socialaccount_socialtoken id    DEFAULT     �   ALTER TABLE ONLY public.socialaccount_socialtoken ALTER COLUMN id SET DEFAULT nextval('public.socialaccount_socialtoken_id_seq'::regclass);
 K   ALTER TABLE public.socialaccount_socialtoken ALTER COLUMN id DROP DEFAULT;
       public          product_name_db_user    false    248    247            �          0    18050    account_emailaddress 
   TABLE DATA           W   COPY public.account_emailaddress (id, email, verified, "primary", user_id) FROM stdin;
    public          product_name_db_user    false    200            �          0    18055    account_emailconfirmation 
   TABLE DATA           ]   COPY public.account_emailconfirmation (id, created, sent, key, email_address_id) FROM stdin;
    public          product_name_db_user    false    202            �          0    18060    accounts_balancetransaction 
   TABLE DATA           r   COPY public.accounts_balancetransaction (id, type_of_transaction, amount, verified, created, user_id) FROM stdin;
    public          product_name_db_user    false    204            �          0    18065    accounts_billingaddress 
   TABLE DATA           x   COPY public.accounts_billingaddress (id, name, address1, address2, zip_code, city, state, country, user_id) FROM stdin;
    public          product_name_db_user    false    206            �          0    18073    accounts_contactnumberotp 
   TABLE DATA           J   COPY public.accounts_contactnumberotp (id, username, created) FROM stdin;
    public          product_name_db_user    false    208            �          0    18078    accounts_customuser 
   TABLE DATA           W  COPY public.accounts_customuser (id, password, last_login, is_superuser, email, is_staff, is_active, date_joined, username, first_name, last_name, picture, aadhaar_number, pan_number, identity_proof, identity_verified, identity_reject_reason, contact_secret, contact_verified, is_willing_master, balance_amount, investment_amount) FROM stdin;
    public          product_name_db_user    false    210            �          0    18084    accounts_customuser_groups 
   TABLE DATA           Q   COPY public.accounts_customuser_groups (id, customuser_id, group_id) FROM stdin;
    public          product_name_db_user    false    211            �          0    18091 $   accounts_customuser_user_permissions 
   TABLE DATA           `   COPY public.accounts_customuser_user_permissions (id, customuser_id, permission_id) FROM stdin;
    public          product_name_db_user    false    214            �          0    18096    accounts_investmenttransaction 
   TABLE DATA           u   COPY public.accounts_investmenttransaction (id, type_of_transaction, amount, verified, pool_id, user_id) FROM stdin;
    public          product_name_db_user    false    216            �          0    18101 
   auth_group 
   TABLE DATA           .   COPY public.auth_group (id, name) FROM stdin;
    public          product_name_db_user    false    218            �          0    18106    auth_group_permissions 
   TABLE DATA           M   COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
    public          product_name_db_user    false    220            �          0    18111    auth_permission 
   TABLE DATA           N   COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
    public          product_name_db_user    false    222            �          0    18116    captcha_captchastore 
   TABLE DATA           \   COPY public.captcha_captchastore (id, challenge, response, hashkey, expiration) FROM stdin;
    public          product_name_db_user    false    224            �          0    18121    django_admin_log 
   TABLE DATA           �   COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
    public          product_name_db_user    false    226            �          0    18130    django_content_type 
   TABLE DATA           C   COPY public.django_content_type (id, app_label, model) FROM stdin;
    public          product_name_db_user    false    228            �          0    18135    django_migrations 
   TABLE DATA           C   COPY public.django_migrations (id, app, name, applied) FROM stdin;
    public          product_name_db_user    false    230            �          0    18143    django_session 
   TABLE DATA           P   COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
    public          product_name_db_user    false    232            �          0    18149    django_site 
   TABLE DATA           7   COPY public.django_site (id, domain, name) FROM stdin;
    public          product_name_db_user    false    233            �          0    18154 
   pools_pool 
   TABLE DATA           i   COPY public.pools_pool (id, codename, name, size, investment, created, activated, master_id) FROM stdin;
    public          product_name_db_user    false    235            �          0    18162    pools_poolinvite 
   TABLE DATA           T   COPY public.pools_poolinvite (id, username, created, accepted, pool_id) FROM stdin;
    public          product_name_db_user    false    237            �          0    18167    pools_poolmember 
   TABLE DATA           @   COPY public.pools_poolmember (id, pool_id, user_id) FROM stdin;
    public          product_name_db_user    false    239            �          0    18172    socialaccount_socialaccount 
   TABLE DATA           v   COPY public.socialaccount_socialaccount (id, provider, uid, last_login, date_joined, extra_data, user_id) FROM stdin;
    public          product_name_db_user    false    241            �          0    18180    socialaccount_socialapp 
   TABLE DATA           ]   COPY public.socialaccount_socialapp (id, provider, name, client_id, secret, key) FROM stdin;
    public          product_name_db_user    false    243            �          0    18188    socialaccount_socialapp_sites 
   TABLE DATA           R   COPY public.socialaccount_socialapp_sites (id, socialapp_id, site_id) FROM stdin;
    public          product_name_db_user    false    245            �          0    18193    socialaccount_socialtoken 
   TABLE DATA           l   COPY public.socialaccount_socialtoken (id, token, token_secret, expires_at, account_id, app_id) FROM stdin;
    public          product_name_db_user    false    247                       0    0    account_emailaddress_id_seq    SEQUENCE SET     J   SELECT pg_catalog.setval('public.account_emailaddress_id_seq', 1, false);
          public          product_name_db_user    false    201                       0    0     account_emailconfirmation_id_seq    SEQUENCE SET     O   SELECT pg_catalog.setval('public.account_emailconfirmation_id_seq', 1, false);
          public          product_name_db_user    false    203                       0    0 "   accounts_balancetransaction_id_seq    SEQUENCE SET     P   SELECT pg_catalog.setval('public.accounts_balancetransaction_id_seq', 1, true);
          public          product_name_db_user    false    205                       0    0    accounts_billingaddress_id_seq    SEQUENCE SET     M   SELECT pg_catalog.setval('public.accounts_billingaddress_id_seq', 1, false);
          public          product_name_db_user    false    207                       0    0     accounts_contactnumberotp_id_seq    SEQUENCE SET     N   SELECT pg_catalog.setval('public.accounts_contactnumberotp_id_seq', 6, true);
          public          product_name_db_user    false    209                       0    0 !   accounts_customuser_groups_id_seq    SEQUENCE SET     O   SELECT pg_catalog.setval('public.accounts_customuser_groups_id_seq', 3, true);
          public          product_name_db_user    false    212                       0    0    accounts_customuser_id_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('public.accounts_customuser_id_seq', 6, true);
          public          product_name_db_user    false    213            	           0    0 +   accounts_customuser_user_permissions_id_seq    SEQUENCE SET     Z   SELECT pg_catalog.setval('public.accounts_customuser_user_permissions_id_seq', 1, false);
          public          product_name_db_user    false    215            
           0    0 %   accounts_investmenttransaction_id_seq    SEQUENCE SET     T   SELECT pg_catalog.setval('public.accounts_investmenttransaction_id_seq', 1, false);
          public          product_name_db_user    false    217                       0    0    auth_group_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.auth_group_id_seq', 3, true);
          public          product_name_db_user    false    219                       0    0    auth_group_permissions_id_seq    SEQUENCE SET     L   SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 39, true);
          public          product_name_db_user    false    221                       0    0    auth_permission_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.auth_permission_id_seq', 80, true);
          public          product_name_db_user    false    223                       0    0    captcha_captchastore_id_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public.captcha_captchastore_id_seq', 1, true);
          public          product_name_db_user    false    225                       0    0    django_admin_log_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, true);
          public          product_name_db_user    false    227                       0    0    django_content_type_id_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public.django_content_type_id_seq', 20, true);
          public          product_name_db_user    false    229                       0    0    django_migrations_id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.django_migrations_id_seq', 29, true);
          public          product_name_db_user    false    231                       0    0    django_site_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.django_site_id_seq', 1, true);
          public          product_name_db_user    false    234                       0    0    pools_pool_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.pools_pool_id_seq', 1, true);
          public          product_name_db_user    false    236                       0    0    pools_poolinvite_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.pools_poolinvite_id_seq', 1, true);
          public          product_name_db_user    false    238                       0    0    pools_poolmember_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.pools_poolmember_id_seq', 1, false);
          public          product_name_db_user    false    240                       0    0 "   socialaccount_socialaccount_id_seq    SEQUENCE SET     Q   SELECT pg_catalog.setval('public.socialaccount_socialaccount_id_seq', 1, false);
          public          product_name_db_user    false    242                       0    0    socialaccount_socialapp_id_seq    SEQUENCE SET     M   SELECT pg_catalog.setval('public.socialaccount_socialapp_id_seq', 1, false);
          public          product_name_db_user    false    244                       0    0 $   socialaccount_socialapp_sites_id_seq    SEQUENCE SET     S   SELECT pg_catalog.setval('public.socialaccount_socialapp_sites_id_seq', 1, false);
          public          product_name_db_user    false    246                       0    0     socialaccount_socialtoken_id_seq    SEQUENCE SET     O   SELECT pg_catalog.setval('public.socialaccount_socialtoken_id_seq', 1, false);
          public          product_name_db_user    false    248            �           2606    18226 3   account_emailaddress account_emailaddress_email_key 
   CONSTRAINT     o   ALTER TABLE ONLY public.account_emailaddress
    ADD CONSTRAINT account_emailaddress_email_key UNIQUE (email);
 ]   ALTER TABLE ONLY public.account_emailaddress DROP CONSTRAINT account_emailaddress_email_key;
       public            product_name_db_user    false    200            �           2606    18228 .   account_emailaddress account_emailaddress_pkey 
   CONSTRAINT     l   ALTER TABLE ONLY public.account_emailaddress
    ADD CONSTRAINT account_emailaddress_pkey PRIMARY KEY (id);
 X   ALTER TABLE ONLY public.account_emailaddress DROP CONSTRAINT account_emailaddress_pkey;
       public            product_name_db_user    false    200            �           2606    18230 ;   account_emailconfirmation account_emailconfirmation_key_key 
   CONSTRAINT     u   ALTER TABLE ONLY public.account_emailconfirmation
    ADD CONSTRAINT account_emailconfirmation_key_key UNIQUE (key);
 e   ALTER TABLE ONLY public.account_emailconfirmation DROP CONSTRAINT account_emailconfirmation_key_key;
       public            product_name_db_user    false    202            �           2606    18232 8   account_emailconfirmation account_emailconfirmation_pkey 
   CONSTRAINT     v   ALTER TABLE ONLY public.account_emailconfirmation
    ADD CONSTRAINT account_emailconfirmation_pkey PRIMARY KEY (id);
 b   ALTER TABLE ONLY public.account_emailconfirmation DROP CONSTRAINT account_emailconfirmation_pkey;
       public            product_name_db_user    false    202            �           2606    18234 <   accounts_balancetransaction accounts_balancetransaction_pkey 
   CONSTRAINT     z   ALTER TABLE ONLY public.accounts_balancetransaction
    ADD CONSTRAINT accounts_balancetransaction_pkey PRIMARY KEY (id);
 f   ALTER TABLE ONLY public.accounts_balancetransaction DROP CONSTRAINT accounts_balancetransaction_pkey;
       public            product_name_db_user    false    204            �           2606    18236 4   accounts_billingaddress accounts_billingaddress_pkey 
   CONSTRAINT     r   ALTER TABLE ONLY public.accounts_billingaddress
    ADD CONSTRAINT accounts_billingaddress_pkey PRIMARY KEY (id);
 ^   ALTER TABLE ONLY public.accounts_billingaddress DROP CONSTRAINT accounts_billingaddress_pkey;
       public            product_name_db_user    false    206            �           2606    18238 ;   accounts_billingaddress accounts_billingaddress_user_id_key 
   CONSTRAINT     y   ALTER TABLE ONLY public.accounts_billingaddress
    ADD CONSTRAINT accounts_billingaddress_user_id_key UNIQUE (user_id);
 e   ALTER TABLE ONLY public.accounts_billingaddress DROP CONSTRAINT accounts_billingaddress_user_id_key;
       public            product_name_db_user    false    206            �           2606    18240 8   accounts_contactnumberotp accounts_contactnumberotp_pkey 
   CONSTRAINT     v   ALTER TABLE ONLY public.accounts_contactnumberotp
    ADD CONSTRAINT accounts_contactnumberotp_pkey PRIMARY KEY (id);
 b   ALTER TABLE ONLY public.accounts_contactnumberotp DROP CONSTRAINT accounts_contactnumberotp_pkey;
       public            product_name_db_user    false    208            �           2606    18242 Z   accounts_customuser_groups accounts_customuser_groups_customuser_id_group_id_c074bdcb_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.accounts_customuser_groups
    ADD CONSTRAINT accounts_customuser_groups_customuser_id_group_id_c074bdcb_uniq UNIQUE (customuser_id, group_id);
 �   ALTER TABLE ONLY public.accounts_customuser_groups DROP CONSTRAINT accounts_customuser_groups_customuser_id_group_id_c074bdcb_uniq;
       public            product_name_db_user    false    211    211            �           2606    18244 :   accounts_customuser_groups accounts_customuser_groups_pkey 
   CONSTRAINT     x   ALTER TABLE ONLY public.accounts_customuser_groups
    ADD CONSTRAINT accounts_customuser_groups_pkey PRIMARY KEY (id);
 d   ALTER TABLE ONLY public.accounts_customuser_groups DROP CONSTRAINT accounts_customuser_groups_pkey;
       public            product_name_db_user    false    211            �           2606    18246 ,   accounts_customuser accounts_customuser_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY public.accounts_customuser
    ADD CONSTRAINT accounts_customuser_pkey PRIMARY KEY (id);
 V   ALTER TABLE ONLY public.accounts_customuser DROP CONSTRAINT accounts_customuser_pkey;
       public            product_name_db_user    false    210            �           2606    18248 d   accounts_customuser_user_permissions accounts_customuser_user_customuser_id_permission_9632a709_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.accounts_customuser_user_permissions
    ADD CONSTRAINT accounts_customuser_user_customuser_id_permission_9632a709_uniq UNIQUE (customuser_id, permission_id);
 �   ALTER TABLE ONLY public.accounts_customuser_user_permissions DROP CONSTRAINT accounts_customuser_user_customuser_id_permission_9632a709_uniq;
       public            product_name_db_user    false    214    214            �           2606    18250 N   accounts_customuser_user_permissions accounts_customuser_user_permissions_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public.accounts_customuser_user_permissions
    ADD CONSTRAINT accounts_customuser_user_permissions_pkey PRIMARY KEY (id);
 x   ALTER TABLE ONLY public.accounts_customuser_user_permissions DROP CONSTRAINT accounts_customuser_user_permissions_pkey;
       public            product_name_db_user    false    214            �           2606    18252 4   accounts_customuser accounts_customuser_username_key 
   CONSTRAINT     s   ALTER TABLE ONLY public.accounts_customuser
    ADD CONSTRAINT accounts_customuser_username_key UNIQUE (username);
 ^   ALTER TABLE ONLY public.accounts_customuser DROP CONSTRAINT accounts_customuser_username_key;
       public            product_name_db_user    false    210            �           2606    18254 B   accounts_investmenttransaction accounts_investmenttransaction_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public.accounts_investmenttransaction
    ADD CONSTRAINT accounts_investmenttransaction_pkey PRIMARY KEY (id);
 l   ALTER TABLE ONLY public.accounts_investmenttransaction DROP CONSTRAINT accounts_investmenttransaction_pkey;
       public            product_name_db_user    false    216            �           2606    18256    auth_group auth_group_name_key 
   CONSTRAINT     Y   ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);
 H   ALTER TABLE ONLY public.auth_group DROP CONSTRAINT auth_group_name_key;
       public            product_name_db_user    false    218            �           2606    18258 R   auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);
 |   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq;
       public            product_name_db_user    false    220    220            �           2606    18260 2   auth_group_permissions auth_group_permissions_pkey 
   CONSTRAINT     p   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);
 \   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_pkey;
       public            product_name_db_user    false    220            �           2606    18262    auth_group auth_group_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.auth_group DROP CONSTRAINT auth_group_pkey;
       public            product_name_db_user    false    218            �           2606    18264 F   auth_permission auth_permission_content_type_id_codename_01ab375a_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);
 p   ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq;
       public            product_name_db_user    false    222    222            �           2606    18266 $   auth_permission auth_permission_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_pkey;
       public            product_name_db_user    false    222            �           2606    18268 5   captcha_captchastore captcha_captchastore_hashkey_key 
   CONSTRAINT     s   ALTER TABLE ONLY public.captcha_captchastore
    ADD CONSTRAINT captcha_captchastore_hashkey_key UNIQUE (hashkey);
 _   ALTER TABLE ONLY public.captcha_captchastore DROP CONSTRAINT captcha_captchastore_hashkey_key;
       public            product_name_db_user    false    224            �           2606    18270 .   captcha_captchastore captcha_captchastore_pkey 
   CONSTRAINT     l   ALTER TABLE ONLY public.captcha_captchastore
    ADD CONSTRAINT captcha_captchastore_pkey PRIMARY KEY (id);
 X   ALTER TABLE ONLY public.captcha_captchastore DROP CONSTRAINT captcha_captchastore_pkey;
       public            product_name_db_user    false    224            �           2606    18272 &   django_admin_log django_admin_log_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_pkey;
       public            product_name_db_user    false    226            �           2606    18274 E   django_content_type django_content_type_app_label_model_76bd3d3b_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);
 o   ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq;
       public            product_name_db_user    false    228    228            �           2606    18276 ,   django_content_type django_content_type_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);
 V   ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT django_content_type_pkey;
       public            product_name_db_user    false    228            �           2606    18278 (   django_migrations django_migrations_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);
 R   ALTER TABLE ONLY public.django_migrations DROP CONSTRAINT django_migrations_pkey;
       public            product_name_db_user    false    230            �           2606    18280 "   django_session django_session_pkey 
   CONSTRAINT     i   ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);
 L   ALTER TABLE ONLY public.django_session DROP CONSTRAINT django_session_pkey;
       public            product_name_db_user    false    232            �           2606    18282 ,   django_site django_site_domain_a2e37b91_uniq 
   CONSTRAINT     i   ALTER TABLE ONLY public.django_site
    ADD CONSTRAINT django_site_domain_a2e37b91_uniq UNIQUE (domain);
 V   ALTER TABLE ONLY public.django_site DROP CONSTRAINT django_site_domain_a2e37b91_uniq;
       public            product_name_db_user    false    233            �           2606    18284    django_site django_site_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.django_site
    ADD CONSTRAINT django_site_pkey PRIMARY KEY (id);
 F   ALTER TABLE ONLY public.django_site DROP CONSTRAINT django_site_pkey;
       public            product_name_db_user    false    233            �           2606    18286 "   pools_pool pools_pool_codename_key 
   CONSTRAINT     a   ALTER TABLE ONLY public.pools_pool
    ADD CONSTRAINT pools_pool_codename_key UNIQUE (codename);
 L   ALTER TABLE ONLY public.pools_pool DROP CONSTRAINT pools_pool_codename_key;
       public            product_name_db_user    false    235            �           2606    18288    pools_pool pools_pool_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.pools_pool
    ADD CONSTRAINT pools_pool_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.pools_pool DROP CONSTRAINT pools_pool_pkey;
       public            product_name_db_user    false    235            �           2606    18290 &   pools_poolinvite pools_poolinvite_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.pools_poolinvite
    ADD CONSTRAINT pools_poolinvite_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.pools_poolinvite DROP CONSTRAINT pools_poolinvite_pkey;
       public            product_name_db_user    false    237                        2606    18292 .   pools_poolinvite pools_poolinvite_username_key 
   CONSTRAINT     m   ALTER TABLE ONLY public.pools_poolinvite
    ADD CONSTRAINT pools_poolinvite_username_key UNIQUE (username);
 X   ALTER TABLE ONLY public.pools_poolinvite DROP CONSTRAINT pools_poolinvite_username_key;
       public            product_name_db_user    false    237                       2606    18294 &   pools_poolmember pools_poolmember_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.pools_poolmember
    ADD CONSTRAINT pools_poolmember_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.pools_poolmember DROP CONSTRAINT pools_poolmember_pkey;
       public            product_name_db_user    false    239                       2606    18296 <   socialaccount_socialaccount socialaccount_socialaccount_pkey 
   CONSTRAINT     z   ALTER TABLE ONLY public.socialaccount_socialaccount
    ADD CONSTRAINT socialaccount_socialaccount_pkey PRIMARY KEY (id);
 f   ALTER TABLE ONLY public.socialaccount_socialaccount DROP CONSTRAINT socialaccount_socialaccount_pkey;
       public            product_name_db_user    false    241                       2606    18298 R   socialaccount_socialaccount socialaccount_socialaccount_provider_uid_fc810c6e_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.socialaccount_socialaccount
    ADD CONSTRAINT socialaccount_socialaccount_provider_uid_fc810c6e_uniq UNIQUE (provider, uid);
 |   ALTER TABLE ONLY public.socialaccount_socialaccount DROP CONSTRAINT socialaccount_socialaccount_provider_uid_fc810c6e_uniq;
       public            product_name_db_user    false    241    241                       2606    18300 Y   socialaccount_socialapp_sites socialaccount_socialapp__socialapp_id_site_id_71a9a768_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.socialaccount_socialapp_sites
    ADD CONSTRAINT socialaccount_socialapp__socialapp_id_site_id_71a9a768_uniq UNIQUE (socialapp_id, site_id);
 �   ALTER TABLE ONLY public.socialaccount_socialapp_sites DROP CONSTRAINT socialaccount_socialapp__socialapp_id_site_id_71a9a768_uniq;
       public            product_name_db_user    false    245    245                       2606    18302 4   socialaccount_socialapp socialaccount_socialapp_pkey 
   CONSTRAINT     r   ALTER TABLE ONLY public.socialaccount_socialapp
    ADD CONSTRAINT socialaccount_socialapp_pkey PRIMARY KEY (id);
 ^   ALTER TABLE ONLY public.socialaccount_socialapp DROP CONSTRAINT socialaccount_socialapp_pkey;
       public            product_name_db_user    false    243                       2606    18304 @   socialaccount_socialapp_sites socialaccount_socialapp_sites_pkey 
   CONSTRAINT     ~   ALTER TABLE ONLY public.socialaccount_socialapp_sites
    ADD CONSTRAINT socialaccount_socialapp_sites_pkey PRIMARY KEY (id);
 j   ALTER TABLE ONLY public.socialaccount_socialapp_sites DROP CONSTRAINT socialaccount_socialapp_sites_pkey;
       public            product_name_db_user    false    245                       2606    18306 S   socialaccount_socialtoken socialaccount_socialtoken_app_id_account_id_fca4e0ac_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.socialaccount_socialtoken
    ADD CONSTRAINT socialaccount_socialtoken_app_id_account_id_fca4e0ac_uniq UNIQUE (app_id, account_id);
 }   ALTER TABLE ONLY public.socialaccount_socialtoken DROP CONSTRAINT socialaccount_socialtoken_app_id_account_id_fca4e0ac_uniq;
       public            product_name_db_user    false    247    247                       2606    18308 8   socialaccount_socialtoken socialaccount_socialtoken_pkey 
   CONSTRAINT     v   ALTER TABLE ONLY public.socialaccount_socialtoken
    ADD CONSTRAINT socialaccount_socialtoken_pkey PRIMARY KEY (id);
 b   ALTER TABLE ONLY public.socialaccount_socialtoken DROP CONSTRAINT socialaccount_socialtoken_pkey;
       public            product_name_db_user    false    247            �           1259    18309 (   account_emailaddress_email_03be32b2_like    INDEX     ~   CREATE INDEX account_emailaddress_email_03be32b2_like ON public.account_emailaddress USING btree (email varchar_pattern_ops);
 <   DROP INDEX public.account_emailaddress_email_03be32b2_like;
       public            product_name_db_user    false    200            �           1259    18310 %   account_emailaddress_user_id_2c513194    INDEX     i   CREATE INDEX account_emailaddress_user_id_2c513194 ON public.account_emailaddress USING btree (user_id);
 9   DROP INDEX public.account_emailaddress_user_id_2c513194;
       public            product_name_db_user    false    200            �           1259    18311 3   account_emailconfirmation_email_address_id_5b7f8c58    INDEX     �   CREATE INDEX account_emailconfirmation_email_address_id_5b7f8c58 ON public.account_emailconfirmation USING btree (email_address_id);
 G   DROP INDEX public.account_emailconfirmation_email_address_id_5b7f8c58;
       public            product_name_db_user    false    202            �           1259    18312 +   account_emailconfirmation_key_f43612bd_like    INDEX     �   CREATE INDEX account_emailconfirmation_key_f43612bd_like ON public.account_emailconfirmation USING btree (key varchar_pattern_ops);
 ?   DROP INDEX public.account_emailconfirmation_key_f43612bd_like;
       public            product_name_db_user    false    202            �           1259    18313 ,   accounts_balancetransaction_user_id_a58534ce    INDEX     w   CREATE INDEX accounts_balancetransaction_user_id_a58534ce ON public.accounts_balancetransaction USING btree (user_id);
 @   DROP INDEX public.accounts_balancetransaction_user_id_a58534ce;
       public            product_name_db_user    false    204            �           1259    18314 1   accounts_customuser_groups_customuser_id_bc55088e    INDEX     �   CREATE INDEX accounts_customuser_groups_customuser_id_bc55088e ON public.accounts_customuser_groups USING btree (customuser_id);
 E   DROP INDEX public.accounts_customuser_groups_customuser_id_bc55088e;
       public            product_name_db_user    false    211            �           1259    18315 ,   accounts_customuser_groups_group_id_86ba5f9e    INDEX     w   CREATE INDEX accounts_customuser_groups_group_id_86ba5f9e ON public.accounts_customuser_groups USING btree (group_id);
 @   DROP INDEX public.accounts_customuser_groups_group_id_86ba5f9e;
       public            product_name_db_user    false    211            �           1259    18316 ;   accounts_customuser_user_permissions_customuser_id_0deaefae    INDEX     �   CREATE INDEX accounts_customuser_user_permissions_customuser_id_0deaefae ON public.accounts_customuser_user_permissions USING btree (customuser_id);
 O   DROP INDEX public.accounts_customuser_user_permissions_customuser_id_0deaefae;
       public            product_name_db_user    false    214            �           1259    18317 ;   accounts_customuser_user_permissions_permission_id_aea3d0e5    INDEX     �   CREATE INDEX accounts_customuser_user_permissions_permission_id_aea3d0e5 ON public.accounts_customuser_user_permissions USING btree (permission_id);
 O   DROP INDEX public.accounts_customuser_user_permissions_permission_id_aea3d0e5;
       public            product_name_db_user    false    214            �           1259    18318 *   accounts_customuser_username_722f3555_like    INDEX     �   CREATE INDEX accounts_customuser_username_722f3555_like ON public.accounts_customuser USING btree (username varchar_pattern_ops);
 >   DROP INDEX public.accounts_customuser_username_722f3555_like;
       public            product_name_db_user    false    210            �           1259    18319 /   accounts_investmenttransaction_pool_id_e43cf3ed    INDEX     }   CREATE INDEX accounts_investmenttransaction_pool_id_e43cf3ed ON public.accounts_investmenttransaction USING btree (pool_id);
 C   DROP INDEX public.accounts_investmenttransaction_pool_id_e43cf3ed;
       public            product_name_db_user    false    216            �           1259    18320 /   accounts_investmenttransaction_user_id_8c54eaa9    INDEX     }   CREATE INDEX accounts_investmenttransaction_user_id_8c54eaa9 ON public.accounts_investmenttransaction USING btree (user_id);
 C   DROP INDEX public.accounts_investmenttransaction_user_id_8c54eaa9;
       public            product_name_db_user    false    216            �           1259    18321    auth_group_name_a6ea08ec_like    INDEX     h   CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);
 1   DROP INDEX public.auth_group_name_a6ea08ec_like;
       public            product_name_db_user    false    218            �           1259    18322 (   auth_group_permissions_group_id_b120cbf9    INDEX     o   CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);
 <   DROP INDEX public.auth_group_permissions_group_id_b120cbf9;
       public            product_name_db_user    false    220            �           1259    18323 -   auth_group_permissions_permission_id_84c5c92e    INDEX     y   CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);
 A   DROP INDEX public.auth_group_permissions_permission_id_84c5c92e;
       public            product_name_db_user    false    220            �           1259    18324 (   auth_permission_content_type_id_2f476e4b    INDEX     o   CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);
 <   DROP INDEX public.auth_permission_content_type_id_2f476e4b;
       public            product_name_db_user    false    222            �           1259    18325 *   captcha_captchastore_hashkey_cbe8d15a_like    INDEX     �   CREATE INDEX captcha_captchastore_hashkey_cbe8d15a_like ON public.captcha_captchastore USING btree (hashkey varchar_pattern_ops);
 >   DROP INDEX public.captcha_captchastore_hashkey_cbe8d15a_like;
       public            product_name_db_user    false    224            �           1259    18326 )   django_admin_log_content_type_id_c4bce8eb    INDEX     q   CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);
 =   DROP INDEX public.django_admin_log_content_type_id_c4bce8eb;
       public            product_name_db_user    false    226            �           1259    18327 !   django_admin_log_user_id_c564eba6    INDEX     a   CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);
 5   DROP INDEX public.django_admin_log_user_id_c564eba6;
       public            product_name_db_user    false    226            �           1259    18328 #   django_session_expire_date_a5c62663    INDEX     e   CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);
 7   DROP INDEX public.django_session_expire_date_a5c62663;
       public            product_name_db_user    false    232            �           1259    18329 (   django_session_session_key_c0390e0f_like    INDEX     ~   CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);
 <   DROP INDEX public.django_session_session_key_c0390e0f_like;
       public            product_name_db_user    false    232            �           1259    18330     django_site_domain_a2e37b91_like    INDEX     n   CREATE INDEX django_site_domain_a2e37b91_like ON public.django_site USING btree (domain varchar_pattern_ops);
 4   DROP INDEX public.django_site_domain_a2e37b91_like;
       public            product_name_db_user    false    233            �           1259    18331 !   pools_pool_codename_c8c6c5b6_like    INDEX     p   CREATE INDEX pools_pool_codename_c8c6c5b6_like ON public.pools_pool USING btree (codename varchar_pattern_ops);
 5   DROP INDEX public.pools_pool_codename_c8c6c5b6_like;
       public            product_name_db_user    false    235            �           1259    18332    pools_pool_master_id_15362b88    INDEX     Y   CREATE INDEX pools_pool_master_id_15362b88 ON public.pools_pool USING btree (master_id);
 1   DROP INDEX public.pools_pool_master_id_15362b88;
       public            product_name_db_user    false    235            �           1259    18333 !   pools_poolinvite_pool_id_1bbd8563    INDEX     a   CREATE INDEX pools_poolinvite_pool_id_1bbd8563 ON public.pools_poolinvite USING btree (pool_id);
 5   DROP INDEX public.pools_poolinvite_pool_id_1bbd8563;
       public            product_name_db_user    false    237            �           1259    18334 '   pools_poolinvite_username_7bb9547d_like    INDEX     |   CREATE INDEX pools_poolinvite_username_7bb9547d_like ON public.pools_poolinvite USING btree (username varchar_pattern_ops);
 ;   DROP INDEX public.pools_poolinvite_username_7bb9547d_like;
       public            product_name_db_user    false    237                       1259    18335 !   pools_poolmember_pool_id_1392167e    INDEX     a   CREATE INDEX pools_poolmember_pool_id_1392167e ON public.pools_poolmember USING btree (pool_id);
 5   DROP INDEX public.pools_poolmember_pool_id_1392167e;
       public            product_name_db_user    false    239                       1259    18336 !   pools_poolmember_user_id_6a7c6bb8    INDEX     a   CREATE INDEX pools_poolmember_user_id_6a7c6bb8 ON public.pools_poolmember USING btree (user_id);
 5   DROP INDEX public.pools_poolmember_user_id_6a7c6bb8;
       public            product_name_db_user    false    239            	           1259    18337 ,   socialaccount_socialaccount_user_id_8146e70c    INDEX     w   CREATE INDEX socialaccount_socialaccount_user_id_8146e70c ON public.socialaccount_socialaccount USING btree (user_id);
 @   DROP INDEX public.socialaccount_socialaccount_user_id_8146e70c;
       public            product_name_db_user    false    241                       1259    18338 .   socialaccount_socialapp_sites_site_id_2579dee5    INDEX     {   CREATE INDEX socialaccount_socialapp_sites_site_id_2579dee5 ON public.socialaccount_socialapp_sites USING btree (site_id);
 B   DROP INDEX public.socialaccount_socialapp_sites_site_id_2579dee5;
       public            product_name_db_user    false    245                       1259    18339 3   socialaccount_socialapp_sites_socialapp_id_97fb6e7d    INDEX     �   CREATE INDEX socialaccount_socialapp_sites_socialapp_id_97fb6e7d ON public.socialaccount_socialapp_sites USING btree (socialapp_id);
 G   DROP INDEX public.socialaccount_socialapp_sites_socialapp_id_97fb6e7d;
       public            product_name_db_user    false    245                       1259    18340 -   socialaccount_socialtoken_account_id_951f210e    INDEX     y   CREATE INDEX socialaccount_socialtoken_account_id_951f210e ON public.socialaccount_socialtoken USING btree (account_id);
 A   DROP INDEX public.socialaccount_socialtoken_account_id_951f210e;
       public            product_name_db_user    false    247                       1259    18341 )   socialaccount_socialtoken_app_id_636a42d7    INDEX     q   CREATE INDEX socialaccount_socialtoken_app_id_636a42d7 ON public.socialaccount_socialtoken USING btree (app_id);
 =   DROP INDEX public.socialaccount_socialtoken_app_id_636a42d7;
       public            product_name_db_user    false    247                       2606    18342 T   account_emailaddress account_emailaddress_user_id_2c513194_fk_accounts_customuser_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.account_emailaddress
    ADD CONSTRAINT account_emailaddress_user_id_2c513194_fk_accounts_customuser_id FOREIGN KEY (user_id) REFERENCES public.accounts_customuser(id) DEFERRABLE INITIALLY DEFERRED;
 ~   ALTER TABLE ONLY public.account_emailaddress DROP CONSTRAINT account_emailaddress_user_id_2c513194_fk_accounts_customuser_id;
       public          product_name_db_user    false    3001    200    210                       2606    18347 U   account_emailconfirmation account_emailconfirm_email_address_id_5b7f8c58_fk_account_e    FK CONSTRAINT     �   ALTER TABLE ONLY public.account_emailconfirmation
    ADD CONSTRAINT account_emailconfirm_email_address_id_5b7f8c58_fk_account_e FOREIGN KEY (email_address_id) REFERENCES public.account_emailaddress(id) DEFERRABLE INITIALLY DEFERRED;
    ALTER TABLE ONLY public.account_emailconfirmation DROP CONSTRAINT account_emailconfirm_email_address_id_5b7f8c58_fk_account_e;
       public          product_name_db_user    false    202    2983    200                       2606    18352 N   accounts_balancetransaction accounts_balancetran_user_id_a58534ce_fk_accounts_    FK CONSTRAINT     �   ALTER TABLE ONLY public.accounts_balancetransaction
    ADD CONSTRAINT accounts_balancetran_user_id_a58534ce_fk_accounts_ FOREIGN KEY (user_id) REFERENCES public.accounts_customuser(id) DEFERRABLE INITIALLY DEFERRED;
 x   ALTER TABLE ONLY public.accounts_balancetransaction DROP CONSTRAINT accounts_balancetran_user_id_a58534ce_fk_accounts_;
       public          product_name_db_user    false    204    3001    210                       2606    18357 J   accounts_billingaddress accounts_billingaddr_user_id_14c3fa39_fk_accounts_    FK CONSTRAINT     �   ALTER TABLE ONLY public.accounts_billingaddress
    ADD CONSTRAINT accounts_billingaddr_user_id_14c3fa39_fk_accounts_ FOREIGN KEY (user_id) REFERENCES public.accounts_customuser(id) DEFERRABLE INITIALLY DEFERRED;
 t   ALTER TABLE ONLY public.accounts_billingaddress DROP CONSTRAINT accounts_billingaddr_user_id_14c3fa39_fk_accounts_;
       public          product_name_db_user    false    210    3001    206                       2606    18362 ]   accounts_customuser_user_permissions accounts_customuser__customuser_id_0deaefae_fk_accounts_    FK CONSTRAINT     �   ALTER TABLE ONLY public.accounts_customuser_user_permissions
    ADD CONSTRAINT accounts_customuser__customuser_id_0deaefae_fk_accounts_ FOREIGN KEY (customuser_id) REFERENCES public.accounts_customuser(id) DEFERRABLE INITIALLY DEFERRED;
 �   ALTER TABLE ONLY public.accounts_customuser_user_permissions DROP CONSTRAINT accounts_customuser__customuser_id_0deaefae_fk_accounts_;
       public          product_name_db_user    false    214    3001    210                       2606    18367 S   accounts_customuser_groups accounts_customuser__customuser_id_bc55088e_fk_accounts_    FK CONSTRAINT     �   ALTER TABLE ONLY public.accounts_customuser_groups
    ADD CONSTRAINT accounts_customuser__customuser_id_bc55088e_fk_accounts_ FOREIGN KEY (customuser_id) REFERENCES public.accounts_customuser(id) DEFERRABLE INITIALLY DEFERRED;
 }   ALTER TABLE ONLY public.accounts_customuser_groups DROP CONSTRAINT accounts_customuser__customuser_id_bc55088e_fk_accounts_;
       public          product_name_db_user    false    211    3001    210                       2606    18372 ]   accounts_customuser_user_permissions accounts_customuser__permission_id_aea3d0e5_fk_auth_perm    FK CONSTRAINT     �   ALTER TABLE ONLY public.accounts_customuser_user_permissions
    ADD CONSTRAINT accounts_customuser__permission_id_aea3d0e5_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;
 �   ALTER TABLE ONLY public.accounts_customuser_user_permissions DROP CONSTRAINT accounts_customuser__permission_id_aea3d0e5_fk_auth_perm;
       public          product_name_db_user    false    3036    214    222                       2606    18377 X   accounts_customuser_groups accounts_customuser_groups_group_id_86ba5f9e_fk_auth_group_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.accounts_customuser_groups
    ADD CONSTRAINT accounts_customuser_groups_group_id_86ba5f9e_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;
 �   ALTER TABLE ONLY public.accounts_customuser_groups DROP CONSTRAINT accounts_customuser_groups_group_id_86ba5f9e_fk_auth_group_id;
       public          product_name_db_user    false    3025    218    211                        2606    18382 Q   accounts_investmenttransaction accounts_investmentt_pool_id_e43cf3ed_fk_pools_poo    FK CONSTRAINT     �   ALTER TABLE ONLY public.accounts_investmenttransaction
    ADD CONSTRAINT accounts_investmentt_pool_id_e43cf3ed_fk_pools_poo FOREIGN KEY (pool_id) REFERENCES public.pools_pool(id) DEFERRABLE INITIALLY DEFERRED;
 {   ALTER TABLE ONLY public.accounts_investmenttransaction DROP CONSTRAINT accounts_investmentt_pool_id_e43cf3ed_fk_pools_poo;
       public          product_name_db_user    false    235    3066    216            !           2606    18387 Q   accounts_investmenttransaction accounts_investmentt_user_id_8c54eaa9_fk_accounts_    FK CONSTRAINT     �   ALTER TABLE ONLY public.accounts_investmenttransaction
    ADD CONSTRAINT accounts_investmentt_user_id_8c54eaa9_fk_accounts_ FOREIGN KEY (user_id) REFERENCES public.accounts_customuser(id) DEFERRABLE INITIALLY DEFERRED;
 {   ALTER TABLE ONLY public.accounts_investmenttransaction DROP CONSTRAINT accounts_investmentt_user_id_8c54eaa9_fk_accounts_;
       public          product_name_db_user    false    210    3001    216            "           2606    18392 O   auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;
 y   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm;
       public          product_name_db_user    false    220    3036    222            #           2606    18397 P   auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;
 z   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id;
       public          product_name_db_user    false    220    218    3025            $           2606    18402 E   auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;
 o   ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co;
       public          product_name_db_user    false    228    222    3049            %           2606    18407 G   django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co    FK CONSTRAINT     �   ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;
 q   ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co;
       public          product_name_db_user    false    228    3049    226            &           2606    18412 L   django_admin_log django_admin_log_user_id_c564eba6_fk_accounts_customuser_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_accounts_customuser_id FOREIGN KEY (user_id) REFERENCES public.accounts_customuser(id) DEFERRABLE INITIALLY DEFERRED;
 v   ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_user_id_c564eba6_fk_accounts_customuser_id;
       public          product_name_db_user    false    3001    210    226            '           2606    18417 B   pools_pool pools_pool_master_id_15362b88_fk_accounts_customuser_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.pools_pool
    ADD CONSTRAINT pools_pool_master_id_15362b88_fk_accounts_customuser_id FOREIGN KEY (master_id) REFERENCES public.accounts_customuser(id) DEFERRABLE INITIALLY DEFERRED;
 l   ALTER TABLE ONLY public.pools_pool DROP CONSTRAINT pools_pool_master_id_15362b88_fk_accounts_customuser_id;
       public          product_name_db_user    false    210    235    3001            (           2606    18422 C   pools_poolinvite pools_poolinvite_pool_id_1bbd8563_fk_pools_pool_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.pools_poolinvite
    ADD CONSTRAINT pools_poolinvite_pool_id_1bbd8563_fk_pools_pool_id FOREIGN KEY (pool_id) REFERENCES public.pools_pool(id) DEFERRABLE INITIALLY DEFERRED;
 m   ALTER TABLE ONLY public.pools_poolinvite DROP CONSTRAINT pools_poolinvite_pool_id_1bbd8563_fk_pools_pool_id;
       public          product_name_db_user    false    235    3066    237            )           2606    18427 C   pools_poolmember pools_poolmember_pool_id_1392167e_fk_pools_pool_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.pools_poolmember
    ADD CONSTRAINT pools_poolmember_pool_id_1392167e_fk_pools_pool_id FOREIGN KEY (pool_id) REFERENCES public.pools_pool(id) DEFERRABLE INITIALLY DEFERRED;
 m   ALTER TABLE ONLY public.pools_poolmember DROP CONSTRAINT pools_poolmember_pool_id_1392167e_fk_pools_pool_id;
       public          product_name_db_user    false    235    239    3066            *           2606    18432 L   pools_poolmember pools_poolmember_user_id_6a7c6bb8_fk_accounts_customuser_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.pools_poolmember
    ADD CONSTRAINT pools_poolmember_user_id_6a7c6bb8_fk_accounts_customuser_id FOREIGN KEY (user_id) REFERENCES public.accounts_customuser(id) DEFERRABLE INITIALLY DEFERRED;
 v   ALTER TABLE ONLY public.pools_poolmember DROP CONSTRAINT pools_poolmember_user_id_6a7c6bb8_fk_accounts_customuser_id;
       public          product_name_db_user    false    239    210    3001            .           2606    18437 O   socialaccount_socialtoken socialaccount_social_account_id_951f210e_fk_socialacc    FK CONSTRAINT     �   ALTER TABLE ONLY public.socialaccount_socialtoken
    ADD CONSTRAINT socialaccount_social_account_id_951f210e_fk_socialacc FOREIGN KEY (account_id) REFERENCES public.socialaccount_socialaccount(id) DEFERRABLE INITIALLY DEFERRED;
 y   ALTER TABLE ONLY public.socialaccount_socialtoken DROP CONSTRAINT socialaccount_social_account_id_951f210e_fk_socialacc;
       public          product_name_db_user    false    241    3078    247            /           2606    18442 K   socialaccount_socialtoken socialaccount_social_app_id_636a42d7_fk_socialacc    FK CONSTRAINT     �   ALTER TABLE ONLY public.socialaccount_socialtoken
    ADD CONSTRAINT socialaccount_social_app_id_636a42d7_fk_socialacc FOREIGN KEY (app_id) REFERENCES public.socialaccount_socialapp(id) DEFERRABLE INITIALLY DEFERRED;
 u   ALTER TABLE ONLY public.socialaccount_socialtoken DROP CONSTRAINT socialaccount_social_app_id_636a42d7_fk_socialacc;
       public          product_name_db_user    false    3083    247    243            ,           2606    18447 P   socialaccount_socialapp_sites socialaccount_social_site_id_2579dee5_fk_django_si    FK CONSTRAINT     �   ALTER TABLE ONLY public.socialaccount_socialapp_sites
    ADD CONSTRAINT socialaccount_social_site_id_2579dee5_fk_django_si FOREIGN KEY (site_id) REFERENCES public.django_site(id) DEFERRABLE INITIALLY DEFERRED;
 z   ALTER TABLE ONLY public.socialaccount_socialapp_sites DROP CONSTRAINT socialaccount_social_site_id_2579dee5_fk_django_si;
       public          product_name_db_user    false    233    3060    245            -           2606    18452 U   socialaccount_socialapp_sites socialaccount_social_socialapp_id_97fb6e7d_fk_socialacc    FK CONSTRAINT     �   ALTER TABLE ONLY public.socialaccount_socialapp_sites
    ADD CONSTRAINT socialaccount_social_socialapp_id_97fb6e7d_fk_socialacc FOREIGN KEY (socialapp_id) REFERENCES public.socialaccount_socialapp(id) DEFERRABLE INITIALLY DEFERRED;
    ALTER TABLE ONLY public.socialaccount_socialapp_sites DROP CONSTRAINT socialaccount_social_socialapp_id_97fb6e7d_fk_socialacc;
       public          product_name_db_user    false    243    245    3083            +           2606    18457 N   socialaccount_socialaccount socialaccount_social_user_id_8146e70c_fk_accounts_    FK CONSTRAINT     �   ALTER TABLE ONLY public.socialaccount_socialaccount
    ADD CONSTRAINT socialaccount_social_user_id_8146e70c_fk_accounts_ FOREIGN KEY (user_id) REFERENCES public.accounts_customuser(id) DEFERRABLE INITIALLY DEFERRED;
 x   ALTER TABLE ONLY public.socialaccount_socialaccount DROP CONSTRAINT socialaccount_social_user_id_8146e70c_fk_accounts_;
       public          product_name_db_user    false    3001    241    210            �      x������ � �      �      x������ � �      �   2   x�3�t�45 =�N##C]#]C++Cm��1W� ��      �      x������ � �      �   N   x�eʱ�0�OA�b��v����@E$��<߮�^��6�N����̨�X��k�z�l�\3�ӆA��ଷ�����      �   �  x�}�[s�0 �g�+��[�4	�$��̂�R/T��tP��"^��/v��jm�停L��I��xD�m;��jJ �ZDR/baב��OĲ,,���0P���_ꖝȃ�|7��H��)m�� �� =r���@�P�E�"> ���!'�6���y�8^��0�'���ʯ���x���4����E�O���=���m��5ʲ��v�����}x]mǞ5L�2���w������FH�Sz��'�C�3H b������ҦuDx� ��͌��7��Sf���j�[��*R�FC�J#�֠lW,ck}lZQ�l�z��,���T�E9Ku�����e���bPt��ɵFu$�J��/5� �W1��4�:r���qdM���0UYR���P�oIe�Y+H���r��Q��DNopbx~6fme;��x1��w�x�"�#q�0�8����A�zώ�կ4�m̀�Ig�����wt�+���,OI<�Z�W��jsj;�/��n�{���OKM�u�xJ1�Ƽ�H�I���3�!�Kz��&��٬�_j�/j���]�檣�"Q��sCw���˪H�PI-%�3{�dLm�?�U��J���7��1�1# ^ֆ���I�YȪ�p����n�i>ϋ�`�$ś�3�������Y�/��j>�m�m�z�M4i�����/�����~��G      �      x�3�4�4�2�4�4�bN#�=... !��      �      x������ � �      �      x������ � �      �   %   x�3��M�KLO-�2��K�c����$ #F��� ��	W      �   �   x��ɑE1�V0SF`�s���1�;u��+�!(�C:m�Ѕcl���1
W�y��q#�l�E�����">����Q�΃x���`�	RT��,�Sw����O����J��Փ�<H��f#�L�Փmj>������O���oD*�      �   P  x�}�[��0E��U��T�g�w����8*�
�Ie�1��$�ҽ̹�-<F}�����L���a��)���Ow�:I��V�|��?mgW)�%� �j�_!�
$*v���}�,�8�Ш�K'�HǴ�Zd�;!
%02�c�|��kR µ67�ȅÙ�qP�J �����ս�d�7Y����69ǉ�H%�g��(�%�Fj��j�^�� �6wK��e�H2���Fh$�]b��]�*=��ԩ��  +l�c��qh�J�}�v���TPÒN�z���$b������c=PK�#�w?�v��u{�w���:�sDFFz�1Q�層7��EN
(}�˖�ik�N�f|�z�uE��L촃!,����	�Iz؎;8����b�����ݸbQ�Ig���!�l��Yi�a�)��HO�̛$�:���eX(�<}���"�����,�9���,'i:4��:�dY��*㿅X����x8�Ð1�0煅����z!�	�Z쬌�F6/�.�4�@�tb�]@d:�˃�s1������&�\K��%翟�b]��}�E�3���v�tfg[��IϬ��?ڮk��>؍��b9��B��OH��8��t�V�pb�"M��p�r&ë��s2��2�~r�pu]�!pnd�!�3��ˎF��F��s?&IM�v�����Ɋ����@]���b&\?#_<DL��`�����q�x	�I2�c��?^l׺3$��?��#(��ln��?�C7=���)��!|EWy�´�(ȋ���^����w� �$�{���3��ľ�������8�b�3b��o1�wb������	@$      �      x������ � �      �   J   x�-�K
� ���)�mQ򁪹�����B�{7F��RX����][=�0���������F����!���d1      �   �   x�mPKn!]ۇ����n�NP#l"����F!R6��l�s�	/��<q[��J�"�����p�x �I�T��dl�B�C��@�6Y�x�פ@��`�4^����K���WvކM�֡�}�sFc>Rʿ��L�lVw��+ʅ��Q�b�a�
4�|k�ɑ�ĺuFsh�O˶�9��R͑j�Qam#�_�O���c�2s����]���n�ZH?��"����5      �   Q  x���M��0����uˮ�}��,�8�5�icZ��ǘ�0
lؠ�Q��UASU~hc_B�v�����>������(E�߄��!bL!E����q�n�U׶=�˺ZH��fE�}��J�jT��m�m����r�R�J�l������ݚƮ�H�˖�Ro�g �I�fhSGtgC����6q�3&�*����;j��c��L���aS2c�3>r=�K�Ye(%X�tf�%�6}Ե?���P�[�	R���0SD����<�<*=��"��R�!�^ʏ���Dzm�GmC�A7���ٮwƁ0�SFٌS��l��Q01�gR���.'��%(J�s�C�#�tN/�z�EVw�_o�H��GI"13�<SXvurag[�PS���U���QC �OҐ�	%W�����c��텔���}j`kJ[�=B.!�f��bZE�'��1n���j�js��Ż�M��x"����L����C��2���}d�*�d�9�E����ҭ�r�y����i�к�a�h*E	N�ʢ�U��ο�L���U�Z�����"hk'JJ	�]���^c0:�Azؓꨏ���,J��*��y8�˪�      �   �  x�E�I��P  �uy��w0b��(�"""�¨"��p�Nu:�w�W�8H].]��+��|�f2/x��_�D�n�vk�/��$��j�9\�4�T��Qw!���Π�kؘ��:����N�dF.�i_'�6��}�ٴ�e���Ąa�)qSQ�o�3m�i�{�Z�7� Ձk�b�>>��c��B�^�����С,w�=}|�}��:�x�s]��L�q_>"���BڐSzȊ�B!}`�R�"f�B A
 
�o�y��!�� ��� +����3:D\Wq��!(���</ˋm���Z��=O��Ί^��=��Nw1 ��k��)*���2��U*�(YQu���`˶�$���y���{�XŬ'�?Iȥ���v;��Od'���-�=�aT;�MA"&�&1䨷=�f��D4�"�>��^�̪����&�g��v8c�m@)o@��� 3}>]��MU7wC牂b��F�z�I�����7�<�x�1����^�V�?���      �      x�3�L�H�-�I�K��Efs��qqq �<	�      �   S   x�3䴴07202402���M,.I-R�T����42�44 =N�]#]C+CS+=cSm�l��1W� ��P      �   7   x�3䴴0� N##C]#]C+CS+S=S3KC3m�4NC�=... �	x      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �     