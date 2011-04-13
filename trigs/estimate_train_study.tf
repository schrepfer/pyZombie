;;Charcreator skill/spell initial cost checker by Damogran
;;Type "list skills all" and "list spells all" in guild to see correctly formatted text in your screen,
;;then cut/paste it to notepad or similar for further editing.
;;Remove duplicates from the lines with your favourite editor (hint: excel is excellent
;;in sorting lines) and save to filename skills.chr or spells.chr
;;
/send set term ansi+
/send set nomore on
/send set use_goahead on
/lp on
/set raceskill=90
/set racespell=80
/def lsk = /set tra=train%;/set t=0%;/set logi=skills.chr%;/set racecost=%raceskill%;!list skills all
/def lsp = /set tra=study%;/set t=0%;/set logi=spells.chr%;/set racecost=%racespell%;!list spells all
/def lista = /_echo %*, estimating with: %tra, estimated: %t
/def -p1 -ag -mregexp -t'^Estimate (train|study) (skill|spell): ([A-z \'\-12]*).$' esti = /set tr=%P3%;/set t=0
/def -p0 -ag -mregexp -t'^\| ([A-z \'\-12]*)([ |0-9Mk.]*)$' ski = /set t=$[t+1]%;/repeat -%t 1 !estimate %tra %P1
;;/def -p0 -ag -mregexp -t'^\| ((\\w+ ?){1,5})' ski = /set t=$[t+1]%;/repeat -%t 1 !estimate %tra %P1
/def -p3 -ag -mglob    -t'\| Skill:  *' sklist= /set tra=train%;/lista Skill
/def -p3 -ag -mglob    -t'\| Spell:  *' splist= /set tra=study%;/lista Spell
/def -p3 -ag -mglob    -t'\| Total:  *' loppu = /lista %*%;/set tra=0
/def -p3 -ag -mglob    -t'\|   5:*' eka = /set tracost=%3
/def -p0 -ag -mglob    -t'\|  ??:*' loput
/def -p3 -ag -mglob    -t'\|  50:*' eka2 = /if ({tracost}<1000)  /set tracost=$[({3}/184) * 100 / {racecost}]%; /else /set tracost=$[({tracost})* 100 / {racecost}]%; /endif%;/test fwrite("%logi","%tr: %tracost")%;/echo %tr: %tracost
/def -p0 -ag -mglob    -t'?-------------*' viivat
/def -p0 -ag -msimple  -t'|=================================================|' muutviivat
