from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import FileConversion
from file_converter.utils import FileConverter
import os

def convert_file(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return render(request, 'file_converter/upload.html', 
                        {'error': 'Please select a file'})
        
        input_file = request.FILES['file']
        output_format = request.POST.get('output_format')
        
        # Get input format from file extension
        input_format = os.path.splitext(input_file.name)[1][1:].lower()
        
        # Create conversion record
        conversion = FileConversion.objects.create(
            input_file=input_file,
            input_format=input_format,
            output_format=output_format
        )
        
        try:
            # Create paths
            input_path = os.path.join(settings.MEDIA_ROOT, 
                                    'uploads', input_file.name)
            output_filename = f"{os.path.splitext(input_file.name)[0]}.{output_format}"
            output_path = os.path.join(settings.MEDIA_ROOT, 
                                     'converted', output_filename)
            
            # Save uploaded file
            with open(input_path, 'wb+') as destination:
                for chunk in input_file.chunks():
                    destination.write(chunk)
            
            # Perform conversion based on formats
            if input_format == 'pdf' and output_format == 'docx':
                FileConverter.pdf_to_docx(input_path, output_path)
            
            elif input_format == 'docx' and output_format == 'pdf':
                FileConverter.docx_to_pdf(input_path, output_path)
            
            elif input_format in ['jpg', 'jpeg', 'png'] and \
                 output_format in ['jpg', 'jpeg', 'png']:
                FileConverter.image_convert(input_path, output_path, 
                                         output_format.upper())
            
            elif input_format in ['jpg', 'jpeg', 'png'] and \
                 output_format == 'pdf':
                FileConverter.images_to_pdf(input_path, output_path)
            
            else:
                raise ValueError(f"Conversion from {input_format} to "
                              f"{output_format} is not supported")
            
            # Save the converted file to model
            with open(output_path, 'rb') as f:
                conversion.output_file.save(output_filename, f)
            
            conversion.status = 'completed'
            conversion.save()
            
            # Clean up temporary files
            os.remove(input_path)
            os.remove(output_path)
            
            # Redirect to the success page
            return redirect('file_converter:conversion_success', pk=conversion.pk)
            
        except Exception as e:
            conversion.status = 'failed'
            conversion.error_message = str(e)
            conversion.save()
            return render(request, 'file_converter/upload.html', 
                        {'error': str(e)})
    
    return render(request, 'file_converter/upload.html')

def conversion_success(request, pk):
    conversion = get_object_or_404(FileConversion, pk=pk)
    download_url = conversion.output_file.url  # For accessing the converted file
    return render(request, 'file_converter/conversion_success.html', {
        'conversion': conversion,
        'download_url': download_url,
    })



# views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Document
from .utils import DocumentEditor
import os
from django.urls import reverse


def upload_document(request):
    if request.method == 'POST':
        file = request.FILES.get('document')
        if file:
            file_type = file.name.split('.')[-1].lower()
            if file_type in ['pdf', 'docx', 'pptx']:
                document = Document.objects.create(
                    file=file,
                    file_type=file_type
                )
                return redirect(reverse('file_converter:edit_document', kwargs={'pk': document.id}))

    return render(request, 'file_converter/edit_upload.html')

def edit_document(request, pk):
    document = Document.objects.get(pk=pk)
    if request.method == 'POST':
        pages_to_remove = request.POST.getlist('remove_pages[]')
        pages_to_add = request.POST.getlist('add_pages[]')
        insert_positions = request.POST.getlist('insert_positions[]')
        
        # Convert to integers
        pages_to_remove = [int(x) for x in pages_to_remove]
        insert_positions = [int(x) for x in insert_positions]
        
        editor = DocumentEditor()
        method = getattr(editor, f'edit_{document.file_type}')
        
        edited_file = method(
            document.file.path,
            pages_to_remove=pages_to_remove,
            pages_to_add=pages_to_add,
            insert_positions=insert_positions
        )
        
        # Save edited file
        output_path = f'edited_{document.file.name}'
        document.edited_file.save(output_path, edited_file)
        
        return JsonResponse({'success': True, 'download_url': document.edited_file.url})
        
    return render(request, 'file_converter/edit.html', {'document': document})
