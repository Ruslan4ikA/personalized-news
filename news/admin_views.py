# news/admin_views.py
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def export_xlsx_view(request):
    ALL_FIELDS = [
        'News_id', 'News_title', 'News_content', 'News_is_published',
        'News_created_at', 'News_updated_at',
        'Category_id', 'Category_name', 'Category_slug',
        'Author_id', 'Author_username', 'Author_email',
        'Vote_id', 'Vote_value', 'Vote_created_at', 'Vote_updated_at',
        'Voter_id', 'Voter_username', 'Voter_email',
    ]

    if request.method == "POST":
        selected_fields = request.POST.getlist("fields")
        if not selected_fields:
            return HttpResponse("Выберите хотя бы одно поле", status=400)

        safe_fields = [f for f in selected_fields if f in ALL_FIELDS]
        if not safe_fields:
            return HttpResponse("Недопустимые поля", status=400)

        try:
            from .admin_export import generate_news_centric_xlsx
            buffer = generate_news_centric_xlsx(safe_fields)
            response = HttpResponse(
                buffer.read(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename=news_full_report.xlsx'
            return response
        except Exception as e:
            return HttpResponse(f"Ошибка: {e}", status=500)

    return render(request, "admin/export_form.html", {
        "fields": ALL_FIELDS,
    })