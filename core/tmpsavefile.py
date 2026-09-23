import pandas as pd
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseBadRequest

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
            headers = df.columns.to_list()
        except Exception as e:
            fs.delete(filename)
            return HttpResponseBadRequest("Couldn't save the headers")

        request.session['temp_csv_file'] = file_path
        request.session['csv_headers'] = headers

        return redirect('map_columns_view')

    return render(request, 'upload.html')