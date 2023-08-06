Title: Writing your journal
Date: 2020-06-06

Writing a journal entry (or blog post) is a process of constant trial and error, so Journal Generator includes a way of previewing the changes you make to the files so you can focus on the fun part, which is writing your entries.

In the jouranl folder, run 

```bash
python app.py serve
```

And automatically an HTTP will be running and listening on port 5500 ready to show your generated journal.

After that, create a file in the `posts` folder and name it using the following rules pattern: `YYYY-MM-DD-title-with-no-spaces.md`.

A good template for an entry would be:

```markdown
Title: Your Entry Title
Date: YYYY-MM-DD

Your content here...
```

These two lines at the top are a special section, the *Meta* section, used for settings things like the Title, Date and other things for the entry. Currently Journal Generator only supports title and date, but in the future it will suppport things like tags, categories or even different authors

