"""
Application.GetOpenDocumentByName
---------------------------------
Gets an open document given its name.
"""
__author__ = "Marco Barboza"


import clr

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")
from Autodesk.Revit.DB import Document
from Autodesk.Revit.UI import UIDocument, UIApplication


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication 
app = uiapp.Application

doc_name = IN[0]


def get_open_document_by_name(active_doc, _app, document_name):
    """Gets an open document within the active session given its name."""
    if document_name:
        open_docs = [o_doc for o_doc in _app.Documents if o_doc.Title != active_doc.Title and not o_doc.IsFamilyDocument]
    
    if open_docs:
        doc_titles = [d.Title for d in open_docs]

        if document_name in doc_titles:
            for title, od in zip(doc_titles, open_docs):
                if title == document_name:
                    return od
    
    return None


if doc_name:
    if app.Documents.Size == 1:
        OUT = "There are no other open documents in Revit.\nTry opening one."
    else:
        open_doc = get_open_document_by_name(doc, app, doc_name)

        if open_doc:
            OUT = open_doc
        else:
            OUT = "There are no open documents matching that name.\nTry another name."
else:
    OUT = "Please input a document name to search for."