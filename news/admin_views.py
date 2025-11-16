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

        if not model_name or model_name not in EXPORTABLE_MODELS:
            return HttpResponse("Invalid model", status=400)

        model = EXPORTABLE_MODELS[model_name]
        available_fields = [f.name for f in model._meta.get_fields() if not f.many_to_one and not f.is_relation or f.one_to_one]

        # Фильтруем только существующие поля
        safe_fields = [f for f in selected_fields if f in available_fields]

        if not safe_fields:
            return HttpResponse("No valid fields selected", status=400)

        try:
            buffer = generate_xlsx(model_name, safe_fields)
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
        fields = [f.name for f in model._meta.get_fields() if not f.many_to_one and (not f.is_relation or f.one_to_one)]

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