

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import os
import sys

sys.path.append(os.path.dirname(__file__) + '/QtProperty' )
sys.path.append(os.path.dirname(__file__) + '/libqt5' )

from PyQt5.QtWidgets import QApplication, QLineEdit
from PyQt5.QtCore import (
    QTranslator, 
    QVariant, 
    QDate, 
    QTime, 
    QDateTime, 
    Qt, 
    QLocale, 
    QPoint, 
    QPointF, 
    QSize, 
    QSizeF, 
    QRect, 
    QRectF
    )

from PyQt5.QtGui import QKeySequence
from pyqtcore import QList
from qtvariantproperty import QtVariantEditorFactory, QtVariantPropertyManager
from qttreepropertybrowser import QtTreePropertyBrowser

context = None
_property_view = None

def init(context_):
    global context
    context = context_


class PropertyViewDock(QDockWidget):
    def __init__(self):
        super().__init__()

        self._props = {}
        self._groups = {}
        self._props_name = {}
        self._init = False

        self.variantManager = QtVariantPropertyManager()
        self.variantFactory = QtVariantEditorFactory()

        self.variantEditor = QtTreePropertyBrowser()
        self.variantEditor.setFactoryForManager(self.variantManager, self.variantFactory)
        #variantEditor.addProperty(topItem)
        self.variantEditor.setPropertiesWithoutValueMarked(True)
        self.variantEditor.setRootIsDecorated(False)

        self.setWidget(self.variantEditor)
        self.setWindowTitle('Property View')

        self.variantManager.valueChangedSignal.connect(self.on_value_change)

    def on_value_change(self, prop, value):
        if prop in self._props_name:
            self._item.set_prop(self._props_name[prop], value)
    
    def add_prop(self, prop, value, prop_map):
        prop_list = prop.split('::')

        group_name = ''
        for name in prop_list[0:-1]:
            tmp = group_name + "::" + name
            if tmp not in self._groups:
                # 新建组
                item0 = self.variantManager.addProperty(QtVariantPropertyManager.groupTypeId(), name)
                if group_name != "":
                    # 寻找父组
                    self._groups[group_name].addSubProperty(item0)
                else:
                    self.variantEditor.addProperty(item0)
                self._groups[tmp] = item0
            group_name = tmp
        
        if prop in prop_map:
            item = self.variantManager.addProperty(prop_map[prop].type(), prop_list[-1])
            value = prop_map[prop].display_value(value)
        else:
            item = self.variantManager.addProperty(QVariant.String, prop_list[-1])
        item.setValue(value)

        if group_name != "":
            self._groups[group_name].addSubProperty(item)
        else:
            self.variantEditor.addProperty(item)

        self._props[prop] = item
        self._props_name[item] = prop
        

    def select_item(self, item):
        self._props = {}
        self._props_name = {}
        self._groups = {}
        self.variantEditor.clear()

        if not item:
            return 


        prop_map = {}
        exts = context.find_extension("Core::Data::Property")
        for ext in exts:
            prop_map[ext.name()] = ext

        self._init = True
        self._item = item
        props = item.get_props()
        for prop in props:
            value = props[prop]
            self.add_prop(prop, value, prop_map)

        self._init = False

    def update_item(self, item, prop):
        if self._item != item:
            return 
        if self._init == True:
            return 

        if prop in self._props:
            value = item.get_prop(prop)
            self._props[prop].setValue(value)
        else:
            prop_map = {}
            exts = context.find_extension("Core::Data::Property")
            for ext in exts:
                prop_map[ext.name()] = ext
                
            value = item.get_prop(prop)
            if prop in prop_map:
                item = self.variantManager.addProperty(prop_map[prop].type(), prop)
                value = prop_map[prop].display_value(value)
            else:
                item = self.variantManager.addProperty(QVariant.String, prop)
            item.setValue(value)
            self.variantEditor.addProperty(item)
            self._props[prop] = item
            self._props_name[item] = prop

class PaneExtension:
    def add_pane(self, frame):
        global _property_view

        self._view = PropertyViewDock()
        _property_view = self._view
        frame.addDockWidget(Qt.RightDockWidgetArea, self._view)

class PropertyExtensionBasicName:
    # 属性名称
    def name(self):
        return "Basic::Name"
    # 属性类型
    def type(self):
        return QVariant.String
    # 属性编辑
    # 返回值为编辑后的属性值
    def edit(self, value):
        return value
    # 获取属性值的展示文本
    # 某些场景下，属性值与属性值的显示不完全一样
    def display_value(self, value):
        return value

class PropertyExtensionTestLength:
    # 属性名称
    def name(self):
        return "Test::Length"
    # 属性类型
    def type(self):
        return QVariant.Int
    # 属性编辑
    # 返回值为编辑后的属性值
    def edit(self, value):
        return value
    # 获取属性值的展示文本
    # 某些场景下，属性值与属性值的显示不完全一样
    def display_value(self, value):
        return int(value)


def on_select_item(event, node):
    global _property_view
    _property_view.select_item(node)

def on_item_prop_change(event, node, prop, old_value):
    global _property_view
    _property_view.update_item(node, prop)

config = {
    'pluginid': 'UI::Core::PropertyView',
    "extensions" : [
        {
            "name": "PL::Basic::Pane",
            "id": "PL::Basic::Pane::PropertyView",
            "impl": PaneExtension()
        },
        {
            "name": "Core::Data::Property",
            "id": "Core::Data::Property::Basic::Name",
            "impl": PropertyExtensionBasicName()
        },
        {
            "name": "Core::Data::Property",
            "id": "Core::Data::Property::Test::Length",
            "impl": PropertyExtensionTestLength()
        }
        
    ],
    "subscribes" : [
        {
            "name": 'event::DataNode::Select',
            "define": on_select_item
        },
        {
            "name": 'event::DataNode::Modify::Prop',
            "define": on_item_prop_change
        }
    ]
}