#! /usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import gtk.gdk
import gobject
import datastore

(
   COLUMN_NAME,
   COLUMN_MAX,
   COLUMN_CURRENT
) = range(3)

class GuildShow(gtk.Dialog):
   def __init__(self,parent,title,guildinfo):
      gtk.Dialog.__init__(self,title,parent,
                          gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                          (gtk.STOCK_OK,gtk.RESPONSE_DELETE_EVENT))
      self.guildinfo = guildinfo

      hbox = gtk.HBox()
      vbox = gtk.VBox()

      frame = gtk.Frame()
      vbox1 = gtk.VBox()

      hbox1 = gtk.HBox()
      hbox1.pack_start(gtk.Label("Skills:"),False)
      self.skillbox = gtk.combo_box_new_text()
      self.skillbox.get_model().set_sort_column_id(0,gtk.SORT_ASCENDING)
      self.skillbox.connect("changed",self.on_skillchange)
      for i,j in guildinfo.level[guildinfo.levels].skills.iteritems():
        self.skillbox.append_text(i)
      hbox1.pack_start(self.skillbox)
      vbox1.pack_start(hbox1)

      hbox1 = gtk.HBox()
      hbox1.pack_start(gtk.Label("Spells:"),False)
      self.spellbox = gtk.combo_box_new_text()
      self.spellbox.get_model().set_sort_column_id(0,gtk.SORT_ASCENDING)
      for i,j in guildinfo.level[guildinfo.levels].spells.iteritems():
        self.spellbox.append_text(i)
      self.spellbox.connect("changed",self.on_spellchange)
      hbox1.pack_start(self.spellbox)
      vbox1.pack_start(hbox1)

      frame.add(vbox1)
      vbox.pack_start(frame,False)

      frame = gtk.Frame()
      hbox1 = gtk.HBox()
      hbox1.pack_start(gtk.Label("Levels:"))
      self.level = IntEntry(2)
      self.level.connect("activate",self.on_clicked)
      self.level.set_text(str(guildinfo.levels))
      hbox1.pack_start(self.level)
      self.lvlButton = gtk.Button("Calculate")
      self.lvlButton.connect("clicked",self.on_clicked)
      hbox1.pack_start(self.lvlButton)
      frame.add(hbox1)
      vbox.pack_start(frame,False)

      frame = gtk.Frame()
      vbox1 = gtk.VBox()

      hbox1 = gtk.HBox()
      hbox1.pack_start(gtk.Label("Maximum levels:"))
      self.maxlvls = IntEntry(2)
      self.maxlvls.set_editable(False)
      self.maxlvls.set_text(str(guildinfo.levels))
      hbox1.pack_start(self.maxlvls)
      vbox1.pack_start(hbox1)

      hbox1 = gtk.HBox()
      hbox1.pack_start(gtk.Label("Selected levels:"))
      self.sellvls = IntEntry(2)
      self.sellvls.set_editable(False)
      hbox1.pack_start(self.sellvls)
      vbox1.pack_start(hbox1)

      hbox1 = gtk.HBox()

      vbox2 = gtk.VBox()
      hbox2 = gtk.HBox()
      hbox2.pack_start(gtk.Label("Str:"))
      self.str = IntEntry(3)
      self.str.set_editable(False)
      hbox2.pack_start(self.str)
      vbox2.pack_start(hbox2)

      hbox2 = gtk.HBox()
      hbox2.pack_start(gtk.Label("Int:"))
      self.int = IntEntry(3)
      self.int.set_editable(False)
      hbox2.pack_start(self.int)
      vbox2.pack_start(hbox2)
      hbox1.pack_start(vbox2)

      vbox2 = gtk.VBox()
      hbox2 = gtk.HBox()
      hbox2.pack_start(gtk.Label("Con:"))
      self.con = IntEntry(3)
      self.con.set_editable(False)
      hbox2.pack_start(self.con)
      vbox2.pack_start(hbox2)

      hbox2 = gtk.HBox()
      hbox2.pack_start(gtk.Label("Wis:"))
      self.wis = IntEntry(3)
      self.wis.set_editable(False)
      hbox2.pack_start(self.wis)
      vbox2.pack_start(hbox2)
      hbox1.pack_start(vbox2)

      vbox2 = gtk.VBox()
      hbox2 = gtk.HBox()
      hbox2.pack_start(gtk.Label("Dex:"))
      self.dex = IntEntry(3)
      self.dex.set_editable(False)
      hbox2.pack_start(self.dex)
      vbox2.pack_start(hbox2)

      hbox2 = gtk.HBox()
      hbox2.pack_start(gtk.Label("Cha:"))
      self.cha = IntEntry(3)
      self.cha.set_editable(False)
      hbox2.pack_start(self.cha)
      vbox2.pack_start(hbox2)
      hbox1.pack_start(vbox2)
      vbox1.pack_start(hbox1)

      hbox1 = gtk.HBox()
      vbox2 = gtk.VBox()

      hbox2 = gtk.HBox()
      hbox2.pack_start(gtk.Label("Hpmax:"))
      self.hpmax = IntEntry(3)
      self.hpmax.set_editable(False)
      hbox2.pack_start(self.hpmax)
      vbox2.pack_start(hbox2)

      hbox2 = gtk.HBox()
      hbox2.pack_start(gtk.Label("Spmax:"))
      self.spmax = IntEntry(3)
      self.spmax.set_editable(False)
      hbox2.pack_start(self.spmax)
      vbox2.pack_start(hbox2)
      hbox1.pack_start(vbox2)

      vbox2 = gtk.VBox()
      hbox2 = gtk.HBox()
      hbox2.pack_start(gtk.Label("Hpregen:"))
      self.hpregen = IntEntry(3)
      self.hpregen.set_editable(False)
      hbox2.pack_start(self.hpregen)
      vbox2.pack_start(hbox2)

      hbox2 = gtk.HBox()
      hbox2.pack_start(gtk.Label("Spregen:"))
      self.spregen = IntEntry(3)
      self.spregen.set_editable(False)
      hbox2.pack_start(self.spregen)
      vbox2.pack_start(hbox2)
      hbox1.pack_start(vbox2)
      vbox1.pack_start(hbox1)

      hbox2 = gtk.HBox()
      vbox2 = gtk.VBox()
      hbox1 = gtk.HBox()
      hbox1.pack_start(gtk.Label("Acid resist:"))
      self.acidres = IntEntry(2)
      self.acidres.set_editable(False)
      hbox1.pack_start(self.acidres)
      vbox2.pack_start(hbox1)
      hbox1 = gtk.HBox()
      hbox1.pack_start(gtk.Label("Asph resist:"))
      self.asphres = IntEntry(2)
      self.asphres.set_editable(False)
      hbox1.pack_start(self.asphres)
      vbox2.pack_start(hbox1)
      hbox1 = gtk.HBox()
      hbox1.pack_start(gtk.Label("Cold resist:"))
      self.coldres = IntEntry(2)
      self.coldres.set_editable(False)
      hbox1.pack_start(self.coldres)
      vbox2.pack_start(hbox1)
      hbox1 = gtk.HBox()
      hbox1.pack_start(gtk.Label("Elec resist:"))
      self.elecres = IntEntry(2)
      self.elecres.set_editable(False)
      hbox1.pack_start(self.elecres)
      vbox2.pack_start(hbox1)
      hbox1 = gtk.HBox()
      hbox1.pack_start(gtk.Label("Fire resist:"))
      self.fireres = IntEntry(2)
      self.fireres.set_editable(False)
      hbox1.pack_start(self.fireres)
      vbox2.pack_start(hbox1)
      hbox2.pack_start(vbox2)

      vbox2 = gtk.VBox()
      hbox1 = gtk.HBox()
      hbox1.pack_start(gtk.Label("Magi resist:"))
      self.magires = IntEntry(2)
      self.magires.set_editable(False)
      hbox1.pack_start(self.magires)
      vbox2.pack_start(hbox1)
      hbox1 = gtk.HBox()
      hbox1.pack_start(gtk.Label("Phys resist:"))
      self.physres = IntEntry(2)
      self.physres.set_editable(False)
      hbox1.pack_start(self.physres)
      vbox2.pack_start(hbox1)
      hbox1 = gtk.HBox()
      hbox1.pack_start(gtk.Label("Pois resist:"))
      self.poisres = IntEntry(2)
      self.poisres.set_editable(False)
      hbox1.pack_start(self.poisres)
      vbox2.pack_start(hbox1)
      hbox1 = gtk.HBox()
      hbox1.pack_start(gtk.Label("Psi resist:"))
      self.psires = IntEntry(2)
      self.psires.set_editable(False)
      hbox1.pack_start(self.psires)
      vbox2.pack_start(hbox1)
      hbox2.pack_start(vbox2)
      vbox1.pack_start(hbox2)
      frame.add(vbox1)
      vbox.pack_start(frame)
      self.level.activate()

      hbox.pack_start(vbox)

      self.percentlist = self.__create_model()
      self.tv = gtk.TreeView(self.percentlist)
      self.__add_columns(self.tv)

      for i in range(min(15,guildinfo.levels)):
         self.percentlist.append()
         self.percentlist[i][0]=i+1
         if i+16 <= guildinfo.levels:
            self.percentlist[i][2]=i+16
         if i+31 <= guildinfo.levels:
            self.percentlist[i][4]=i+31

      frame = gtk.Frame()
      frame.add(self.tv)
      hbox.pack_start(frame)

      self.vbox.pack_start(hbox)

      self.vbox.show_all()
   def __add_columns(self, treeview):
      renderer = gtk.CellRendererText()
      column = gtk.TreeViewColumn("lvl",renderer,text=0)
      treeview.append_column(column)
      renderer = gtk.CellRendererText()
      column = gtk.TreeViewColumn("percent",renderer,text=1)
      treeview.append_column(column)
      renderer = gtk.CellRendererText()
      column = gtk.TreeViewColumn("lvl",renderer,text=2)
      treeview.append_column(column)
      renderer = gtk.CellRendererText()
      column = gtk.TreeViewColumn("percent",renderer,text=3)
      treeview.append_column(column)
      renderer = gtk.CellRendererText()
      column = gtk.TreeViewColumn("lvl",renderer,text=4)
      treeview.append_column(column)
      renderer = gtk.CellRendererText()
      column = gtk.TreeViewColumn("percent",renderer,text=5)
      treeview.append_column(column)
   def __create_model(self):
      model = gtk.ListStore(
         gobject.TYPE_INT,
         gobject.TYPE_STRING,
         gobject.TYPE_INT,
         gobject.TYPE_STRING,
         gobject.TYPE_INT,
         gobject.TYPE_STRING,
      )
      return model
   def on_skillchange(self,w):
      if w.get_active() == -1:
         return
      self.spellbox.set_active(-1)
      name = self.skillbox.get_model()[self.skillbox.get_active()][0]
      for i in range(min(15,self.guildinfo.levels)):
         try:
            self.percentlist[i][1]=str(self.guildinfo.level[i+1].skills[name])+"%"
         except KeyError:
            self.percentlist[i][1]="0%"
         if i+16 <= self.guildinfo.levels:
            try:
               self.percentlist[i][3]=str(self.guildinfo.level[i+16].skills[name])+"%"
            except KeyError:
               self.percentlist[i][3]="0%"
         if i+31 <= self.guildinfo.levels:
            try:
               self.percentlist[i][5]=str(self.guildinfo.level[i+31].skills[name])+"%"
            except KeyError:
               self.percentlist[i][5]="0%"

   def on_spellchange(self,w):
      if w.get_active() == -1:
         return
      self.skillbox.set_active(-1)
      name = self.spellbox.get_model()[self.spellbox.get_active()][0]
      for i in range(min(15,self.guildinfo.levels)):
         try:
            self.percentlist[i][1]=str(self.guildinfo.level[i+1].spells[name])+"%"
         except KeyError:
            self.percentlist[i][1]="0%"
         if i+16 <= self.guildinfo.levels:
            try:
               self.percentlist[i][3]=str(self.guildinfo.level[i+16].spells[name])+"%"
            except KeyError:
               self.percentlist[i][3]="0%"
         if i+31 <= self.guildinfo.levels:
            try:
               self.percentlist[i][5]=str(self.guildinfo.level[i+31].spells[name])+"%"
            except KeyError:
               self.percentlist[i][5]="0%"
   def on_clicked(self,w):
      lvl = max(1,min(int(self.level.get_text()),self.guildinfo.levels))
      level = self.guildinfo.level[lvl]

      self.sellvls.set_text(str(lvl))

      self.str.set_text(str(level.str))
      self.int.set_text(str(level.int))
      self.con.set_text(str(level.con))
      self.wis.set_text(str(level.wis))
      self.dex.set_text(str(level.dex))
      self.cha.set_text(str(level.cha))

      self.hpmax.set_text(str(level.hpmax))
      self.spmax.set_text(str(level.spmax))
      self.hpregen.set_text(str(level.hpr))
      self.spregen.set_text(str(level.spr))

      self.acidres.set_text(str(level.acidres))
      self.asphres.set_text(str(level.asphres))
      self.coldres.set_text(str(level.coldres))
      self.elecres.set_text(str(level.elecres))
      self.fireres.set_text(str(level.fireres))
      self.magires.set_text(str(level.magires))
      self.physres.set_text(str(level.physres))
      self.poisres.set_text(str(level.poisres))
      self.psires.set_text(str(level.psires))

class DataShow(gtk.Dialog):
   def __init__(self,parent,title,text):
      gtk.Dialog.__init__(self,title,parent,
                       gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                       (gtk.STOCK_OK,gtk.RESPONSE_DELETE_EVENT))
      self.tb = gtk.TextBuffer()
      self.tv = gtk.TextView(self.tb)
      self.tv.set_editable(False)
      self.tb.set_text(title + "\n\n" + text)
      self.vbox.pack_start(self.tv)
      self.tv.show()


class IntEntry(gtk.Entry):
   def __init__(self,max=0):
      gtk.Entry.__init__(self,max)

      if max != 0:
         self.set_width_chars(max)

      self.set_text(str(0))
      self.value = 0

      self.connect("insert-text",self.on_edit)

   def on_edit(self,editable,new_text,nt_length,pos):
      # all that can be done given limitation of this widget
      try:
         value = int(new_text)
      except ValueError:
         self.stop_emission("insert-text")

class trainedStatsWindow(gtk.Frame):
   def __init__(self,onChange,statscost):
      gtk.Frame.__init__(self,"STAT TRAINING")
      self.set_border_width(3)
      self.recalcFunc = onChange
      self.statscost = statscost
      vbox = gtk.VBox()

      hbox = gtk.HBox()
      vbox2 = gtk.VBox()

      hbox2 = gtk.HBox()
      hbox2.pack_start(gtk.Label("Str:"))
      self.str = IntEntry(2)
      self.str.connect("changed",self.on_edit)
      hbox2.pack_start(self.str)
      vbox2.pack_start(hbox2)

      hbox2 = gtk.HBox()
      hbox2.pack_start(gtk.Label("Con:"))
      self.con = IntEntry(2)
      self.con.connect("changed",self.on_edit)
      hbox2.pack_start(self.con)
      vbox2.pack_start(hbox2)

      hbox2 = gtk.HBox()
      hbox2.pack_start(gtk.Label("Dex:"))
      self.dex = IntEntry(2)
      self.dex.connect("changed",self.on_edit)
      hbox2.pack_start(self.dex)
      vbox2.pack_start(hbox2)
      hbox.pack_start(vbox2)

      vbox2 = gtk.VBox()

      hbox2 = gtk.HBox()
      hbox2.pack_start(gtk.Label("Int:"))
      self.int = IntEntry(2)
      self.int.connect("changed",self.on_edit)
      hbox2.pack_start(self.int)
      vbox2.pack_start(hbox2)

      hbox2 = gtk.HBox()
      hbox2.pack_start(gtk.Label("Wis:"))
      self.wis = IntEntry(2)
      self.wis.connect("changed",self.on_edit)
      hbox2.pack_start(self.wis)
      vbox2.pack_start(hbox2)

      hbox2 = gtk.HBox()
      hbox2.pack_start(gtk.Label("Cha:"))
      self.cha = IntEntry(2)
      self.cha.connect("changed",self.on_edit)
      hbox2.pack_start(self.cha)
      vbox2.pack_start(hbox2)
      hbox.pack_start(vbox2)

      vbox.pack_start(hbox)
      hbox = gtk.HBox()
      hbox.pack_start(gtk.Label("Total spent on stats:"))
      self.total = IntEntry(6)
      self.total.set_editable(False)
      self.total.set_text("0")
      hbox.pack_start(self.total)
      hbox.pack_start(gtk.Label("Megs"))
      vbox.pack_start(hbox)
      self.add(vbox)
   def on_edit(self,editable):
      try:
         editable.value = int(editable.get_text())
      except ValueError:
         editable.value = 0

      totalcost = 0
      totalcost += self.statscost[max(min(self.str.value,50),0)]
      totalcost += self.statscost[max(min(self.con.value,50),0)]
      totalcost += self.statscost[max(min(self.dex.value,50),0)]
      totalcost += self.statscost[max(min(self.int.value,50),0)]
      totalcost += self.statscost[max(min(self.wis.value,50),0)]
      totalcost += self.statscost[max(min(self.cha.value,50),0)]

      totalcost = int(totalcost/1000000)

      self.total.set_text(str(totalcost))
      self.recalcFunc()
      return

class raceWindow(gtk.Frame):
   def __init__(self,raceData,raceInfo,onChange,parent):
      gtk.Frame.__init__(self,"RACE")
      self.set_border_width(3)
      hbox = gtk.HBox()
      self.recalcFunc = onChange
      self.raceData = raceData
      self.raceInfo = raceInfo
      self.parentWindow = parent

      self.model = self.__create_model()
      self.model.set_sort_column_id(0,gtk.SORT_ASCENDING)
      self.races = gtk.TreeView(self.model)
      self.races.set_headers_visible(False)
      self.races.connect("button-release-event",self.on_active)

      self.raceSelection = self.races.get_selection()
      self.raceSelection.set_mode(gtk.SELECTION_SINGLE)
      self.raceSelection.connect("changed",self.on_selection_change)

      self.__add_column(self.races)
      scroll = gtk.ScrolledWindow()
      scroll.set_shadow_type(gtk.SHADOW_ETCHED_IN)
      scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
      scroll.add(self.races)
      hbox.pack_start(scroll)

      hbox2 = gtk.HBox()

      vbox = gtk.VBox()

      hbox3 = gtk.HBox()
      hbox3.pack_start(gtk.Label("Str:"))
      self.str = IntEntry(3)
      self.str.set_editable(False)
      hbox3.pack_start(self.str)
      vbox.pack_start(hbox3)

      hbox3 = gtk.HBox()
      hbox3.pack_start(gtk.Label("Con:"))
      self.con = IntEntry(3)
      self.con.set_editable(False)
      hbox3.pack_start(self.con)
      vbox.pack_start(hbox3)

      hbox3 = gtk.HBox()
      hbox3.pack_start(gtk.Label("Dex:"))
      self.dex = IntEntry(3)
      self.dex.set_editable(False)
      hbox3.pack_start(self.dex)
      vbox.pack_start(hbox3)

      hbox3 = gtk.HBox()
      hbox3.pack_start(gtk.Label("Int:"))
      self.int = IntEntry(3)
      self.int.set_editable(False)
      hbox3.pack_start(self.int)
      vbox.pack_start(hbox3)

      hbox3 = gtk.HBox()
      hbox3.pack_start(gtk.Label("Wis:"))
      self.wis = IntEntry(3)
      self.wis.set_editable(False)
      hbox3.pack_start(self.wis)
      vbox.pack_start(hbox3)

      hbox2.pack_start(vbox)

      vbox = gtk.VBox()
      hbox3 = gtk.HBox()
      hbox3.pack_start(gtk.Label("Cha:"))
      self.cha = IntEntry(3)
      self.cha.set_editable(False)
      hbox3.pack_start(self.cha)
      vbox.pack_start(hbox3)

      hbox3 = gtk.HBox()
      hbox3.pack_start(gtk.Label("Size:"))
      self.siz = IntEntry(3)
      self.siz.set_editable(False)
      hbox3.pack_start(self.siz)
      vbox.pack_start(hbox3)

      hbox3 = gtk.HBox()
      hbox3.pack_start(gtk.Label("Exp:"))
      self.exp = IntEntry(3)
      self.exp.set_editable(False)
      hbox3.pack_start(self.exp)
      vbox.pack_start(hbox3)

      hbox3 = gtk.HBox()
      hbox3.pack_start(gtk.Label("Hpr:"))
      self.hpr = IntEntry(3)
      self.hpr.set_editable(False)
      hbox3.pack_start(self.hpr)
      vbox.pack_start(hbox3)

      hbox3 = gtk.HBox()
      hbox3.pack_start(gtk.Label("Spr:"))
      self.spr = IntEntry(3)
      self.spr.set_editable(False)
      hbox3.pack_start(self.spr)
      vbox.pack_start(hbox3)

      hbox2.pack_start(vbox)

      vbox = gtk.VBox()
      hbox3 = gtk.HBox()
      hbox3.pack_start(gtk.Label("Sk Max:"))
      self.skillmax = IntEntry(3)
      self.skillmax.set_editable(False)
      hbox3.pack_start(self.skillmax)
      vbox.pack_start(hbox3)

      hbox3 = gtk.HBox()
      hbox3.pack_start(gtk.Label("Sp Max:"))
      self.spellmax = IntEntry(3)
      self.spellmax.set_editable(False)
      hbox3.pack_start(self.spellmax)
      vbox.pack_start(hbox3)

      hbox3 = gtk.HBox()
      hbox3.pack_start(gtk.Label("Sk Cost:"))
      self.skillcost = IntEntry(3)
      self.skillcost.set_editable(False)
      hbox3.pack_start(self.skillcost)
      vbox.pack_start(hbox3)

      hbox3 = gtk.HBox()
      hbox3.pack_start(gtk.Label("Sp Cost:"))
      self.spellcost = IntEntry(3)
      self.spellcost.set_editable(False)
      hbox3.pack_start(self.spellcost)
      vbox.pack_start(hbox3)

      hbox2.pack_start(vbox)

      hbox.pack_start(hbox2)

      self.add(hbox)
   def __create_model(self):
      model = gtk.ListStore(gobject.TYPE_STRING)
      for name, data in self.raceData.iteritems():
         iter = model.append()

         model.set(iter,
              0, name,
         )
      return model
   def __add_column(self,treeview):
      renderer = gtk.CellRendererText()
      column = gtk.TreeViewColumn("name",renderer,text=COLUMN_NAME)

      treeview.append_column(column)

   def on_selection_change(self,treeselection):
      # find which changed, then set the data for raceWindow accord.
      # then issue an self.recalcFunc so all else that needs cleaning will be
      (model,listy) = treeselection.get_selected_rows()
      curr_race = self.raceData[model[listy[0]][0]]
      self.curr_race = curr_race.name
      self.str.set_text(str(curr_race.str))
      self.con.set_text(str(curr_race.con))
      self.dex.set_text(str(curr_race.dex))
      self.int.set_text(str(curr_race.int))
      self.wis.set_text(str(curr_race.wis))
      self.cha.set_text(str(curr_race.cha))
      self.siz.set_text(str(curr_race.size))
      self.exp.set_text(str(curr_race.exp))
      self.hpr.set_text(str(curr_race.hpr))
      self.spr.set_text(str(curr_race.spr))
      self.skillmax.set_text(str(curr_race.skillmax))
      self.spellmax.set_text(str(curr_race.spellmax))
      self.skillcost.set_text(str(curr_race.skillcost))
      self.spellcost.set_text(str(curr_race.spellcost))

      self.recalcFunc()
      return

   def on_active(self,w,event):
      if event.get_state() & gtk.gdk.BUTTON3_MASK:
         (store, iter) = w.get_selection().get_selected()
         name = store.get_value(iter,0)
         dialog = DataShow(self.parentWindow,name,self.raceInfo[name])
         if dialog.run() != gtk.RESPONSE_NONE:
            dialog.destroy()
      return False


class guildWindow(gtk.Frame):
   def __init__(self,guildstore,onChange,parentWindow):
      gtk.Frame.__init__(self,"GUILDS")
      self.set_border_width(3)
      self.guildstore = guildstore
      self.parentWindow = parentWindow

      self.recalcFunc = onChange

      self.guildstore.set_sort_column_id(0,gtk.SORT_ASCENDING)

      hbox = gtk.HBox()
      self.filteredguild = self.guildstore.filter_new()
      self.filteredguild.set_visible_column(3)
      self.tvguild = gtk.TreeView(self.filteredguild)
      self.__add_columns1(self.tvguild)
      self.tvguild.set_headers_visible(False)
      #self.tvguild.connect("row-activated",self.dc_addguild)
      self.tvguild.connect("button-release-event",self.on_active)
      scrollw = gtk.ScrolledWindow()
      scrollw.set_border_width(3)

      scrollw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
      scrollw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
      scrollw.add(self.tvguild)
      hbox.pack_start(scrollw)

      vbox = gtk.VBox()
      vbox.pack_start(gtk.Label("Free"))
      self.freelvl = IntEntry(3)
      self.freelvl.connect("changed",self.on_edit)
      vbox.pack_start(self.freelvl)
      hbox.pack_start(vbox,False)

      self.add(hbox)
   def __add_columns1(self, treeview):
      model = treeview.get_model()

      # name column
      renderer = gtk.CellRendererText()
      column = gtk.TreeViewColumn("name",renderer,text=COLUMN_NAME)

      treeview.append_column(column)

      # max skill/spell %
      renderer = gtk.CellRendererText()
      column = gtk.TreeViewColumn("max",renderer,text=COLUMN_MAX)

      treeview.append_column(column)

      renderer = gtk.CellRendererText()
      renderer.connect("edited",self.on_cell_edited,(model,2))
      renderer.set_property('editable',True)
      column = gtk.TreeViewColumn("curr",renderer,text=COLUMN_CURRENT)

      treeview.append_column(column)

   def guildadd(self,model,path,iter,guilddict):
      guild = model[path][0]
      if model[path][2] > 0:
         if guilddict.has_key(guild):
            guilddict[guild] += model[path][2]
         else:
            guilddict[guild] = model[path][2]


   def on_cell_edited(self, cell, path, new_text, model):
      treestore, column = model
      treestore = self.guildstore
      try:
         level = int(new_text)
      except ValueError:
         # can just return since we are not changing anything
         return
      guilds = {}
      self.guildstore.foreach(self.guildadd,guilds)
      levels = 0
      for i,j in guilds.iteritems():
         levels += j
      level = min(max(level,0),treestore[path][1])
      levels -= treestore[path][column]
      level = max(min(120-levels,level),0)
      if level < self.guildstore.guilds[treestore[path][0]].levels:
         self.hidesubs(treestore,treestore.get_iter(path))
      if level >= treestore[path][1]:
         level = treestore[path][1]
         self.viewsubs(treestore,treestore.get_iter(path))
         self.tvguild.expand_row(path,True)
      if treestore[path][column] == level:
         return

      treestore[path][column] = level

      self.recalcFunc()
      return
   def hidesubs(self,treestore,iter):
      iter = treestore.iter_children(iter)
      while iter:
         treestore.set_value(iter,2,0)
         treestore.set_value(iter,3,False)
         self.hidesubs(treestore,iter)
         iter = treestore.iter_next(iter)
      return
   def viewsubs(self,treestore,iter):
      iter = treestore.iter_children(iter)
      while iter:
         treestore.set_value(iter,3,True)
         iter = treestore.iter_next(iter)
      return

   def addGuild(self,widget):
      # need to do checking for subguilds, etc
      (model,iter) = self.tvunselected.get_selection().get_selected()
      if iter == None:
         return

      levels = int(self.freelvl.value)
#      levels = 0
      for i in self.selected:
         levels += i[1]
      if levels == 120:
         return

      guildname = model[model.get_path(iter)][0]
      guildlevels = model[model.get_path(iter)][1]

      self.unselected.remove(iter)

      if levels + guildlevels > 120:
         self.selected.append([guildname,120 - levels])
      else:
         self.selected.append([guildname,guildlevels])
         for i, j in self.guilds[guildname].subs.iteritems():
            self.unselected.append([i,j.levels])

      self.selected.set_sort_column_id(0,gtk.SORT_ASCENDING)
      self.unselected.set_sort_column_id(0,gtk.SORT_ASCENDING)
      self.recalcFunc()


   def on_active(self,w,event):
      if event.get_state() & gtk.gdk.BUTTON3_MASK:
         (store, iter) = w.get_selection().get_selected()
         name = store.get_value(iter,0)
         dialog = GuildShow(self.parentWindow,name,self.guildstore.guilds[name])
         if dialog.run() != gtk.RESPONSE_NONE:
            dialog.destroy()
      #elif event.get_state() & gtk.gdk.BUTTON2_MASK:
      #  (store, iter) = w.get_selection().get_selected()
      #  store.set_value(iter, 2, store.get_value(iter, 1))
      return False

   def on_edit(self,editable):
      try:
         editable.value = int(editable.get_text())
      except ValueError:
         editable.value = 0
      self.recalcFunc()



class charDataWindow(gtk.Frame):
   def __init__(self):
      gtk.Frame.__init__(self,"CHARACTER DATA")
      self.set_border_width(3)
      hbox = gtk.HBox()

      vbox = gtk.VBox()
      hbox2 = gtk.HBox()
      hbox2.pack_start(gtk.Label("Hpmax"))
      self.hpmax = IntEntry(4)
      self.hpmax.set_editable(False)
      hbox2.pack_start(self.hpmax)
      vbox.pack_start(hbox2)

      hbox2 = gtk.HBox()
      hbox2.pack_start(gtk.Label("Spmax"))
      self.spmax = IntEntry(4)
      self.spmax.set_editable(False)
      hbox2.pack_start(self.spmax)
      vbox.pack_start(hbox2)

      hbox2 = gtk.HBox()
      hbox2.pack_start(gtk.Label("Hpregen"))
      self.hpregen = IntEntry(3)
      self.hpregen.set_editable(False)
      hbox2.pack_start(self.hpregen)
      vbox.pack_start(hbox2)

      hbox2 = gtk.HBox()
      hbox2.pack_start(gtk.Label("Spregen"))
      self.spregen = IntEntry(3)
      self.spregen.set_editable(False)
      hbox2.pack_start(self.spregen)
      vbox.pack_start(hbox2)

      hbox2 = gtk.HBox()
      hbox2.pack_start(gtk.Label("Skillmax"))
      self.skillmax = IntEntry(3)
      self.skillmax.set_editable(False)
      hbox2.pack_start(self.skillmax)
      vbox.pack_start(hbox2)

      hbox2 = gtk.HBox()
      hbox2.pack_start(gtk.Label("Spellmax"))
      self.spellmax= IntEntry(3)
      self.spellmax.set_editable(False)
      hbox2.pack_start(self.spellmax)
      vbox.pack_start(hbox2)

      hbox.pack_start(vbox)

      # right side now
      vbox = gtk.VBox()
      hbox2 = gtk.HBox()
      vbox2 = gtk.VBox()
      hbox3 = gtk.HBox()
      hbox3.pack_start(gtk.Label("Str:"))
      self.str = IntEntry(3)
      self.str.set_editable(False)
      hbox3.pack_start(self.str)
      vbox2.pack_start(hbox3)

      hbox3 = gtk.HBox()
      hbox3.pack_start(gtk.Label("Int:"))
      self.int = IntEntry(3)
      self.int.set_editable(False)
      hbox3.pack_start(self.int)
      vbox2.pack_start(hbox3)

      hbox2.pack_start(vbox2)

      vbox2 = gtk.VBox()
      hbox3 = gtk.HBox()
      hbox3.pack_start(gtk.Label("Con:"))
      self.con = IntEntry(3)
      self.con.set_editable(False)
      hbox3.pack_start(self.con)
      vbox2.pack_start(hbox3)

      hbox3 = gtk.HBox()
      hbox3.pack_start(gtk.Label("Wis:"))
      self.wis = IntEntry(3)
      self.wis.set_editable(False)
      hbox3.pack_start(self.wis)
      vbox2.pack_start(hbox3)

      hbox2.pack_start(vbox2)

      vbox2 = gtk.VBox()
      hbox3 = gtk.HBox()
      hbox3.pack_start(gtk.Label("Dex:"))
      self.dex = IntEntry(3)
      self.dex.set_editable(False)
      hbox3.pack_start(self.dex)
      vbox2.pack_start(hbox3)

      hbox3 = gtk.HBox()
      hbox3.pack_start(gtk.Label("Cha:"))
      self.cha = IntEntry(3)
      self.cha.set_editable(False)
      hbox3.pack_start(self.cha)
      vbox2.pack_start(hbox3)

      hbox2.pack_start(vbox2)

      vbox.pack_start(hbox2)

      hbox2 = gtk.HBox()
      vbox2 = gtk.VBox()
      hbox3 = gtk.HBox()
      hbox3.pack_start(gtk.Label("Final"))
      self.level = IntEntry(3)
      self.level.set_editable(False)
      hbox3.pack_start(self.level)
      vbox2.pack_start(hbox3)

      hbox3 = gtk.HBox()
      hbox3.pack_start(gtk.Label("Task points:"))
      self.tps = IntEntry(5)
      self.tps.set_editable(False)
      hbox3.pack_start(self.tps)
      vbox2.pack_start(hbox3)

      hbox3 = gtk.HBox()
      hbox3.pack_start(gtk.Label("QPs used:"))
      self.qps = IntEntry(4)
      self.qps.set_editable(False)
      hbox3.pack_start(self.qps)
      vbox2.pack_start(hbox3)

      hbox2.pack_start(vbox2)
      vbox2 = gtk.VBox()
      hbox3 = gtk.HBox()
      hbox3.pack_start(gtk.Label("Experience:"))
      self.exp = IntEntry(5)
      self.exp.set_editable(False)
      hbox3.pack_start(self.exp)
      hbox3.pack_start(gtk.Label("M"))
      vbox2.pack_start(hbox3)

      hbox3 = gtk.HBox()
      hbox3.pack_start(gtk.Label("Gold:"))
      self.gold = IntEntry(5)
      self.gold.set_editable(False)
      hbox3.pack_start(self.gold)
      hbox3.pack_start(gtk.Label("k"))
      vbox2.pack_start(hbox3)

      hbox3 = gtk.HBox()
      hbox3.pack_start(gtk.Label("Exp saved:"))
      self.expsaved = IntEntry(4)
      self.expsaved.set_editable(False)
      hbox3.pack_start(self.expsaved)
      hbox3.pack_start(gtk.Label("M"))
      vbox2.pack_start(hbox3)

      hbox2.pack_start(vbox2)

      vbox.pack_start(hbox2)

      hbox.pack_start(vbox)

      self.add(hbox)

class qpsWindow(gtk.Frame):
   def __init__(self,onChange):
      gtk.Frame.__init__(self,"QUEST POINTS")
      self.set_border_width(3)
      self.recalcFunc = onChange
      hbox = gtk.HBox()
      hbox.pack_start(gtk.Label("Enter"))
      self.qps = IntEntry(5)
      self.qps.connect("changed",self.on_edit)
      hbox.pack_start(self.qps)
      hbox.pack_start(gtk.Label("qps"))

      self.add(hbox)
   def on_edit(self,editable):
      try:
         editable.value = int(editable.get_text())
      except ValueError:
         editable.value = 0
      self.recalcFunc()

class wishWindow(gtk.Frame):
   def __init__(self,onChange):
      gtk.Frame.__init__(self,"WISHES")
      self.set_border_width(3)
      self.recalcFunc = onChange
      vbox = gtk.VBox()

      self.wish1 = gtk.CheckButton("Better stats")
      self.wish1.set_active(False)
      self.wish1.connect("toggled",self.toggle_cb)
      vbox.pack_start(self.wish1)

      self.wish2 = gtk.CheckButton("Better techniques")
      self.wish2.set_active(False)
      self.wish2.connect("toggled",self.toggle_cb)
      vbox.pack_start(self.wish2)

      self.wish3 = gtk.CheckButton("Better spells")
      self.wish3.set_active(False)
      self.wish3.connect("toggled",self.toggle_cb)
      vbox.pack_start(self.wish3)

      self.wish4 = gtk.CheckButton("Lesser physical improvement")
      self.wish4.set_active(False)
      self.wish4.connect("toggled",self.toggle_cb)
      vbox.pack_start(self.wish4)

      self.wish5 = gtk.CheckButton("Lesser magical improvement")
      self.wish5.set_active(False)
      self.wish5.connect("toggled",self.toggle_cb)
      vbox.pack_start(self.wish5)

      self.wish6 = gtk.CheckButton("Lesser casting speed")
      self.wish6.set_active(False)
      self.wish6.connect("toggled",self.toggle_cb)
      vbox.pack_start(self.wish6)

      self.wish7 = gtk.CheckButton("Lesser critical blow")
      self.wish7.set_active(False)
      self.wish7.connect("toggled",self.toggle_cb)
      vbox.pack_start(self.wish7)

      self.wish8 = gtk.CheckButton("True seeing")
      self.wish8.set_active(False)
      self.wish8.connect("toggled",self.toggle_cb)
      vbox.pack_start(self.wish8)

      self.wish9 = gtk.CheckButton("Thick skin")
      self.wish9.set_active(False)
      self.wish9.connect("toggled",self.toggle_cb)
      vbox.pack_start(self.wish9)

      self.wish10 = gtk.CheckButton("Superior stats")
      self.wish10.set_active(False)
      self.wish10.connect("toggled",self.toggle_cb)
      vbox.pack_start(self.wish10)

      self.wish11 = gtk.CheckButton("Superior techniques")
      self.wish11.set_active(False)
      self.wish11.connect("toggled",self.toggle_cb)
      vbox.pack_start(self.wish11)

      self.wish12 = gtk.CheckButton("Superior spells")
      self.wish12.set_active(False)
      self.wish12.connect("toggled",self.toggle_cb)
      vbox.pack_start(self.wish12)

      self.wish13 = gtk.CheckButton("Greater physical improvement")
      self.wish13.set_active(False)
      self.wish13.connect("toggled",self.toggle_cb)
      vbox.pack_start(self.wish13)

      self.wish14 = gtk.CheckButton("Greater magical improvement")
      self.wish14.set_active(False)
      self.wish14.connect("toggled",self.toggle_cb)
      vbox.pack_start(self.wish14)

      self.wish15 = gtk.CheckButton("Greater casting speed")
      self.wish15.set_active(False)
      self.wish15.connect("toggled",self.toggle_cb)
      vbox.pack_start(self.wish15)

      self.wish16 = gtk.CheckButton("Greater critical blow")
      self.wish16.set_active(False)
      self.wish16.connect("toggled",self.toggle_cb)
      vbox.pack_start(self.wish16)

      self.add(vbox)
   def toggle_cb(self,button):
      self.recalcFunc()

class skillspells(gtk.ScrolledWindow):
   def __init__(self,onChange,datastore,parent):
      # init "ScrolledWindow class"
      # pack in the necessary
      # should take model from outside source
      # so it can be cleared and such as needed
      # or make the model excessable from outside
      self.recalcFunc = onChange
      self.datastore = datastore
      self.parentWindow = parent
      gtk.ScrolledWindow.__init__(self)
      self.set_border_width(3)

      self.set_shadow_type(gtk.SHADOW_ETCHED_IN)
      self.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)


      self.model = self.__create_model()

      treeview = gtk.TreeView(self.model)
      treeview.get_selection().set_mode(gtk.SELECTION_SINGLE)

      self.__add_columns(treeview)
      treeview.connect("button-release-event",self.on_active)

      self.add(treeview)


   def __create_model(self):
      model = gtk.ListStore(
         gobject.TYPE_STRING,
         gobject.TYPE_INT,
         gobject.TYPE_INT
      )
      return model

   def __add_columns(self, treeview):
      model = treeview.get_model()

      # name column
      renderer = gtk.CellRendererText()
      column = gtk.TreeViewColumn("name",renderer,text=COLUMN_NAME)

      treeview.append_column(column)

      # max skill/spell %
      renderer = gtk.CellRendererText()
      column = gtk.TreeViewColumn("max",renderer,text=COLUMN_MAX)

      treeview.append_column(column)

      # currently studied/trained %
      renderer = gtk.CellRendererText()
      renderer.connect("edited",self.on_cell_edited,(model,COLUMN_CURRENT))
      renderer.set_property('editable',True)
      column = gtk.TreeViewColumn("cur",renderer,text=COLUMN_CURRENT)

      treeview.append_column(column)



   def on_cell_edited(self, cell, path, new_text, model):
      liststore, column = model
      # need to do mod 5 and 0 < < max checking
      try:
         percent = int(new_text)
      except ValueError:
         # can just return since we are not changing anything
         return
      percent = min(liststore[path][1],max(0,percent))
      percent = percent - percent%5
      liststore[path][column] = percent
      self.recalcFunc()
      return

   def on_active(self,w,event):
      if event.get_state() & gtk.gdk.BUTTON3_MASK:
         (store, iter) = w.get_selection().get_selected()
         name = store.get_value(iter,0)
         dialog = DataShow(self.parentWindow,name,self.datastore[name])
         if dialog.run() != gtk.RESPONSE_NONE:
            dialog.destroy()
      elif event.get_state() & gtk.gdk.BUTTON2_MASK:
        (store, iter) = w.get_selection().get_selected()
        store.set_value(iter, 2, store.get_value(iter, 1))
      return False



class Base:

   def __init__(self):
      self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
      self.window.connect("destroy", lambda *w: gtk.main_quit())
      self.window.set_default_size(840,500)
      self.datastore = datastore.datastore()

      hbox = gtk.HBox()

      vbox = gtk.VBox(True)
      self.charData = charDataWindow()
      vbox.pack_start(self.charData)
      self.raceW = raceWindow(self.datastore.races,
                              self.datastore.racedesc, self.recalc,self.window)
      vbox.pack_start(self.raceW)
      self.guild = guildWindow(self.datastore.guildstore,self.recalc,self.window)
      vbox.pack_start(self.guild)
      hbox.pack_start(vbox)

      vbox = gtk.VBox()
      self.wishes = wishWindow(self.recalc)
      vbox.pack_start(self.wishes)
      self.statTraining = trainedStatsWindow(self.recalc,self.datastore.statcost)
      vbox.pack_start(self.statTraining)
      self.questPoints = qpsWindow(self.recalc)
      vbox.pack_start(self.questPoints)

      hbox.pack_start(vbox)


      frame = gtk.Frame("TRAIN and STUDY")
      frame.set_border_width(3)
      vbox = gtk.VBox()
      self.skills = skillspells(self.recalc,self.datastore.skilldesc,
                                self.window)
      vbox.pack_start(self.skills)
      self.spells = skillspells(self.recalc,self.datastore.spelldesc,
                                self.window)
      vbox.pack_start(self.spells)

      frame.add(vbox)

      self.spells.model.clear()
      self.skills.model.clear()

      hbox.pack_start(frame)

      vbox = gtk.VBox()
      vbox.pack_start(hbox)
      self.writeButton = gtk.Button("Write Out")
      self.writeButton.connect("clicked",self.write_out)
      vbox.pack_start(self.writeButton)
      self.window.add(vbox)

      self.window.show_all()
   def guildadd(self,model,path,iter,guilddict):
      guild = model[path][0]
      if model[path][2] > 0:
         if guilddict.has_key(guild):
            guilddict[guild] += model[path][2]
         else:
            guilddict[guild] = model[path][2]


   def recalc(self):
      # first, calculate max skills and max spells
      maxskill = int(self.raceW.skillmax.get_text())
      if self.wishes.wish2.get_active():
         maxskill += 5
      if self.wishes.wish11.get_active():
         maxskill += 10
      self.charData.skillmax.set_text(str(maxskill))

      maxspell = int(self.raceW.spellmax.get_text())
      if self.wishes.wish3.get_active():
         maxspell += 5
      if self.wishes.wish12.get_active():
         maxspell += 10
      self.charData.spellmax.set_text(str(maxspell))

      # list all the guilds
      guilds = {}
      self.guild.guildstore.foreach(self.guildadd,guilds)
      # calculate what the new max learnable skills/spells are
      skills = {}
      spells = {}
      for k,l in guilds.iteritems():
         tempspell = self.datastore.guildstore.guilds[k].level[l].spells
         for i, j in tempspell.iteritems():
            spellname = i
            percent = int(((j/5)*maxspell)/100)*5
            if percent == 0:
               percent = 5
            if spells.has_key(spellname):
               percent = max(percent,spells[spellname])
            spells[spellname] = percent
         tempskill = self.datastore.guildstore.guilds[k].level[l].skills
         for i, j in tempskill.iteritems():
            skillname = i
            percent = int(((j/5)*maxskill)/100)*5
            if percent == 0:
               percent = 5
            if skills.has_key(skillname):
               percent = max(percent,skills[skillname])
            skills[skillname] = percent


      removeN = []
      # iterate over the liststores,
      self.spells.model.foreach(self.skillspell_update_cb,(spells,removeN))
      removeN.reverse()
      for path in removeN:
         self.spells.model.remove(self.spells.model.get_iter(path))
      for i, j in spells.iteritems():
         self.spells.model.append([i,j,0])

      removeN = []
      self.skills.model.foreach(self.skillspell_update_cb,(skills,removeN))
      removeN.reverse()
      for path in removeN:
         self.skills.model.remove(self.skills.model.get_iter(path))
      for i, j in skills.iteritems():
         self.skills.model.append([i,j,0])
      self.spells.model.set_sort_column_id(0,gtk.SORT_ASCENDING)
      self.skills.model.set_sort_column_id(0,gtk.SORT_ASCENDING)
      # either modifying the max/current
      # or putting the path in a list to be removed in reverse latter


      # calculate stats. str, etc first then hp,sp, etc
      # stats wishes

      # calculate by adding up all bonuses, +100,
      # then reducing by racial effectiveness

      self.str = 100
      self.int = 100
      self.con = 100
      self.wis = 100
      self.dex = 100
      self.cha = 100
      self.hpmax = 0
      self.spmax = 0
      self.hpr = 0
      self.spr = 0

      if self.wishes.wish1.get_active():
			self.str += 15
			self.int += 15
			self.con += 15
			self.wis += 15
			self.dex += 15
			self.cha += 15
      if self.wishes.wish10.get_active():
			self.str += 30
			self.int += 30
			self.con += 30
			self.wis += 30
			self.dex += 30
			self.cha += 30
      # trained stats
      self.str += int(self.statTraining.str.value)
      self.int += int(self.statTraining.int.value)
      self.con += int(self.statTraining.con.value)
      self.wis += int(self.statTraining.wis.value)
      self.dex += int(self.statTraining.dex.value)
      self.cha += int(self.statTraining.cha.value)
      # guild stats
      totallevels = 0
      for i,j in guilds.iteritems():
         level = self.datastore.guildstore.guilds[i].level[j]
         totallevels += j
         self.str += level.str
         self.int += level.int
         self.con += level.con
         self.wis += level.wis
         self.dex += level.dex
         self.cha += level.cha
         self.hpmax += level.hpmax
         self.spmax += level.spmax
         self.spr += level.spr
         self.hpr += level.hpr
      guildlevels = totallevels
      totallevels += int(self.guild.freelvl.value)

      # apply racial effectiveness
      self.str = int((int(self.raceW.str.get_text())*self.str)/100)
      self.int = int((int(self.raceW.int.get_text())*self.int)/100)
      self.con = int((int(self.raceW.con.get_text())*self.con)/100)
      self.wis = int((int(self.raceW.wis.get_text())*self.wis)/100)
      self.dex = int((int(self.raceW.dex.get_text())*self.dex)/100)
      self.cha = int((int(self.raceW.cha.get_text())*self.cha)/100)

      self.charData.str.set_text(str(self.str))
      self.charData.int.set_text(str(self.int))
      self.charData.con.set_text(str(self.con))
      self.charData.wis.set_text(str(self.wis))
      self.charData.dex.set_text(str(self.dex))
      self.charData.cha.set_text(str(self.cha))

      # lesser and greater improvements wishes
      if self.wishes.wish4.get_active():
         self.hpmax += int(0.75*int(self.raceW.con.get_text()) + 0.5*int(self.raceW.siz.get_text())+25)
      if self.wishes.wish5.get_active():
         self.spmax += int(0.75*int(self.raceW.int.get_text()) + 0.5*int(self.raceW.wis.get_text())+50)
      if self.wishes.wish13.get_active():
         self.hpmax += int(1.5*int(self.raceW.con.get_text()) + int(self.raceW.siz.get_text())+50)
      if self.wishes.wish14.get_active():
         self.spmax += int(1.5*int(self.raceW.int.get_text()) + int(self.raceW.wis.get_text())+100)

      self.hpmax += 2*int(self.raceW.siz.get_text())+self.con*3
      self.spmax += 3*self.wis + 4*self.int
      self.spr += int(self.raceW.spr.get_text())
      self.hpr += int(self.raceW.hpr.get_text())


      self.charData.hpregen.set_text(str(self.hpr))
      self.charData.spregen.set_text(str(self.spr))
      self.charData.hpmax.set_text(str(self.hpmax))
      self.charData.spmax.set_text(str(self.spmax))

      self.charData.level.set_text(str(totallevels))

      # calculate exp needed
      # exp from levels
      self.exp = 0
      qpslevel = self.datastore.qps.findlevel(self.questPoints.qps.value)
      if qpslevel > totallevels:
         qpslevel = totallevels
      self.exp += self.datastore.lvlcosts.expneeded(qpslevel)
      # exp saved with qps
      self.charData.expsaved.set_text(str(int(round((self.exp*25)/100/1000000))))

      self.exp = int(round((self.exp*75)/100))

      self.exp += self.datastore.lvlcosts.expneeded(totallevels) - self.datastore.lvlcosts.expneeded(qpslevel)
      # exp from guildlevels
      self.exp += int(round((self.datastore.lvlcosts.expneeded(guildlevels)*40)/100))


      # and qps used
      self.charData.qps.set_text(str(self.datastore.qps.qpsneeded(qpslevel)))

      # exp from spells/skills
      skillcost = int(self.raceW.skillcost.get_text())
      goldcost = 0
      for row in self.skills.model:
         (expcost, goldC)= self.datastore.skills.cost(row[0],row[2],skillcost)
         self.exp += expcost
         goldcost += goldC
      spellcost = int(self.raceW.spellcost.get_text())
      for row in self.spells.model:
         (expcost, goldC) = self.datastore.spells.cost(row[0],row[2],spellcost)
         self.exp += expcost
         goldcost += goldC

      # and gold needed
      self.charData.gold.set_text(str(2 * int(round(goldcost/1000) / 3)))

      # exp from stats
      self.exp += self.datastore.statcost[max(min(self.statTraining.str.value,50),0)]
      self.exp += self.datastore.statcost[max(min(self.statTraining.con.value,50),0)]
      self.exp += self.datastore.statcost[max(min(self.statTraining.dex.value,50),0)]
      self.exp += self.datastore.statcost[max(min(self.statTraining.int.value,50),0)]
      self.exp += self.datastore.statcost[max(min(self.statTraining.wis.value,50),0)]
      self.exp += self.datastore.statcost[max(min(self.statTraining.cha.value,50),0)]

      self.charData.exp.set_text(str(int(round(self.exp/1000000))))
      # calculate tps
      lessertotal = 0
      greatertotal = 0
      if self.wishes.wish1.get_active():
         lessertotal += 1
      if self.wishes.wish2.get_active():
         lessertotal += 1
      if self.wishes.wish3.get_active():
         lessertotal += 1
      if self.wishes.wish4.get_active():
         lessertotal += 1
      if self.wishes.wish5.get_active():
         lessertotal += 1
      if self.wishes.wish6.get_active():
         lessertotal += 1
      if self.wishes.wish7.get_active():
         lessertotal += 1
      if self.wishes.wish8.get_active():
         lessertotal += 1
      if self.wishes.wish9.get_active():
         lessertotal += 1
      if self.wishes.wish10.get_active():
         greatertotal += 1
      if self.wishes.wish11.get_active():
         greatertotal += 1
      if self.wishes.wish12.get_active():
         greatertotal += 1
      if self.wishes.wish13.get_active():
         greatertotal += 1
      if self.wishes.wish14.get_active():
         greatertotal += 1
      if self.wishes.wish15.get_active():
         greatertotal += 1
      if self.wishes.wish16.get_active():
         greatertotal += 1

      tpstotal = self.datastore.tps.lesser[lessertotal]
      tpstotal += self.datastore.tps.greater[greatertotal]
      self.charData.tps.set_text(str(tpstotal))


   def skillspell_update_cb(self,model,path,iter,data):
      try:
         model[path][1] = data[0][model[path][0]]
         model[path][2] = min(model[path][1],model[path][2])
         del data[0][model[path][0]]
      except KeyError:
         data[1].append(path)
      return False
   def write_guild(self,rows,fileobj,indent):
      if not rows:
         return None
      for row in rows:
         if row[2] > 0:
            print >> fileobj,indent + row[0], row[2], "levels"
         self.write_guild(row.iterchildren(),fileobj,"  " + indent)
      return None

   def write_out(self,w):
      filesel = gtk.FileSelection()
      filesel.set_filename("example.txt")
      self.filedrop = "example.txt"
      filesel.cancel_button.connect("clicked",
                                 lambda w: filesel.destroy())
      filesel.ok_button.connect("clicked",self.get_filename,filesel)
      filesel.run()
      filesel.destroy()
      fileobj = open(self.filedrop,"w")
      print >> fileobj, "Z O M B I E M U D   C H A R A C T E R C R E A T O R"
      print >> fileobj
      print >> fileobj, "---------------------------------------------------"
      print >> fileobj, "RACE:",self.raceW.curr_race
      print >> fileobj, "---------------------------------------------------"
      print >> fileobj
      print >> fileobj, "GUILDS"
      print >> fileobj, "---------------------------------------------------"
      self.write_guild(self.guild.guildstore,fileobj,"")
      print >> fileobj
      print >> fileobj, "RESULTING CHARACTER"
      print >> fileobj, "---------------------------------------------------"
      print >> fileobj, "Hpmax:          ", self.charData.hpmax.get_text()
      print >> fileobj, "Spmax:          ", self.charData.spmax.get_text()
      print >> fileobj, "Hpregen:        ", self.charData.hpregen.get_text()
      print >> fileobj, "Spregen:        ", self.charData.spregen.get_text()
      print >> fileobj, "Skillmax:       ", self.charData.skillmax.get_text()
      print >> fileobj, "Spellmax:       ", self.charData.spellmax.get_text()
      print >> fileobj, "Str:            ", self.charData.str.get_text()
      print >> fileobj, "Con:            ", self.charData.con.get_text()
      print >> fileobj, "Dex:            ", self.charData.dex.get_text()
      print >> fileobj, "Int:            ", self.charData.int.get_text()
      print >> fileobj, "Wis:            ", self.charData.wis.get_text()
      print >> fileobj, "Cha:            ", self.charData.cha.get_text()
      print >> fileobj, "Final level:    ", self.charData.level.get_text()
      print >> fileobj, "Task points:    ", self.charData.tps.get_text()
      print >> fileobj, "Quest Points:   ", self.charData.qps.get_text()
      print >> fileobj, "Experience:     ", self.charData.exp.get_text(),"M"
      print >> fileobj, "Gold Cost:      ", self.charData.gold.get_text(), "k"
      print >> fileobj
      print >> fileobj, "WISHES"
      print >> fileobj, "---------------------------------------------------"
      wishes = False
      print >> fileobj, "Lesser Wishes:"
      if self.wishes.wish1.get_active():
         print >> fileobj, ' ' + self.wishes.wish1.get_label()
         wishes = True
      if self.wishes.wish2.get_active():
         print >> fileobj, ' ' + self.wishes.wish2.get_label()
         wishes = True
      if self.wishes.wish3.get_active():
         print >> fileobj, ' ' + self.wishes.wish3.get_label()
         wishes = True
      if self.wishes.wish4.get_active():
         print >> fileobj, ' ' + self.wishes.wish4.get_label()
         wishes = True
      if self.wishes.wish5.get_active():
         print >> fileobj, ' ' + self.wishes.wish5.get_label()
         wishes = True
      if self.wishes.wish6.get_active():
         print >> fileobj, ' ' + self.wishes.wish6.get_label()
         wishes = True
      if self.wishes.wish7.get_active():
         print >> fileobj, ' ' + self.wishes.wish7.get_label()
         wishes = True
      if self.wishes.wish8.get_active():
         print >> fileobj, ' ' + self.wishes.wish8.get_label()
         wishes = True
      if self.wishes.wish9.get_active():
         print >> fileobj, ' ' + self.wishes.wish9.get_label()
         wishes = True
      if not wishes:
         print >> fileobj, ' ' + "None"
      wishes = False
      print >> fileobj, "Greater Wishes:"
      if self.wishes.wish10.get_active():
         print >> fileobj, ' ' + self.wishes.wish10.get_label()
         wishes = True
      if self.wishes.wish11.get_active():
         print >> fileobj, ' ' + self.wishes.wish11.get_label()
         wishes = True
      if self.wishes.wish12.get_active():
         print >> fileobj, ' ' + self.wishes.wish12.get_label()
         wishes = True
      if self.wishes.wish13.get_active():
         print >> fileobj, ' ' + self.wishes.wish13.get_label()
         wishes = True
      if self.wishes.wish14.get_active():
         print >> fileobj, ' ' + self.wishes.wish14.get_label()
         wishes = True
      if self.wishes.wish15.get_active():
         print >> fileobj, ' ' + self.wishes.wish15.get_label()
         wishes = True
      if self.wishes.wish16.get_active():
         print >> fileobj, ' ' + self.wishes.wish16.get_label()
         wishes = True
      if not wishes:
         print >> fileobj, ' ' + "None"

      print >> fileobj
      print >> fileobj, "STAT TRAINING"
      print >> fileobj, "---------------------------------------------------"
      if self.statTraining.str.value:
        print >> fileobj, 'Str: ' + str(self.statTraining.str.value)
      if self.statTraining.int.value:
        print >> fileobj, 'Int: ' + str(self.statTraining.int.value)
      if self.statTraining.con.value:
        print >> fileobj, 'Con: ' + str(self.statTraining.con.value)
      if self.statTraining.wis.value:
        print >> fileobj, 'Wis: ' + str(self.statTraining.wis.value)
      if self.statTraining.dex.value:
        print >> fileobj, 'Dex: ' + str(self.statTraining.dex.value)
      if self.statTraining.cha.value:
        print >> fileobj, 'Cha: ' + str(self.statTraining.cha.value)

      print >> fileobj
      print >> fileobj, "SKILLS"
      print >> fileobj, "---------------------------------------------------"
      found = False
      for row in self.skills.model:
         if row[2] > 0:
            found = True
            print >> fileobj, row[0],row[2],"/",row[1]
      if not found:
        print >> fileobj, "None"
      print >> fileobj
      print >> fileobj, "SPELLS"
      print >> fileobj, "---------------------------------------------------"
      found = False
      for row in self.spells.model:
         if row[2] > 0:
            found = True
            print >> fileobj, row[0],row[2],"/",row[1]
      if not found:
        print >> fileobj, "None"
      fileobj.close()

   def get_filename(self,w,filesel):
      self.filedrop = filesel.get_filename()

   def main(self):
      old_cwd = os.getcwd()
      try:
        os.chdir(os.path.dirname(sys.argv[0]))
        gtk.main()
      finally:
        os.chdir(old_cwd)


if __name__ == "__main__":
   base = Base()
   base.main()
