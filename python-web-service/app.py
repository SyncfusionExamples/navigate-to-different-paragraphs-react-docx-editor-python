from flask import Flask, json, request, Response, send_file, send_from_directory
from flask_cors import CORS #import CORS from flask_cors

import clr #import clr from pythonnet
import os
from io import BytesIO

app = Flask(
__name__,
static_folder='frontend/dist',
static_url_path=''
)
# CORS(app) #enable CORS on the app

# ---- Minimal CORS + large-file support ----
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024 # 500 MB
app.config['MAX_FORM_MEMORY_SIZE'] = 500 * 1024 * 1024 # 500 MB

CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    supports_credentials=False,
    expose_headers=["Content-Disposition", "Content-Length", "Content-Type"],
)

# Force CORS headers on EVERY response (including 413/500 errors)
@app.after_request
def add_cors_on_errors(resp):
    resp.headers["Access-Control-Allow-Origin"]  = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return resp
# -------------------------------------------

# get the current working directory
current_working_directory = os.getcwd()

# Load explicit DLLs from the publish folder (direct AddReference calls).
# `dotnet publish -r linux-x64` drops the artefacts at
#   bin/Release/netstandard2.0/linux-x64/publish/
# while a plain `dotnet publish -c Release` drops them at
#   bin/Release/netstandard2.0/publish/
# Check both so the same code works locally and in the Linux container.
_publish_candidate_a = current_working_directory + "/.NET Standard Wrapper Library/WebServiceLibrary/bin/Release/netstandard2.0/publish/"
_publish_candidate_b = current_working_directory + "/.NET Standard Wrapper Library/WebServiceLibrary/bin/Release/netstandard2.0/linux-x64/publish/"
_publish_candidate_c = current_working_directory + "/.NET Standard Wrapper Library/WebServiceLibrary/runtimes/"
publish_base = _publish_candidate_a if os.path.isdir(_publish_candidate_a) else _publish_candidate_b

# Native runtimes may be placed in either of these locations, depending on
# how `dotnet publish` was invoked:
#   1) <publishBase>/runtimes/linux-x64/native/   (default NuGet layout)
#   2) <publishBase>/                              (when the publish RID
#                                                   matches the container RID
#                                                   and NuGet flattens the layout)
# Check both, and also always include <publishBase> itself since the .so files
# need to be on LD_LIBRARY_PATH for the .NET runtime's dlopen() to succeed.
runtimes_base = publish_base + "runtimes/"

native_search_dirs = [
    os.path.join(runtimes_base, "linux-x64", "native"),
    publish_base,
]

# De-duplicate while preserving order.
_seen = set()
runtime_dirs = []
for d in native_search_dirs:
    if d not in _seen:
        _seen.add(d)
        runtime_dirs.append(d)
        
native_search_dirs_win = [
    os.path.join(_publish_candidate_c, "win-x64", "native"),
    publish_base,
]

# De-duplicate for windows.
for d in native_search_dirs_win:
    if d not in _seen:
        _seen.add(d)
        runtime_dirs.append(d)

for runtime_dir in runtime_dirs:
    if os.path.isdir(runtime_dir):
        os.environ["PATH"] = (
            runtime_dir + os.pathsep + os.environ.get("PATH", "")
        )
        # On Linux, the dynamic loader uses LD_LIBRARY_PATH for .so lookup.
        # Without this, libSkiaSharp.so / libHarfBuzzSharp.so cannot be found
        # and SkiaSharp throws "cannot open shared object file".
        if "LD_LIBRARY_PATH" in os.environ:
            os.environ["LD_LIBRARY_PATH"] = (
                runtime_dir + os.pathsep + os.environ["LD_LIBRARY_PATH"]
            )
        else:
            os.environ["LD_LIBRARY_PATH"] = runtime_dir
        # Also expose the directory to the .NET host for native assembly probing
        os.environ["DOTNET_ADDITIONAL_DEPS"] = (
            (os.environ.get("DOTNET_ADDITIONAL_DEPS", "") + os.pathsep + runtime_dir).strip(os.pathsep)
        )
        # Surface a clear startup message so deployment issues are easy to spot.
        try:
            so_files = sorted(f for f in os.listdir(runtime_dir) if f.endswith(".so"))
        except OSError:
            so_files = []
        print(f"[startup] Native runtime dir: {runtime_dir} ({len(so_files)} .so files: {so_files})")
    else:
        print(f"[startup] Native runtime dir not found: {runtime_dir}")

clr.AddReference(publish_base + "WebServiceLibrary.dll")
clr.AddReference(publish_base + "Syncfusion.EJ2.DocumentEditor.dll")
clr.AddReference(publish_base + "Syncfusion.DocIO.Portable.dll")
clr.AddReference(publish_base + "Syncfusion.Compression.Portable.dll")
clr.AddReference(publish_base + "Syncfusion.OfficeChart.Portable.dll")
clr.AddReference(publish_base + "Syncfusion.Licensing.dll")
clr.AddReference(publish_base + "Newtonsoft.Json.dll")
clr.AddReference(publish_base + "System.Text.Encoding.CodePages.dll")
clr.AddReference(publish_base + "Syncfusion.EJ2.Spreadsheet.dll")
clr.AddReference(publish_base + "BitMiracle.LibTiff.NET.dll")
clr.AddReference(publish_base + "HarfBuzzSharp.dll")
clr.AddReference(publish_base + "Microsoft.Bcl.AsyncInterfaces.dll")
clr.AddReference(publish_base + "SkiaSharp.dll")
clr.AddReference(publish_base + "SkiaSharp.HarfBuzz.dll")
clr.AddReference(publish_base + "Syncfusion.EJ2.dll")
clr.AddReference(publish_base + "Syncfusion.Licensing.dll")
clr.AddReference(publish_base + "Syncfusion.MetafileRenderer.Portable.dll")
clr.AddReference(publish_base + "Syncfusion.Pdf.Imaging.Portable.dll")
clr.AddReference(publish_base + "Syncfusion.Pdf.Portable.dll")
clr.AddReference(publish_base + "Syncfusion.SkiaSharpHelper.Portable.dll")
clr.AddReference(publish_base + "Syncfusion.XlsIO.Portable.dll")
clr.AddReference(publish_base + "Syncfusion.XlsIORenderer.Portable.dll")
clr.AddReference(publish_base + "System.Buffers.dll")
clr.AddReference(publish_base + "System.Memory.dll")
clr.AddReference(publish_base + "System.Numerics.Vectors.dll")
clr.AddReference(publish_base + "System.Runtime.CompilerServices.Unsafe.dll")
clr.AddReference(publish_base + "System.Text.Encoding.CodePages.dll")
clr.AddReference(publish_base + "System.Text.Encodings.Web.dll")
clr.AddReference(publish_base + "System.Text.Json.dll")
clr.AddReference(publish_base + "System.Threading.Tasks.Extensions.dll")
clr.AddReference(publish_base + "Microsoft.AspNetCore.Mvc.Core.dll")
clr.AddReference(publish_base + "Microsoft.AspNetCore.Mvc.Abstractions.dll")
clr.AddReference(publish_base + "Microsoft.AspNetCore.Razor.dll")
clr.AddReference(publish_base + "Syncfusion.Presentation.Portable.dll")
clr.AddReference(publish_base + "Syncfusion.PresentationRenderer.Portable.dll")

#import our Documenteditor class from our C# namespace DocumentEditorLibrary
from WebServiceLibrary import WebService
from Syncfusion.Licensing import SyncfusionLicenseProvider

#import our SpreadsheetEditor class from our C# namespace SpreadsheetLibrary
from WebServiceLibrary import WebService
from Syncfusion.EJ2.Spreadsheet import SaveSettings, SaveType
from Syncfusion.Licensing import SyncfusionLicenseProvider
from System import Enum
from System.IO import SeekOrigin

# Register your Syncfusion license
# SyncfusionLicenseProvider.RegisterLicense("")

docEditor = WebService() #create our Documenteditor object

@app.route('/Import', methods=['POST'])
def importDocument():
    if 'files' in request.files:
        files = request.files['files']
        # Get the stream data
        stream_data = files.stream.read()
        # Get the file name
        file_name = files.filename
        # Calling our Import method from our Documenteditor class which will return the SFDT string
        return docEditor.Import(stream_data, file_name)
    else:
        return ""

@app.route('/SystemClipboard', methods=['POST'])
def systemClipboard():
    # Get the SFDT data from the request
    content = request.json['content']
    # Get the type from the request
    type = request.json['type']
    # Calling our SystemClipboard method from our Documenteditor class which will return the SFDT string
    return docEditor.SystemClipboard(content, type)

@app.route('/RestrictEditing', methods=['POST'])
def restrictEditing():
    passwordBase64 = request.json['passwordBase64']
    slatBase64 = request.json['saltBase64']
    spinCount = request.json['spinCount']
    # Calling our RestrictEditing method from our Documenteditor class which will return the array of System.String represents the password and salt value.
    jsonString = docEditor.RestrictEditing(passwordBase64, slatBase64, spinCount)
    return json.loads(jsonString)

@app.route('/Save', methods=['POST'])
def save():
    # Get the SFDT data from the request
    content = request.json['content']
    # Get the file name from the request
    fileName = request.json['fileName']
    # Calling our Save method from our Documenteditor class which will save the document in the given file name.
    result = docEditor.Save(content, fileName)
    print(result)
    return result

# Register Syncfusion license
SyncfusionLicenseProvider.RegisterLicense("Enter your license key here")

spreadEditor = WebService() #create our SpreadsheetEditor object

@app.route('/OpenExcel', methods=['POST'])
def openExcel():
    if 'file' in request.files:
        files = request.files['file']
        # Get the stream data
        print(files)
        stream_data = files.stream.read()
        # Calling our Open method from our SpreadsheetEditor class which will return the Workbook JSON string
        return spreadEditor.Open(stream_data)
    else:
        return ""

@app.route('/SaveExcel', methods=['POST'])
def saveExcel():
    try:
        # Extract parameters from form data
        json_data = request.form.get('JSONData', '')
        save_type = request.form.get('saveType', 'Xlsx')  # Default to Xlsx
        file_name = request.form.get('fileName', 'Sample')
        
        # Extract PDF layout settings if provided
        pdf_layout_settings = request.form.get('pdfLayoutSettings', '{}')
        
        # Create SaveSettings object
        save_settings = SaveSettings()
        save_settings.JSONData = json_data
        # Convert string to SaveType enum
        save_settings.SaveType = Enum.Parse(SaveType, save_type)
        save_settings.FileName = file_name
        save_settings.PdfLayoutSettings = pdf_layout_settings
        
        # Call the Save method from SpreadsheetEditor class
        file_stream = spreadEditor.Save(save_settings)
        
        # Convert .NET MemoryStream to bytes
        file_stream.Seek(0, SeekOrigin.Begin)  # Seek to beginning
        stream_bytes = file_stream.ToArray()  # Convert to byte array
        file_stream.Dispose()  # Clean up the stream
        
        # Convert bytes to BytesIO for Flask
        output = BytesIO(stream_bytes)
        output.seek(0)
        
        extension = f".{save_type.lower()}"
        # Get the mime type based on the save type.
        mime_type = {
            "xls":  "application/vnd.ms-excel",
            "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "pdf": "application/pdf",
            "csv": "text/csv"
        }.get(save_type.lower(), "application/octet-stream")

        return send_file(
            output,
            as_attachment=True,
            download_name=f"{file_name}{extension}",
            mimetype=mime_type
        )

    except Exception as e:
        import traceback
        error_msg = f"Error saving file: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        return error_msg, 500


SyncfusionLicenseProvider.RegisterLicense("Enter your license key here")

presentationLib = WebService() #create our Presentation object

@app.route('/PPTLoadFile', methods=['POST'])
def pptLoadFile():
    try:
        content = request.json['data']
        viewNotes = bool(request.json.get('viewNotes', False))
        result = presentationLib.PPTLoadFile(content, viewNotes)
        if result is None:
            return app.response_class(
                response=json.dumps({"error": "Invalid input or empty PPT"}),
                status=400,
                mimetype='application/json'
            )
        speaker_notes = {}
        for item in result.SpeakerNotes:
            speaker_notes[str(item.Key)] = item.Value
        response = {
            "pdfBase64": result.PdfBase64,
            "speakerNotes": speaker_notes
        }
        return app.response_class(
            response=json.dumps(response),
            mimetype='application/json'
        )
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        print(f"[PPTLoadFile] ERROR: {e}\n{tb}")
        return app.response_class(
            response=json.dumps({"error": str(e), "trace": tb}),
            status=500,
            mimetype='application/json'
        )

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    if path:
        requested_file = os.path.join(app.static_folder, path)
        if os.path.exists(requested_file):
            return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    app.run(debug=True) # http://localhost:5000/
    # app.run(host='', port=5001, debug=True) # http://localhost:5001/
