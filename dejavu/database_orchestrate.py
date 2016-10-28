
from porc import Client

from porc import Patch

from dejavu.database import Database

client = Client("7e23e64c-f1a8-4072-90c7-6c00c804c0e5")
# tables
FINGERPRINTS_TABLENAME = "fingerprints"
SONGS_TABLENAME = "songs"

# fields
FIELD_FINGERPRINTED = "fingerprinted"
    
class OrchestrateDatabase(Database):
    type = "orchestrate"

    def __init__(self, **options):
            super(OrchestrateDatabase, self).__init__()
            self._options = options
        
    def insert(self, hash, sid, offset):
        """
        Insert a (sha1, song_id, offset) row into database.
        """
       

    def insert_song(self, songname, file_hash):
        """
        Inserts song in the database and returns the ID of the inserted record.
        """
        client.post(SONGS_TABLENAME, {
          "songname": songname, 
          "file_hash" : file_hash
        })

    
    def insert_hashes(self, sid, hashes):
        """
        Insert series of hash => song_id, offset
        values into the database.
        """
        values = []
        for hash, offset in hashes:
                 client.put(FINGERPRINTS_TABLENAME, hash, {
                     "song_id": sid, 
                     "offset": offset
                  })

                
    def set_song_fingerprinted(self, sid):
        """
        Set the fingerprinted flag to TRUE (1) once a song has been completely
        fingerprinted in the database.
        """
        patch = Patch()
        patch.add("fingerprinted", True)

        client.patch(SONGS_TABLENAME, sid, patch)



    def setup(self):
        """
        Creates any non-existing tables required for dejavu to function.
        This also removes all songs that have been added but have no
        fingerprints associated with them.
        """

    def empty(self):
        """
        Called when the database should be cleared of all data.
        """
        pass

    def delete_unfingerprinted_songs(self):
        """
        Called to remove any song entries that do not have any fingerprints
        associated with them.
        """
        pass
    
    def get_num_songs(self):
        """
        Returns the amount of songs in the database.
        """
        pass

    def get_num_fingerprints(self):
        """
        Returns the number of fingerprints in the database.
        """
        pass

    def get_songs(self):
        """
        Returns all fully fingerprinted songs in the database.
        """
        pages = client.search(SONGS_TABLENAME, 'fingerprinted:True')
        # get all items in the collection
        items = pages.all()
        return items
    
    def get_song_by_id(self, sid):
        """
        Return a song by its identifier
        sid: Song identifier
        """
        pass
    
    def insert(self, hash, sid, offset):
        """
        Inserts a single fingerprint into the database.
          hash: Part of a sha1 hash, in hexadecimal format
           sid: Song identifier this fingerprint is off
        offset: The offset this hash is from
        """
        pass

    def query(self, hash):
        """
        Returns all matching fingerprint entries associated with
        the given hash as parameter.
        hash: Part of a sha1 hash, in hexadecimal format
        """
        pass
    
    def get_iterable_kv_pairs(self):
        """
        Returns all fingerprints in the database.
        """
        pass
    
    def return_matches(self, hashes):
        """
        Searches the database for pairs of (hash, offset) values.
        hashes: A sequence of tuples in the format (hash, offset)
        -   hash: Part of a sha1 hash, in hexadecimal format
        - offset: Offset this hash was created from/at.
        Returns a sequence of (sid, offset_difference) tuples.
                      sid: Song identifier
        offset_difference: (offset - database_offset)
        """
        pass



