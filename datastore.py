#! /usr/bin/env python

import re
import gtk
import sys

class Race(object):

   def __init__(self,name):
      self.name = name
      self.str = 0
      self.dex = 0
      self.con = 0
      self.int = 0
      self.wis = 0
      self.cha = 0
      self.size = 0
      self.exp = 0
      self.spr = 0
      self.hpr = 0
      self.skillmax = 0
      self.spellmax = 0
      self.skillcost = 0
      self.spellcost = 0

   def printSelf(self):
      print self.name, self.str, self.dex, self.con, self.int, self.wis
      print "  ", self.size, self.exp, self.spr, self.hpr
      print "  ", self.skillmax, self.spellmax, self.skillcost, self.spellcost


class Races(dict):

   def __init__(self, filename):
      fileobj = open(filename.lower(),'r')
      dict.__init__(self)
      lines = fileobj.readlines()
      for i in lines:
         s = re.match(r"^([^#:]+):([\d ]+):([\d ]+):([\d ]+):([\d ]+):([\d ]+):(?:([\d ]+):)?([\d ]+):([\d ]+):([\d ]+):([\d ]+):([\d ]+):([\d ]+):([\d ]+):([\d ]+)",i)
         if not s:
            continue
         raceName = s.group(1).rstrip()
         race = Race(raceName)
         race.str = int(s.group(2))
         race.dex = int(s.group(3))
         race.con = int(s.group(4))
         race.int = int(s.group(5))
         race.wis = int(s.group(6))
         race.cha = int(s.group(7)) if s.group(7) else 100
         race.size = int(s.group(8))
         race.exp = int(s.group(9))
         race.spr = int(s.group(10))
         race.hpr = int(s.group(11))
         race.skillmax = int(s.group(12))
         race.spellmax = int(s.group(13))
         race.skillcost = int(s.group(14))
         race.spellcost = int(s.group(15))
         self[raceName] = race

class RaceDesc(dict):
   def __init__(self,filename):
      fileobj = open(filename.lower(),'r')
      dict.__init__(self)
      raceName = ""
      lines = fileobj.readlines()
      self[raceName] = ""
      for i in lines:
         s = re.match(r"Help race ([\w ]+)",i)
         if not not s:
            raceName = s.group(1).rstrip()
            raceName = raceName.lstrip()
            self[raceName] = ""
         else:
            self[raceName] += i

class SkillDesc(dict):
   def __init__(self,filename):
      fileobj = open(filename.lower(),'r')
      dict.__init__(self)
      skillName = ""
      lines = fileobj.readlines()
      self[skillName] = ""
      for i in lines:
         s = re.match(r"Help on skill: ([\w \']+).",i)
         if not not s:
            skillName = s.group(1).rstrip()
            skillName = skillName.lstrip()
            skillName = skillName.lower()
            self[skillName] = ""
         else:
            self[skillName] += i


class SpellDesc(dict):
   def __init__(self,filename):
      fileobj = open(filename.lower(),'r')
      dict.__init__(self)
      spellName = ""
      lines = fileobj.readlines()
      self[spellName] = ""
      for i in lines:
         s = re.match(r"Help on spell: ([\w \']+).",i)
         if not not s:
            spellName = s.group(1).rstrip()
            spellName = spellName.lstrip()
            spellName = spellName.lower()
            self[spellName] = ""
         else:
            self[spellName] += i

class TaskPoints(object):
   def __init__(self):
      self.lesser = [0,100,300,700,1400,2500,4100,6300,9200,12900]
      self.greater = [0,200,550,1200,2300,4000,6450,9800]


class TrainCosts(object):
   def __init__(self,filename):
      fileobj = open(filename.lower(),'r')
      self.data = {}
      lines = fileobj.readlines()
      for i in lines:
         s = re.match(r"(.+):( *\d*)",i)
         if not not s:
            if not s.group(2):
               self.data[s.group(1)] = 0
            else:
               self.data[s.group(1)] = int(s.group(2))
      # FIXME
      # don't know what to do about >100% can have up to 115
      # "shouldn't" need past 110 since with 100 base cost
      # it should max out at 115 regardless
      # 34040+20202+2506 ~ 105?
      #
      # NOTE: it seems that this works very well, except that the base costs
      # is off for many spells/skills

      # i've check with Arghun's and from what i can tell, it gets them
      # "wrong" for small values too, i may just have to keep it as this
      # better skill cost file will help correct
      # proper cost can be calced buy dividing the 50% cost by 184
      # accounting for race cost
      # read from costs.txt?

      self.costlist = [0,1,2,4,8,13,22,38,64,109,184,310,523,882,1487,2506,
                       4222,7115,11989,20202,34040,999999,999999,999999]

   def cost(self,name,studyPercent,costPercent):
      # the cost calculated here is almost correct
      studyPercent = int(studyPercent) / 5
      tempCost = 0
      if not self.data.has_key(name):
          return (0,0)

      for i in range(studyPercent + 1):
         tempCost += min(self.costlist[i]*self.data[name],10000000)
      tempCost = int((tempCost*costPercent)/100)

      return (tempCost,int((tempCost*6666)/10000000))

class StatCost(list):
   def __init__(self,filename):
      fileobj = open(filename.lower(),'r')
      list.__init__(self,[0])
      lines = fileobj.readlines()
      for i in lines:
         self.append(int(i))
      for i in range(1,len(self)):
         self[i] += self[i - 1]


class QuestPoints(object):
   """ class to load and maintain quest points """
   def __init__(self,filename):
      fileobj = open(filename.lower(),'r')
      self.qps = [0]
      while True:
         currentline = fileobj.readline()
         if not currentline:
            break
         self.qps.append(int(currentline))
      fileobj.close()
      for i in range(1,len(self.qps)):
         self.qps[i] = self.qps[i] + self.qps[i - 1]
   def findlevel(self,qps):
      for i in range(len(self.qps)):
         if self.qps[i] > qps:
            return i - 1
      return 120
   def qpsneeded(self,level):
      return self.qps[level]
   def dump(self):
      for i in self.qps:
         print i


class LevelCosts(object):
   """ This class reads and holds level costs """
   def __init__(self,filename):
      fileobj = open(filename.lower(),'r')
      self.costs = [0]
      while True:
         currentline = fileobj.readline()
         if not currentline:
            break
         self.costs.append(int(currentline))
      fileobj.close()
      for i in range(1,len(self.costs)):
         self.costs[i] = self.costs[i] + self.costs[i - 1]
   def findlevel(self,exp):
      for i in range(len(self.costs)):
         if self.costs[i] > exp:
            return i - 1
      return 120
   def expneeded(self,level):
      return self.costs[level]
   def dump(self):
      for i in self.costs:
         print i


class GuildStore(gtk.TreeStore):
   """This class loads the possible guilds"""
   def __init__(self,filename):
      fileobj = open(filename.lower(),'r')
      gtk.TreeStore.__init__(self,str,int,int,'gboolean')
      currentlines = fileobj.readlines()
      # name, lvls, maxlvls,viewable
      self.guilds = {}
      for i in currentlines:
         s = re.match(r"(\S+) (\d+)",i)
         if not not s:
            iter = self.append(None,[s.group(1),int(s.group(2)),0,True])
            print "loading guild",s.group(1)
            self.guilds[s.group(1)] = Guild(s.group(1),s.group(2))
            print "loaded guild",s.group(1)
            self.loadsubs(self.guilds[s.group(1)],iter)
#Guild(s.group(1),int(s.group(2)))
      print "loaded guilds"
      for i,j in self.guilds.iteritems():
         print i
   def loadsubs(self,guild,parent):
      for i,j in guild.subs.iteritems():
         print "   with subguild", i,j
         iter = self.append(parent,[i,j,0,False])
         if not self.guilds.has_key(i):
            self.guilds[i] = Guild(i,j)
            self.loadsubs(self.guilds[i],iter)

class Guild(object):
   """This class reads and holds a guild"""
   def __init__(self,name,levels):
      currentlvl = 0
      self.level = []
      self.excludeguilds = []
      self.excluderaces = []
      self.levels = 0
      self.subs = {}
      loadingsubs = False
      loadingguilds = False
      loadingraces = False
      self.name = name
      try:
         fileobj = open("data/" + name.lower() + ".chr",'r')
      except IOError:
         print "error finding","data/" + name.lower() + ".chr"
         return

      currentlines = fileobj.readlines()
      self.level.append(GuildLevel())
      for i in currentlines:
         #check for lvl stuff
         s = re.match(r"\|  (  | \d|\d\d) \|",i)
         if not not s:
            if not (s.group(1) == "  "):
               # change the level
               newlvl = int(s.group(1))
               if newlvl != currentlvl + 1:
                  raise
               currentlvl = newlvl
               self.level.append(GuildLevel())
            s = re.search(r"(Intelligence|Int)\((\d+)\)",i)
            if not not s:
               self.level[currentlvl].int = int(s.group(2))
            s = re.search(r"(Charisma|Cha)\((\d+)\)",i)
            if not not s:
               self.level[currentlvl].cha = int(s.group(2))
            s = re.search(r"(Wisdom|Wis)\((\d+)\)",i)
            if not not s:
               self.level[currentlvl].wis = int(s.group(2))
            s = re.search(r"(Strength|Str)\((\d+)\)",i)
            if not not s:
               self.level[currentlvl].str = int(s.group(2))
            s = re.search(r"(Constitution|Con)\((\d+)\)",i)
            if not not s:
               self.level[currentlvl].con = int(s.group(2))
            s = re.search(r"(Dexterity|Dex)\((\d+)\)",i)
            if not not s:
               self.level[currentlvl].dex = int(s.group(2))
            s = re.search(r"(Hit points|Hp)\((\d+)\)",i)
            if not not s:
               self.level[currentlvl].hpmax = int(s.group(2))
            s = re.search(r"(Spell points|Sp)\((\d+)\)",i)
            if not not s:
               self.level[currentlvl].spmax = int(s.group(2))
            s = re.search(r"(Spell point regeneration|Sp_regen)\((\d+)\)",i)
            if not not s:
               self.level[currentlvl].spr = int(s.group(2))
            s = re.search(r"(Hit point regeneration|Hp_regen)\((\d+)\)",i)
            if not not s:
               self.level[currentlvl].hpr = int(s.group(2))
            s = re.search(r"Physical resistance\((\d+)\)",i)
            if not not s:
               self.level[currentlvl].physres = int(s.group(1))
            s = re.search(r"Asphyxiation resistance\((\d+)\)",i)
            if not not s:
               self.level[currentlvl].asphres = int(s.group(1))
            s = re.search(r"Psionic resistance\((\d+)\)",i)
            if not not s:
               self.level[currentlvl].psires = int(s.group(1))
            s = re.search(r"Poison resistance\((\d+)\)",i)
            if not not s:
               self.level[currentlvl].poisres = int(s.group(1))
            s = re.search(r"Acid resistance\((\d+)\)",i)
            if not not s:
               self.level[currentlvl].acidres = int(s.group(1))
            s = re.search(r"Magical resistance\((\d+)\)",i)
            if not not s:
               self.level[currentlvl].magires = int(s.group(1))
            s = re.search(r"Electric resistance\((\d+)\)",i)
            if not not s:
               self.level[currentlvl].elecres = int(s.group(1))
            s = re.search(r"Fire resistance\((\d+)\)",i)
            if not not s:
               self.level[currentlvl].fireres = int(s.group(1))
            s = re.search(r"Cold resistance\((\d+)\)",i)
            if not not s:
               self.level[currentlvl].coldres = int(s.group(1))
               #parse some out some stuff and add to current level

         # checking for the spell/skill section
         s = re.match(r"Level (\d+) abilities:",i)
         if not not s:
            currentlvl = int(s.group(1))

         s = re.match(r"May train skill (.+) to (\d+)%",i)
         if not not s:
            self.level[currentlvl].addskill(s.group(1), int(s.group(2)))

         s = re.match(r"May study spell (.+) to (\d+)%",i)
         if not not s:
            self.level[currentlvl].addspell(s.group(1), int(s.group(2)))

         s = re.match(r"Subguilds:",i)
         if not not s:
            loadingsubs = True
            loadingguilds = False
            loadinraces = False
            continue
         s = re.match(r"Notguilds:",i)
         if not not s:
            loadingguilds = True
            loadingsubs = False
            loadingraces = False
            continue
         s = re.match(r"Notraces:",i)
         if not not s:
            loadingraces = True
            loadingguilds = False
            loadingsubs = False
            continue

         if loadingsubs:
            s = re.match(r"(.+) (\d+)",i)
            if not not s:
               self.subs[s.group(1)] = int(s.group(2))
#Guild(s.group(1),int(s.group(2)))
         if loadingguilds:
            s = re.match(r"([\w][\w ]*)",i)
            if not not s:
               self.excludeguilds.append(s.group(1).rstrip())
         if loadingraces:
            s = re.match(r"([\w][\w ]*)",i)
            if not not s:
               self.excluderaces.append(s.group(1).rstrip())
      # now we must accumulate each level
      self.levels = currentlvl

      for i in range(len(self.level) - 1):
         for j, k in self.level[i].spells.iteritems():
            self.level[i + 1].addspell(j,k)
         for j, k in self.level[i].skills.iteritems():
            self.level[i + 1].addskill(j,k)
         self.level[i + 1].int += self.level[i].int
         self.level[i + 1].cha += self.level[i].cha
         self.level[i + 1].wis += self.level[i].wis
         self.level[i + 1].str += self.level[i].str
         self.level[i + 1].con += self.level[i].con
         self.level[i + 1].dex += self.level[i].dex
         self.level[i + 1].hpmax += self.level[i].hpmax
         self.level[i + 1].spmax += self.level[i].spmax
         self.level[i + 1].spr += self.level[i].spr
         self.level[i + 1].hpr += self.level[i].hpr
         self.level[i + 1].physres += self.level[i].physres
         self.level[i + 1].asphres += self.level[i].asphres
         self.level[i + 1].psires += self.level[i].psires
         self.level[i + 1].poisres += self.level[i].poisres
         self.level[i + 1].acidres += self.level[i].acidres
         self.level[i + 1].magires += self.level[i].magires
         self.level[i + 1].elecres += self.level[i].elecres
         self.level[i + 1].fireres += self.level[i].fireres
         self.level[i + 1].coldres += self.level[i].coldres

class GuildLevel(object):
   def __init__(self):
      self.int = 0
      self.cha = 0
      self.wis = 0
      self.str = 0
      self.con = 0
      self.dex = 0
      self.hpmax = 0
      self.spmax = 0
      self.spr = 0
      self.hpr = 0
      self.physres = 0
      self.asphres = 0
      self.psires = 0
      self.poisres = 0
      self.acidres = 0
      self.magires = 0
      self.elecres = 0
      self.fireres = 0
      self.coldres = 0
      self.skills = {}
      self.spells = {}
   def addskill(self,skillname,percent):
      if self.skills.has_key(skillname):
         if self.skills[skillname] < percent:
            self.skills[skillname] = percent
      else:
         self.skills[skillname] = percent
   def addspell(self,spellname,percent):
      if self.spells.has_key(spellname):
         if self.spells[spellname] < percent:
            self.spells[spellname] = percent
      else:
         self.spells[spellname] = percent

class datastore(object):
   def __init__(self):
      self.qps = QuestPoints("data/questpoints.chr")
      print "loaded qps"
      self.statcost = StatCost("data/statcost.chr")
      print "loaded statcost"
      self.lvlcosts = LevelCosts("data/levelcosts.chr")
      print "loaded levelcost"
      self.spells = TrainCosts("data/spells.chr")
      print "loaded spellcost"
      self.skills = TrainCosts("data/skills.chr")
      print "loaded skillcost"
      self.guildstore = GuildStore("data/guilds.chr")
      print "loaded guildlist"
      self.races = Races("data/races.chr")
      print "loaded races"
      self.racedesc = RaceDesc("data/help_races.chr")
      print "loaded racedesc"
      self.skilldesc = SkillDesc("data/help_skill.chr")
      print "loaded skilldesc"
      self.spelldesc = SpellDesc("data/help_spell.chr")
      print "loaded spelldesc"
      self.tps = TaskPoints()
      print "loaded tps"


if __name__ == "__main__":
   CCreator = datastore()
   print "stat costs from 0 to 50"
   for i in CCreator.statcost:
      print i
   print "the quest points required for full discount"
   print "from 0 to 120"
   for i in CCreator.qps.qps:
      print i
   print "level costs, before discount"
   for i in CCreator.lvlcosts.costs:
      print i
   print "list of guilds"
   CCreator.guildstore.foreach(lambda x,y,z: sys.stdout.write(x[y][0]+" "+str(x[y][1])+"\n"))
   for i, j in CCreator.guildstore.guilds.iteritems():
      print i
      print "Subguilds:"
      for k, l in j.subs.iteritems():
         print k
      print ""

   for j, k in CCreator.guildstore.guilds["Abjurer"].level[45].spells.iteritems():
      print j, k
      for l in range(0,105,5):
         print CCreator.spells.cost(j,l,80)
   print CCreator.racedesc["Merrow"]
   print CCreator.skilldesc["Power kick".lower()]
   print CCreator.spelldesc["Magic missile".lower()]

