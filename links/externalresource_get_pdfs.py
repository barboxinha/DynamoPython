"""
ExternalResource.GetPDFs
------------------
Retrieves PDF files and their usage information from a document.
"""
__author__ = "Marco Barboza"


import clr

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import ExternalResourceUtils, ExternalResourceTypes, ImageInstance, FilteredElementCollector


def get_pdfs(doc) -> list:
    """
    Retrieves all PDF file references from the given document.
    """
    pdfs = []
    img_ids = ExternalResourceUtils.GetAllExternalResourceReferences(doc, ExternalResourceTypes.BuiltInExternalResourceTypes.Image)

    if img_ids:
        img_files = [doc.GetElement(id) for id in img_ids]
        pdfs = [img for img in img_files if img.FamilyName == "PDF image"]

    return pdfs


doc = DocumentManager.Instance.CurrentDBDocument

pdf_files = get_pdfs(doc)
pdf_names = [pdf.GetExternalResourceReference(ExternalResourceTypes.BuiltInExternalResourceTypes.Image).GetResourceShortDisplayName() for pdf in pdf_files]
pdf_paths = [pdf.Path for pdf in pdf_files]
img_instances = FilteredElementCollector(doc).OfClass(ImageInstance).ToElements()
pdf_counts = []

for pdf in pdf_files:
    if img_instances:
        pdf_instances = [img for img in img_instances if img.GetTypeId().Equals(pdf.Id)]
        pdf_counts.append(len(pdf_instances))

pdfs = {"Name": pdf_names, "Path": pdf_paths, "Count": pdf_counts}

OUT = pdfs