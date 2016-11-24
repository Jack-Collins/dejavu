import decoder
import gzip
import shutil
import os
def compress_directory(path, extensions):
	for filename, _ in decoder.find_files(path, extensions):
		#don't compress already compressed files
		if os.path.isfile(filename + '.gz'):
			print "%s already compressed" % filename			
		else:
			print 'compressing %s' % filename
			with open(filename) as f_in:
				with gzip.open(filename + '.gz', 'wb') as f_out:
					shutil.copyfileobj(f_in, f_out)
		print "the Kolgomorov complexity approximation is " + str(float(os.path.getsize(filename + '.gz')) / float(os.path.getsize(filename)))			
			

compress_directory('../mp3', ['.mp3'])
