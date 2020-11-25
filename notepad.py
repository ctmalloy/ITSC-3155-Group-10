import tkinter 
import os	
import pathlib 
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *

class Notepad: 

	root = Tk() 

	# default window width and height 
	thisWidth = 300
	thisHeight = 300
	thisTextArea = Text(root) 
	thisMenuBar = Menu(root) 
	thisFileMenu = Menu(thisMenuBar, tearoff=0) 
	thisEditMenu = Menu(thisMenuBar, tearoff=0) 
	thisHelpMenu = Menu(thisMenuBar, tearoff=0) 
	thisRightClickMenu = Menu(root, tearoff = 0) 
	
	# To add scrollbar 
	thisScrollBar = Scrollbar(thisTextArea)	 
	file = None

	# To add right click menu

	def __init__(self,**kwargs): 

		# Set icon 
		try: 
				self.root.wm_iconbitmap("Notepad.ico") 
		except: 
				pass

		# Set window size (the default is 300x300) 

		try: 
			self.thisWidth = kwargs['width'] 
		except KeyError: 
			pass

		try: 
			self.thisHeight = kwargs['height'] 
		except KeyError: 
			pass

		# Set the window text 
		self.root.title("Untitled - Notepad") 

		# Center the window 
		screenWidth = self.root.winfo_screenwidth() 
		screenHeight = self.root.winfo_screenheight() 
	
		# For left-alling 
		left = (screenWidth / 2) - (self.thisWidth / 2) 
		
		# For right-allign 
		top = (screenHeight / 2) - (self.thisHeight /2) 
		
		# For top and bottom 
		self.root.geometry('%dx%d+%d+%d' % (self.thisWidth, 
											self.thisHeight, 
											left, top)) 

		# To make the textarea auto resizable 
		self.root.grid_rowconfigure(0, weight=1) 
		self.root.grid_columnconfigure(0, weight=1) 

		# Add controls (widget) 
		self.thisTextArea.grid(sticky = N + E + S + W) 
		
		# To open new file 
		self.thisFileMenu.add_command(label="New", command=self.newFile)	 
		
		# To open a already existing file 
		self.thisFileMenu.add_command(label="Open", command=self.openFile) 
		
		# To save current file 
		self.thisFileMenu.add_command(label="Save", command=self.saveFile)	 

		# To create a line in the dialog		 
		self.thisFileMenu.add_separator()										 
		self.thisFileMenu.add_command(label="Exit", command=self.quitApplication) 
		self.thisMenuBar.add_cascade(label="File", menu=self.thisFileMenu)	 
		
		# To give a feature of cut 
		self.thisEditMenu.add_command(label="Cut", command=self.cut)			 
	
		# to give a feature of copy	 
		self.thisEditMenu.add_command(label="Copy", command=self.copy)		 
		
		# To give a feature of paste 
		self.thisEditMenu.add_command(label="Paste", command=self.paste)		 
		
		# To give a feature of editing 
		self.thisMenuBar.add_cascade(label="Edit", menu=self.thisEditMenu)	 
		
		# To create a feature of description of the notepad 
		self.thisHelpMenu.add_command(label="About Notepad", command=self.showAbout) 
		self.thisMenuBar.add_cascade(label="Help", menu=self.thisHelpMenu) 

		self.root.config(menu=self.thisMenuBar) 

		self.thisScrollBar.pack(side=RIGHT,fill=Y)					 
		
		# Scrollbar will adjust automatically according to the content		 
		self.thisScrollBar.config(command=self.thisTextArea.yview)	 
		self.thisTextArea.config(yscrollcommand=self.thisScrollBar.set) 

		# To create a right click menu
		self.thisRightClickMenu.add_command(label="Cut", command=self.cut)
		self.thisRightClickMenu.add_command(label="Copy", command=self.copy)
		self.thisRightClickMenu.add_command(label="Paste", command=self.paste)
		self.thisRightClickMenu.add_command(label="Select All", command=self.select_all)
		self.thisTextArea.bind("<Button-3>", self.do_popup)

	def do_popup(self, event): 
	    try: 
	        self.thisRightClickMenu.tk_popup(event.x_root, event.y_root) 
	    finally: 
	        self.thisRightClickMenu.grab_release() 	
		
	def quitApplication(self): 
		self.root.destroy() 
		# exit() 

	def showAbout(self): 
		showinfo("Notepad","Mrinal Verma") 

	def openFile(self): 
		
		self.file = askopenfilename(defaultextension=".txt", 
									filetypes=[("All Files","*.*"), 
										("Text Documents","*.txt")]) 

		if self.file == "": 
			
			# no file to open 
			self.file = None
		else: 
			
			# Try to open the file 
			# set the window title 
			self.root.title(os.path.basename(self.file) + " - Notepad") 
			self.thisTextArea.delete(1.0,END) 

			file = open(self.file,"r") 

			self.thisTextArea.insert(1.0,file.read()) 

			file.close() 

		
	def newFile(self): 
		self.root.title("Untitled - Notepad") 
		self.file = None
		self.thisTextArea.delete(1.0,END) 

	def saveFile(self): 

		if self.file == None: 
			# Save as new file 
			self.file = asksaveasfilename(initialfile='Untitled.txt', 
											defaultextension=".txt", 
											filetypes=[("All Files","*.*"), 
												("Text Documents","*.txt")]) 

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
	
	def run(self): 
		# Run main application 
		self.root.mainloop()



# Run main application 
notepad = Notepad(width=600,height=400) 
file = pathlib.Path("usb")
file2 = pathlib.Path("local")
if not file.exists() and not file2.exists():
	result = messagebox.askquestion("Welcome!", "Are you a USB user?")
	if result == 'yes':
		#create usb file
		usb_file = open("usb", "w+")
		usb_file.close()
		notepad.run()
	else:
		#create local file
		local_file = open("local", "w+")
		local_file.close()
		notepad.run()
elif file.exists() or file2.exists():
	notepad.run()


