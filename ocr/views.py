import cv2 as cv
import pytesseract
from PIL import Image

from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from .models import Document, Page
from .forms import DocumentForm, DocumentEditForm

from django.urls import reverse
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404


def image_to_text(image_path: str) -> str:
    img = cv.imread(image_path)
    image_text = pytesseract.image_to_string(img)
    return image_text


@login_required(login_url='user:login')
def home(request):
    user = request.user
    data = Document.objects.all().filter(owner=user)
    return render(request, 'home.html', {'data': data})


@login_required(login_url='user:login')
def upload_document(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        file = request.FILES['file']
        user = request.user

        image = Image.open(file)

        document_text = pytesseract.image_to_string(image)

        form = Document.objects.create(
            title=title, owner=user, file=file, document_text=document_text)
        form.save()
        return redirect(reverse('ocr:home'))
    else:
        form = DocumentForm()
    return render(request, 'upload.html', {'form': form, })


@login_required(login_url='user:login')
def generate_pdf(request, id):
    # text = document.document_text
    document = Document.objects.get(id=id)

    # Get the generated OCR text
    ocr_text = document.document_text
    # ocr_text = request.GET.get('document_text')

    # Create a BytesIO buffer for the PDF
    buffer = BytesIO()

    # Create the PDF object using ReportLab
    pdf = canvas.Canvas(buffer, pagesize=letter)

    x = 100  # x-coordinate remains constant for all lines
    y = 400  # starting y-coordinate

    # Split the text into lines and iterate over them
    lines = ocr_text.split('\n')

    for line in lines:
        pdf.drawString(x, y, line)
        y -= 20  # decrement y-coordinate for the next line

    text_height = len(lines) * 20  # Assuming each line is 20 units in height
    if text_height > y:
        pdf.setPageSize((letter[0], text_height + 100))

    # Save the PDF
    pdf.showPage()
    pdf.save()

    # Rewind the buffer and create the FileResponse
    buffer.seek(0)
    response = FileResponse(buffer, as_attachment=True,
                            filename=f'{document.title}.pdf')
    return response


@login_required(login_url='user:login')
def edit(request, pk):
    item = Document.objects.get(id=pk)
    form = DocumentEditForm(instance=item)

    if request.method == 'POST':
        form = DocumentEditForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect(reverse('ocr:home'))

    return render(request, 'edit.html', {'form': form, 'item': item})


@login_required(login_url='user:login')
def delete_content(request, pk: int):
    item = get_object_or_404(Document, id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect(reverse('ocr:home'))
    return render(request, 'delete.html', {'item': item})
