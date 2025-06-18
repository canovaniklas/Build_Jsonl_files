import os

# Folder where the files are located
folder_path = "/Users/niklascanova/Desktop/allegra-raw-2012-05-07(2)/rm"

# List of files to delete
files_to_delete = [
    "1997-12-31-5.txt",
    "1997-12-31-7.txt",
    "1998-09-16-1.txt",
    "1998-09-16-1-sr.txt",
    "1998-09-16-1-vl.txt",
    "1998-11-19-2.txt",
    "1999-01-22-1.txt",
    "2000-11-02-3.txt",
    "2001-03-20-2.txt",
    "2001-03-28-1.txt",
    "2001-03-30-1.txt",
    "2001-04-25-2.txt",
    "2001-05-30-1.txt",
    "2001-05-30-2.txt",
    "2001-06-19-1.txt",
    "2001-08-14-1.txt",
    "2001-10-02-1.txt",
    "2001-11-02-1.txt",
    "2001-12-06-1.txt",
    "2001-12-10-1.txt",
    "2001-12-13-2.txt",
    "2001-12-13-3.txt",
    "2001-12-21-3.txt",
    "2002-01-03-1.txt",
    "2002-01-22-1.txt",
    "2002-04-15-1.txt",
    "2002-06-28-1.txt",
    "2002-07-11-3.txt",
    "2002-08-30-1.txt",
    "2002-08-30-2.txt",
    "2002-09-26-2.txt",
    "2002-10-15-1.txt",
    "2003-03-26-1.txt",
    "2003-04-08-1.txt",
    "2003-08-12-1.txt",
    "2006-08-03-2.txt",
    "2006-08-14-1.txt",
    "2008-01-09-1.txt",
    "2008-01-10-1.txt",
    "2008-01-10-2.txt",
    "2008-01-17-1.txt",
    "2008-11-20-2.txt",
    "2009032501.txt",
    "2010012601.txt",
    "2010042903.txt"
]


# Delete files
for filename in files_to_delete:
    file_path = os.path.join(folder_path, filename)
    try:
        os.remove(file_path)
        print(f"Deleted: {filename}")
    except FileNotFoundError:
        print(f"Not found: {filename}")
    except Exception as e:
        print(f"Error deleting {filename}: {e}")
