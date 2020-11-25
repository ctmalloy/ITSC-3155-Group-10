import tkinter 
import os	
import pathlib 
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *

class Notepad: 
	# Root Tk object
	root = Tk() 

	# Deafault Window Size
	thisWidth = 300
	thisHeight = 300

	# Add Text Area
	thisTextArea = Text(root)

	# Add Menu Bar
	thisMenuBar = Menu(root) 
	thisFileMenu = Menu(thisMenuBar, tearoff=0) 
	thisEditMenu = Menu(thisMenuBar, tearoff=0) 
	thisHelpMenu = Menu(thisMenuBar, tearoff=0) 
	
	# Add Scrollbar 
	thisScrollBar = Scrollbar(thisTextArea)	 
	file = None

	# Add Right-Click Menu
	thisRightClickMenu = Menu(root, tearoff = 0)

	# Constructor 
	def __init__(self,**kwargs):
		# Set Window Icon 
		try: 
			self.root.wm_iconbitmap("Notepad.ico") 
		except: 
			pass

		# Set Window Title 
		self.root.title("Untitled - Notepad")

		# Set Window Size
		try: 
			self.thisWidth = kwargs['width'] 
		except KeyError: 
			pass

		try: 
			self.thisHeight = kwargs['height'] 
		except KeyError: 
			pass 

		# Center Window
		screenWidth = self.root.winfo_screenwidth() 
		screenHeight = self.root.winfo_screenheight() 
	
		# Set Window geometry
		width = (screenWidth / 2) - (self.thisWidth / 2) 
		height = (screenHeight / 2) - (self.thisHeight /2) 
		self.root.geometry('%dx%d+%d+%d' % (self.thisWidth, self.thisHeight, width, height)) 

		# To make the textarea auto resizable 
		self.root.grid_rowconfigure(0, weight=1) 
		self.root.grid_columnconfigure(0, weight=1) 

		# Add controls (widget) 
		self.thisTextArea.grid(sticky = N + E + S + W)
		self.thisTextArea.configure(undo=True,autoseparators=True, maxundo=-1)
		
		# File Menu
		self.thisFileMenu.add_command(label="New", command=self.newFile)	 
		self.thisFileMenu.add_command(label="Open", command=self.openFile) 
		self.thisFileMenu.add_command(label="Save", command=self.saveFile)	 	 
		self.thisFileMenu.add_separator()										 
		self.thisFileMenu.add_command(label="Exit", command=self.quitApplication) 
		self.thisMenuBar.add_cascade(label="File", menu=self.thisFileMenu)	

		# Edit Menu	
		self.thisEditMenu.add_command(label="Cut", command=self.cut)			 
		self.thisEditMenu.add_command(label="Copy", command=self.copy)		 
		self.thisEditMenu.add_command(label="Paste", command=self.paste) 
		self.thisMenuBar.add_cascade(label="Edit", menu=self.thisEditMenu)	 
		
		# Help Menu
		self.thisHelpMenu.add_command(label="About Notepad", command=self.showAbout) 
		self.thisMenuBar.add_cascade(label="Help", menu=self.thisHelpMenu) 

		# Configure menu
		self.root.config(menu=self.thisMenuBar) 

		# Add Scrollbar
		self.thisScrollBar.pack(side=RIGHT,fill=Y)						 
		self.thisScrollBar.config(command=self.thisTextArea.yview)	 
		self.thisTextArea.config(yscrollcommand=self.thisScrollBar.set) 

		# To create a right click menu
		self.thisRightClickMenu.add_command(label="Cut", command=self.cut)
		self.thisRightClickMenu.add_command(label="Copy", command=self.copy)
		self.thisRightClickMenu.add_command(label="Paste", command=self.paste)
		self.thisRightClickMenu.add_command(label="Select All", command=self.select_all)
		self.thisRightClickMenu.add_command(label="Undo", command=self.undo)
		self.thisRightClickMenu.add_command(label="Redo", command=self.redo)
		self.thisTextArea.bind("<Button-3>", self.right_click)

	def right_click(self, event): 
	    try: 
	        self.thisRightClickMenu.tk_popup(event.x_root, event.y_root) 
	    finally: 
	        self.thisRightClickMenu.grab_release() 	
		
	def quitApplication(self): 
		self.root.destroy() 
		# exit() 

	def showAbout(self): 
		showinfo("Notepad","ITSC 3155") 

	def openFile(self): 
		usb = pathlib.Path("usb")

		if usb.exists():
			self.file = askopenfilename(initialdir="Notes", defaultextension=".txt", filetypes=[("All Files","*.*"), ("Text Documents","*.txt")]) 
		else:
			self.file = askopenfilename(defaultextension=".txt", filetypes=[("All Files","*.*"), ("Text Documents","*.txt")]) 
		
		if self.file == "": 
			# no file to open 
			self.file = None
		else: 
			# Set Window Title 
			self.root.title(os.path.basename(self.file) + " - Notepad") 
			self.thisTextArea.delete(1.0,END) 

			# Open File
			file = open(self.file,"r") 
			self.thisTextArea.insert(1.0,file.read()) 
			file.close() 

		
	def newFile(self): 
		self.root.title("Untitled - Notepad") 
		self.file = None
		self.thisTextArea.delete(1.0,END) 

	def saveFile(self): 
		usb = pathlib.Path("usb")

		if self.file == None: 
			# Save as new file 
			if usb.exists():
				self.file = asksaveasfilename(initialdir="Notes", initialfile='Untitled.txt', defaultextension=".txt",
					filetypes=[("All Files","*.*"), ("Text Documents","*.txt")])
			else:
				self.file = asksaveasfilename(initialfile='Untitled.txt', defaultextension=".txt",
					filetypes=[("All Files","*.*"), ("Text Documents","*.txt")])

			if self.file == "": 
				self.file = None
			else: 
				
				# Try to save the file 
				file = open(self.file,"w") 
				file.write(self.thisTextArea.get(1.0,END)) 
				file.close() 
				
				# Change the window title 
				self.root.title(os.path.basename(self.file) + " - Notepad") 
				
			
		else: 
			file = open(self.file,"w") 
			file.write(self.thisTextArea.get(1.0,END)) 
			file.close() 

	def cut(self): 
		self.thisTextArea.event_generate("<<Cut>>") 

	def copy(self): 
		self.thisTextArea.event_generate("<<Copy>>") 

	def paste(self): 
		self.thisTextArea.event_generate("<<Paste>>") 

	def select_all(self):
		self.thisTextArea.tag_add(SEL, "1.0", END)
		#self.thisTextArea.mark_set(INSERT, "1.0")
		self.thisTextArea.see(INSERT)
		return 'break'

	def undo(self):
		self.thisTextArea.event_generate("<<Undo>>")

	def redo(self):
		self.thisTextArea.event_generate("<<Redo>>")
	
	def run(self): 
		# Run this instance
		self.root.mainloop()

if __name__=="__main__": 
	notepad = Notepad(width=600,height=400) 
	file = pathlib.Path("usb")
	file2 = pathlib.Path("local")
	if not file.exists() and not file2.exists():
		result = messagebox.askquestion("Welcome!", "Are you a USB user?")
		if result == 'yes':
			#create usb file
			usb_file = open("usb", "w+")
			usb_file.close()
			os.mkdir("Notes")
			notepad.run()			
		else:
			#create local file
			local_file = open("local", "w+")
			local_file.close()
			notepad.run()
	elif file.exists() or file2.exists():
		notepad.run()