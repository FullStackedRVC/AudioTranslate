If you get the error:
"google_trans_new.google_trans_new.google_new_transError: 404 (Not Found) from TTS API. Probable cause: Unknown"

It is because of a bug and this is the solution:
1. search in the python library for the google_trans_new.py file.
"Lib\site-packages "google_trans_new_google_trans_new.py"
(I use virtual machine and it is easier for me to find it)

Open it and change the codes to these:

16 / URL_SUFFIX_DEFAULT = 'com'

90/ def __init__(self, url_suffix="com", timeout=5, proxies=None):

151/ response = (decoded_line).

233/ response = (decoded_line)

3. That should work, if it doesn't then google the error and you will get help in these cases:
google_trans_new.google_trans_new.google_new_transError: 404 (Not Found) from TTS API. Probable cause: Unknown

