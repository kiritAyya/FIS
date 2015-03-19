import Tkinter
import tkMessageBox
import MySQLdb
import re
import sys
from PIL import Image, ImageTk
from time import gmtime, strftime

class FootApp(Tkinter.Tk):
	def __init__(self,parent):
		Tkinter.Tk.__init__(self,parent)
		self.parent = parent
		self.initialize()

	def initialize(self):
		self.grid()
		self.resizable(False,False)
		#im = Tkinter.PhotoImage(file="/home/kirit/Desktop/Python_pgs/images.jpg")
		#myvar = Tkinter.Label(self,image = im)
		#myvar.image = im
		#myvar.place(x=10,y=0)
		self.db = MySQLdb.connect("localhost","root","user","football")
		self.cur = self.db.cursor()
		self.Games = Tkinter.Button(self,text=u"Games",command=self.LeagueWindow)
		self.Standings = Tkinter.Button(self,text=u"Points Table",command=self.PointsTable)
		self.TeamSearch = Tkinter.Button(self,text=u"Search",command=self.TeamSearch)
		self.Exit = Tkinter.Button(self,text=u"Exit",command=self.destroy)
		self.BPL = Tkinter.Button(self,text=u"Barclays Premier League",command=self.OnClickBPL)
		self.ISL = Tkinter.Button(self,text=u"Indian Super League",command=self.OnClickISL)
		self.Exit.grid(column=0,row=6,pady=5)
		self.Standings.grid(column=0,row=0,pady=5)
		self.Games.grid(column=0,row=1,pady=5)
		self.TeamSearch.grid(column=0,row=2,pady=5)
		self.BPL.grid(column=0,row=3,pady=5)
		self.ISL.grid(column=0,row=4,pady=5)
		self.grid_columnconfigure(0,weight=1)
		self.geometry("300x280+300+300")

	def OnClickBPL(self):																							
		self.BPL_win = Tkinter.Toplevel()
		self.BPL_win.title('Barclays Premier League')
		#im = Tkinter.PhotoImage(file="/home/kirit/Desktop/Python_pgs/BPL.jpg")
		#myvar = Tkinter.Label(self.BPL_win,image = im)
		#myvar.image = im
		#myvar.place(x=0,y=0)
		self.stats = Tkinter.Button(self.BPL_win,text=u"Statistics",command=self.NewWindStats)
		self.teams = Tkinter.Button(self.BPL_win,text=u"Teams",command=self.NewWind)
		self.lineups =  Tkinter.Button(self.BPL_win,text=u"Team Lineups",command=self.LineUps)
		self.upcoming = Tkinter.Button(self.BPL_win,text=u"Upcoming Games",command=self.UpG)
		self.Exit = Tkinter.Button(self.BPL_win,text=u"Cancel",command=self.BPL_win.destroy)
		self.Exit.grid(column=0,row=5,pady=30)
		self.stats.grid(column=0,row=0,pady=30)
		self.teams.grid(column=0,row=1,pady=30)
		self.lineups.grid(column=0,row=2,pady=30)
		self.upcoming.grid(column=0,row=3,pady=30)
		self.BPL_win.grid_columnconfigure(0, weight=1)
		self.resizable(False,False)
		self.BPL_win.geometry("450x450+300+300")
	
	def  NewWindStats(self):
		show_full_table = """SELECT team_name,stats 
							 FROM teams
							 WHERE league_name='Barclays Premier League'"""
		self.cur.execute(show_full_table)
		res = self.cur.fetchall()
		self.display_stuff = Tkinter.StringVar()
		self.res_wind = Tkinter.Toplevel()
		self.res_wind.title('Statistics')
		self.res_wind.geometry("300x200+300+300")
		self.res_wind.resizable(False,False)
		self.res_wind.grid()
		self.line=2.0
		self.display = Tkinter.Text(self.res_wind,height=100,width=100)
		self.display.grid(column=0,row=0,columnspan=2,rowspan=15)
		self.display.config(state="normal")
		self.display.delete(1.0, "end")
		self.display_stuff.set(u" Team\t\t\tTimes Won\n\n")
		self.display.insert(1.0,self.display_stuff.get())
		for row in res:
			self.display_stuff.set(" "+row[0]+"\t\t\t"+str(row[1])+"\n")
			self.display.insert(self.line,self.display_stuff.get())
			self.line += 1.0
		self.display.config(state="disabled")

	def NewWind(self):
		show_full_table = """SELECT team_name 
							 FROM teams
							 WHERE league_name='Barclays Premier League'"""
		self.cur.execute(show_full_table)
		res = self.cur.fetchall()
		self.display_stuff = Tkinter.StringVar()
		self.res_wind = Tkinter.Toplevel()
		self.res_wind.title('Teams')
		self.res_wind.geometry("200x200+300+300")
		self.res_wind.resizable(False,False)
		self.res_wind.grid()
		self.line=2.0
		self.display = Tkinter.Text(self.res_wind,height=100,width=100)
		self.display.grid(column=0,row=0,columnspan=2,rowspan=15)
		self.display.config(state="normal")
		self.display.delete(1.0, "end")
		self.display_stuff.set(u"           Team\n\n")
		self.display.insert(1.0,self.display_stuff.get())
		for row in res:
			self.display_stuff.set(" "+row[0]+"\n")
			self.display.insert(self.line,self.display_stuff.get())
			self.line += 1.0
		self.display.config(state="disabled")

	def LineUps(self):
		self.search_win = Tkinter.Toplevel()
		self.search_win.title('Search')
		self.search_win.geometry("300x100+300+300")
		self.search_win.resizable(False,False)
		self.search_win.grid()
		self.TE = Tkinter.StringVar()
		self.team_entry = Tkinter.Entry(self.search_win,textvariable=self.TE)
		self.team_entry.grid(column=0,row=0,pady=10,padx=10,columnspan=5)
		self.team_entry.bind("<Return>",self.LineUpsonEnter)
		self.Exit = Tkinter.Button(self.search_win,text=u"Cancel",command=self.search_win.destroy)
		self.Exit.grid(column=0,row=1,pady=5)
		self.search_win.grid_columnconfigure(0,weight=1)
		self.TE.set(u"Type team name here...")
		self.team_entry.focus_set()
		self.team_entry.selection_range(0, Tkinter.END)

	def LineUpsonEnter(self,event):
		query = """SELECT player_name,player_pos
				   FROM players
				   WHERE team = '%s'""" %(self.TE.get())
		self.cur.execute(query)
		res = self.cur.fetchall()
		self.display_stuff = Tkinter.StringVar()
		self.res_wind = Tkinter.Toplevel()
		self.res_wind.title('%s Lineup'%(self.TE.get()))
		self.res_wind.geometry("300x200+300+300")
		self.res_wind.resizable(False,False)
		self.res_wind.grid()
		self.line=2.0
		self.display = Tkinter.Text(self.res_wind,height=100,width=100)
		self.display.grid(column=0,row=0,columnspan=2,rowspan=15)
		self.display.config(state="normal")
		self.display.delete(1.0, "end")
		self.display_stuff.set(u" Player Name\t\t\t\tPos.\n\n")
		self.display.insert(1.0,self.display_stuff.get())
		for row in res:
			self.display_stuff.set(" "+row[0]+"\t\t\t\t"+row[1]+"\n")
			self.display.insert(self.line,self.display_stuff.get())
			self.line += 1.0
		self.display.config(state="disabled")
		

	def UpG(self):
		local_date = strftime("%d-%m-%Y", gmtime())
		for i in range(0,len(local_date)):
			_date = str(local_date[0])+str(local_date[1])
			_month = str(local_date[3])+str(local_date[4])
			_year = str(local_date[8])+str(local_date[9])
		_date = int(_date)
		_month = int(_month)
		_year = int(_year)

		query = """SELECT DISTINCT league.date,Team_1,Team_2,Time
				   FROM league,game
				   WHERE league.date = game.date AND
				   league.date IN
				   (SELECT league.date
				   	FROM league
				   	WHERE league.league = 'Barclays Premier League') """
		self.cur.execute(query)
		res = self.cur.fetchall()
		self.display_stuff = Tkinter.StringVar()
		self.res_wind = Tkinter.Toplevel()
		self.res_wind.title('Upcoming Fixtures')
		self.res_wind.geometry("500x200+300+300")
		self.res_wind.resizable(False,False)
		self.res_wind.grid()
		self.line=2.0
		self.display = Tkinter.Text(self.res_wind,height=100,width=100)
		self.display.grid(column=0,row=0,columnspan=2,rowspan=15)
		self.display.config(state="normal")
		self.display.delete(1.0, "end")
		self.display_stuff.set(u"  Date\t\t\tMatch\t\t\t\tTiming\n\n")
		self.display.insert(1.0,self.display_stuff.get())
		for row in res:
			temp = row[0]
			_temp_d = str(temp[0])+str(temp[1])
			_temp_m = str(temp[3])+str(temp[4])
			_temp_y = str(temp[6])+str(temp[7])
			_temp_d = int(_temp_d)
			_temp_y = int(_temp_y)
			_temp_m = int(_temp_m)

			if _temp_d >= _date and _temp_m >= _month:
				self.display_stuff.set(" "+row[0]+"\t\t"+row[1]+" vs. "+row[2]+"\t\t\t\t\t"+row[3]+"\n")
				self.display.insert(self.line,self.display_stuff.get())
				self.line += 1.0		
		self.display.config(state="disabled")


	def OnClickISL(self):
		self.ISL_win = Tkinter.Toplevel()
		self.ISL_win.title('Indina Super League')
		#im = Tkinter.PhotoImage(file="/home/kirit/Desktop/Python_pgs/ISL.jpg")
		#myvar = Tkinter.Label(self.ISL_win,image = im)
		#myvar.image = im
		#myvar.place(x=0,y=0)
		self.stats = Tkinter.Button(self.ISL_win,text=u"Statistics",command=self.ISLNewWindStats)
		self.teams = Tkinter.Button(self.ISL_win,text=u"Teams",command=self.ISLNewWind)
		self.lineups =  Tkinter.Button(self.ISL_win,text=u"Team Lineups",command=self.ISLLineUps)
		self.upcoming = Tkinter.Button(self.ISL_win,text=u"Upcoming Games",command=self.ISLUpG)
		self.Exit = Tkinter.Button(self.ISL_win,text=u"Cancel",command=self.ISL_win.destroy)
		self.Exit.grid(column=0,row=5,pady=30)
		self.stats.grid(column=0,row=0,pady=30)
		self.teams.grid(column=0,row=1,pady=30)
		self.lineups.grid(column=0,row=2,pady=30)
		self.upcoming.grid(column=0,row=3,pady=30)
		self.ISL_win.grid_columnconfigure(0, weight=1)
		self.resizable(False,False)
		self.ISL_win.geometry("450x450+300+300")
	
	def  ISLNewWindStats(self):
		show_full_table = """SELECT team_name,stats 
							 FROM teams
							 WHERE league_name='Indian Super League'"""
		self.cur.execute(show_full_table)
		res = self.cur.fetchall()
		self.display_stuff = Tkinter.StringVar()
		self.res_wind = Tkinter.Toplevel()
		self.res_wind.title('Statistics')
		self.res_wind.geometry("300x200+300+300")
		self.res_wind.resizable(False,False)
		self.res_wind.grid()
		self.line=2.0
		self.display = Tkinter.Text(self.res_wind,height=100,width=100)
		self.display.grid(column=0,row=0,columnspan=2,rowspan=15)
		self.display.config(state="normal")
		self.display.delete(1.0, "end")
		self.display_stuff.set(u" Team\t\t\tTimes Won\n\n")
		self.display.insert(1.0,self.display_stuff.get())
		for row in res:
			self.display_stuff.set(" "+row[0]+"\t\t\t"+str(row[1])+"\n")
			self.display.insert(self.line,self.display_stuff.get())
			self.line += 1.0
		self.display.config(state="disabled")

	def ISLNewWind(self):
		show_full_table = """SELECT team_name 
							 FROM teams
							 WHERE league_name='Indian Super League'"""
		self.cur.execute(show_full_table)
		res = self.cur.fetchall()
		self.display_stuff = Tkinter.StringVar()
		self.res_wind = Tkinter.Toplevel()
		self.res_wind.title('Teams')
		self.res_wind.geometry("200x200+300+300")
		self.res_wind.resizable(False,False)
		self.res_wind.grid()
		self.line=2.0
		self.display = Tkinter.Text(self.res_wind,height=100,width=100)
		self.display.grid(column=0,row=0,columnspan=2,rowspan=15)
		self.display.config(state="normal")
		self.display.delete(1.0, "end")
		self.display_stuff.set(u"           Team\n\n")
		self.display.insert(1.0,self.display_stuff.get())
		for row in res:
			self.display_stuff.set(" "+row[0]+"\n")
			self.display.insert(self.line,self.display_stuff.get())
			self.line += 1.0
		self.display.config(state="disabled")

	def ISLLineUps(self):
		self.search_win = Tkinter.Toplevel()
		self.search_win.title('Search')
		self.search_win.geometry("300x100+300+300")
		self.search_win.resizable(False,False)
		self.search_win.grid()
		self.TE = Tkinter.StringVar()
		self.team_entry = Tkinter.Entry(self.search_win,textvariable=self.TE)
		self.team_entry.grid(column=0,row=0,pady=10,padx=10,columnspan=5)
		self.team_entry.bind("<Return>",self.ISLLineUpsonEnter)
		self.Exit = Tkinter.Button(self.search_win,text=u"Cancel",command=self.search_win.destroy)
		self.Exit.grid(column=0,row=1,pady=5)
		self.search_win.grid_columnconfigure(0,weight=1)
		self.TE.set(u"Type team name here...")
		self.team_entry.focus_set()
		self.team_entry.selection_range(0, Tkinter.END)

	def ISLLineUpsonEnter(self,event):
		query = """SELECT player_name,player_pos
				   FROM players
				   WHERE team = '%s'""" %(self.TE.get())
		self.cur.execute(query)
		res = self.cur.fetchall()
		self.display_stuff = Tkinter.StringVar()
		self.res_wind = Tkinter.Toplevel()
		self.res_wind.title('%s Lineup'%(self.TE.get()))
		self.res_wind.geometry("300x200+300+300")
		self.res_wind.resizable(False,False)
		self.res_wind.grid()
		self.line=2.0
		self.display = Tkinter.Text(self.res_wind,height=100,width=100)
		self.display.grid(column=0,row=0,columnspan=2,rowspan=15)
		self.display.config(state="normal")
		self.display.delete(1.0, "end")
		self.display_stuff.set(u" Player Name\t\t\t\tPos.\n\n")
		self.display.insert(1.0,self.display_stuff.get())
		for row in res:
			self.display_stuff.set(" "+row[0]+"\t\t\t\t"+row[1]+"\n")
			self.display.insert(self.line,self.display_stuff.get())
			self.line += 1.0
		self.display.config(state="disabled")
		

	def ISLUpG(self):
		#local_date = strftime("%d-%m-%Y", gmtime())
		local_date = '05-10-2014'
		for i in range(0,len(local_date)):
			_date = str(local_date[0])+str(local_date[1])
			_month = str(local_date[3])+str(local_date[4])
			_year = str(local_date[8])+str(local_date[9])
		_date = int(_date)
		_month = int(_month)
		_year = int(_year)

		query = """SELECT DISTINCT league.date,Team_1,Team_2,Time
				   FROM league,game
				   WHERE league.date = game.date AND
				   league.date IN
				   (SELECT league.date
				   	FROM league
				   	WHERE league.league = 'Indian Super League') """
		self.cur.execute(query)
		res = self.cur.fetchall()
		self.display_stuff = Tkinter.StringVar()
		self.res_wind = Tkinter.Toplevel()
		self.res_wind.title('Upcoming Fixtures')
		self.res_wind.geometry("500x200+300+300")
		self.res_wind.resizable(False,False)
		self.res_wind.grid()
		self.line=2.0
		self.display = Tkinter.Text(self.res_wind,height=100,width=100)
		self.display.grid(column=0,row=0,columnspan=2,rowspan=15)
		self.display.config(state="normal")
		self.display.delete(1.0, "end")
		self.display_stuff.set(u"  Date\t\t\tMatch\t\t\t\tTiming\n\n")
		self.display.insert(1.0,self.display_stuff.get())
		for row in res:
			temp = row[0]
			if temp[0]=='2' and temp[1]=='-':
				_temp_d = str(0)+str(temp[0])
				_temp_m = str(temp[2])+str(temp[3])
				_temp_y = str(temp[5])+str(temp[6])
				_temp_d = int(_temp_d)
				_temp_y = int(_temp_y)
				_temp_m = int(_temp_m)
			else:
				_temp_d = str(temp[0])+str(temp[1])
				_temp_m = str(temp[3])+str(temp[4])
				_temp_y = str(temp[6])+str(temp[7])
				_temp_d = int(_temp_d)
				_temp_y = int(_temp_y)
				_temp_m = int(_temp_m)

			if _temp_d >= _date and _temp_m >= _month:
				self.display_stuff.set(" "+row[0]+"\t\t"+row[1]+" vs. "+row[2]+"\t\t\t\t\t"+row[3]+"\n")
				self.display.insert(self.line,self.display_stuff.get())
				self.line += 1.0		
		self.display.config(state="disabled")

	def LeagueWindow(self):
		show_full_table = """SELECT * FROM game;"""
		self.cur.execute(show_full_table)
		res = self.cur.fetchall()
		self.display_stuff = Tkinter.StringVar()
		self.res_wind = Tkinter.Toplevel()
		self.res_wind.title('Games')
		self.res_wind.geometry("580x400+300+300")
		self.res_wind.resizable(False,False)
		self.res_wind.grid()
		self.line=2.0
		self.display = Tkinter.Text(self.res_wind,height=100,width=100)
		self.display.grid(column=0,row=0,columnspan=2,rowspan=15)
		self.display.config(state="normal")
		self.display.delete(1.0, "end")
		self.display_stuff.set(u"  Date\t\t\tMatch\t\t\t\t\tTiming\n\n")
		self.display.insert(1.0,self.display_stuff.get())
		for row in res:
			self.display_stuff.set(" "+row[0]+"\t\t"+row[1]+" vs. "+row[2]+"\t\t\t\t\t\t"+row[3]+"\n")
			self.display.insert(self.line,self.display_stuff.get())
			self.line += 1.0
		self.display.config(state="disabled")

	def PointsTable(self):
		self.ask_wind = Tkinter.Toplevel()
		self.ask_wind.title('League Standings')
		self.ask_wind.geometry("300x100+200+300")
		labl = Tkinter.Label(self.ask_wind,text=u"Type in the league (BPL/ISL)")
		labl.grid(column=0,row=0,padx=15)
		self.ask_wind.resizable(False,False)
		self.leagueEnt = Tkinter.StringVar()
		self.ent = Tkinter.Entry(self.ask_wind,textvariable=self.leagueEnt)
		self.ent.grid(column=0,row=1,columnspan=3)
		self.ent.bind("<Return>",self.Onlclick)
		self.Exit = Tkinter.Button(self.ask_wind,text=u"Cancel",command=self.ask_wind.destroy)
		self.Exit.grid(column=0,row=5)
		self.ask_wind.grid_columnconfigure(0,weight=1)
		self.ent.focus_set()
		self.ent.selection_range(0, Tkinter.END)
	
	def Onlclick(self,event):	
		if self.leagueEnt.get() == "BPL":
			show_full_table = """SELECT pos,team_name,W,D,L,pts 
								 FROM points
								 WHERE l_name='%s'"""%(self.leagueEnt.get())
		elif self.leagueEnt.get() == "ISL":
			show_full_table = """SELECT pos,team_name,W,D,L,pts 
								 FROM points
								 WHERE l_name='%s'"""%(self.leagueEnt.get())
		else:
			tkMessageBox.showinfo("League Standings","Invalid Choice")
			self.ask_wind.destroy

		self.cur.execute(show_full_table)
		res = self.cur.fetchall()
		self.display_stuff = Tkinter.StringVar()
		self.res_wind = Tkinter.Toplevel()
		self.res_wind.title('League Standings')
		self.res_wind.geometry("450x180+300+300")
		self.res_wind.resizable(False,False)
		self.res_wind.grid()
		self.line=2.0
		self.display = Tkinter.Text(self.res_wind,height=10,width=100)
		self.display.grid(column=0,row=0,columnspan=2,rowspan=15)
		self.display.config(state="normal")
		self.display.delete(1.0, "end")
		self.display_stuff.set(u" Pos.\t\tTeam\t\t\tW\tD\tL\tP\n\n")
		self.display.insert(1.0,self.display_stuff.get())
		for row in res:
			self.display_stuff.set(" "+str(row[0])+"\t\t"+row[1]+"\t\t\t"+str(row[2])+"\t"+str(row[3])+"\t"+str(row[4])+"\t"+str(row[5])+"\n")
			self.display.insert(self.line,self.display_stuff.get())
			self.line += 1.0
		self.display.config(state="disabled")

	def TeamSearch(self):
		self.search = Tkinter.Toplevel()
		self.search.title('SEARCH')
		self.search.geometry("300x100+300+300")
		self.search.resizable(False,False)
		self.searchEntry = Tkinter.StringVar()
		self.entry = Tkinter.Entry(self.search,textvariable=self.searchEntry)
		self.searchEntry.set(u"Search here...")
		self.entry.grid(column=0,row=1,columnspan=5,padx=10,pady=10)
		self.entry.bind("<Return>",self.OnEnter)
		self.Exit = Tkinter.Button(self.search,text=u"Cancel",command=self.search.destroy)
		self.Exit.grid(column=0,row=5)
		self.search.grid_columnconfigure(0, weight=1)
		self.entry.focus_set()
		self.entry.selection_range(0,Tkinter.END)

	def OnEnter(self,event):
		Matches = re.match(r"^ALL\sMATCHES\sOF\sTEAM\s([A-Z\s*a-z]+)",str(self.searchEntry.get()),re.IGNORECASE)
		Score = re.match(r"^RESULT\sOF\sGAME\s([A-Z\s*a-z]+)\svs\s([A-Z\s*a-z]+)",str(self.searchEntry.get()),re.IGNORECASE)
		Leagues = re.match(r"^MATCHES\sOF\sLEAGUE\s([A-Z\s*a-z]+)",str(self.searchEntry.get()),re.IGNORECASE)
		Player_Stats = re.match(r"^TOP\sSCORER\sOF\sTEAM\s([A-Z\s*a-z]+)",str(self.searchEntry.get()),re.IGNORECASE)
		League_Scorer = re.match(r"^TOP\sSCORER\sOF\sLEAGUE\s([A-Z\s*a-z]+)",str(self.searchEntry.get()),re.IGNORECASE)
		if Matches:
			team_name = Matches.group(1)
		
			query = """SELECT game.date,Team_1,Team_2,Time 
						FROM game
						WHERE Team_1 ='%s' or Team_2 ='%s' """ % (team_name,team_name)
			try:
				self.cur.execute(query)
			except MySQLdb.Error, e:
				tkMessageBox.showerror("Search Error","%s" %(e))

			res = self.cur.fetchall()
			self.display_stuff = Tkinter.StringVar()
			self.res_wind = Tkinter.Toplevel()
			self.res_wind.title('Search Result')
			self.res_wind.geometry("500x180+300+300")
			self.res_wind.resizable(False,False)
			self.res_wind.grid()
			self.display = Tkinter.Text(self.res_wind,height=20,width=100)
			self.display.grid(column=0,row=0,columnspan=2,rowspan=15)
			self.display_stuff.set(u"  Date\t\t\tMatch\t\t\t\tTiming\n\n")
			self.display.insert(1.0,self.display_stuff.get())
			self.line=2.0
			for row in res:
				self.display_stuff.set(" "+row[0]+"\t\t"+row[1]+" vs. "+row[2]+"\t\t\t\t\t"+row[3]+"\n")
				self.display.insert(self.line,self.display_stuff.get())
				self.line += 1.0
			self.display.config(state="disabled")
		elif Score:
			team1 = Score.group(1)
			team2 = Score.group(2)

			query = """SELECT DISTINCT score,scorer_time 
					   FROM results,game 
					   WHERE day = game.date and game.date IN 
					   (SELECT game.date 
					   	FROM game
					   	WHERE Team_1='%s' and Team_2='%s')""" %(team1,team2)
			
			try:
				self.cur.execute(query)
			except MySQLdb.Error, e:
				tkMessageBox.showerror("Search Error","%s"  %(e))

			res = self.cur.fetchall()
			self.display_stuff = Tkinter.StringVar()
			self.res_wind = Tkinter.Toplevel()
			self.res_wind.title('Search Result')
			self.res_wind.geometry("500x180+300+300")
			self.res_wind.resizable(False,False)
			self.res_wind.grid()
			self.display = Tkinter.Text(self.res_wind,height=10,width=100)
			self.display.grid(column=0,row=0,columnspan=2,rowspan=15)
			self.display_stuff.set(u" Score\tScorer@Time\n\n")
			self.display.insert(1.0,self.display_stuff.get())
			self.line=2.0
			for row in res:
				self.display_stuff.set(" "+row[0]+"\t"+row[1]+"\n")
				self.display.insert(self.line,self.display_stuff.get())
				self.line += 1.0
			self.display.config(state="disabled")
		elif Leagues:
			league_name = Leagues.group(1)

			query = """SELECT Team_1,Team_2,game.date,time
					   FROM game,league
					   WHERE league.date = game.date AND league.league IN
					   (SELECT 	league
					   	FROM league
					   	WHERE league.league = '%s')""" %(league_name)
			try:
				self.cur.execute(query)
			except MySQLdb.Error, e:
				tkMessageBox.showerror("Search Error","%s" %(e))

			res = self.cur.fetchall()
			self.display_stuff = Tkinter.StringVar()
			self.res_wind = Tkinter.Toplevel()
			self.res_wind.title('Search Result')
			self.res_wind.geometry("600x180+300+300")
			self.res_wind.resizable(False,False)
			self.res_wind.grid()
			self.display = Tkinter.Text(self.res_wind,height=10,width=100)
			self.display.grid(column=0,row=0,columnspan=2,rowspan=15)
			self.display_stuff.set(u" Teams\t\t\t\t\t\tDate\t\tTime\n\n")
			self.display.insert(1.0,self.display_stuff.get())
			self.line=2.0
			for row in res:
				self.display_stuff.set(" "+row[0]+" vs "+row[1]+"\t\t\t\t\t\t"+row[2]+"\t\t"+row[3]+"\n")
				self.display.insert(self.line,self.display_stuff.get())
				self.line += 1.0
			self.display.config(state="disabled")
		elif Player_Stats:
			team_name = Player_Stats.group(1)
			q1 = """SELECT @maxgoal := max(player_goals)
					FROM players
					WHERE team = '%s'""" %(team_name)
			self.cur.execute(q1)
			res = self.cur.fetchall()
			q2 = """SELECT player_name,player_goals
					FROM players
					WHERE player_goals = @maxgoal AND
					team = '%s'""" %(team_name)
			self.cur.execute(q2)
			res = self.cur.fetchall()		  
			self.display_stuff = Tkinter.StringVar()
			self.res_wind = Tkinter.Toplevel()
			self.res_wind.title('Search Result')
			self.res_wind.geometry("180x180+300+300")
			self.res_wind.resizable(False,False)
			self.res_wind.grid()
			self.display = Tkinter.Text(self.res_wind,height=10,width=100)
			self.display.grid(column=0,row=0,columnspan=2,rowspan=15)
			self.display_stuff.set(u" Player\t\tGoals\n\n")
			self.display.insert(1.0,self.display_stuff.get())
			self.line=2.0
			for row in res:
				self.display_stuff.set(" "+row[0]+"\t\t"+str(row[1])+"\n")
				self.display.insert(self.line,self.display_stuff.get())
				self.line += 1.0
			self.display.config(state="disabled")
		elif League_Scorer:
			league_name = League_Scorer.group(1)
			lnames = ["Barclays Premier League","barclays premier league","Indian Super League","indian super league"]
			
			if league_name not in lnames:
				tkMessageBox.showerror("Search","No league called %s" %(league_name))
				self.search.destroy
			else:	
				q1 = """SELECT @mgl := max(player_goals)
					FROM players,teams
					WHERE teams.league_name = '%s' AND
					team = team_name""" %(league_name)
				
				self.cur.execute(q1)
				res = self.cur.fetchall()
				
				query = """SELECT player_name,player_goals
				           FROM players,teams
				           WHERE player_goals = @mgl AND
				           team = team_name AND
				           team_name IN
				           (SELECT team_name
				            FROM teams 
				            WHERE league_name = '%s')""" %(league_name)
				try:
					self.cur.execute(query)
				except MySQLdb.Error, e:
					tkMessageBox.showerror("Search Error","%s" %(e))

				res = self.cur.fetchall()
				self.display_stuff = Tkinter.StringVar()
				self.res_wind = Tkinter.Toplevel()
				self.res_wind.title('Search Result')
				self.res_wind.geometry("500x180+300+300")
				self.res_wind.resizable(False,False)
				self.res_wind.grid()
				self.display = Tkinter.Text(self.res_wind,height=10,width=100)
				self.display.grid(column=0,row=0,columnspan=2,rowspan=15)
				self.display_stuff.set(u" PLayer\t\t\tGoals\n\n")
				self.display.insert(1.0,self.display_stuff.get())
				self.line=2.0
				for row in res:
					self.display_stuff.set(" "+row[0]+"\t\t"+str(row[1])+"\n")
					self.display.insert(self.line,self.display_stuff.get())
					self.line += 1.0
				self.display.config(state="disabled")
		else:
			tkMessageBox.showerror("Error","Invalid Format")


if __name__ == "__main__":
	w =  FootApp(None)
	w.title('Football Info System')
	w.mainloop()