# How to Navigate to Different Paragraphs in a DOCX Editor using Python

This sample demonstrates how to programmatically locate, highlight, and navigate to specific paragraphs in a DOCX document using the Syncfusion® React DOCX Editor and a Python backend service. The application highlights predefined paragraphs, creates bookmarks for navigation, and allows users to quickly move between highlighted sections through a findings panel.

## Running the Sample

### Server-Side Setup (Python Web Service)

#### 1. Navigate to the .NET Wrapper Project

```bash
cd .NET Standard Wrapper Library
```

#### 2. Build the Wrapper Library

```bash
dotnet build -c Release
```

#### 3. Publish the Wrapper Library

```bash
dotnet publish -c Release
```

#### 4. Navigate to the Python Service

```bash
cd ../python-web-service
```

#### 5. Install Required Python Packages

```bash
pip install -r requirements.txt
```

#### 6. Start the Python Service

```bash
python app.py

or

py app.py
```

The service will start at:

```text
http://127.0.0.1:5000/
```

### Client-Side Setup (React Application)

#### 1. Navigate to the React Application

```bash
cd frontend
```

#### 2. Install Dependencies

```bash
npm install
```
### 3. Configure Service URLs

**Document Editor**

```typescript
serviceUrl = "http://127.0.0.1:5000/"
```

#### 4. Start the Application

```bash
npm run dev
```

Open the application using the URL displayed in the terminal.

# License 

This is a commercial product and requires a paid license for possession or use. Syncfusion's licensed software, including this component, is subject to the terms and conditions of [Syncfusion's EULA](https://www.syncfusion.com/license/studio/22.2.5/syncfusion_essential_studio_eula.pdf?utm_source=github&utm_medium=listing&utm_campaign=github-react-docx-editor-examples). You can purchase a license [here](https://www.syncfusion.com/sales/products?utm_source=github&utm_medium=listing&utm_campaign=github-react-docx-editor-examples) or start a free 30\-day trial [here](https://www.syncfusion.com/account/manage-trials/start-trials?utm_source=github&utm_medium=listing&utm_campaign=github-react-docx-editor-examples).

# About Syncfusion&reg;

Founded in 2001 and headquartered in Research Triangle Park, N.C., Syncfusion&reg; has more than 29,000 customers and more than 1 million users, including large financial institutions, Fortune 500 companies, and global IT consultancies.

Today, we provide 1700+ components and frameworks for web ([Blazor](https://www.syncfusion.com/blazor-components?utm_source=github&utm_medium=listing&utm_campaign=github-react-docx-editor-examples), [ASP.NET Core](https://www.syncfusion.com/aspnet-core-ui-controls?utm_source=github&utm_medium=listing&utm_campaign=github-react-docx-editor-examples), [ASP.NET MVC](https://www.syncfusion.com/aspnet-mvc-ui-controls?utm_source=github&utm_medium=listing&utm_campaign=github-react-docx-editor-examples), [ASP.NET WebForms](https://www.syncfusion.com/jquery/aspnet-webforms-ui-controls?utm_source=github&utm_medium=listing&utm_campaign=github-react-docx-editor-examples), [JavaScript](https://www.syncfusion.com/javascript-ui-controls?utm_source=github&utm_medium=listing&utm_campaign=github-react-docx-editor-examples), [Angular](https://www.syncfusion.com/angular-ui-components?utm_source=github&utm_medium=listing&utm_campaign=github-react-docx-editor-examples), [React](https://www.syncfusion.com/react-ui-components?utm_source=github&utm_medium=listing&utm_campaign=github-react-docx-editor-examples), [Vue](https://www.syncfusion.com/vue-ui-components?utm_source=github&utm_medium=listing&utm_campaign=github-react-docx-editor-examples), and [Flutter](https://www.syncfusion.com/flutter-widgets?utm_source=github&utm_medium=listing&utm_campaign=github-react-docx-editor-examples)), mobile ([Xamarin](https://www.syncfusion.com/xamarin-ui-controls?utm_source=github&utm_medium=listing&utm_campaign=github-react-docx-editor-examples), [Flutter](https://www.syncfusion.com/flutter-widgets?utm_source=github&utm_medium=listing&utm_campaign=github-react-docx-editor-examples), [UWP](https://www.syncfusion.com/uwp-ui-controls?utm_source=github&utm_medium=listing&utm_campaign=github-react-docx-editor-examples), and [JavaScript](https://www.syncfusion.com/javascript-ui-controls?utm_source=github&utm_medium=listing&utm_campaign=github-react-docx-editor-examples), [.NET MAUI](https://www.syncfusion.com/maui-controls?utm_source=github&utm_medium=listing&utm_campaign=github-react-docx-editor-examples)) and desktop development ([WinForms](https://www.syncfusion.com/winforms-ui-controls?utm_source=github&utm_medium=listing&utm_campaign=github-react-docx-editor-examples), [WPF](https://www.syncfusion.com/wpf-ui-controls?utm_source=github&utm_medium=listing&utm_campaign=github-react-docx-editor-examples), [WinUI](https://www.syncfusion.com/winui-controls?utm_source=github&utm_medium=listing&utm_campaign=github-react-docx-editor-examples), [Flutter](https://www.syncfusion.com/flutter-widgets?utm_source=github&utm_medium=listing&utm_campaign=github-react-docx-editor-examples), [UWP](https://www.syncfusion.com/uwp-ui-controls?utm_source=github&utm_medium=listing&utm_campaign=github-react-docx-editor-examples), and [.NET MAUI](https://www.syncfusion.com/maui-controls?utm_source=github&utm_medium=listing&utm_campaign=github-react-docx-editor-examples)) a. We provide ready-to-deploy enterprise software for dashboards, reports, data integration, and big data processing. Many customers have saved millions in licensing fees by deploying our software.