program requires pygtk-2.0 or better

execute program with "python pyZombie.py"

http://home.comcast.net/~thp1017/

Note: all filenames should be lowercase on casesensitive platforms
Use the lcf script supplied in the trigs directory.
Change the data directory to "data".
Change your current directory to the data directory.
Execute "../trigs/lcf *".


Note 2: there are two options for data formats.
The old format, commonly used by Arghun's CharCreator, and the new format
i.e. the info straight from Zombiemud. Both formats work for this Prog.

To generate the guild files use the commands:
/log <guild>.chr
info
/eval /for i 1 <max level> info $$[i]
/log off

and add the sub guilds after this in the format:
Subguilds:
Harmonizers 9
Grand_medics 9

be sure to check for extraneous text from channels and emotes that may
have been logged


--------
Important Note:

The skill cost file that is distributed with Arghun's is sorta "wrong" for
this Calculator.  The low cost skills are approximated in Arghun's with
different scaler than the medium to high cost skills/spells.

To get proper working values for small cost, anything that doesn't double
for the first few trains, take the 50% value and divide by 184.

That SHOULD do the trick, there is no guarentee.  using the typical given file,
this Calculator will over shoot, so it is "safe"...

Included in this zip is mostly updated spells.chr and skills.chr. I may have
missed/couldn't get to some of the skills/spells
-------


This program is brought to you by Gam, who has to much time on his hands.
Updated by Conglomo to deal with the new money costs.
