# add_braille
This is a script which adds braille to a font. I made it because the vim plugin minimap needs braille characters to work properly.

### Instructions.

You need Python 3 and FontForge. 

(I wrote this on Ubundu originally where there's a specific package "python3-fontforge", but from what I gather installing FontForge should work, maybe after a restart.)

Put the script in a directory, and add two subdirectories called "fonts-in" and "fonts-out".

Put whatever ttf font file you want to run this on in the "fonts-in" directory. I suggest starting with only one and checking if it worked. There are programs specifically to view font files so this can be done without installing.

Run the script, and the fonts-out directory should have your results.


This is a single file program, so if something doesn't work, try reading it over to see if you can spot the issue.

Otherwise feel free to open up an issue and I'll see what I can do.
