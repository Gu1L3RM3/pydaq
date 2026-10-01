"""Resizable table editors for Data-Driven Control coefficient inputs."""
import ast
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QSizePolicy,
)


def _number(text):
    value = float(text)
    return int(value) if value.is_integer() else value


class VectorTableInput(QWidget):
    """One-row, resizable coefficient editor compatible with QLineEdit.text()."""
    def __init__(self, values=None, parent=None, minimum_size=1, maximum_size=50):
        super().__init__(parent)
        self._updating = False
        layout = QVBoxLayout(self); layout.setContentsMargins(0, 0, 0, 0); layout.setSpacing(4)
        controls = QHBoxLayout(); controls.setContentsMargins(0, 0, 0, 0)
        controls.addWidget(QLabel('Size:'))
        self.size_spin = QSpinBox(); self.size_spin.setRange(minimum_size, maximum_size)
        controls.addWidget(self.size_spin); controls.addStretch(); layout.addLayout(controls)
        self.table = QTableWidget(1, minimum_size); self.table.setMinimumHeight(72); self.table.setMaximumHeight(82)
        self.table.verticalHeader().setVisible(False); self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.addWidget(self.table)
        self.size_spin.valueChanged.connect(self._resize)
        self.set_values([1] if values is None else values)

    def _resize(self, size):
        old = self.values(allow_empty=True)
        self.table.setColumnCount(size)
        self.table.setHorizontalHeaderLabels([str(i) for i in range(size)])
        for j, value in enumerate(old[:size]): self._set_cell(j, value)

    def _set_cell(self, column, value):
        item = QTableWidgetItem(str(value)); item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table.setItem(0, column, item)

    def set_values(self, values):
        if hasattr(values, 'tolist'): values = values.tolist()
        if isinstance(values, tuple): values = list(values)
        if values and isinstance(values[0], (list, tuple)):
            values = [v for row in values for v in row]
        values = list(values) if values else [0]
        self.size_spin.blockSignals(True); self.size_spin.setValue(len(values)); self.size_spin.blockSignals(False)
        self.table.setColumnCount(len(values)); self.table.setHorizontalHeaderLabels([str(i) for i in range(len(values))])
        for j, value in enumerate(values): self._set_cell(j, value)

    def values(self, allow_empty=False):
        result=[]
        for j in range(self.table.columnCount()):
            item=self.table.item(0,j); text='' if item is None else item.text().strip()
            if not text:
                if allow_empty: result.append(0); continue
                raise ValueError(f'Coefficient {j} cannot be empty.')
            result.append(_number(text))
        return result

    def text(self): return repr(self.values())
    def setText(self, text): self.set_values(ast.literal_eval(str(text)))
    def clear(self): self.set_values([0])


class BetaTableInput(QWidget):
    """Resizable beta editor with separate numerator and denominator tables."""
    def __init__(self, beta=None, parent=None):
        super().__init__(parent)
        layout=QVBoxLayout(self); layout.setContentsMargins(0,0,0,0); layout.setSpacing(5)
        controls=QHBoxLayout(); controls.addWidget(QLabel('Basis functions:'))
        self.rows_spin=QSpinBox(); self.rows_spin.setRange(1,50); controls.addWidget(self.rows_spin)
        controls.addWidget(QLabel('Numerator size:')); self.num_cols_spin=QSpinBox(); self.num_cols_spin.setRange(1,50); controls.addWidget(self.num_cols_spin)
        controls.addWidget(QLabel('Denominator size:')); self.den_cols_spin=QSpinBox(); self.den_cols_spin.setRange(1,50); controls.addWidget(self.den_cols_spin); controls.addStretch(); layout.addLayout(controls)
        layout.addWidget(QLabel('Numerator coefficients'))
        self.num_table=self._table(); layout.addWidget(self.num_table)
        layout.addWidget(QLabel('Denominator coefficients'))
        self.den_table=self._table(); layout.addWidget(self.den_table)
        self.rows_spin.valueChanged.connect(self._resize); self.num_cols_spin.valueChanged.connect(self._resize); self.den_cols_spin.valueChanged.connect(self._resize)
        if beta is None: beta=[([1],[1,-1]),([0,1],[1,-1])]
        self.set_beta(beta)

    @staticmethod
    def _table():
        table=QTableWidget(); table.setMinimumHeight(115); table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch); table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents); return table

    def _snapshot(self, table):
        return [[table.item(i,j).text() if table.item(i,j) else '' for j in range(table.columnCount())] for i in range(table.rowCount())]

    def _resize(self):
        old_num=self._snapshot(self.num_table); old_den=self._snapshot(self.den_table)
        rows=self.rows_spin.value(); nc=self.num_cols_spin.value(); dc=self.den_cols_spin.value()
        self._set_dimensions(self.num_table,rows,nc,'b'); self._set_dimensions(self.den_table,rows,dc,'a')
        self._restore(self.num_table,old_num); self._restore(self.den_table,old_den)

    @staticmethod
    def _set_dimensions(table, rows, cols, prefix):
        table.setRowCount(rows); table.setColumnCount(cols); table.setVerticalHeaderLabels([f'beta {i+1}' for i in range(rows)]); table.setHorizontalHeaderLabels([f'{prefix}{j}' for j in range(cols)])

    @staticmethod
    def _restore(table,data):
        for i,row in enumerate(data[:table.rowCount()]):
            for j,text in enumerate(row[:table.columnCount()]):
                if text!='':
                    item=QTableWidgetItem(text); item.setTextAlignment(Qt.AlignmentFlag.AlignCenter); table.setItem(i,j,item)

    def set_beta(self,beta):
        beta=list(beta); rows=max(1,len(beta)); nc=max(len(list(pair[0])) for pair in beta); dc=max(len(list(pair[1])) for pair in beta)
        for spin,value in [(self.rows_spin,rows),(self.num_cols_spin,nc),(self.den_cols_spin,dc)]: spin.blockSignals(True); spin.setValue(value); spin.blockSignals(False)
        self._set_dimensions(self.num_table,rows,nc,'b'); self._set_dimensions(self.den_table,rows,dc,'a'); self.num_table.clearContents(); self.den_table.clearContents()
        for i,(num,den) in enumerate(beta):
            for table,values in [(self.num_table,num),(self.den_table,den)]:
                for j,value in enumerate(values):
                    item=QTableWidgetItem(str(value)); item.setTextAlignment(Qt.AlignmentFlag.AlignCenter); table.setItem(i,j,item)

    @staticmethod
    def _row_values(table,row):
        texts=[table.item(row,j).text().strip() if table.item(row,j) else '' for j in range(table.columnCount())]
        while texts and texts[-1]=='': texts.pop()
        if not texts: raise ValueError(f'beta row {row+1} cannot be empty.')
        return [_number(text if text else '0') for text in texts]

    def beta(self): return [(self._row_values(self.num_table,i),self._row_values(self.den_table,i)) for i in range(self.rows_spin.value())]
    def toPlainText(self): return repr(self.beta())
    def setPlainText(self,text): self.set_beta(ast.literal_eval(str(text)))
    def text(self): return self.toPlainText()
    def setText(self,text): self.setPlainText(text)


def replace_widget(owner, attribute, replacement):
    old=getattr(owner,attribute,None)
    if old is None: return replacement
    layout=old.parentWidget().layout() if old.parentWidget() else None
    if layout is not None: layout.replaceWidget(old,replacement)
    replacement.setParent(old.parentWidget()); old.hide(); old.setParent(None); setattr(owner,attribute,replacement)
    return replacement


def install_matrix_inputs(owner, names):
    """Replace named text coefficient controls and preserve their current values."""
    for attribute, kind in names:
        old=getattr(owner,attribute,None)
        if old is None: continue
        current=old.toPlainText() if hasattr(old,'toPlainText') else old.text()
        widget=BetaTableInput(parent=old.parentWidget()) if kind=='beta' else VectorTableInput(parent=old.parentWidget())
        replace_widget(owner,attribute,widget)
        try:
            widget.setPlainText(current) if kind=='beta' else widget.setText(current)
        except Exception:
            pass
