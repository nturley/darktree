import argparse
import json
import os
import sys

from PySide2.QtCore import QFile, Qt
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QTreeWidgetItem, QFileDialog
import qdarkstyle

if hasattr(sys,'frozen'):
    main_ui_path = os.path.join(sys._MEIPASS, "main.ui")
else:
    main_ui_path = os.path.join(os.path.dirname(__file__), "main.ui")

# store main window and netlist in a global
window = None
netlist = None

def walk_module(module, parent, ancestry):
    modules = netlist['modules']
    cell_parent = QTreeWidgetItem(parent, ['cells'])
    cell_parent.full_name = ancestry
    for k, cell in module['cells'].items():
        cell_type = cell['type']
        cell['name'] = k
        disp_name = k + ' : ' + cell_type
        cell_item = QTreeWidgetItem(cell_parent, [disp_name])
        cell_item.model = cell
        cell_item.full_name = ancestry + '/' + k
        if cell_type in modules:
            walk_module(modules[cell_type], cell_item, cell_item.full_name)
    nets_parent = QTreeWidgetItem(parent, ['nets'])
    nets_parent.full_name = ancestry
    for k, net in module['netnames'].items():
        net_item = QTreeWidgetItem(nets_parent, [k])
        net_item.model = net
        net_item.full_name = ancestry + '/' + k
        net['name'] = k

def update_hierarchy_tree(fname):
    global netlist
    with open(fname) as f:
        netlist = json.load(f)
    modules = netlist['modules']
    top_module = list(modules.items())[0][0]
    for k, v in modules.items():
        attrs = v.get('attributes', {})
        if 'top' in attrs:
            top_module = k
    window.treeWidget.clear()
    root_item = QTreeWidgetItem(window.treeWidget)
    root_item.setText(0, top_module)
    root_item.full_name = top_module
    root_item.model = modules[top_module]
    walk_module(modules[top_module], root_item, top_module)
    window.treeWidget.expandAll()

def open_dialog():
    fname, _ = QFileDialog.getOpenFileName(window, 'Open file', '', 'Yosys JSON (*.json)')
    if fname:
        update_hierarchy_tree(fname)

def treeselectchanged():
    window.propertyTree.clear()
    if len(window.treeWidget.selectedItems()) == 0:
        return
    selected = window.treeWidget.selectedItems()[0]
    if not hasattr(selected, 'model'):
        selected = selected.parent()
    model = selected.model
    props = ['name', 'type', 'hide_name']
    for prop in props:
        if prop in model:
            QTreeWidgetItem(window.propertyTree, [prop, str(model[prop])])
    nested_props = ['parameters', 'attributes']
    for prop in nested_props:
        if prop in model:
            new_item = QTreeWidgetItem(window.propertyTree, [prop, ''])
            for k, v in model[prop].items():
                QTreeWidgetItem(new_item, [k, str(v)])
    window.propertyTree.expandAll()
    window.statusbar.showMessage(selected.full_name)

def run_app(argv, json_netlist):
    app = QApplication(argv)
    file = QFile(main_ui_path)
    file.open(QFile.ReadOnly)
    loader = QUiLoader()
    global window
    window = loader.load(file)
    window.treeWidget.clear()
    window.propertyTree.clear()
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    window.actionOpen.triggered.connect(open_dialog)
    window.treeWidget.itemSelectionChanged.connect(treeselectchanged)
    if json_netlist:
        update_hierarchy_tree(json_netlist)
    window.show()
    sys.exit(app.exec_())

def main():
    parser = argparse.ArgumentParser(description='Netlist Hierarchy Viewer')
    parser.add_argument('json_netlist', type=str,
                    help='Yosys JSON Netlist', nargs='?', default='')
    args = parser.parse_args()
    run_app(sys.argv, args.json_netlist)

if __name__ == '__main__':
    main()

