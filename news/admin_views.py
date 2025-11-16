# news/admin_views.py
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from .admin_export import EXPORTABLE_MODELS, generate_xlsx

@staff_member_required
def export_xlsx_view(request):
    if request.method == "POST":
        model_name = request.POST.get("model")
        selected_fields = request.POST.getlist("fields")
        print("🔍 POST model_name:", model_name)
        print("🔍 POST selected_fields:", selected_fields)

        if not model_name or model_name not in EXPORTABLE_MODELS:
            return HttpResponse("Invalid model", status=400)

        # Пропускаем фильтрацию — поля доверенные
        if not selected_fields:
            return HttpResponse("No fields selected", status=400)

        try:
            buffer = generate_xlsx(model_name, selected_fields)
            response = HttpResponse(
                buffer.read(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = f'attachment; filename={model_name}_export.xlsx'
            return response
        except Exception as e:
            return HttpResponse(f"Error: {e}", status=500)

    # GET: показать форму
    model_name = request.GET.get("model")
    fields = []
    if model_name and model_name in EXPORTABLE_MODELS:
        model = EXPORTABLE_MODELS[model_name]
        # Базовые поля
        base_fields = [f.name for f in model._meta.get_fields()
                       if not f.many_to_one and (not f.is_relation or f.one_to_one)]
        # Дополнительные связанные поля
        if model_name == 'news':
            base_fields += ['author__username', 'category__name']
        elif model_name == 'vote':
            base_fields += ['user__username', 'news__title']
        fields = base_fields

    # Готовим список для шаблона: [(имя_модели, человекочитаемое_название), ...]
    model_choices = []
    for key, model_class in EXPORTABLE_MODELS.items():
        verbose_name = model_class._meta.verbose_name_plural or model_class.__name__
        model_choices.append((key, verbose_name.capitalize()))

    return render(request, "admin/export_form.html", {
        "model_choices": model_choices,
        "selected_model": model_name,
        "fields": fields,
    })