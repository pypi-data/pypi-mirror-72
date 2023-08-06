from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSlot, QThread, QLocale
import sys


Cb = 1.602176e-19  # coulomb
h = 6.626068e-34  # J.s
c = 2.997924586e8  # m.s-1


class UnitsConverter(QObject):
    def __init__(self, parent=None):
        super().__init__()
        QLocale.setDefault(QLocale(QLocale.English, QLocale.UnitedStates))
        if parent is None:
            parent = QtWidgets.QGroupBox('Units Converter')
        self.parent = parent
        self.setupUi()

        
        #self.ui.E_nm_sb.setOpts(siPrefix=False,step=0.1,decimals=3)


        self.ui.E_cm_sb.editingFinished.connect(self.update_values_from_cm)
        self.ui.E_eV_sb.editingFinished.connect(self.update_values_from_eV)
        self.ui.E_Hz_sb.editingFinished.connect(self.update_values_from_Hz)
        #self.ui.E_J_sb.editingFinished.connect(self.update_values_from_J)
        self.ui.E_cm_fom_nm_sb.editingFinished.connect(self.update_from_cm_nm)
        self.ui.E_nm_ref_sb.editingFinished.connect(self.update_from_cm_nm_ref)
        self.ui.E_nm_sb.editingFinished.connect(self.update_values_from_nm)

        self.ui.E_nm_ref_sb.setValue(632.8)
        self.ui.E_nm_ref_sb.editingFinished.emit()

    def setupUi(self):
        self.ui = QObject()

        vlayout = QtWidgets.QVBoxLayout()
        self.parent.setLayout(vlayout)

        self.ui.E_cm_sb = QtWidgets.QDoubleSpinBox()
        self.ui.E_cm_sb.setRange(0, 1e12)
        self.ui.E_cm_sb.setSuffix(' cm-1')
        self.ui.E_eV_sb = QtWidgets.QDoubleSpinBox()
        self.ui.E_eV_sb.setRange(0, 1e12)
        self.ui.E_eV_sb.setSuffix(' eV')
        self.ui.E_Hz_sb = QtWidgets.QDoubleSpinBox()
        self.ui.E_Hz_sb.setRange(0, 1e20)
        self.ui.E_Hz_sb.setSuffix(' Hz')
        self.ui.E_J_sb = QtWidgets.QDoubleSpinBox()
        self.ui.E_J_sb.setRange(0, 1e12)
        self.ui.E_J_sb.setSuffix(' J')
        self.ui.E_cm_fom_nm_sb = QtWidgets.QDoubleSpinBox()
        self.ui.E_cm_fom_nm_sb.setRange(-1e12, 1e12)
        self.ui.E_cm_fom_nm_sb.setSuffix(' cm-1')
        self.ui.E_nm_ref_sb = QtWidgets.QDoubleSpinBox()
        self.ui.E_nm_ref_sb.setRange(0.1, 1e12)
        self.ui.E_nm_ref_sb.setSuffix(' nm')
        self.ui.E_nm_sb = QtWidgets.QDoubleSpinBox()
        self.ui.E_nm_sb.setRange(0.1, 1e12)
        self.ui.E_nm_sb.setSuffix(' nm')

        widget1 = QtWidgets.QWidget()
        widget1.setLayout(QtWidgets.QHBoxLayout())
        widget1.layout().addWidget(self.ui.E_nm_sb)
        widget1.layout().addWidget(self.ui.E_cm_sb)
        vlayout.addWidget(widget1)

        widget2 = QtWidgets.QWidget()
        widget2.setLayout(QtWidgets.QHBoxLayout())
        widget2.layout().addWidget(self.ui.E_eV_sb)
        widget2.layout().addWidget(self.ui.E_Hz_sb)
        vlayout.addWidget(widget2)


        widget3 = QtWidgets.QGroupBox('Relative cm-1')
        widget3.setLayout(QtWidgets.QHBoxLayout())
        widget3.layout().addWidget(self.ui.E_nm_ref_sb)
        widget3.layout().addWidget(self.ui.E_cm_fom_nm_sb)
        vlayout.addWidget(widget3)


    def update_values_from_nm(self):
        E_nm = self.ui.E_nm_sb.value()
        self.update_ui(E_nm)

    def update_values_from_eV(self):
        E_eV = self.ui.E_eV_sb.value()
        E_nm = self.eV2nm(E_eV)
        self.update_ui(E_nm)

    def update_from_cm_nm(self):
        E_cm = self.ui.E_cm_fom_nm_sb.value()
        E_nm = self.ui.E_nm_ref_sb.value()
        E_cm = 1 / (E_nm * 1e-7) - E_cm
        E_nm = 1 / (E_cm * 1e-7)
        self.update_ui(E_nm)

    def update_from_cm_nm_ref(self):
        E_nm = self.ui.E_nm_ref_sb.value()
        E_cm = self.ui.E_cm_fom_nm_sb.value()
        E_cm = 1 / (E_nm * 1e-7) - E_cm
        E_nm = 1 / (E_cm * 1e-7)
        self.update_ui(E_nm, update_cmref=False)

    def update_values_from_Hz(self):
        E_Hz = self.ui.E_Hz_sb.value()
        E_nm = 300 / E_Hz
        self.update_ui(E_nm)

    def update_values_from_cm(self):
        E_cm = self.ui.E_cm_sb.value()
        E_nm = 1 / (E_cm * 1e-7)
        self.update_ui(E_nm)

    def update_ui(self, E_nm, update_cmref=True):
        self.ui.E_cm_sb.editingFinished.disconnect(self.update_values_from_cm)
        self.ui.E_eV_sb.editingFinished.disconnect(self.update_values_from_eV)
        self.ui.E_Hz_sb.editingFinished.disconnect(self.update_values_from_Hz)
        #self.ui.E_J_sb.editingFinished.connect(self.update_values_from_J)
        self.ui.E_nm_sb.editingFinished.disconnect(self.update_values_from_nm)
        self.ui.E_cm_fom_nm_sb.editingFinished.disconnect(self.update_from_cm_nm)

        self.ui.E_nm_sb.setValue(E_nm)
        self.ui.E_eV_sb.setValue(self.nm2eV(E_nm))
        self.ui.E_cm_sb.setValue(self.eV2cm(self.nm2eV(E_nm)))
        self.ui.E_Hz_sb.setValue(3e8/E_nm)
        if update_cmref:
            diff = -self.nm2eV(E_nm) + self.nm2eV(self.ui.E_nm_ref_sb.value())
            if diff != 0.:
                diff = self.eV2cm(diff)
            self.ui.E_cm_fom_nm_sb.setValue(diff)


        self.ui.E_cm_sb.editingFinished.connect(self.update_values_from_cm)
        self.ui.E_eV_sb.editingFinished.connect(self.update_values_from_eV)
        self.ui.E_Hz_sb.editingFinished.connect(self.update_values_from_Hz)
        #self.ui.E_J_sb.editingFinished.connect(self.update_values_from_J)
        self.ui.E_nm_sb .editingFinished.connect(self.update_values_from_nm)
        self.ui.E_cm_fom_nm_sb.editingFinished.connect(self.update_from_cm_nm)

    def nm2eV(self, E_nm):
        E_freq = c / E_nm * 1e9
        E_J = E_freq * h
        E_eV = E_J / Cb
        return E_eV

    def eV2cm(self, E_eV):
        E_nm = self.eV2nm(E_eV)
        E_cm = 1 / (E_nm * 1e-7)
        return E_cm

    def eV2nm(self, E_eV):
        E_J = E_eV * Cb
        E_freq = E_J / h
        E_nm = c / E_freq * 1e9
        return E_nm


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    prog = UnitsConverter()
    prog.parent.show()
    sys.exit(app.exec_())
