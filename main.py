try:
    import tkinter as tk    # python 3
except ImportError:
    import Tkinter as tk    # python 2
from abc import ABC, abstractmethod
from math import pi, e, sqrt, log, log10, factorial, radians, sin, cos, tan, sinh, cosh, tanh
from numpy import cbrt
from datetime import date
from forex_python.converter import CurrencyRates, CurrencyCodes

class CalculatorApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (SelectionMenu, Calculator, DateCalculator, CurrencyConverter, VolumeConverter, LengthConverter,
                WeightAndMassConverter, TemperatureConverter, EnergyConverter, AreaConverter, SpeedConverter, TimeConverter,
                PowerConverter, DataConverter, PressureConverter, AngleConverter):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Calculator")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class Frame():
    def set_bg_color(self, color):
        self.configure(bg=color)

    def set_header_text(self, text):
        self.header = tk.Label(self, text=text, font=("Arial", 16), bg="black", fg="white").place(x=60, y=8)


class Abstract(ABC):
    @abstractmethod
    def equal(self):
        pass


class AnswerField():   
    def summon_answer_field(self, row, columnSpan):
        self.text = tk.Entry(self, width=21, justify="right", bd=0, bg="black", fg="white", font=("Arial", 32))
        self.text.grid(row=row, columnspan=columnSpan, pady = 8)
        self.text.insert(tk.END, 0)
    
    def update(self, char):
        self.text.config(fg="white")
        if len(self.text.get()) < 15: # limit to 15 characters
            if char == ".":
                self.text.insert(tk.END, char)
                self.dotButton["state"] = "disabled"
                return None
            elif char == 0 and self.text.get() != "0":
                self.text.insert(tk.END, char)
            elif char != 0 and self.text.get() == "0":
                self.text.delete(len(self.text.get()) - 1, tk.END)
                self.text.insert(tk.END, char)
            elif self.text.get() == "-0":
                self.text.delete(1, tk.END)
                self.text.insert(tk.END, char)
            elif char != 0:
                self.text.insert(tk.END, char)
    
    def set_text(self, pastValue, value):
        if value % 1 == 0:
            value = int(value)
        if value == float(pastValue):
            self.text.config(fg="black")
            self.after(100, lambda: self.text.config(fg="white"))
        self.text.delete(0, tk.END)
        if len(str(round(value, 12))) <= 15 and len(self.text.get()) <= 18:
            self.text.insert(0, f"{round(value, 12):,}")
        else:
            self.text.insert(0, f"{round(value, 12):e}")
    
    def negative(self):
        if self.text.get().replace(',', '') == "0" or float(self.text.get().replace(',', '')) > 0:
            self.text.insert(0, "-")
        else:
            self.text.delete(0, 1)
    
    def clear(self):
        self.text.config(fg="white")
        self.dotButton["state"] = "normal"
        self.memory = None
        self.text.delete(0, tk.END)
        self.text.insert(tk.END, 0)
    
    def delete(self):
        self.text.config(fg="white")
        self.text.delete(len(self.text.get()) - 1, tk.END) if len(self.text.get()) != 1 else self.clear()
        if "." not in self.text.get():
            self.dotButton["state"] = "normal"

    def get_value(self):
        try:
            float(self.text.get().replace(',', ''))
        except ValueError:
            self.text.delete(0, tk.END)
            self.text.insert(0, "Error")
        self.__value = float(self.text.get().replace(',', ''))
        if self.__value % 1 == 0:
            self.__value = int(self.__value)
        return self.__value


class NumPad(AnswerField):   
    def summon(self):
        self.clearButton = tk.Button(self, width=5, height=2, text="AC", font=("Arial", 18), bg="#D4D4D2", bd=0, command=self.clear).grid(row=3, column=2)
        self.negativeButton = tk.Button(self, width=5, height=2, text="+/-", font=("Arial", 18), bg="#D4D4D2", bd=0, command=self.negative)
        self.negativeButton.grid(row=3, column=3)
        self.deleteButton = tk.Button(self, width=5, height=2, text="<", font=("Arial", 18), bg="#D4D4D2", bd=0, command=self.delete).grid(row=3, column=4)

        self.sevenButton = tk.Button(self, width=5, height=2, text="7", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update(7)).grid(row=4, column=2)
        self.eightButton = tk.Button(self, width=5, height=2, text="8", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update(8)).grid(row=4, column=3)
        self.nineButton = tk.Button(self, width=5, height=2, text="9", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update(9)).grid(row=4, column=4)

        self.fourButton = tk.Button(self, width=5, height=2, text="4", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update(4)).grid(row=5, column=2)
        self.fiveButton = tk.Button(self, width=5, height=2, text="5", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update(5)).grid(row=5, column=3)
        self.sixButton = tk.Button(self, width=5, height=2, text="6", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update(6)).grid(row=5, column=4)

        self.oneButton = tk.Button(self, width=5, height=2, text="1", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update(1)).grid(row=6, column=2)
        self.twoButton = tk.Button(self, width=5, height=2, text="2", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update(2)).grid(row=6, column=3)
        self.threeButton = tk.Button(self, width=5, height=2, text="3", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update(3)).grid(row=6, column=4)

        self.zeroButton = tk.Button(self, width=5, height=2, text="0", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update(0)).grid(row=7, column=3)
        self.dotButton = tk.Button(self, width=5, height=2, text=".", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update("."))
        self.dotButton.grid(row=7, column=4)
        self.equalButton = tk.Button(self, width=5, height=2, text="=", font=("Arial", 18), bg="#FF9500", fg="white", bd=0, command=self.equal).grid(row=7, column=2)

    def disable_negative(self):
        self.negativeButton.config(state="disabled")


class SelectionButton():
    def summon(self, controller):
        self.switchButton = tk.Button(self, text="≡", bg="#1C1C1C", fg="white", bd=0, font=("Arial", 18), width=3, 
                                    command=lambda: controller.show_frame("SelectionMenu")).grid(row=1, column=1, sticky="w")


class OptionMenu():
    def summon(self, variable1, variable2, list):
        self.fromText = tk.Label(self, text="From", font=("Arial", 16), bg="black", fg="white").grid(row=3, column=1, padx=8, sticky="w")

        self.fromUnit = tk.OptionMenu(self, variable1, *list)
        self.fromUnit.config(width=19, bd=0, bg="#505050", fg="white", font=("Arial", 18))
        self.fromUnit.grid(row=4, column=1, padx=8)

        self.toText = tk.Label(self, text="To", font=("Arial", 16), bg="black", fg="white").grid(row=5, column=1, padx=8, sticky="w")

        self.toUnit = tk.OptionMenu(self, variable2, *list)
        self.toUnit.config(width=19, bd=0, bg="#505050", fg="white", font=("Arial", 18))
        self.toUnit.grid(row=6, column=1, padx=8)


class VerticalScrolledFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        canvas = tk.Canvas(self, bd=0, highlightthickness=0, yscrollcommand=vscrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command=canvas.yview)

        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        self.interior = interior = tk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior, anchor=tk.NW)

        def _configure_interior(event):
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                canvas.config(width=interior.winfo_reqwidth())

        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)


class SelectionMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Frame.set_bg_color(self, "black")

        scrollFrame = VerticalScrolledFrame(self)
        scrollFrame.pack()

        pageList = ["Calculator", "DateCalculator", "CurrencyConverter", "VolumeConverter", "LengthConverter",
                "WeightAndMassConverter", "TemperatureConverter", "EnergyConverter", "AreaConverter", "SpeedConverter", "TimeConverter",
                "PowerConverter", "DataConverter", "PressureConverter", "AngleConverter"]
        for index, page in enumerate(pageList):
            spacedText = ""
            for i, letter in enumerate(page):
                if i and letter.isupper():
                    spacedText += " "
                spacedText += letter
            self.button = tk.Button(scrollFrame.interior, width=36, font=("Arial", 18), text=f"  {spacedText}", anchor="w", bg="#1C1C1C", fg="white", bd=1, 
                                    command=lambda index=index: open_page(pageList[index])).pack()

        def open_page(page):
            controller.show_frame(page)
            

class Calculator(tk.Frame, Abstract, AnswerField):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Frame.set_bg_color(self, "black")
        Frame.set_header_text(self, "Calculator")
        self.switchButton = tk.Button(self, text="≡", bg="#1C1C1C", fg="white", bd=0, font=("Arial", 18), width=3, 
                                    command=lambda: controller.show_frame("SelectionMenu")).grid(row=1, column=1, sticky="w")

        self.__value = 0
        self.__memory = 0
        self.__reVal = None
        self.__lockSecInput = False
        self.__operator = None

        AnswerField.summon_answer_field(self, 2, 8)

        self.factorialButton = tk.Button(self, width=5, height=2, text="x!", font=("Arial", 18), bg="#1C1C1C", fg="white", bd=0, command=self.factorial).grid(row=3, column=1)
        self.sqrtButton = tk.Button(self, width=5, height=2, text="√x", font=("Arial", 18), bg="#1C1C1C", fg="white", bd=0, command=self.sqrt).grid(row=3, column=2)
        self.squareButton = tk.Button(self, width=5, height=2, text="x²", font=("Arial", 18), bg="#1C1C1C", fg="white", bd=0, command=self.square).grid(row=3, column=3)
        self.clearButton = tk.Button(self, width=5, height=2, text="AC", font=("Arial", 18), bg="#D4D4D2", bd=0, command=self.clear).grid(row=3, column=4)
        self.percentButton = tk.Button(self, width=5, height=2, text="%", font=("Arial", 18), bg="#D4D4D2", bd=0, command=self.percent).grid(row=3, column=5)
        self.deleteButton = tk.Button(self, width=5, height=2, text="<", font=("Arial", 18), bg="#D4D4D2", bd=0, command=self.delete).grid(row=3, column=6)
        self.plusButton = tk.Button(self, width=5, height=2, text="+", font=("Arial", 18), bg="#FF9500", fg="white", bd=0, command=self.add).grid(row=3, column=7)

        self.lnButton = tk.Button(self, width=5, height=2, text="ln", font=("Arial", 18), bg="#1C1C1C", fg="white", bd=0, command=self.ln).grid(row=4, column=1)
        self.cbrtButton = tk.Button(self, width=5, height=2, text="∛x", font=("Arial", 18), bg="#1C1C1C", fg="white", bd=0, command=self.cbrt).grid(row=4, column=2)
        self.cubeButton = tk.Button(self, width=5, height=2, text="x³", font=("Arial", 18), bg="#1C1C1C", fg="white", bd=0, command=self.cube).grid(row=4, column=3)
        self.sevenButton = tk.Button(self, width=5, height=2, text="7", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update(7)).grid(row=4, column=4)
        self.eightButton = tk.Button(self, width=5, height=2, text="8", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update(8)).grid(row=4, column=5)
        self.nineButton = tk.Button(self, width=5, height=2, text="9", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update(9)).grid(row=4, column=6)
        self.minusButton = tk.Button(self, width=5, height=2, text="-", font=("Arial", 18), bg="#FF9500", fg="white", bd=0, command=self.minus).grid(row=4, column=7)

        self.commonLog = tk.Button(self, width=5, height=2, text="log", font=("Arial", 18), bg="#1C1C1C", fg="white", bd=0, command=self.log10).grid(row=5, column=1)
        self.sinhButton = tk.Button(self, width=5, height=2, text="sinh", font=("Arial", 18), bg="#1C1C1C", fg="white", bd=0, command=self.sinh).grid(row=5, column=2)
        self.sinButton = tk.Button(self, width=5, height=2, text="sin", font=("Arial", 18), bg="#1C1C1C", fg="white", bd=0, command=self.sin).grid(row=5, column=3)
        self.fourButton = tk.Button(self, width=5, height=2, text="4", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update(4)).grid(row=5, column=4)
        self.fiveButton = tk.Button(self, width=5, height=2, text="5", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update(5)).grid(row=5, column=5)
        self.sixButton = tk.Button(self, width=5, height=2, text="6", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update(6)).grid(row=5, column=6)
        self.multiplyButton = tk.Button(self, width=5, height=2, text="x", font=("Arial", 18), bg="#FF9500", fg="white", bd=0, command=self.multiply).grid(row=5, column=7)

        self.eButton = tk.Button(self, width=5, height=2, text="e", font=("Arial", 18), bg="#1C1C1C", fg="white", bd=0, command=self.eVal).grid(row=6, column=1)
        self.coshButton = tk.Button(self, width=5, height=2, text="cosh", font=("Arial", 18), bg="#1C1C1C", fg="white", bd=0, command=self.cosh).grid(row=6, column=2)
        self.cosButton = tk.Button(self, width=5, height=2, text="cos", font=("Arial", 18), bg="#1C1C1C", fg="white", bd=0, command=self.cos).grid(row=6, column=3)
        self.oneButton = tk.Button(self, width=5, height=2, text="1", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update(1)).grid(row=6, column=4)
        self.twoButton = tk.Button(self, width=5, height=2, text="2", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update(2)).grid(row=6, column=5)
        self.threeButton = tk.Button(self, width=5, height=2, text="3", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update(3)).grid(row=6, column=6)
        self.divideButton = tk.Button(self, width=5, height=2, text="÷", font=("Arial", 18), bg="#FF9500", fg="white", bd=0, command=self.divide).grid(row=6, column=7)

        self.piButton = tk.Button(self, width=5, height=2, text="π", font=("Arial", 18), bg="#1C1C1C", fg="white", bd=0, command=self.piVal).grid(row=7, column=1)
        self.tanhButton = tk.Button(self, width=5, height=2, text="tanh", font=("Arial", 18), bg="#1C1C1C", fg="white", bd=0, command=self.tanh).grid(row=7, column=2)
        self.tanButton = tk.Button(self, width=5, height=2, text="tan", font=("Arial", 18), bg="#1C1C1C", fg="white", bd=0, command=self.tan).grid(row=7, column=3)
        self.negativeButton = tk.Button(self, width=5, height=2, text="+/-", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=self.negative).grid(row=7, column=4)
        self.zeroButton = tk.Button(self, width=5, height=2, text="0", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update(0)).grid(row=7, column=5)
        self.dotButton = tk.Button(self, width=5, height=2, text=".", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update("."))
        self.dotButton.grid(row=7, column=6)
        self.equalButton = tk.Button(self, width=5, height=2, text="=", font=("Arial", 18), bg="#FF9500", fg="white", bd=0, command=self.equal).grid(row=7, column=7)

    def update(self, char):
        if self.__lockSecInput == True:
            self.dotButton["state"] = "normal"
            self.text.delete(0, tk.END)
            self.text.insert(tk.END, 0)
            self.__lockSecInput = False
        if len(self.text.get()) < 18: # limit to 18 characters (including commas)
            if char == ".":
                self.text.insert(tk.END, char)
                self.dotButton["state"] = "disabled"
                return None
            elif char == 0 and self.text.get() != "0":
                self.text.insert(tk.END, char)
            elif char != 0 and self.text.get() == "0":
                self.text.delete(len(self.text.get()) - 1, tk.END)
                self.text.insert(tk.END, char)
            elif self.text.get() == "-0":
                self.text.delete(1, tk.END)
                self.text.insert(tk.END, char)
            elif char != 0:
                self.text.insert(tk.END, char)
            
    def clear(self):
        self.dotButton["state"] = "normal"
        self.__memory = 0
        self.__reVal = None
        self.__operator = None
        self.text.delete(0, tk.END)
        self.text.insert(tk.END, 0)

    def delete(self):
        if len(self.text.get()) != 1:
            self.text.delete(len(self.text.get()) - 1, tk.END)
        else:
            self.text.delete(0, tk.END)
            self.text.insert(tk.END, 0)
        if "." not in self.text.get():
            self.dotButton["state"] = "normal"

    def negative(self):
        if self.text.get().replace(',', '') == "0" or float(self.text.get().replace(',', '')) > 0:
            self.text.insert(0, "-")
        else:
            self.text.delete(0, 1)
        
    def add(self):
        self.__memory = self.text.get().replace(',', '')
        self.__lockSecInput = True
        self.__operator = "+"
    
    def minus(self):
        self.__memory = self.text.get().replace(',', '')
        self.__lockSecInput = True
        self.__operator = "-"

    def multiply(self):
        self.__memory = self.text.get().replace(',', '')
        self.__lockSecInput = True
        self.__operator = "*"
    
    def divide(self):
        self.__memory = self.text.get().replace(',', '')
        self.__lockSecInput = True
        self.__operator = "/"
    
    def percent(self):
        try:
            float(self.text.get().replace(',', ''))
        except ValueError:
            self.text.delete(0, tk.END)
            self.text.insert(0, "Error")
        self.set_text(0, float(self.text.get().replace(',', ''))/100)

    def square(self):
        try:
            float(self.text.get().replace(',', ''))
        except ValueError:
            self.text.delete(0, tk.END)
            self.text.insert(0, "Error")
        self.__memory = self.text.get().replace(',', '')
        self.set_text(self.__memory, float(self.text.get().replace(',', ''))**2)

    def cube(self):
        try:
            float(self.text.get().replace(',', ''))
        except ValueError:
            self.text.delete(0, tk.END)
            self.text.insert(0, "Error")
        self.__memory = self.text.get().replace(',', '')
        self.set_text(self.__memory, float(self.text.get().replace(',', ''))**3)
    
    def sqrt(self):
        try:
            sqrt(float(self.text.get().replace(',', '')))
        except ValueError:
            self.text.delete(0, tk.END)
            self.text.insert(0, "Error")
        self.__memory = self.text.get().replace(',', '')
        self.set_text(self.__memory, sqrt(float(self.text.get().replace(',', ''))))
    
    def cbrt(self):
        try:
            cbrt(float(self.text.get().replace(',', '')))
        except ValueError:
            self.text.delete(0, tk.END)
            self.text.insert(0, "Error")
        self.__memory = self.text.get().replace(',', '')
        self.set_text(self.__memory, cbrt(float(self.text.get().replace(',', ''))))

    def sin(self):
        try:
            sin(radians(float(self.text.get().replace(',', ''))))
        except ValueError:
            self.text.delete(0, tk.END)
            self.text.insert(0, "Error")
        self.__memory = self.text.get().replace(',', '')
        self.set_text(self.__memory, sin(radians(float(self.text.get().replace(',', '')))))
    
    def cos(self):
        try:
            cos(radians(float(self.text.get().replace(',', ''))))
        except ValueError:
            self.text.delete(0, tk.END)
            self.text.insert(0, "Error")
        self.__memory = self.text.get().replace(',', '')
        self.set_text(self.__memory, cos(radians(float(self.text.get().replace(',', '')))))
    
    def tan(self):
        try:
            tan(radians(float(self.text.get().replace(',', ''))))
        except ValueError:
            self.text.delete(0, tk.END)
            self.text.insert(0, "Error")
        self.__memory = self.text.get().replace(',', '')
        self.set_text(self.__memory, tan(radians(float(self.text.get().replace(',', '')))))
    
    def sinh(self):
        try:
            sinh(float(self.text.get().replace(',', '')))
        except ValueError:
            self.text.delete(0, tk.END)
            self.text.insert(0, "Error")
        self.__memory = self.text.get().replace(',', '')
        self.set_text(self.__memory, sinh(float(self.text.get().replace(',', ''))))
    
    def cosh(self):
        try:
            cosh(float(self.text.get().replace(',', '')))
        except ValueError:
            self.text.delete(0, tk.END)
            self.text.insert(0, "Error")
        self.__memory = self.text.get().replace(',', '')
        self.set_text(self.__memory, cosh(float(self.text.get().replace(',', ''))))
    
    def tanh(self):
        try:
            tanh(float(self.text.get().replace(',', '')))
        except ValueError:
            self.text.delete(0, tk.END)
            self.text.insert(0, "Error")
        self.__memory = self.text.get().replace(',', '')
        self.set_text(self.__memory, tanh(float(self.text.get().replace(',', ''))))
    
    def ln(self):
        try:
            log(float(self.text.get().replace(',', '')))
        except ValueError:
            self.text.delete(0, tk.END)
            self.text.insert(0, "Error")
        self.__memory = self.text.get().replace(',', '')
        self.set_text(self.__memory, log(float(self.text.get().replace(',', ''))))
    
    def log10(self):
        try:
            log10(float(self.text.get().replace(',', '')))
        except ValueError:
            self.text.delete(0, tk.END)
            self.text.insert(0, "Error")
        self.__memory = self.text.get().replace(',', '')
        self.set_text(self.__memory, log10(float(self.text.get().replace(',', ''))))
    
    def factorial(self):
        try:
            factorial(int(self.text.get().replace(',', '')))
        except ValueError:
            self.text.delete(0, tk.END)
            self.text.insert(0, "Error")
        self.__memory = self.text.get().replace(',', '')
        self.set_text(self.__memory, factorial(int(self.text.get().replace(',', ''))))
    
    def eVal(self):
        self.set_text(self.__memory, e)
    
    def piVal(self):
        self.set_text(self.__memory, pi)
        
    def equal(self):
        self.__displayedText = self.text.get().replace(',', '').replace(',', '')
        try:
            float(self.__memory)
            float(self.__displayedText)
        except ValueError:
            self.text.delete(0, tk.END)
            self.text.insert(0, "Error")
        if self.__memory != 0 and len(self.text.get()) < 18: # limit to 18 characters (including commas)
            if self.__operator != None:
                if self.__operator == "+":
                    if self.__reVal == None:
                        self.__value = float(self.__memory) + float(self.__displayedText)
                        self.__reVal = float(self.__displayedText)
                    else:
                        self.__value += self.__reVal
                elif self.__operator == "-":
                    if self.__reVal == None:
                        self.__value = float(self.__memory) - float(self.__displayedText)
                        self.__reVal = float(self.__displayedText)
                    else:
                        self.__value -= self.__reVal
                elif self.__operator == "*":
                    if self.__reVal == None:
                        self.__value = float(self.__memory) * float(self.__displayedText)
                        self.__reVal = float(self.__displayedText)
                    else:
                        self.__value *= self.__reVal
                elif self.__operator == "/":
                    try:
                        float(self.__memory) / float(self.__displayedText)
                    except ZeroDivisionError:
                        self.text.delete(0, tk.END)
                        self.text.insert(0, "Error")
                    if self.__reVal == None:
                        self.__value = float(self.__memory) / float(self.__displayedText)
                        self.__reVal = float(self.__displayedText)
                    else:
                        self.__value /= self.__reVal
                self.__lockSecInput = True
                self.set_text(self.__displayedText, self.__value)


class DateCalculator(tk.Frame, Abstract, AnswerField):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        Frame.set_bg_color(self, "black")
        Frame.set_header_text(self, "Date Calculator")
        self.switchButton = tk.Button(self, text="≡", bg="#1C1C1C", fg="white", bd=0, font=("Arial", 18), width=3, 
                                    command=lambda: controller.show_frame("SelectionMenu")).grid(row=1, sticky="w")

        self.text = tk.Entry(self, width=21, justify="right", bd=0, bg="black", fg="white", font=("Arial", 32))
        self.text.grid(row=2, padx=8, pady = 8, sticky="w")
        self.text.insert(tk.END, "Same dates")

        self.fromText = tk.Label(self, text="From (format: 02/12/2021)", font=("Arial", 16), bg="black", fg="white").grid(row=4, padx=8, sticky="w")

        self.fromDate = tk.Entry(self, width=21, justify="left", bd=0, bg="#505050", fg="white", font=("Arial", 22))
        self.fromDate.grid(row=5, padx=8, pady = 8, sticky="w")
        self.fromDate.insert(tk.END, date.today().strftime("%d/%m/%Y"))

        self.fromText = tk.Label(self, text="To (format: 02/12/2021)", font=("Arial", 16), bg="black", fg="white").grid(row=6, padx=8, sticky="w")

        self.toDate = tk.Entry(self, width=21, justify="left", bd=0, bg="#505050", fg="white", font=("Arial", 22))
        self.toDate.grid(row=7, padx=8, pady = 8, sticky="w")
        self.toDate.insert(tk.END, date.today().strftime("%d/%m/%Y"))

        self.calcButton = tk.Button(self, height=2, text="Calculate", font=("Arial", 18), bg="#FF9500", fg="white", bd=0).grid(row=9, padx=8, sticky="w")
    
    def equal(self):
        pass


class CurrencyConverter(tk.Frame, Abstract, AnswerField):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        Frame.set_bg_color(self, "black")
        Frame.set_header_text(self, "Currency Converter")
        SelectionButton.summon(self, controller)

        self.__value = 0
        self.__fromCurrencyVal = tk.StringVar(value="USD")
        self.__toCurrencyVal = tk.StringVar(value="THB")
        self.__currencyList = ["USD", "JPY", "EUR", "THB", "IDR", "BGN", "ILS", "GBP", "AUD", "CHF", "HKD"]

        AnswerField.summon_answer_field(self, 2, 5)
        OptionMenu.summon(self, self.__fromCurrencyVal, self.__toCurrencyVal, self.__currencyList)
        NumPad.summon(self)
        NumPad.disable_negative(self)
    
    def equal(self):
        pass


class VolumeConverter(tk.Frame, Abstract, AnswerField):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Frame.set_bg_color(self, "black")
        Frame.set_header_text(self, "Volume Converter")
        SelectionButton.summon(self, controller)

        self.__value = 0
        self.__fromUnitVal = tk.StringVar(value="Milliliters")
        self.__toUnitVal = tk.StringVar(value="Teaspoons (US)")
        self.__volume = {"Milliliters": 0.001, "Cubic centimeters": 0.001, "Liters": 1, "Cubic meters": 1000, "Teaspoons (US)": 0.004929, 
                        "Tablespoons (US)": 0.014787, "Fluid ounces (US)": 0.029574, "Cups (US)": 0.236588, "Pints (US)": 0.473176,
                        "Quarts (US)": 0.946353, "Gallons (US)": 3.785412, "Cubic inches": 0.016387, "Cubic feet": 28.31685, 
                        "Cubic yards": 764.5549, "Teaspoons (UK)": 0.005919, "Tablespoons (UK)": 0.017758, "Fluid ounces (UK)": 0.028413, 
                        "Pints (UK)": 0.568261, "Quarts (UK)": 1.136523, "Gallons (UK)": 4.54609}

        AnswerField.summon_answer_field(self, 2, 5)
        OptionMenu.summon(self, self.__fromUnitVal, self.__toUnitVal, list(self.__volume.keys()))
        NumPad.summon(self)
        NumPad.disable_negative(self)

    def equal(self):
        self.__value = AnswerField.get_value(self)
        AnswerField.set_text(self, self.__value, self.__value * self.__volume[self.__fromUnitVal.get()] / self.__volume[self.__toUnitVal.get()])


class LengthConverter(tk.Frame, Abstract, AnswerField):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        Frame.set_bg_color(self, "black")
        Frame.set_header_text(self, "Length Converter")
        SelectionButton.summon(self, controller)

        self.__value = 0
        self.__fromUnitVal = tk.StringVar(value="Centimeters")
        self.__toUnitVal = tk.StringVar(value="Inches")
        self.__length = {"Nanometers": 0.000000001, "Microns": 0.000001, "Millimeters": 0.001, "Centimeters": 0.01, "Meters": 1, 
                        "Kilometers": 1000, "Inches": 0.0254, "Feet": 0.3048, "Yards": 0.9144, "Miles": 1609.344, "Nautical Miles": 1852}

        AnswerField.summon_answer_field(self, 2, 5)
        OptionMenu.summon(self, self.__fromUnitVal, self.__toUnitVal, list(self.__length.keys()))
        NumPad.summon(self)
        NumPad.disable_negative(self)

    def equal(self):
        self.__value = AnswerField.get_value(self)
        AnswerField.set_text(self, self.__value, self.__value * self.__length[self.__fromUnitVal.get()] / self.__length[self.__toUnitVal.get()])


class WeightAndMassConverter(tk.Frame, Abstract, AnswerField):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        Frame.set_bg_color(self, "black")
        Frame.set_header_text(self, "Weight and Mass Converter")
        SelectionButton.summon(self, controller)

        self.__value = 0
        self.__fromUnitVal = tk.StringVar(value="Kilograms")
        self.__toUnitVal = tk.StringVar(value="Pounds")
        self.__weightMass = {"Carats": 0.0002, "Milligrams": 0.000001, "Centigrams": 0.00001, "Decigrams": 0.0001, "Grams": 0.001, 
                            "Dekagrams": 0.01, "Hectogram": 0.1, "Kilograms": 1, "Metric tonnes": 1000, "Ounces": 0.02835, "Pounds": 0.453592, 
                            "Stone": 6.350293, "Short tons (US)": 907.1847, "Long tons (US)": 1016.047}

        AnswerField.summon_answer_field(self, 2, 5)
        OptionMenu.summon(self, self.__fromUnitVal, self.__toUnitVal, list(self.__weightMass.keys()))
        NumPad.summon(self)
        NumPad.disable_negative(self)

    def equal(self):
        self.__value = AnswerField.get_value(self)
        AnswerField.set_text(self, self.__value, self.__value * self.__weightMass[self.__fromUnitVal.get()] / self.__weightMass[self.__toUnitVal.get()])


class TemperatureConverter(tk.Frame, Abstract, AnswerField):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        Frame.set_bg_color(self, "black")
        Frame.set_header_text(self, "Temperature Converter")
        SelectionButton.summon(self, controller)

        self.__value = 0
        self.__fromUnitVal = tk.StringVar(value="Celsius")
        self.__toUnitVal = tk.StringVar(value="Fahrenheit")
        self.__temperatureList = ["Celsius", "Fahrenheit", "Kelvin"]

        AnswerField.summon_answer_field(self, 2, 5)
        OptionMenu.summon(self, self.__fromUnitVal, self.__toUnitVal, self.__temperatureList)
        NumPad.summon(self)

    def equal(self):
        self.__value = AnswerField.get_value(self)
        if self.__fromUnitVal.get() != self.__toUnitVal.get():
            if self.__fromUnitVal.get() == "Celsius":
                if self.__toUnitVal.get() == "Fahrenheit":
                    AnswerField.set_text(self, self.__value, (self.__value * 9 / 5) + 32)
                else:
                    AnswerField.set_text(self, self.__value, self.__value + 273.15)
            elif self.__fromUnitVal.get() == "Fahrenheit":
                if self.__toUnitVal.get() == "Celsius":
                    AnswerField.set_text(self, self.__value, (self.__value - 32) * 5 / 9)
                else:
                    AnswerField.set_text(self, self.__value, ((self.__value - 32) * 5 / 9) + 273.15)
            elif self.__fromUnitVal.get() == "Kelvin":
                if self.__toUnitVal.get() == "Celsius":
                    AnswerField.set_text(self, self.__value, self.__value - 273.15)
                else:
                    AnswerField.set_text(self, self.__value, ((self.__value - 273.15) * (9 / 5) + 32))
        else:
            AnswerField.set_text(self, self.__value, self.__value)


class EnergyConverter(tk.Frame, Abstract, AnswerField):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        Frame.set_bg_color(self, "black")
        Frame.set_header_text(self, "Energy Converter")
        SelectionButton.summon(self, controller)

        self.__value = 0
        self.__fromUnitVal = tk.StringVar(value="Joules")
        self.__toUnitVal = tk.StringVar(value="Food calories")
        self.__energy = {"Electron volts": 1.602177*(10**-19), "Joules": 1, "Kilojoules": 1000, "Thermal calories": 4.184, 
                        "Food calories": 4184, "Foot-pounds": 1.355818, "British thermal units": 1055.056}

        AnswerField.summon_answer_field(self, 2, 5)
        OptionMenu.summon(self, self.__fromUnitVal, self.__toUnitVal, list(self.__energy.keys()))
        NumPad.summon(self)
        NumPad.disable_negative(self)

    def equal(self):
        self.__value = AnswerField.get_value(self)
        AnswerField.set_text(self, self.__value, self.__value * self.__energy[self.__fromUnitVal.get()] / self.__energy[self.__toUnitVal.get()])


class AreaConverter(tk.Frame, Abstract, AnswerField):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        Frame.set_bg_color(self, "black")
        Frame.set_header_text(self, "Area Converter")
        SelectionButton.summon(self, controller)

        self.__value = 0
        self.__fromUnitVal = tk.StringVar(value="Square meters")
        self.__toUnitVal = tk.StringVar(value="Square feet")
        self.__area = {"Square millimeters": 0.000001, "Square centimeters": 0.0001, "Square meters": 1, "Hectares": 100000, 
                    "Square kilometers": 1000000, "Square inches": 0.000645, "Square feet": 0.092903, "Square yards": 0.836127, 
                    "Acres": 4046.856, "Square miles": 2589988}

        AnswerField.summon_answer_field(self, 2, 5)
        OptionMenu.summon(self, self.__fromUnitVal, self.__toUnitVal, list(self.__area.keys()))
        NumPad.summon(self)
        NumPad.disable_negative(self)

    def equal(self):
        self.__value = AnswerField.get_value(self)
        AnswerField.set_text(self, self.__value, self.__value * self.__area[self.__fromUnitVal.get()] / self.__area[self.__toUnitVal.get()])


class SpeedConverter(tk.Frame, Abstract, AnswerField):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        Frame.set_bg_color(self, "black")
        Frame.set_header_text(self, "Speed Converter")
        SelectionButton.summon(self, controller)

        self.__value = 0
        self.__fromUnitVal = tk.StringVar(value="Kilometers per hour")
        self.__toUnitVal = tk.StringVar(value="Miles per hour")
        self.__speed = {"Centimeters per second": 0.01, "Meters per second": 1, "Kilometers per hour": 0.277778, "Feet per second": 0.3048, 
                        "Miles per hour": 0.447, "Knots": 0.5144, "Mach": 340.3}

        AnswerField.summon_answer_field(self, 2, 5)
        OptionMenu.summon(self, self.__fromUnitVal, self.__toUnitVal, list(self.__speed.keys()))
        NumPad.summon(self)
        NumPad.disable_negative(self)

    def equal(self):
        self.__value = AnswerField.get_value(self)
        AnswerField.set_text(self, self.__value, self.__value * self.__speed[self.__fromUnitVal.get()] / self.__speed[self.__toUnitVal.get()])


class TimeConverter(tk.Frame, Abstract, AnswerField):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        Frame.set_bg_color(self, "black")
        Frame.set_header_text(self, "Time Converter")
        SelectionButton.summon(self, controller)

        self.__value = 0
        self.__fromUnitVal = tk.StringVar(value="Hours")
        self.__toUnitVal = tk.StringVar(value="Minutes")
        self.__time = {"Microseconds": 0.000001, "Milliseconds": 0.001, "Seconds": 1, "Minutes": 60, "Hours": 3600, "Days": 86400, 
                            "Weeks": 604800, "Years": 31557600}

        AnswerField.summon_answer_field(self, 2, 5)
        OptionMenu.summon(self, self.__fromUnitVal, self.__toUnitVal, list(self.__time.keys()))
        NumPad.summon(self)
        NumPad.disable_negative(self)

    def equal(self):
        self.__value = AnswerField.get_value(self)
        AnswerField.set_text(self, self.__value, self.__value * self.__time[self.__fromUnitVal.get()] / self.__time[self.__toUnitVal.get()])


class PowerConverter(tk.Frame, Abstract, AnswerField):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        Frame.set_bg_color(self, "black")
        Frame.set_header_text(self, "Power Converter")
        SelectionButton.summon(self, controller)

        self.__value = 0
        self.__fromUnitVal = tk.StringVar(value="Kilowats")
        self.__toUnitVal = tk.StringVar(value="Horsepower (US)")
        self.__power = {"Watts": 1, "Kilowats": 1000, "Horsepower (US)": 745.6999, "Foot-pounds/minute": 0.022597, "BTUs/minute": 17.58427}

        AnswerField.summon_answer_field(self, 2, 5)
        OptionMenu.summon(self, self.__fromUnitVal, self.__toUnitVal, list(self.__power.keys()))
        NumPad.summon(self)

    def equal(self):
        self.__value = AnswerField.get_value(self)
        AnswerField.set_text(self, self.__value, self.__value * self.__power[self.__fromUnitVal.get()] / self.__power[self.__toUnitVal.get()])


class DataConverter(tk.Frame, Abstract, AnswerField):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        Frame.set_bg_color(self, "black")
        Frame.set_header_text(self, "Data Converter")
        SelectionButton.summon(self, controller)

        self.__value = 0
        self.__fromUnitVal = tk.StringVar(value="Gigabytes")
        self.__toUnitVal = tk.StringVar(value="Megabytes")
        self.__data = {"Bits": 0.000000125, "Bytes": 0.000001, "Kilobits": 0.000125, "Kibibits": 0.000128, "Kilobytes": 0.001, 
                        "Kibibytes": 0.001024, "Megabits": 0.125, "Mebibits": 0.131072, "Megabytes": 1, "Mebibytes": 1.048576,
                        "Gigabits": 125, "Gibibits": 134.2177, "Gigabytes": 1000, "Gibibytes": 1073.742, "Terabits": 125000, 
                        "Tebibits": 137439, "Terabytes": 1000000, "Tebibytes": 1099512, "Petabits": 125000000, "Pebibits": 140737488, 
                        "Petabytes": 10**9, "Pebibytes": 1125899907, "Exabits": 1.25*(10**8), "Exbibits": 144115188076, 
                        "Exabytes": 10**12, "Exibytes": 1152921504607, "Zetabits": 1.25*(10**14), "Zebibits": 147573952589676,
                        "Zetabytes": 10**15, "Zebibytes": 1.180592*(10**15), "Yottabit": 1.25*(10**17), "Yobibits": 1.511157*(10**17), 
                        "Yottabyte": 10**18, "Yobibytes": 1.208926*(10**18)}

        AnswerField.summon_answer_field(self, 2, 5)
        OptionMenu.summon(self, self.__fromUnitVal, self.__toUnitVal, list(self.__data.keys()))
        NumPad.summon(self)
        NumPad.disable_negative(self)

    def equal(self):
        self.__value = AnswerField.get_value(self)
        AnswerField.set_text(self, self.__value, self.__value * self.__data[self.__fromUnitVal.get()] / self.__data[self.__toUnitVal.get()])


class PressureConverter(tk.Frame, Abstract, AnswerField):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        Frame.set_bg_color(self, "black")
        Frame.set_header_text(self, "Pressure Converter")
        SelectionButton.summon(self, controller)

        self.__value = 0
        self.__fromUnitVal = tk.StringVar(value="Atmospheres")
        self.__toUnitVal = tk.StringVar(value="Bars")
        self.__pressure = {"Atmospheres": 101325, "Bars": 100000, "Kilopascals": 1000, "Millimeters of mercury": 133.3, 
                            "Pascals": 1, "Pounds per square inch": 6894.757}

        AnswerField.summon_answer_field(self, 2, 5)
        OptionMenu.summon(self, self.__fromUnitVal, self.__toUnitVal, list(self.__pressure.keys()))
        NumPad.summon(self)
        NumPad.disable_negative(self)

    def equal(self):
        self.__value = AnswerField.get_value(self)
        AnswerField.set_text(self, self.__value, self.__value * self.__pressure[self.__fromUnitVal.get()] / self.__pressure[self.__toUnitVal.get()])

class AngleConverter(tk.Frame, Abstract, AnswerField):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        Frame.set_bg_color(self, "black")
        Frame.set_header_text(self, "Angle Converter")
        SelectionButton.summon(self, controller)

        self.__value = 0
        self.__fromUnitVal = tk.StringVar(value="Degrees")
        self.__toUnitVal = tk.StringVar(value="Radians")
        self.__angle = {"Degrees": 1, "Radians": 57.29578, "Gradians": 0.9}

        AnswerField.summon_answer_field(self, 2, 5)
        OptionMenu.summon(self, self.__fromUnitVal, self.__toUnitVal, list(self.__angle.keys()))
        NumPad.summon(self)

    def equal(self):
        self.__value = AnswerField.get_value(self)
        AnswerField.set_text(self, self.__value, self.__value * self.__angle[self.__fromUnitVal.get()] / self.__angle[self.__toUnitVal.get()])


if __name__ == "__main__":
    app = CalculatorApp()
    app.title("Calculatory")
    app.resizable(width=False, height=False)
    app.mainloop()