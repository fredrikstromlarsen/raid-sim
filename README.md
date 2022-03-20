# RAID SIM

The ` backend/`` folder contains the "drives" and their data. The  `frontend/` folder is the filesystem seen from the users perspective, no drives present, just the files and folders.

## How it should work

Create or upload a file to the `frontend/` directory, and see that nothing happens (in the frontend). Your file is readable, writable and/or executable. However, in the `backend/` directory the files have been dissected and distributed accross the files according to the RAID configuration.

**To test it** you can upload the files, then, delete a directory (or intentionally make a "drive" fail) and watch how it behaves: hotswapping, restoring, or possibly just corrupting the files on the frontend side.

This way the application may work as a RAID-simulator so that you can test your RAID configuration before deploying it on your own system.
