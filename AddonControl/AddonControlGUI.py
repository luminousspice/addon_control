from PyQt4 import QtCore, QtGui
import aqt

class AddonControlGUI(QtGui.QWidget):
    def __init__(self, control):
        super(AddonControlGUI, self).__init__()
        self.control = control
        self.current_list = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle('AddonControl')

        # main layout
        self.vbox = QtGui.QVBoxLayout()

        self.setup_filter_row()
        self.setup_table_row()
        self.setup_buttons_row()

        self.setLayout(self.vbox)

        self.fill_table(self.control.all_addons())

        self.show()

    def setup_filter_row(self):
        filter_label = QtGui.QLabel("Filter:", self)
        self.filter_field = QtGui.QLineEdit(self)
        self.connect(self.filter_field, QtCore.SIGNAL("textChanged(QString)"), \
                self.refesh_table)

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(filter_label)
        hbox.addWidget(self.filter_field)

        self.vbox.addLayout(hbox)

    def setup_table_row(self):
        self.table = QtGui.QTableWidget(self)
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.table)

        self.vbox.addLayout(hbox)

    def setup_buttons_row(self):
        update_button = QtGui.QPushButton('Update Package Lists', self)
        install_button = QtGui.QPushButton('Install', self)
        remove_button = QtGui.QPushButton('Remove', self)
        self.connect(update_button, QtCore.SIGNAL('clicked()'), self.update_repos)
        self.connect(install_button, QtCore.SIGNAL('clicked()'), self.install_selected)
        self.connect(remove_button, QtCore.SIGNAL('clicked()'), self.remove_selected)

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(update_button)
        hbox.addWidget(install_button)
        hbox.addWidget(remove_button)

        self.vbox.addLayout(hbox)

    def refesh_table(self, text):
        # get filter string from textbox
        matches = self.control.fuzzy_search_addons(text)
        self.fill_table(matches)
    
    def fill_table(self, addons):
        self.table.setColumnCount(2)
        self.table.setRowCount( len(addons) )
        # do the headers
        item1 = QtGui.QTableWidgetItem("Addon Name")
        item2 = QtGui.QTableWidgetItem("Status")
        self.table.setHorizontalHeaderItem(0, item1)
        self.table.setHorizontalHeaderItem(1, item2)

        for i, addon in enumerate(addons):
            item_name = QtGui.QTableWidgetItem(addon.name)
            item_status = QtGui.QTableWidgetItem( \
                    "Installed" if addon.installed else "Not Installed")
            self.table.setItem(i, 0, item_name)
            self.table.setItem(i, 1, item_status)

        self.current_list = addons

    def install_selected(self):
        aqt.mw.progress.start(immediate=True, label='Installing Addon')

        index = self.table.currentRow()
        self.control.install_addon( self.current_list[index] )
        self.control.save_state()
        self.control.load_addons()

        self.fill_table( self.control.all_addons() )
        self.filter_field.setText('')

        aqt.mw.progress.finish()
    
    def remove_selected(self):
        aqt.mw.progress.start(immediate=True, label='Removing Addon')

        index = self.table.currentRow()
        self.control.remove_addon( self.current_list[index] )
        self.control.save_state()
        self.control.load_addons()

        self.fill_table( self.control.all_addons() )
        self.filter_field.setText('')

        aqt.mw.progress.finish()
        aqt.utils.showInfo("Restart Anki to remove the plugin")
    
    def update_repos(self):
        aqt.mw.progress.start(immediate=True, label='Updating Repos')
        self.control.update_repos()
        aqt.mw.progress.finish()
