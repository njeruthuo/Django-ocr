from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import DocumentForm, DocumentEditForm
from .models import Document

# Not yet installed
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch


# Storage classes
from django.core.files.storage import FileSystemStorage


import cv2 as cv
from PIL import Image
import pytesseract


def image_to_text(image_path: str) -> str:
    img = cv.imread(image_path)
    image_text = pytesseract.image_to_string(img)
    return image_text


def home(request):
    data = Document.objects.all()
    return render(request, 'home.html', {'data': data})


def upload_document(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        file = request.FILES['file']

        image = Image.open(file)

        document_text = pytesseract.image_to_string(image)
        form = Document.objects.create(
            title=title, file=file, document_text=document_text)
        form.save()
        return redirect(reverse('ocr:home'))
    else:
        form = DocumentForm()
    return render(request, 'upload.html', {'form': form})


def edit(request, pk):
    item = Document.objects.get(id=pk)
    form = DocumentEditForm(instance=item)

    if request.method == 'POST':
        form = DocumentEditForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect(reverse('ocr:home'))

    return render(request, 'edit.html', {'form': form, 'item': item})


def delete_content(request, pk: int):
    item = get_object_or_404(Document, id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect(reverse('ocr:home'))
    return render(request, 'delete.html', {'item': item})



def convert_to_pdf(request, pk):
    item = get_object_or_404(Document, id=pk)
    title = item.title
    document_text = item.document_text
    created = item.uploaded_at

    pdf_file = canvas.Canvas(f"{title}{created}.pdf", pagesize=letter)
    pdf_file.setFont("Helvetica", 12)
    pdf_file.drawString(1*inch, 10*inch, document_text)
    pdf_file.save()

    file_storage = FileSystemStorage()
    filename = file_storage.save(
        f"pdf/{title}{created}.pdf", open(f"{title}{created}.pdf", "rb"))

    print("File saved as:", file_storage.path(filename))

    return render(request, 'convert.html', {})
