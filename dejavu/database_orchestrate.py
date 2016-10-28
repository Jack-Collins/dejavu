from __future__ import absolute_import
from itertools import izip_longest
import Queue

from porc import Client

from dejavu.database import Database


class OrchestrateDatabase(Database):
    type = "orchestrate"

    # tables
    FINGERPRINTS_TABLENAME = "fingerprints"
    SONGS_TABLENAME = "songs"

    # fields
    FIELD_FINGERPRINTED = "fingerprinted"

    # creates
    CREATE_FINGERPRINTS_TABLE = """
        CREATE TABLE IF NOT EXISTS `%s` (
             `%s` binary(10) not null,
             `%s` mediumint unsigned not null,
             `%s` int unsigned not null,
         INDEX (%s),
         UNIQUE KEY `unique_constraint` (%s, %s, %s),
         FOREIGN KEY (%s) REFERENCES %s(%s) ON DELETE CASCADE
    ) ENGINE=INNODB;""" % (
        FINGERPRINTS_TABLENAME, Database.FIELD_HASH,
        Database.FIELD_SONG_ID, Database.FIELD_OFFSET, Database.FIELD_HASH,
        Database.FIELD_SONG_ID, Database.FIELD_OFFSET, Database.FIELD_HASH,
        Database.FIELD_SONG_ID, SONGS_TABLENAME, Database.FIELD_SONG_ID
    )

    CREATE_SONGS_TABLE = """
        CREATE TABLE IF NOT EXISTS `%s` (
            `%s` mediumint unsigned not null auto_increment,
            `%s` varchar(250) not null,
            `%s` tinyint default 0,
            `%s` binary(20) not null,
        PRIMARY KEY (`%s`),
        UNIQUE KEY `%s` (`%s`)
    ) ENGINE=INNODB;""" % (
        SONGS_TABLENAME, Database.FIELD_SONG_ID, Database.FIELD_SONGNAME, FIELD_FINGERPRINTED,
        Database.FIELD_FILE_SHA1,
        Database.FIELD_SONG_ID, Database.FIELD_SONG_ID, Database.FIELD_SONG_ID,
    )

    # inserts (ignores duplicates)
    INSERT_FINGERPRINT = """
        INSERT IGNORE INTO %s (%s, %s, %s) values
            (UNHEX(%%s), %%s, %%s);
    """ % (FINGERPRINTS_TABLENAME, Database.FIELD_HASH, Database.FIELD_SONG_ID, Database.FIELD_OFFSET)

    INSERT_SONG = "INSERT INTO %s (%s, %s) values (%%s, UNHEX(%%s));" % (
        SONGS_TABLENAME, Database.FIELD_SONGNAME, Database.FIELD_FILE_SHA1)

    # selects
    SELECT = """
        SELECT %s, %s FROM %s WHERE %s = UNHEX(%%s);
    """ % (Database.FIELD_SONG_ID, Database.FIELD_OFFSET, FINGERPRINTS_TABLENAME, Database.FIELD_HASH)

    SELECT_MULTIPLE = """
        SELECT HEX(%s), %s, %s FROM %s WHERE %s IN (%%s);
    """ % (Database.FIELD_HASH, Database.FIELD_SONG_ID, Database.FIELD_OFFSET,
           FINGERPRINTS_TABLENAME, Database.FIELD_HASH)

    SELECT_ALL = """
        SELECT %s, %s FROM %s;
    """ % (Database.FIELD_SONG_ID, Database.FIELD_OFFSET, FINGERPRINTS_TABLENAME)

    SELECT_SONG = """
        SELECT %s, HEX(%s) as %s FROM %s WHERE %s = %%s;
    """ % (Database.FIELD_SONGNAME, Database.FIELD_FILE_SHA1, Database.FIELD_FILE_SHA1, SONGS_TABLENAME, Database.FIELD_SONG_ID)

    SELECT_NUM_FINGERPRINTS = """
        SELECT COUNT(*) as n FROM %s
    """ % (FINGERPRINTS_TABLENAME)

    SELECT_UNIQUE_SONG_IDS = """
        SELECT COUNT(DISTINCT %s) as n FROM %s WHERE %s = 1;
    """ % (Database.FIELD_SONG_ID, SONGS_TABLENAME, FIELD_FINGERPRINTED)

    SELECT_SONGS = """
        SELECT %s, %s, HEX(%s) as %s FROM %s WHERE %s = 1;
    """ % (Database.FIELD_SONG_ID, Database.FIELD_SONGNAME, Database.FIELD_FILE_SHA1, Database.FIELD_FILE_SHA1,
           SONGS_TABLENAME, FIELD_FINGERPRINTED)

    # drops
    DROP_FINGERPRINTS = "DROP TABLE IF EXISTS %s;" % FINGERPRINTS_TABLENAME
    DROP_SONGS = "DROP TABLE IF EXISTS %s;" % SONGS_TABLENAME

    # update
    UPDATE_SONG_FINGERPRINTED = """
        UPDATE %s SET %s = 1 WHERE %s = %%s
    """ % (SONGS_TABLENAME, FIELD_FINGERPRINTED, Database.FIELD_SONG_ID)

    # delete
    DELETE_UNFINGERPRINTED = """
        DELETE FROM %s WHERE %s = 0;
    """ % (SONGS_TABLENAME, FIELD_FINGERPRINTED)

    def __init__(self, **options):
        super(OrchestrateDatabase, self).__init__()
        self.cursor = cursor_factory(**options)
        self._options = options

    def after_fork(self):
        # Clear the cursor cache, we don't want any stale connections from
        # the previous process.
        Cursor.clear_cache()

    def setup(self):
        """
        Creates any non-existing tables required for dejavu to function.

        This also removes all songs that have been added but have no
        fingerprints associated with them.
        """
        with self.cursor() as cur:
            cur.execute(self.CREATE_SONGS_TABLE)
            cur.execute(self.CREATE_FINGERPRINTS_TABLE)
            cur.execute(self.DELETE_UNFINGERPRINTED)

    def empty(self):
        """
        Drops tables created by dejavu and then creates them again
        by calling `SQLDatabase.setup`.

        .. warning:
            This will result in a loss of data
        """

        self.setup()

    def delete_unfingerprinted_songs(self):
        """
        Removes all songs that have no fingerprints associated with them.
        """

    def get_num_songs(self):
        """
        Returns number of songs the database has fingerprinted.
        """
       return 0

    def get_num_fingerprints(self):
        """
        Returns number of fingerprints the database has fingerprinted.
        """
        return 0

    def set_song_fingerprinted(self, sid):
        """
        Set the fingerprinted flag to TRUE (1) once a song has been completely
        fingerprinted in the database.
        """
   
    def get_songs(self):
        """
        Return songs that have the fingerprinted flag set TRUE (1).
        """
       

    def get_song_by_id(self, sid):
        """
        Returns song by its ID.
        """
        
    def insert(self, hash, sid, offset):
        """
        Insert a (sha1, song_id, offset) row into database.
        """
      

    def insert_song(self, songname, file_hash):
        """
        Inserts song in the database and returns the ID of the inserted record.
        """
        

    def query(self, hash):
        """
        Return all tuples associated with hash.

        If hash is None, returns all entries in the
        database (be careful with that one!).
        """
      

    def get_iterable_kv_pairs(self):
        """
        Returns all tuples in database.
        """
        

    def insert_hashes(self, sid, hashes):
        """
        Insert series of hash => song_id, offset
        values into the database.
        """
       

    def return_matches(self, hashes):
        """
        Return the (song_id, offset_diff) tuples associated with
        a list of (sha1, sample_offset) values.
        """
       

    def __getstate__(self):
        return (self._options,)

    def __setstate__(self, state):
        self._options, = state
        self.cursor = cursor_factory(**self._options)


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return (filter(None, values) for values
            in izip_longest(fillvalue=fillvalue, *args))


def cursor_factory(**factory_options):
    def cursor(**options):
        options.update(factory_options)
        return Cursor(**options)
    return cursor


class Cursor(object):
    """
    Establishes a connection to the database and returns an open cursor.


    ```python
    # Use as context manager
    with Cursor() as cur:
        cur.execute(query)
    ```
    """
    _cache = Queue.Queue(maxsize=5)

    def __init__(self, cursor_type=mysql.cursors.Cursor, **options):
        super(Cursor, self).__init__()

        try:
            conn = self._cache.get_nowait()
        except Queue.Empty:
            conn = mysql.connect(**options)
        else:
            # Ping the connection before using it from the cache.
            conn.ping(True)

        self.conn = conn
        self.conn.autocommit(False)
        self.cursor_type = cursor_type

    @classmethod
    def clear_cache(cls):
        cls._cache = Queue.Queue(maxsize=5)

    def __enter__(self):
        self.cursor = self.conn.cursor(self.cursor_type)
        return self.cursor

    def __exit__(self, extype, exvalue, traceback):
        # if we had a MySQL related error we try to rollback the cursor.
        if extype is mysql.MySQLError:
            self.cursor.rollback()

        self.cursor.close()
        self.conn.commit()

        # Put it back on the queue
        try:
            self._cache.put_nowait(self.conn)
        except Queue.Full:
            self.conn.close()
