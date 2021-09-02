def importData (self, urlList='../tmp/share_list.txt', directory=None, uri="file://"):
        """
        Read either a file or directory to extract key metadata from the file name

        TODOS:
            1. the URI and URL Combo need to be updated to reflect the ability of the system to access interaction data
        """
        items = []
        url = ""
        if urlList and not directory: # Pick up the list of shares and URLs when stored in Minio/S3
            entry_dict = {}
            url_regex = re.compile ('^URL:')
            share_regex = re.compile ('^Share:')
            thumb_regex = re.compile ('^thumb_')
            with open (urlList, 'r') as f:
                for file in f.readlines ():
                    if url_regex.match (file):
                        url = file.strip ('URL: ')
                        (file_name, file_hash) = self.getIndex (url) # Clean up the file namd and hash it
                        if thumb_regex.match (file_name): continue # Skip thumb_
                        entry_dict[file_hash] = file_name.split ('-') # Separate out the metadata
                    elif share_regex.match (file):
                        share = unquote (file.strip ('Share:')).strip ()
                        (file_name, file_hash) = self.getIndex (share)
                        if thumb_regex.match (file_name): # Detect if this is a thumbnail
                            file_name = file_name.replace ('thumb_', '')
                            file_hash = self.hashIt (file_name)
                            entry_dict[file_hash].append (share) # Append the thumbnail
                        else:
                            entry_dict[file_hash].append (share) # Append the interaction resource
                f.close ()
            return list (entry_dict.values ()) # unwind the dict into a list and return
        else: # Fall back to gathering data from the file system
            files = os.listdir (directory)
            url = uri + directory
            for file in files:
                raw_file = file
                file = file.split('.')[0] # remove the .extension
                entry = file.split ('-') # get the raw data
                entry.append (url + raw_file)
                items.append (entry)
            return items