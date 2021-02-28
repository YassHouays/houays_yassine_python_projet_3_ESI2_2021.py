from PySide2 import QtWidgets
import currency_converter
import json

class App(QtWidgets.QWidget) : 

    def __init__(self):
        super().__init__()
        self.c = currency_converter.CurrencyConverter()
        self.setWindowTitle("Convertisseur de devises")
        self.setup_ui()
        self.set_default_values()
        self.setup_connections()
       

    def setup_ui(self):
        self.layout = QtWidgets.QHBoxLayout(self)
        self.CheckDeviseFrom = QtWidgets.QComboBox()
        self.ValueMontant = QtWidgets.QDoubleSpinBox()
        self.CheckDeviseTo = QtWidgets.QComboBox()
        self.ValueMontantConverti = QtWidgets.QDoubleSpinBox()
        self.ReverseButton = QtWidgets.QPushButton("Inverser devises")
        self.CheckCurrencyFrom = QtWidgets.QComboBox()
        self.CheckCurrencyTo = QtWidgets.QComboBox()

        self.layout.addWidget(self.CheckDeviseFrom)
        self.layout.addWidget(self.CheckCurrencyFrom)
        self.layout.addWidget(self.ValueMontant)
        self.layout.addWidget(self.CheckDeviseTo)
        self.layout.addWidget(self.CheckCurrencyTo)
        self.layout.addWidget(self.ValueMontantConverti)
        self.layout.addWidget(self.ReverseButton)
        
    def setup_currency_list(self,file):
        with open (file, "r") as f :
          self.contenu = json.load(f) 
          return self.contenu
          

    def set_default_values(self):
        self.CheckDeviseFrom.addItems(sorted(list(self.c.currencies)))
        self.CheckDeviseTo.addItems(sorted(list(self.c.currencies)))
        self.CheckCurrencyFrom.addItems(sorted(list(self.setup_currency_list("./datas/currencies.json").values())))
        self.CheckCurrencyTo.addItems(sorted(list(self.setup_currency_list("./datas/currencies.json").values())))
        self.CheckDeviseFrom.setCurrentText("EUR")
        self.CheckDeviseTo.setCurrentText("USD")
        self.CheckCurrencyFrom.setCurrentText("Euro")
        self.CheckCurrencyTo.setCurrentText("Dollar")
        self.ValueMontant.setRange(1, 1000000)
        self.ValueMontantConverti.setRange(1,1000000)
        self.ValueMontant.setValue(100)
        self.ValueMontantConverti.setValue(100)
        

    def setup_connections(self):
        self.CheckDeviseFrom.activated.connect(self.compute)
        self.CheckDeviseTo.activated.connect(self.compute)
        self.CheckCurrencyFrom.activated.connect(self.compute_2)
        self.CheckCurrencyTo.activated.connect(self.compute_2)
        self.ValueMontant.valueChanged.connect(self.compute)
        self.ReverseButton.clicked.connect(self.inverser_devise)

    def compute_2(self):
        montant = self.ValueMontant.value()
        GetDeviseFromName = self.CheckCurrencyFrom.currentText()
        GetDeviseFromFile = self.setup_currency_list("./datas/currencies_2.json").get(GetDeviseFromName)
        GetDeviseToName = self.CheckCurrencyTo.currentText()
        GetDeviseFromFile = self.setup_currency_list("./datas/currencies_2.json").get(GetDeviseToName)
        self.CheckDeviseFrom.setCurrentText(GetDeviseFromFile)
        self.CheckDeviseTo.setCurrentText(GetDeviseFromFile)
        try : 
            resultat = self.c.convert(montant, GetDeviseFromFile, GetDeviseFromFile)
        except currency_converter.currency_converter.RateNotFoundError : 
            print("Erreur sur la conversion")
        else : 
            self.ValueMontantConverti.setValue(resultat)

    def compute(self):
        montant = self.ValueMontant.value()
        DeviseFrom = self.CheckDeviseFrom.currentText()
        GetDeviseFromName = self.setup_currency_list("./datas/currencies.json").get(DeviseFrom)
        self.CheckCurrencyFrom.setCurrentText(GetDeviseFromName)
        DeviseTo = self.CheckDeviseTo.currentText()
        GetDeviseToName = self.setup_currency_list("./datas/currencies.json").get(DeviseTo)
        self.CheckCurrencyTo.setCurrentText(GetDeviseToName)
        try : 
            resultat = self.c.convert(montant, DeviseFrom, DeviseTo)
        except currency_converter.currency_converter.RateNotFoundError : 
            print("Erreur sur la conversion")
        else : 
            self.ValueMontantConverti.setValue(resultat)

    def inverser_devise(self):
        DeviseFrom = self.CheckDeviseFrom.currentText()
        DeviseTo = self.CheckDeviseTo.currentText()
        self.CheckDeviseFrom.setCurrentText(DeviseTo)
        self.CheckDeviseTo.setCurrentText(DeviseFrom)
        self.compute()