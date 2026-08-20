using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Text;
using Syncfusion.EJ2.DocumentEditor;
using Syncfusion.EJ2.Spreadsheet;
using Syncfusion.Pdf;
using Syncfusion.Presentation;
using Syncfusion.PresentationRenderer;
using Syncfusion.XlsIO;
using WDocument = Syncfusion.DocIO.DLS.WordDocument;
using WFormatType = Syncfusion.DocIO.FormatType;

namespace WebServiceLibrary
{
    public class WebService
    {
        #region Document Editor APIs
        public string Import(byte[] byteArr, string fileName)
        {
            try
            {
                int index = fileName.LastIndexOf('.');
                string type = index > -1 && index < fileName.Length - 1 ? fileName.Substring(index) : ".docx";
                MemoryStream stream = new MemoryStream(byteArr);
                stream.Position = 0;

                WordDocument document = WordDocument.Load(stream, GetFormatType(type.ToLower()));
                string json = Newtonsoft.Json.JsonConvert.SerializeObject(document);
                document.Dispose();
                stream.Dispose();
                return json;
            }
            catch (Exception ex)
            {
                Trace.WriteLine($"Error loading Word document: {ex.Message}");
                return $"Error loading Word document: {ex.Message}";
            }
        }

      
        public string SystemClipboard(string Content, string type)
        {
            if (Content != null && Content != "")
            {
                try
                {
                    WordDocument document = WordDocument.LoadString(Content, GetFormatType(type.ToLower()));
                    string json = Newtonsoft.Json.JsonConvert.SerializeObject(document);
                    document.Dispose();
                    return json;
                }
                catch (Exception ex)
                {
                    return ex.Message;
                }
            }
            return "";
        }
        public string Save(string content, string fileName)
        {
            try
            {
                string name = fileName;
                string format = RetrieveFileType(name);
                if (string.IsNullOrEmpty(name))
                {
                    name = "Document1.doc";
                }
                WDocument document = WordDocument.Save(content);
                FileStream fileStream = new FileStream(name, FileMode.OpenOrCreate, FileAccess.ReadWrite);
                document.Save(fileStream, GetWFormatType(format));
                document.Close();
                fileStream.Close();
                return "Pass";
            }
            catch (Exception ex)
            {
                return ex.Message;
            }
        }

        private string RetrieveFileType(string name)
        {
            int index = name.LastIndexOf('.');
            string format = index > -1 && index < name.Length - 1 ?
                name.Substring(index) : ".doc";
            return format;
        }

        public string RestrictEditing(string passwordBase64, string saltBase64, int spinCount)
        {
            if (passwordBase64 == "" && passwordBase64 == null)
                return null;
            string[] result = WordDocument.ComputeHash(passwordBase64, saltBase64, spinCount);
            return Newtonsoft.Json.JsonConvert.SerializeObject(result);
        }

        internal static Syncfusion.EJ2.DocumentEditor.FormatType GetFormatType(string format)
        {
            if (string.IsNullOrEmpty(format))
                throw new NotSupportedException("EJ2 DocumentEditor does not support this file format.");
            switch (format.ToLower())
            {
                case ".dotx":
                case ".docx":
                case ".docm":
                case ".dotm":
                    return Syncfusion.EJ2.DocumentEditor.FormatType.Docx;
                case ".dot":
                case ".doc":
                    return Syncfusion.EJ2.DocumentEditor.FormatType.Doc;
                case ".rtf":
                    return Syncfusion.EJ2.DocumentEditor.FormatType.Rtf;
                case ".txt":
                    return Syncfusion.EJ2.DocumentEditor.FormatType.Txt;
                case ".xml":
                    return Syncfusion.EJ2.DocumentEditor.FormatType.WordML;
                case ".html":
                    return Syncfusion.EJ2.DocumentEditor.FormatType.Html;
                default:
                    throw new NotSupportedException("EJ2 DocumentEditor does not support this file format.");
            }
        }
        internal static WFormatType GetWFormatType(string format)
        {
            if (string.IsNullOrEmpty(format))
                throw new NotSupportedException("EJ2 DocumentEditor does not support this file format.");
            switch (format.ToLower())
            {
                case ".dotx":
                    return WFormatType.Dotx;
                case ".docx":
                    return WFormatType.Docx;
                case ".docm":
                    return WFormatType.Docm;
                case ".dotm":
                    return WFormatType.Dotm;
                case ".dot":
                    return WFormatType.Dot;
                case ".doc":
                    return WFormatType.Doc;
                case ".rtf":
                    return WFormatType.Rtf;
                case ".html":
                    return WFormatType.Html;
                case ".txt":
                    return WFormatType.Txt;
                case ".xml":
                    return WFormatType.WordML;
                case ".odt":
                    return WFormatType.Odt;
                default:
                    throw new NotSupportedException("EJ2 DocumentEditor does not support this file format.");
            }
        }
        #endregion

        #region Spreadsheet APIs
        public string Open(byte[] byteArr)
        {
            // Loading the bytes array to stream.
            MemoryStream stream = new MemoryStream(byteArr);
            //Creates a new instance for ExcelEngine
            ExcelEngine excelEngine = new ExcelEngine();

            //Initialize IApplication
            IApplication application = excelEngine.Excel;
            //Loads or open an existing workbook through Open method of IWorkbooks
            IWorkbook workbook = application.Workbooks.Open(stream);
            //OpenRequest open = new OpenRequest();
            //// Converting the stream into FormFile.
            //open.File = new FormFile(stream, 0, bytes.Length, "Sample", "Sample." + "xlsx");
            //var result = Workbook.Open(open);
            var spreadsheet = new SheetOpen();
            var result = spreadsheet.ProcessWorkBook(workbook, new OpenRequest());
            return result;
        }

        public Stream Save(SaveSettings settings)
        {
            return Workbook.Save<Stream>(settings);
        }
        #endregion

        #region presentation APIs
        public PresentationResult PPTLoadFile(string base64, bool viewNotes)
        {
            if (base64 != string.Empty)
            {

                string data = base64.Split(',')[1];
                byte[] bytes = Convert.FromBase64String(data);
                var outputStream = new MemoryStream();
                string base64String;
                var speakerNotes = new Dictionary<int, string>();
                using (Stream stream = new MemoryStream(bytes))
                {
                    IPresentation pptxDoc = Presentation.Open(stream);
                    PresentationToPdfConverterSettings pdfConverterSettings = new PresentationToPdfConverterSettings();
                    if (viewNotes == true) {
                        pdfConverterSettings.PublishOptions = PublishOptions.NotesPages;
                    }
                    for (int i = 0; i < pptxDoc.Slides.Count; i++)
                    {
                        ISlide slide = pptxDoc.Slides[i];
                        StringBuilder textBuilder = new StringBuilder();
                        if (slide.NotesSlide?.NotesTextBody != null)
                        {
                            foreach (IParagraph paragraph in slide.NotesSlide.NotesTextBody.Paragraphs)
                            {
                                textBuilder.AppendLine(paragraph.Text);
                            }
                            speakerNotes.Add(i + 1, textBuilder.ToString().Trim());
                        }
                    }
                    using (PdfDocument pdfDoc = PresentationToPdfConverter.Convert(pptxDoc, pdfConverterSettings))
                    {
                        pptxDoc.Close();
                        pdfDoc.Save(outputStream);
                        outputStream.Position = 0;
                        byte[] byteArray = outputStream.ToArray();
                        pdfDoc.Close();
                        outputStream.Close();
                        base64String = Convert.ToBase64String(byteArray);
                    }
                    return new PresentationResult
                    {
                        PdfBase64 = "data:application/pdf;base64," + base64String,
                        SpeakerNotes = speakerNotes
                    };
                }
            }
            return null;
        }
        public class PresentationResult
        {
            public string PdfBase64 { get; set; }
            public Dictionary<int, string> SpeakerNotes { get; set; }
        }
        #endregion
    }
}
