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
        self.folderPath = tkFileDialog.askdirectory()
        #tkMessageBox.showinfo("",folderPath)
        self.browse_value.set = self.folderPath
        self.browse_textbox.config(state='normal')
        self.browse_textbox.delete(0,'end')
        self.browse_textbox.insert(0,self.folderPath)
        self.browse_textbox.config(state='readonly')
        self.structure_path = self.folderPath+"/Structure.txt"
        self.train_path = self.folderPath +"/train.csv"
        self.test_path = self.folderPath + "/test.csv"
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
        self.bins_amount = int(self.discretization_textbox.get())
        print("number of bins: " + str(self.bins_amount))
        print("starting building model")
        #check bins value
        if(self.validBinValue(self.bins_amount)):
            #get Structure.text data
            self.structure = Structure.Structure(self.structure_path)
            self.structure.prepere_structure()

            self.train = Train.Train(self.train_path, self.structure.get_structure(), self.bins_amount)

            if (self.train.check_bin_max() <= int(self.discretization_textbox.get())):
                tkMessageBox.showinfo("Alert", "Invalid discretization bins value")
                return

            self.train.clean_train()

            self.classifier = Classifier.Classifier(self.train, self.structure, self.bins_amount, self.folderPath)
            self.classifier.build_model()

            tkMessageBox.showinfo("Naive Bayes Classifier", "Building classifier using train-set is done!")

    def classfy(self):
        #create new test
        print("starting classifying model")
        test = Test.Test(self.test_path,self.structure.get_structure(),self.classifier,self.bins_amount)
        test.clean_test()
        test.classify_test()
        tkMessageBox.showinfo("Done","Classification is Done!\n results in output file")

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
