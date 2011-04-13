/purge
/set cc=0
/def query = /result %{1}
/def rl=/set cc=0%;/helppi
/def rodut =/if (cc<41) /repeat -1 1 /helppi%;/endif
/def helppi =/set cc=$[cc+1]%;/set ctemp=r$[cc]%;/set ctemp=$[query({ctemp})]%;help race %ctemp%;/set rh=1%;/rodut
/def -mglob -ag -t'------------------------------------------------------------------------------' r1 = /if (rh=1) /_echo %*%;/echo Help race %ctemp%;/endif%;/set rh=0
/set r1=Ajoatling
/set r2=Catfolk
/set r3=Centaur
/set r4=Cherub
/set r5=Cromagnon
/set r6=Cyclops
/set r7=Devil
/set r8=Djinni
/set r9=Drow
/set r10=Dwarf
/set r11=Duck
/set r12=Elf
/set r13=Ent
/set r14=Giant
/set r15=Gnome
/set r16=Golem
/set r17=Halfling
/set r18=Hobbit
/set r19=Human
/set r20=Imp
/set r21=Kobold
/set r22=Korred
/set r23=Lizardman
/set r24=Merfolk
/set r25=Merrow
/set r26=Mind Flayer
/set r27=Minotaur
/set r28=Orc
/set r29=Satyr
/set r30=Seraph
/set r31=Sprite
/set r32=Thrikhren
/set r33=Tinman
/set r34=Titan
/set r35=Toadman
/set r36=Treant
/set r37=Troll
/set r38=Valkyrie
/set r39=Vampire
/set r40=Wolfman
/set r41=Yeti
