from django.shortcuts import render
from django.http import HttpResponse
from .upload_forms import UploadFileForm

import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage

import rispy, bibtexparser
import pandas as pd

## upload interface 
def upload(request):
    return render(request, "upload/upload.html")

## uploading file
def upload_this(request):

    ## Default table
    file_content = None
    uploaded_file = None
    filename = None

    ## Upload logic
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                uploaded_file = request.FILES['file']
                filename = uploaded_file.name

                # Read and save file
                file_content = uploaded_file.read().decode('utf-8')
                saved_file_path = save_file(request, filename, uploaded_file)

                # Process .ris files
                if filename.endswith('.ris'):
                    try:
                        parse_ris(saved_file_path)
                    except Exception as e:
                        print(f"Error parsing RIS file: {e}")

                # Process .bib or .bibtex files
                elif filename.endswith('.bib') or filename.endswith('.bibtex'):
                    try:
                        parse_bibtex(saved_file_path)
                    except Exception as e:
                        print(f"Error parsing BibTeX file: {e}")

                else:
                    print('Unsupported file type')

            except Exception as e:
                print(f"File processing failed: {e}")

        else:
            print("Form is not valid")

    else:
        form = UploadFileForm()


    ## Rendering contents
    return render(request, 'upload/upload_this.html', {
        'form': form,
        'file_content': file_content,
        'filename': filename
    })

## save file to aplication
def save_file(request, filename, uploaded_file):
    try:
        file_extension = filename.split('.')[-1].lower()
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')

        # Ensure the directory exists
        os.makedirs(upload_dir, exist_ok=True)

        # Save the file using Django's file storage
        fs = FileSystemStorage(location=upload_dir)
        saved_filename = fs.save(filename, uploaded_file)
        saved_file_path = fs.path(saved_filename)

        return saved_file_path

    except OSError as e:
        print(f"File system error: {e}")
    except Exception as e:
        print(f"Unexpected error saving file: {e}")

    return None  # Return None if saving failed

## parsing .bib and .bibtex files
def parse_bibtex(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as bibfile:
            bib_database = bibtexparser.load(bibfile)

            bib_df = pd.DataFrame(bib_database.entries)
            bib_df.rename(columns=lambda c: c.lower(), inplace=True)
            bib_df_n = normalize_columns(bib_df)

            save_path = os.path.join(settings.MEDIA_ROOT, 'parsed_data.csv')
            bib_df_n.to_csv(save_path, index='false')

            return bib_df

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except UnicodeDecodeError:
        print(f"Failed to decode file: {file_path}")
    except bibtexparser.bparser.BibTexParserError as e:
        print(f"BibTeX parsing error: {e}")
    except Exception as e:
        print(f"Unexpected error while parsing BibTeX: {e}")

    return pd.DataFrame()  # Return empty DataFrame on failure

## parsing .ris files
def parse_ris(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as risfile:
            ris_database = rispy.load(risfile)
            ris_df = pd.DataFrame(ris_database)
            save_path = os.path.join(settings.MEDIA_ROOT, 'parsed_data.csv')
            ris_df.to_csv(save_path, index='false')
            return ris_df

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except UnicodeDecodeError:
        print(f"Failed to decode RIS file: {file_path}")
    except rispy.RisException as e:
        print(f"RIS parsing error: {e}")
    except Exception as e:
        print(f"Unexpected error while parsing RIS file: {e}")

    return pd.DataFrame()  # Return empty DataFrame on failure


def normalize_columns(df): 
    column_map = {
    'author': 'AU',
    'title': 'TI',
    'journal': 'JO',
    'booktitle': 'T2',
    'year': 'PY',
    'volume': 'VL',
    'number': 'IS',
    'pages': 'SP',  # RIS also uses 'EP' for end page
    'doi': 'DO',
    'url': 'UR',
    'abstract': 'AB',
    'keywords': 'KW',
    'publisher': 'PB',
    'editor': 'ED',
    'type': 'TY'  # Mapped manually from @article, etc.
    }

    # Convert all column names to lower (to match .bib keys)
    df.columns = [col.lower() for col in df.columns]

    # Rename known columns
    normalized_columns = {
        col: column_map.get(col, col.upper())  # map or fallback to upper original
        for col in df.columns
    }

    df.rename(columns=normalized_columns, inplace=True)

    return df