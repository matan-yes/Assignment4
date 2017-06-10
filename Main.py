import tkMessageBox,os , tkFileDialog, Structure, Train , Test , Classifier
from Tkinter import Tk, Label, Button, Entry, IntVar, END, W, E ,StringVar





class MainWindow:
    # c'tor

    def __init__(self,master):
        self.master = master

        master.title("Naive Bayes Classifier")
        creators_lbl = Label(master,text = "Alon Galperin\nMatan Yeshurun", font="David" , fg="Blue")

        #browse_button = Button(master, text="Browse", command=lambda: self.loadDataFromPath(browse_textbox.get()),height=1,width=10)
        browse_button = Button(master, text="Browse", command=lambda: self.getDirPath(), height=1, width=10)
        self.browse_value = StringVar()
        self.browse_textbox = Entry(master, width=55, exportselection=0, textvariable=self.browse_value)

        browse_lbl = Label(master, text="Directory Path: ")

        build_button = Button (master, text="Build",command=lambda :self.build(), height=1,width=20)
        classify_button = Button(master, text="Classify", command=lambda: self.classfy(), height=1, width=20)
        discretization_lbl = Label(master, text="Discretization Bins:")
        self.discretization_textbox = Entry(master,width=25)

        creators_lbl.place(x=220 , y=20)

        browse_button.place(x=500, y=95)
        self.browse_textbox.place(x=150,y=100)
        browse_lbl.place(x=40, y=100)

        self.discretization_textbox.place(x=150,y=150)
        discretization_lbl.place(x=40,y=150)
        build_button.place(x=200, y=200)
        classify_button.place(x=200, y=250)
        master.minsize(width=600, height=400)
        master.maxsize(width=600, height=400)

    def update(self,param):
        if param is 'Browse':
            tkMessageBox.showinfo("message Box","Browse")
        else:
            if param is 'build':
                tkMessageBox.showinfo("message Box","build")


    def loadDataFromPath(self,value):
        if os.path.exists(value):
            tkMessageBox.showinfo("message Box-path exists",value)
            x = tkFileDialog.askdirectory(**self.dir_opt)

        else:
            tkMessageBox.showinfo("Path not exists" ,"Path not exists: "+value )

    def getDirPath(self):
        folderPath = tkFileDialog.askdirectory()
        #tkMessageBox.showinfo("",folderPath)
        self.browse_value.set = folderPath
        self.browse_textbox.config(state='normal')
        self.browse_textbox.delete(0,'end')
        self.browse_textbox.insert(0,folderPath)
        self.browse_textbox.config(state='readonly')
        self.structure_path = folderPath+"/Structure.txt"
        self.train_path = folderPath+"/train.csv"
        self.test_path = folderPath + "/test.csv"
        if (not os.path.exists(self.structure_path)):
            tkMessageBox.showinfo("Alert","Structure file does not exists in the given path\nPlease select another folder of insert structure file into selected folder and pick again\nMissing 'Structure.text in: "+self.structure_path)

        if (not os.path.exists(self.train_path)):
            tkMessageBox.showinfo("Alert","train file does not exists in the given path\nPlease select another folder of insert structure file into selected folder and pick again\nMissing 'train.csv in: "+self.train_path)

        if (not os.path.exists(self.test_path)):
            tkMessageBox.showinfo("Alert","Structure file does not exists in the given path\nPlease select another folder of insert structure file into selected folder and pick again\nMissing 'test.csv in: "+self.test_path)
        if(not os.path.exists(self.structure_path) or not os.path.exists(self.train_path) or not os.path.exists(self.test_path)):
            self.getDirPath()
        else:
            tkMessageBox.showinfo("Alert","All files are in the right place!")

    def build(self):
        #check bins value
        if(self.validBinValue(self.discretization_textbox.get())):
            #get Structure.txet data
            s = Structure.Structure(self.structure_path)
            #myStructure = s.get_structure()
            s.prepere_structure()
            #print myStructure
            #print s.prepere_structure()

            #print s.get_structure()
            t = Train.Train(self.train_path)
            #if (s.check_bin_max() <= int(self.discretization_textbox.get())):
            #print(t.check_bin_max())
            if (t.check_bin_max() <= int(self.discretization_textbox.get())):
                tkMessageBox.showinfo("Alert", "Invalid discretization bins value")
                return
            #print t.get_train()
            t.clean_train()
            self.classfier = Classifier.Classifier.buil_model(t)
            tkMessageBox.showinfo("Naive Bayes Classifier", "Building classifier using train-set is done!")

    def classfy(self):
            #create new test
            test = Test.Test(self.test_path)
            test.clean_test()
            test.classify_test()





    def validBinValue(self,bins):
        try:
            x = int(bins)
            if(x > 1):
                return True
            else:
                tkMessageBox.showinfo("Alert", "Invalid discretization bins value")
                return False
        except:
            tkMessageBox.showinfo("Alert","Invalid discretization bins value")
            return False







root = Tk()
my_gui = MainWindow(root)
root.mainloop()
