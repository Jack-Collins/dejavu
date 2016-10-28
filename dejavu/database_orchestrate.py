
from porc import Client
client = new Client("7e23e64c-f1a8-4072-90c7-6c00c804c0e5")

class OrchestrateDatabase(Database):
    type = "orchestrate"

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
        client.put(FINGERPRINTS_TABLENAME, hash, {
          "song_id": sid, 
          "offset": offset
        })

    def insert_song(self, songname, file_hash):
        """
        Inserts song in the database and returns the ID of the inserted record.
        """
         client.put(SONGS_TABLENAME, file_hash, {
          "songname": songname
        })

    
    def insert_hashes(self, sid, hashes):
        """
        Insert series of hash => song_id, offset
        values into the database.
        """
       


