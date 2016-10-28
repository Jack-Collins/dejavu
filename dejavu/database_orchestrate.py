
from porc import Client
from porc import Patch

from dejavu.database import Database

class OrchestrateDatabase(Database):
    type = "orchestrate"

    client = new Client("7e23e64c-f1a8-4072-90c7-6c00c804c0e5")
    
     # tables
        FINGERPRINTS_TABLENAME = "fingerprints"
        SONGS_TABLENAME = "songs"

     # fields
        FIELD_FINGERPRINTED = "fingerprinted"

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
