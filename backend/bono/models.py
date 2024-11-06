# bono/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from reportlab.pdfgen import canvas
from django.contrib.auth.models import AbstractUser
import os

#User Table
class User(AbstractUser):
    is_superadmin = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_user = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    gender = models.CharField(max_length=10, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    photo = models.ImageField(upload_to='images/', null=True, blank=True)
    status = models.BooleanField(default=True)  # Assuming `status=True` means active
    deleted_by = models.ForeignKey('self', related_name='deleted_users', null=True, blank=True, on_delete=models.SET_NULL)
    added_by = models.ForeignKey('self', related_name='users_added', null=True, blank=True, on_delete=models.SET_NULL)
    status_changed_by = models.ForeignKey('self', related_name='status_changed_users', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateField(auto_now_add=True)


# Bono Table
class Bonos(models.Model):
    khat_owner_name = models.CharField(max_length=255)
    khat_type=(('qudaa','Qudaa'), 
               ('urata','Urata'), 
               ('Qarxii','Qarxii'))
    khat_type = models.CharField(max_length=200, choices=khat_type)
    count = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey('User', default=None, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.khat_owner_name} - {self.khat_type}"

# GeneratedBono Table
class GeneratedBono(models.Model):
    # Foreign keys referencing Bono attributes
    bono = models.ForeignKey(Bonos, default=None, related_name='generated_bonos', on_delete=models.CASCADE)

    # Additional attributes
    price = models.DecimalField(max_digits=10, decimal_places=2)
    trader_signature = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey('User', default=None, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Generated Bono for {self.bono.khat_owner_name} - {self.bono.khat_type} - {self.price}"


# Directory to store the generated PDFs
PDF_DIR = 'generated_bonos_pdfs'

# Create directory if it doesn't exist
if not os.path.exists(PDF_DIR):
    os.makedirs(PDF_DIR)

# Signal to generate PDF after a new GeneratedBono instance is saved
@receiver(post_save, sender=GeneratedBono)
def generate_bono_pdf(sender, instance, created, **kwargs):
    if created:
        # Create the PDF filename
        pdf_filename = f"{PDF_DIR}/{instance.id}_bono.pdf"

        # Create a canvas object
        c = canvas.Canvas(pdf_filename)

        # Set PDF Title
        c.setTitle(f"Bono Receipt - {instance.bono.khat_owner_name}")

        # Add content to the PDF
        c.drawString(100, 800, f"Boonoo Jimaa")
        c.drawString(100, 780, f"Abbaa Jimaa: {instance.bono.khat_owner_name}")
        c.drawString(100, 760, f"Gosa Jimaa: {instance.bono.khat_type}")
        c.drawString(100, 740, f"Kiiloo: {instance.bono.count}")
        c.drawString(100, 720, f"Gatii: {instance.price} ETB")
        c.drawString(100, 700, f"Waliigala: {instance.price * instance.bono.count} ETB")
        c.drawString(100, 680, f"Trader Signature: {instance.trader_signature}")
        c.drawString(100, 660, f"Date: {instance.date.strftime('%Y-%m-%d %H:%M:%S')}")
        c.drawString(100, 640, f"Added By: {instance.added_by.username}")

        # Finalize and save the PDF
        c.save()

        print(f"PDF generated and saved as {pdf_filename}")