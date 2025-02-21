# music-gen-AI

`beatovenWorkflow.py`: Code for querying and downloading songs from beatoven.ai
- make sure to put all email accounts and passwords in a local pwordProtect.py file before running. `pwordProtect_template.py` provides a working template of the structure without real emails

`sunoWorkflow.py`: Code for querying and downloading songs from Suno
- store Sterne emails/passwords in a .txt file called accounts.txt, where each line is a email, followed by a comma and then the password (no spaces)
- For now, keep num_drivers<5 to avoid crashing. To use other accounts, just reorder your accounts.txt file
- Be careful for some microsoft login errors (sometimes asks to login via code instead of password - must manually bypass)

`stableAudioWorkflow.py`: Code for querying and downloading songs from Stable Audio

`mubertWorkflow.py`: Code for querying and downloading songs from Mubert
- Need to create more facebook accounts to run multi-account workflows
- Login is (relatively) slow on purpose just to bypass facebook bot detection
