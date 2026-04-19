#!/usr/bin/env python3
import os
import sys
from pathlib import Path

from PySide6.QtCore import Qt, QSize, QSettings, QRect
from PySide6.QtGui import QPixmap, QImage, QIcon, QPainter, QPageLayout, QPageSize
from PySide6.QtPrintSupport import QPrinter, QPrintDialog, QPrinterInfo
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QFrame,
    QComboBox,
    QSpinBox,
    QCheckBox,
    QGroupBox,
    QFileDialog,
    QMessageBox,
    QSizePolicy,
    QGridLayout,
    QListView,
    QAbstractItemView,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
)

from PIL import Image, ImageOps, ImageDraw

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

PAPER_SIZES = {
    "Carta": (2550, 3300),
    "A4": (2480, 3508),
    "Oficio": (2550, 4200),
}

LAYOUT_CONFIGS = {
    "1 foto por hoja": ("grid", 1, 1),
    "2 fotos por hoja": ("grid", 2, 1),
    "4 fotos por hoja": ("grid", 2, 2),
    "6 fotos por hoja": ("grid", 3, 2),
    "9 fotos por hoja": ("grid", 3, 3),
    "Foto carnet 3x4": ("carnet", 0, 0),
}

TEXTS = {
    "es": {
        "app_title": "PhotoWizard Qt",
        "top_group": "Configuración de impresión",
        "printer": "Impresora",
        "paper": "Papel",
        "quality": "Calidad",
        "paper_type": "Tipo de papel",
        "orientation": "Orientación",
        "preview_group": "Vista previa",
        "design_group": "Diseño",
        "bottom_group": "Fotos seleccionadas",
        "add_photos": "Agregar fotos",
        "remove": "Quitar",
        "up": "Subir",
        "down": "Bajar",
        "clear": "Limpiar",
        "copies_each": "Copias de cada",
        "frame_image": "Enmarcar la imagen",
        "save_png": "Guardar PNG",
        "save_pdf": "Guardar PDF",
        "print": "Imprimir",
        "settings": "⚙ Ajustes",
        "language": "Idioma",
        "spanish": "Español",
        "english": "English",
        "settings_title": "Ajustes",
        "settings_saved": "Configuración guardada.",
        "ready": "Listo.",
        "no_printers": "No se detectaron impresoras",
        "printers_detected": "Impresoras detectadas: {printers}",
        "preview_placeholder": "Aquí aparecerá la vista previa",
        "no_images_loaded": "Sin imágenes cargadas",
        "page_x_of_y": "Página {current} de {total}",
        "select_photos_title": "Seleccionar fotos",
        "images_filter": "Imágenes (*.jpg *.jpeg *.png *.bmp *.webp)",
        "added_images": "Se agregaron {count} imagen(es).",
        "remove_warning": "Selecciona una foto para quitar.",
        "photo_removed": "Foto quitada.",
        "photo_up": "Foto movida hacia arriba.",
        "photo_down": "Foto movida hacia abajo.",
        "list_cleared": "Lista de fotos limpiada.",
        "without_images": "Sin imágenes",
        "preview_error": "No se pudo generar la vista previa",
        "preview_status_error": "Error en vista previa",
        "layout_status": "{layout} | {total} imagen(es) totales | Copias: {copies} | Calidad: {quality}",
        "warning": "Atención",
        "save_png_title": "Guardar página actual como PNG",
        "save_pdf_title": "Guardar todas las páginas como PDF",
        "saved_png": "Página guardada como PNG:\n{path}",
        "saved_pdf": "PDF guardado en:\n{path}",
        "success": "Éxito",
        "save_no_pages": "No hay páginas para guardar.",
        "save_png_error": "No se pudo guardar el PNG.\n\n{error}",
        "save_pdf_error": "No se pudo guardar el PDF.\n\n{error}",
        "no_printer_selected": "No hay impresora seleccionada.",
        "add_image_first": "Primero agrega una imagen.",
        "print_success": "Trabajo enviado correctamente a:\n{printer}",
        "print_title": "Impresión",
        "print_error_title": "Error de impresión",
        "print_error_text": "No se pudo imprimir. Puede que alguna opción no sea compatible con la impresora.",
        "general_error": "Error",
    },
    "en": {
        "app_title": "PhotoWizard Qt",
        "top_group": "Print settings",
        "printer": "Printer",
        "paper": "Paper",
        "quality": "Quality",
        "paper_type": "Paper type",
        "orientation": "Orientation",
        "preview_group": "Preview",
        "design_group": "Layout",
        "bottom_group": "Selected photos",
        "add_photos": "Add photos",
        "remove": "Remove",
        "up": "Up",
        "down": "Down",
        "clear": "Clear",
        "copies_each": "Copies each",
        "frame_image": "Frame image",
        "save_png": "Save PNG",
        "save_pdf": "Save PDF",
        "print": "Print",
        "settings": "⚙ Settings",
        "language": "Language",
        "spanish": "Español",
        "english": "English",
        "settings_title": "Settings",
        "settings_saved": "Settings saved.",
        "ready": "Ready.",
        "no_printers": "No printers detected",
        "printers_detected": "Printers detected: {printers}",
        "preview_placeholder": "Preview will appear here",
        "no_images_loaded": "No images loaded",
        "page_x_of_y": "Page {current} of {total}",
        "select_photos_title": "Select photos",
        "images_filter": "Images (*.jpg *.jpeg *.png *.bmp *.webp)",
        "added_images": "{count} image(s) added.",
        "remove_warning": "Select a photo to remove.",
        "photo_removed": "Photo removed.",
        "photo_up": "Photo moved up.",
        "photo_down": "Photo moved down.",
        "list_cleared": "Photo list cleared.",
        "without_images": "No images",
        "preview_error": "Could not generate preview",
        "preview_status_error": "Preview error",
        "layout_status": "{layout} | {total} total image(s) | Copies: {copies} | Quality: {quality}",
        "warning": "Warning",
        "save_png_title": "Save current page as PNG",
        "save_pdf_title": "Save all pages as PDF",
        "saved_png": "Page saved as PNG:\n{path}",
        "saved_pdf": "PDF saved to:\n{path}",
        "success": "Success",
        "save_no_pages": "There are no pages to save.",
        "save_png_error": "Could not save PNG.\n\n{error}",
        "save_pdf_error": "Could not save PDF.\n\n{error}",
        "no_printer_selected": "No printer selected.",
        "add_image_first": "Add an image first.",
        "print_success": "Job sent successfully to:\n{printer}",
        "print_title": "Print",
        "print_error_title": "Print error",
        "print_error_text": "Could not print. Some option may not be supported by the printer.",
        "general_error": "Error",
    }
}

QUALITY_OPTIONS = {
    "es": ["Borrador", "Estándar", "Alta"],
    "en": ["Draft", "Standard", "High"],
}
QUALITY_CODES = {
    "es": {"Borrador": "3", "Estándar": "4", "Alta": "5"},
    "en": {"Draft": "3", "Standard": "4", "High": "5"},
}
PAPER_TYPE_OPTIONS = {
    "es": ["Papel normal", "Glossy brillante", "Glossy mate"],
    "en": ["Plain paper", "Glossy", "Matte glossy"],
}
PAPER_TYPE_CODES = {
    "es": {"Papel normal": "stationery", "Glossy brillante": "photographic-glossy", "Glossy mate": "photographic-matte"},
    "en": {"Plain paper": "stationery", "Glossy": "photographic-glossy", "Matte glossy": "photographic-matte"},
}
ORIENTATION_OPTIONS = {
    "es": ["Vertical", "Horizontal"],
    "en": ["Portrait", "Landscape"],
}


class SettingsDialog(QDialog):
    def __init__(self, parent, lang):
        super().__init__(parent)
        self.setModal(True)
        self.lang = lang
        self.setWindowTitle(parent.tr_text("settings_title"))
        layout = QVBoxLayout(self)
        form = QFormLayout()
        self.lang_combo = QComboBox()
        self.lang_combo.addItem(TEXTS["es"]["spanish"], "es")
        self.lang_combo.addItem(TEXTS["en"]["english"], "en")
        self.lang_combo.setCurrentIndex(0 if lang == "es" else 1)
        form.addRow(parent.tr_text("language"), self.lang_combo)
        layout.addLayout(form)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def selected_language(self):
        return self.lang_combo.currentData()


class ClickablePreviewLabel(QLabel):
    def __init__(self, text=""):
        super().__init__(text)
        self.setAlignment(Qt.AlignCenter)
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("""
            QLabel {
                background: #f3f4f6;
                border: 1px solid #cfd4dc;
                color: #4b5563;
                padding: 12px;
            }
        """)

    def set_preview_pixmap(self, pixmap: QPixmap):
        self.setText("")
        self.setPixmap(pixmap)

    def clear_preview(self, text):
        self.setPixmap(QPixmap())
        self.setText(text)


class LayoutButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setCheckable(True)
        self.setMinimumHeight(42)
        self.setMaximumHeight(46)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setStyleSheet("""
            QPushButton {
                text-align: center;
                padding: 6px 8px;
                border: 1px solid #cbd5e1;
                background: white;
                border-radius: 6px;
                font-size: 11px;
            }
            QPushButton:checked {
                background: #e8f0fe;
                border: 2px solid #4a90e2;
                font-weight: bold;
            }
        """)


class PhotoWizardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("NoobStudios", "PhotoWizard")
        self.lang = self.settings.value("language", "es")
        self.image_paths = []
        self.layout_buttons = {}
        self.current_layout = "1 foto por hoja"
        self.preview_pages = []
        self.current_page_index = 0

        self.resize(900, 600)
        self.setMinimumSize(900, 600)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        self.setWindowFlag(Qt.WindowCloseButtonHint, True)

        self._build_ui()
        self.connect_signals()
        self.select_layout("1 foto por hoja")
        self.load_printers()
        self.apply_language()

    def tr_text(self, key):
        return TEXTS.get(self.lang, TEXTS["es"]).get(key, key)

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(14, 14, 14, 14)
        main_layout.setSpacing(10)

        # top actions
        top_actions = QHBoxLayout()
        top_actions.addStretch()
        self.settings_btn = QPushButton()
        self.settings_btn.setMaximumHeight(30)
        top_actions.addWidget(self.settings_btn)
        main_layout.addLayout(top_actions)

        # Barra superior
        self.top_group = QGroupBox()
        top_layout = QGridLayout(self.top_group)
        top_layout.setHorizontalSpacing(8)
        top_layout.setVerticalSpacing(6)

        self.printer_label = QLabel()
        self.paper_label = QLabel()
        self.quality_label = QLabel()
        self.paper_type_label = QLabel()
        self.orientation_label = QLabel()

        self.printer_combo = QComboBox()
        self.printer_combo.setMinimumWidth(280)
        self.printer_combo.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.paper_combo = QComboBox()
        self.paper_combo.addItems(["Carta", "A4", "Oficio"])

        self.quality_combo = QComboBox()
        self.paper_type_combo = QComboBox()
        self.orientation_combo = QComboBox()

        top_layout.addWidget(self.printer_label, 0, 0)
        top_layout.addWidget(self.paper_label, 0, 1)
        top_layout.addWidget(self.quality_label, 0, 2)
        top_layout.addWidget(self.paper_type_label, 0, 3)
        top_layout.addWidget(self.orientation_label, 0, 4)

        top_layout.addWidget(self.printer_combo, 1, 0)
        top_layout.addWidget(self.paper_combo, 1, 1)
        top_layout.addWidget(self.quality_combo, 1, 2)
        top_layout.addWidget(self.paper_type_combo, 1, 3)
        top_layout.addWidget(self.orientation_combo, 1, 4)

        top_layout.setColumnStretch(0, 2)
        top_layout.setColumnStretch(1, 1)
        top_layout.setColumnStretch(2, 1)
        top_layout.setColumnStretch(3, 1)
        top_layout.setColumnStretch(4, 1)

        main_layout.addWidget(self.top_group)

        # center
        center_layout = QHBoxLayout()
        center_layout.setSpacing(10)

        self.preview_group = QGroupBox()
        self.preview_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        preview_layout = QVBoxLayout(self.preview_group)
        preview_layout.setSpacing(8)

        nav_layout = QHBoxLayout()
        self.prev_page_btn = QPushButton("◀")
        self.next_page_btn = QPushButton("▶")
        self.prev_page_btn.setFixedWidth(32)
        self.next_page_btn.setFixedWidth(32)
        self.page_info_label = QLabel()
        self.preview_status_label = QLabel()
        self.preview_status_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        nav_layout.addWidget(self.prev_page_btn)
        nav_layout.addWidget(self.page_info_label)
        nav_layout.addWidget(self.next_page_btn)
        nav_layout.addStretch()
        nav_layout.addWidget(self.preview_status_label)

        self.preview_label = ClickablePreviewLabel("")
        self.preview_label.setMinimumSize(560, 300)
        self.preview_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        preview_layout.addLayout(nav_layout)
        preview_layout.addWidget(self.preview_label, 1)

        self.side_group = QGroupBox()
        self.side_group.setMinimumWidth(190)
        self.side_group.setMaximumWidth(220)
        side_layout = QVBoxLayout(self.side_group)
        side_layout.setSpacing(6)

        for text in LAYOUT_CONFIGS.keys():
            btn = LayoutButton(text)
            btn.clicked.connect(lambda checked=False, name=text: self.select_layout(name))
            side_layout.addWidget(btn)
            self.layout_buttons[text] = btn

        side_layout.addStretch()

        center_layout.addWidget(self.preview_group, 4)
        center_layout.addWidget(self.side_group, 1)
        main_layout.addLayout(center_layout, 1)

        # bottom
        self.bottom_group = QGroupBox()
        self.bottom_group.setMaximumHeight(170)
        bottom_layout = QVBoxLayout(self.bottom_group)
        bottom_layout.setSpacing(4)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(6)

        self.add_btn = QPushButton()
        self.remove_btn = QPushButton()
        self.up_btn = QPushButton()
        self.down_btn = QPushButton()
        self.clear_btn = QPushButton()

        for btn in [self.add_btn, self.remove_btn, self.up_btn, self.down_btn, self.clear_btn]:
            btn.setMaximumHeight(30)

        buttons_layout.addWidget(self.add_btn)
        buttons_layout.addWidget(self.remove_btn)
        buttons_layout.addWidget(self.up_btn)
        buttons_layout.addWidget(self.down_btn)
        buttons_layout.addWidget(self.clear_btn)
        buttons_layout.addStretch()

        self.photos_list = QListWidget()
        self.photos_list.setViewMode(QListView.IconMode)
        self.photos_list.setResizeMode(QListView.Adjust)
        self.photos_list.setMovement(QListView.Static)
        self.photos_list.setWrapping(False)
        self.photos_list.setFlow(QListView.LeftToRight)
        self.photos_list.setSpacing(8)
        self.photos_list.setIconSize(QSize(72, 72))
        self.photos_list.setGridSize(QSize(110, 92))
        self.photos_list.setMinimumHeight(96)
        self.photos_list.setMaximumHeight(108)
        self.photos_list.setSelectionMode(QAbstractItemView.SingleSelection)

        options_layout = QHBoxLayout()
        options_layout.setSpacing(6)
        self.copies_label = QLabel()
        options_layout.addWidget(self.copies_label)

        self.copies_spin = QSpinBox()
        self.copies_spin.setRange(1, 99)
        self.copies_spin.setValue(1)
        self.copies_spin.setMaximumWidth(72)
        self.copies_spin.setMaximumHeight(28)
        options_layout.addWidget(self.copies_spin)

        self.fill_check = QCheckBox()
        options_layout.addWidget(self.fill_check)
        options_layout.addStretch()

        self.save_png_btn = QPushButton()
        self.save_pdf_btn = QPushButton()
        self.print_btn = QPushButton()

        for btn in [self.save_png_btn, self.save_pdf_btn, self.print_btn]:
            btn.setMaximumHeight(30)

        self.print_btn.setStyleSheet("""
            QPushButton {
                background: #4a90e2;
                color: white;
                font-weight: bold;
                padding: 4px 10px;
                border-radius: 6px;
            }
        """)

        options_layout.addWidget(self.save_png_btn)
        options_layout.addWidget(self.save_pdf_btn)
        options_layout.addWidget(self.print_btn)

        bottom_layout.addLayout(buttons_layout)
        bottom_layout.addWidget(self.photos_list)
        bottom_layout.addLayout(options_layout)

        main_layout.addWidget(self.bottom_group)

        self.statusBar()

    def connect_signals(self):
        self.settings_btn.clicked.connect(self.open_settings)
        self.add_btn.clicked.connect(self.add_photos)
        self.remove_btn.clicked.connect(self.remove_selected_photo)
        self.up_btn.clicked.connect(self.move_selected_up)
        self.down_btn.clicked.connect(self.move_selected_down)
        self.clear_btn.clicked.connect(self.clear_photos)
        self.save_png_btn.clicked.connect(self.save_current_png)
        self.save_pdf_btn.clicked.connect(self.save_all_pdf)
        self.print_btn.clicked.connect(self.print_selected)
        self.photos_list.currentRowChanged.connect(self.on_current_photo_changed)
        self.copies_spin.valueChanged.connect(self.update_preview)
        self.fill_check.stateChanged.connect(self.update_preview)
        self.paper_combo.currentIndexChanged.connect(self.update_preview)
        self.orientation_combo.currentIndexChanged.connect(self.update_preview)
        self.quality_combo.currentIndexChanged.connect(self.update_preview)
        self.prev_page_btn.clicked.connect(self.prev_page)
        self.next_page_btn.clicked.connect(self.next_page)

    def apply_language(self):
        self.setWindowTitle(self.tr_text("app_title"))
        self.settings_btn.setText(self.tr_text("settings"))
        self.top_group.setTitle(self.tr_text("top_group"))
        self.printer_label.setText(self.tr_text("printer"))
        self.paper_label.setText(self.tr_text("paper"))
        self.quality_label.setText(self.tr_text("quality"))
        self.paper_type_label.setText(self.tr_text("paper_type"))
        self.orientation_label.setText(self.tr_text("orientation"))
        self.preview_group.setTitle(self.tr_text("preview_group"))
        self.side_group.setTitle(self.tr_text("design_group"))
        self.bottom_group.setTitle(self.tr_text("bottom_group"))
        self.add_btn.setText(self.tr_text("add_photos"))
        self.remove_btn.setText(self.tr_text("remove"))
        self.up_btn.setText(self.tr_text("up"))
        self.down_btn.setText(self.tr_text("down"))
        self.clear_btn.setText(self.tr_text("clear"))
        self.copies_label.setText(self.tr_text("copies_each"))
        self.fill_check.setText(self.tr_text("frame_image"))
        self.save_png_btn.setText(self.tr_text("save_png"))
        self.save_pdf_btn.setText(self.tr_text("save_pdf"))
        self.print_btn.setText(self.tr_text("print"))

        current_quality = self.quality_combo.currentText()
        self.quality_combo.blockSignals(True)
        self.quality_combo.clear()
        self.quality_combo.addItems(QUALITY_OPTIONS[self.lang])
        default_quality = QUALITY_OPTIONS[self.lang][1]
        if current_quality in QUALITY_OPTIONS[self.lang]:
            self.quality_combo.setCurrentText(current_quality)
        else:
            self.quality_combo.setCurrentText(default_quality)
        self.quality_combo.blockSignals(False)

        current_ptype = self.paper_type_combo.currentText()
        self.paper_type_combo.blockSignals(True)
        self.paper_type_combo.clear()
        self.paper_type_combo.addItems(PAPER_TYPE_OPTIONS[self.lang])
        if current_ptype in PAPER_TYPE_OPTIONS[self.lang]:
            self.paper_type_combo.setCurrentText(current_ptype)
        else:
            self.paper_type_combo.setCurrentIndex(0)
        self.paper_type_combo.blockSignals(False)

        current_ori = self.orientation_combo.currentText()
        self.orientation_combo.blockSignals(True)
        self.orientation_combo.clear()
        self.orientation_combo.addItems(ORIENTATION_OPTIONS[self.lang])
        if current_ori in ORIENTATION_OPTIONS[self.lang]:
            self.orientation_combo.setCurrentText(current_ori)
        else:
            self.orientation_combo.setCurrentIndex(0)
        self.orientation_combo.blockSignals(False)

        self.statusBar().showMessage(self.tr_text("ready"))
        self.update_preview()

    def open_settings(self):
        dialog = SettingsDialog(self, self.lang)
        if dialog.exec():
            self.lang = dialog.selected_language()
            self.settings.setValue("language", self.lang)
            self.apply_language()
            self.statusBar().showMessage(self.tr_text("settings_saved"))

    def on_current_photo_changed(self):
        self.current_page_index = 0
        self.update_preview()

    def update_page_navigation(self):
        total = len(self.preview_pages)
        if total == 0:
            self.page_info_label.setText(self.tr_text("page_x_of_y").format(current=0, total=0))
            self.prev_page_btn.setEnabled(False)
            self.next_page_btn.setEnabled(False)
            return
        self.page_info_label.setText(self.tr_text("page_x_of_y").format(current=self.current_page_index + 1, total=total))
        self.prev_page_btn.setEnabled(self.current_page_index > 0)
        self.next_page_btn.setEnabled(self.current_page_index < total - 1)

    def prev_page(self):
        if self.current_page_index > 0:
            self.current_page_index -= 1
            self.update_preview()

    def next_page(self):
        if self.current_page_index < len(self.preview_pages) - 1:
            self.current_page_index += 1
            self.update_preview()

    def get_printers(self):
        printers = []
        try:
            for printer in QPrinterInfo.availablePrinters():
                name = printer.printerName().strip()
                if name and name not in printers:
                    printers.append(name)
        except Exception:
            pass
        return printers

    def load_printers(self):
        printers = self.get_printers()
        self.printer_combo.clear()
        if printers:
            self.printer_combo.addItems(printers)
            self.printer_combo.setToolTip("\n".join(printers))
            self.statusBar().showMessage(
                self.tr_text("printers_detected").format(printers=", ".join(printers))
            )
        else:
            self.printer_combo.addItem(self.tr_text("no_printers"))
            self.printer_combo.setToolTip(self.tr_text("no_printers"))
            self.statusBar().showMessage(self.tr_text("no_printers"))

    def add_photos(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            self.tr_text("select_photos_title"),
            os.path.expanduser("~/Imágenes"),
            self.tr_text("images_filter")
        )
        if not files:
            return
        added = 0
        for path in files:
            ext = os.path.splitext(path)[1].lower()
            if ext not in SUPPORTED_EXTENSIONS:
                continue
            if path not in self.image_paths:
                self.image_paths.append(path)
                added += 1
        self.refresh_photos_list()
        if self.photos_list.count() > 0 and self.photos_list.currentRow() < 0:
            self.photos_list.setCurrentRow(0)
        self.statusBar().showMessage(self.tr_text("added_images").format(count=added))
        self.update_preview()

    def refresh_photos_list(self):
        self.photos_list.clear()
        for path in self.image_paths:
            item = QListWidgetItem(os.path.basename(path))
            item.setToolTip(path)
            try:
                thumb = Image.open(path).convert("RGB")
                thumb = ImageOps.contain(thumb, (72, 72), method=Image.Resampling.LANCZOS)
                qimage = QImage(thumb.tobytes(), thumb.width, thumb.height, thumb.width * 3, QImage.Format_RGB888)
                item.setIcon(QIcon(QPixmap.fromImage(qimage.copy())))
            except Exception:
                pass
            self.photos_list.addItem(item)

    def remove_selected_photo(self):
        row = self.photos_list.currentRow()
        if row < 0 or row >= len(self.image_paths):
            QMessageBox.warning(self, self.tr_text("warning"), self.tr_text("remove_warning"))
            return
        del self.image_paths[row]
        self.refresh_photos_list()
        if self.image_paths:
            self.photos_list.setCurrentRow(min(row, len(self.image_paths) - 1))
        self.statusBar().showMessage(self.tr_text("photo_removed"))
        self.update_preview()

    def move_selected_up(self):
        row = self.photos_list.currentRow()
        if row <= 0:
            return
        self.image_paths[row - 1], self.image_paths[row] = self.image_paths[row], self.image_paths[row - 1]
        self.refresh_photos_list()
        self.photos_list.setCurrentRow(row - 1)
        self.statusBar().showMessage(self.tr_text("photo_up"))
        self.update_preview()

    def move_selected_down(self):
        row = self.photos_list.currentRow()
        if row < 0 or row >= len(self.image_paths) - 1:
            return
        self.image_paths[row + 1], self.image_paths[row] = self.image_paths[row], self.image_paths[row + 1]
        self.refresh_photos_list()
        self.photos_list.setCurrentRow(row + 1)
        self.statusBar().showMessage(self.tr_text("photo_down"))
        self.update_preview()

    def clear_photos(self):
        self.image_paths.clear()
        self.refresh_photos_list()
        self.preview_pages = []
        self.current_page_index = 0
        self.preview_label.clear_preview(self.tr_text("preview_placeholder"))
        self.preview_status_label.setText(self.tr_text("no_images_loaded"))
        self.statusBar().showMessage(self.tr_text("list_cleared"))
        self.update_page_navigation()

    def select_layout(self, name):
        self.current_layout = name
        for layout_name, button in self.layout_buttons.items():
            button.setChecked(layout_name == name)
        self.current_page_index = 0
        self.update_preview()

    def get_expanded_image_list(self):
        copies = max(1, int(self.copies_spin.value()))
        expanded = []
        for path in self.image_paths:
            expanded.extend([path] * copies)
        return expanded

    def get_page_size(self):
        width, height = PAPER_SIZES[self.paper_combo.currentText()]
        current_orientation = self.orientation_combo.currentText()
        if current_orientation in ("Horizontal", "Landscape"):
            return height, width
        return width, height

    def prepare_image_for_cell(self, img, cell_w, cell_h):
        if self.fill_check.isChecked():
            return ImageOps.fit(img, (cell_w, cell_h), method=Image.Resampling.LANCZOS)
        fitted = ImageOps.contain(img, (cell_w, cell_h), method=Image.Resampling.LANCZOS)
        bg = Image.new("RGB", (cell_w, cell_h), "white")
        x = (cell_w - fitted.width) // 2
        y = (cell_h - fitted.height) // 2
        bg.paste(fitted, (x, y))
        return bg

    def build_page_preview(self, images):
        page_w, page_h = self.get_page_size()
        page = Image.new("RGB", (page_w, page_h), "white")
        if not images:
            return None
        layout_type, cols, rows = LAYOUT_CONFIGS[self.current_layout]
        margin = 55
        gap = 16

        if layout_type == "carnet":
            photo_w = int((3 / 2.54) * 300)
            photo_h = int((4 / 2.54) * 300)
            usable_w = page_w - 2 * margin
            usable_h = page_h - 2 * margin
            cols = max(1, (usable_w + gap) // (photo_w + gap))
            rows = max(1, (usable_h + gap) // (photo_h + gap))
            block_w = cols * photo_w + (cols - 1) * gap
            block_h = rows * photo_h + (rows - 1) * gap
            start_x = max(margin, (page_w - block_w) // 2)
            start_y = max(margin, (page_h - block_h) // 2)

            for i, path in enumerate(images[: cols * rows]):
                img = Image.open(path).convert("RGB")
                fitted = self.prepare_image_for_cell(img, photo_w, photo_h)
                r = i // cols
                c = i % cols
                x = start_x + c * (photo_w + gap)
                y = start_y + r * (photo_h + gap)
                page.paste(fitted, (x, y))
        else:
            usable_w = page_w - 2 * margin - (cols - 1) * gap
            usable_h = page_h - 2 * margin - (rows - 1) * gap
            cell_w = usable_w // cols
            cell_h = usable_h // rows
            for i, path in enumerate(images[: cols * rows]):
                img = Image.open(path).convert("RGB")
                fitted = self.prepare_image_for_cell(img, cell_w, cell_h)
                r = i // cols
                c = i % cols
                x = margin + c * (cell_w + gap)
                y = margin + r * (cell_h + gap)
                page.paste(fitted, (x, y))
        return page

    def build_all_pages(self):
        expanded = self.get_expanded_image_list()
        if not expanded:
            return []
        layout_type, cols, rows = LAYOUT_CONFIGS[self.current_layout]
        if layout_type == "carnet":
            page_w, page_h = self.get_page_size()
            margin = 55
            gap = 16
            photo_w = int((3 / 2.54) * 300)
            photo_h = int((4 / 2.54) * 300)
            usable_w = page_w - 2 * margin
            usable_h = page_h - 2 * margin
            cols = max(1, (usable_w + gap) // (photo_w + gap))
            rows = max(1, (usable_h + gap) // (photo_h + gap))
            slots = cols * rows
        else:
            slots = cols * rows

        pages = []
        for start in range(0, len(expanded), slots):
            batch = expanded[start:start + slots]
            page = self.build_page_preview(batch)
            if page is not None:
                pages.append(page)
        return pages

    def update_preview(self):
        if not self.image_paths:
            self.preview_pages = []
            self.current_page_index = 0
            self.preview_label.clear_preview(self.tr_text("preview_placeholder"))
            self.preview_status_label.setText(self.tr_text("no_images_loaded"))
            self.update_page_navigation()
            return
        try:
            self.preview_pages = self.build_all_pages()
            if not self.preview_pages:
                self.current_page_index = 0
                self.preview_label.clear_preview(self.tr_text("without_images"))
                self.preview_status_label.setText(self.tr_text("without_images"))
                self.update_page_navigation()
                return
            if self.current_page_index >= len(self.preview_pages):
                self.current_page_index = len(self.preview_pages) - 1

            page = self.preview_pages[self.current_page_index]
            container_w = max(360, self.preview_label.width() - 16)
            container_h = max(220, self.preview_label.height() - 16)
            preview = ImageOps.contain(page, (container_w, container_h), method=Image.Resampling.LANCZOS)

            qimage = QImage(preview.tobytes(), preview.width, preview.height, preview.width * 3, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimage.copy())
            self.preview_label.set_preview_pixmap(pixmap)

            total_images = len(self.get_expanded_image_list())
            self.preview_status_label.setText(
                self.tr_text("layout_status").format(
                    layout=self.current_layout,
                    total=total_images,
                    copies=self.copies_spin.value(),
                    quality=self.quality_combo.currentText()
                )
            )
            self.update_page_navigation()
        except Exception as e:
            self.preview_pages = []
            self.current_page_index = 0
            self.preview_label.clear_preview(self.tr_text("preview_error"))
            self.preview_status_label.setText(self.tr_text("preview_status_error"))
            self.update_page_navigation()
            self.statusBar().showMessage(f"{self.tr_text('general_error')}: {e}")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_preview()

    def get_cups_quality_value(self):
        return QUALITY_CODES[self.lang].get(self.quality_combo.currentText(), "4")

    def get_cups_media_type(self):
        return PAPER_TYPE_CODES[self.lang].get(self.paper_type_combo.currentText(), "stationery")

    def get_cups_media_size(self):
        return {"Carta": "Letter", "A4": "A4", "Oficio": "Legal"}.get(self.paper_combo.currentText(), "Letter")

    def save_current_png(self):
        if not self.preview_pages:
            self.update_preview()
        if not self.preview_pages:
            QMessageBox.warning(self, self.tr_text("warning"), self.tr_text("save_no_pages"))
            return
        default_name = f"photowizard_page_{self.current_page_index + 1}.png"
        path, _ = QFileDialog.getSaveFileName(
            self,
            self.tr_text("save_png_title"),
            os.path.join(os.path.expanduser("~/Imágenes"), default_name),
            "PNG (*.png)"
        )
        if not path:
            return
        if not path.lower().endswith(".png"):
            path += ".png"
        try:
            self.preview_pages[self.current_page_index].save(path, "PNG")
            self.statusBar().showMessage(path)
            QMessageBox.information(self, self.tr_text("success"), self.tr_text("saved_png").format(path=path))
        except Exception as e:
            QMessageBox.critical(self, self.tr_text("general_error"), self.tr_text("save_png_error").format(error=e))

    def save_all_pdf(self):
        if not self.preview_pages:
            self.update_preview()
        if not self.preview_pages:
            QMessageBox.warning(self, self.tr_text("warning"), self.tr_text("save_no_pages"))
            return
        path, _ = QFileDialog.getSaveFileName(
            self,
            self.tr_text("save_pdf_title"),
            os.path.join(os.path.expanduser("~/Documentos"), "photowizard.pdf"),
            "PDF (*.pdf)"
        )
        if not path:
            return
        if not path.lower().endswith(".pdf"):
            path += ".pdf"
        try:
            first = self.preview_pages[0]
            rest = self.preview_pages[1:]
            first.save(path, "PDF", resolution=300.0, save_all=True, append_images=rest)
            self.statusBar().showMessage(path)
            QMessageBox.information(self, self.tr_text("success"), self.tr_text("saved_pdf").format(path=path))
        except Exception as e:
            QMessageBox.critical(self, self.tr_text("general_error"), self.tr_text("save_pdf_error").format(error=e))

    def print_selected(self):
        if not self.preview_pages:
            self.update_preview()
        if not self.preview_pages:
            QMessageBox.warning(self, self.tr_text("warning"), self.tr_text("add_image_first"))
            return
        try:
            printer = QPrinter(QPrinter.HighResolution)
            printer.setDocName("PhotoWizard")

            page_size_map = {
                "Carta": QPageSize(QPageSize.Letter),
                "A4": QPageSize(QPageSize.A4),
                "Oficio": QPageSize(QPageSize.Legal),
            }
            selected_paper = self.paper_combo.currentText()
            if selected_paper in page_size_map:
                printer.setPageSize(page_size_map[selected_paper])

            orientation = self.orientation_combo.currentText()
            if orientation in ("Horizontal", "Landscape"):
                printer.setPageOrientation(QPageLayout.Landscape)
            else:
                printer.setPageOrientation(QPageLayout.Portrait)

            dialog = QPrintDialog(printer, self)
            dialog.setWindowTitle(self.tr_text("print_title"))
            if dialog.exec() != QDialog.Accepted:
                return

            painter = QPainter()
            if not painter.begin(printer):
                QMessageBox.critical(self, self.tr_text("general_error"), self.tr_text("print_error_text"))
                return

            for i, pil_page in enumerate(self.preview_pages):
                if i > 0:
                    printer.newPage()

                page_rgb = pil_page.convert("RGB")
                qimage = QImage(
                    page_rgb.tobytes(),
                    page_rgb.width,
                    page_rgb.height,
                    page_rgb.width * 3,
                    QImage.Format_RGB888
                ).copy()

                pixmap = QPixmap.fromImage(qimage)

                rect = printer.pageLayout().paintRectPixels(printer.resolution())
                scaled = pixmap.scaled(
                    rect.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )

                x = rect.x() + (rect.width() - scaled.width()) // 2
                y = rect.y() + (rect.height() - scaled.height()) // 2
                target = QRect(x, y, scaled.width(), scaled.height())
                painter.drawPixmap(target, scaled)

            painter.end()
            printer_name = printer.printerName().strip()
            if printer_name:
                self.statusBar().showMessage(self.tr_text("print_success").format(printer=printer_name))
            else:
                self.statusBar().showMessage(self.tr_text("print_title"))
        except Exception as e:
            QMessageBox.critical(
                self,
                self.tr_text("general_error"),
                f"{self.tr_text('print_error_text')}\n\n{e}"
            )



def find_window_icon():
    candidates = [
        "/app/share/icons/hicolor/256x256/apps/cl.noobstudios.PhotoWizard.png",
        "/app/share/icons/hicolor/512x512/apps/cl.noobstudios.PhotoWizard.png",
        "/usr/share/icons/hicolor/256x256/apps/cl.noobstudios.PhotoWizard.png",
        "/usr/share/pixmaps/cl.noobstudios.PhotoWizard.png",
        str(Path(__file__).resolve().parent / "assets" / "cl.noobstudios.PhotoWizard.png"),
        str(Path(__file__).resolve().parent / "cl.noobstudios.PhotoWizard.png"),
    ]
    for path in candidates:
        if os.path.exists(path):
            return QIcon(path)
    icon = QIcon.fromTheme("cl.noobstudios.PhotoWizard")
    if not icon.isNull():
        return icon
    return QIcon()


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setApplicationName("PhotoWizard")
    app.setDesktopFileName("cl.noobstudios.PhotoWizard")

    icon = find_window_icon()
    if not icon.isNull():
        app.setWindowIcon(icon)

    window = PhotoWizardWindow()
    if not icon.isNull():
        window.setWindowIcon(icon)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
