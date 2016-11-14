import os
import os.path
import hashlib
import time

__author__ = 'Giovanni Moretti'


def create_file_signature(filename):
    """CreateFileHash (file): create a signature for the specified file
       Returns a tuple containing three values:
          (the pathname of the file, its last modification time, SHA1 hash)
    """

    f = None
    signature = None
    try:
        mod_time = int(os.path.getmtime(filename))

        f = open(filename, "rb")    # open for reading in binary mode
        _hash = hashlib.sha1()
        s = f.read(16384)
        while s:
            _hash.update(s)
            s = f.read(16384)

        hash_value = _hash.hexdigest()
        signature = (filename,  mod_time, hash_value)
    except IOError:
        signature = None
    except OSError:
        signature = None
    finally:
        if f:
            f.close()
    return signature

if __name__ == '__main__':
    # =================================================================
    # Test signature creation
    sig = create_file_signature('rhyme.txt')
    print("SHA1 hash", sig)

    # =================================================================
    # Convert last modification time from numeric into printable form
    print("Last modified:", time.ctime(sig[1]))
