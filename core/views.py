import os
import pandas as pd
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .forms import MappingForm
from .analyze import run_analysis

def upload_csv_file(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']

        if not csv_file.name.endswith('.csv'):
            return HttpResponseBadRequest("Only CSV files are available")

        fs = FileSystemStorage(location='tmp/')
        filename = fs.save(csv_file.name, csv_file)
        file_path = fs.path(filename)

        try:
            df = pd.read_csv(file_path, nrows=0)

            if len(df.columns) == 1:
                df = pd.read_csv(file_path, sep=';', nrows=0)

            headers = [str(col).strip() for col in df.columns.tolist()]
        except Exception as e:
            fs.delete(filename)
            return HttpResponseBadRequest("Couldn't save the headers")

        request.session['temp_csv_file'] = file_path
        request.session['csv_headers'] = headers

        return redirect('map_columns_view')

    return render(request, 'upload.html')

def map_columns_view(request):
    headers = request.session.get('csv_headers')
    file_path = request.session.get('temp_csv_file')

    if not headers or not file_path:
        return redirect('upload_csv_file')

    if request.method == 'POST':
        form = MappingForm(request.POST, headers=headers)

        if form.is_valid():
            mapping = form.cleaned_data

            report = run_analysis(file_path, mapping)

            if "error" in report:
                    form.add_error(None, report["error"])
                    return render(request, 'map_columns.html', {'form': form})

            request.session['analysis_report'] = report

            if os.path.exists(file_path):
                os.remove(file_path)
            del request.session['csv_headers']
            del request.session['temp_csv_file']

            return redirect('analysis_results_view')

    else:
        form = MappingForm(headers=headers)

    return render(request, 'map_columns.html', {'form' : form})

def analysis_results_view(request):
    report = request.session.get('analysis_report')
    
    if not report:
        return redirect('upload_csv_file')
        
    return render(request, 'results.html', {'report': report})

def download_pdf_view(request):
    report = request.session.get('analysis_report')
    
    if not report:
        return redirect('upload_csv_file')
        
    template_path = 'pdf_report.html'
    context = {'report': report}
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Business_Analysis_Report.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse('There was an error generating PDF file.', status=500)
        
    return response