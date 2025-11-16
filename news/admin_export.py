# news/admin_export.py
from django.utils.encoding import force_str
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from io import BytesIO
from .models import Category, News, Vote

EXPORTABLE_MODELS = {
    'category': Category,
    'news': News,
    'vote': Vote,
}

def safe_value(value):
    if value is None:
        return ''
    if isinstance(value, (int, float, bool)):
        return value
    if hasattr(value, 'strftime'):
        return value.isoformat()
    return str(force_str(value))

def generate_xlsx(model_name, selected_fields):
    model = EXPORTABLE_MODELS.get(model_name)
    if not model:
        raise ValueError("Invalid model name")

    queryset = model.objects.all().values(*selected_fields)

    print("📊 Export data sample:", list(queryset[:2]))

    wb = Workbook()
    ws = wb.active
    title = str(force_str(model._meta.verbose_name_plural or model.__name__))[:31]
    ws.title = title or 'Export'

    # Заголовки
    for col_num, field in enumerate(selected_fields, 1):
        ws[get_column_letter(col_num) + '1'] = field

    # Данные
    for row_num, record in enumerate(queryset, 2):
        for col_num, field in enumerate(selected_fields, 1):
            value = record[field]
            ws[get_column_letter(col_num) + str(row_num)] = safe_value(value)

    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer