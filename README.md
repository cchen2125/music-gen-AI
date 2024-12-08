# music-gen-AI

`beatovenWorkflow.py`: Code for querying and downloading songs from beatoven.ai
- make sure to put all email accounts and passwords in a local pwordProtect.py file before running. `pwordProtect_template.py` provides a working template of the structure without real emails

`sunoWorkflow.py`: Code for querying and downloading songs from Suno
- store Sterne emails/passwords in a .txt file called accounts.txt, where each line is a email, followed by a comma and then the password (no spaces)
- So far microsoft accounts have only been made for Robert and John. As time goes on and we make more, we increase NUM_DRIVERS to len(sterne_names)
