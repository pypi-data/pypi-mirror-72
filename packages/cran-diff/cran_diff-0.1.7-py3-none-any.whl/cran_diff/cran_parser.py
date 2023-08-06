from tqdm import tqdm
import os
import urllib
import tarfile
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import requests
from bs4 import BeautifulSoup, SoupStrainer
from datetime import datetime, timedelta
from dateutil import parser
from deb_pkg_tools.control import deb822_from_string
from deb_pkg_tools.control import parse_control_fields
from deb_pkg_tools.deps import parse_depends


from .populate_db import *

from .rcom import RCom
import csv

from .models import Packages
from .models import Imports
from .models import Suggests
from .models import Exports
from .models import Arguments
from .models import News
from .models import Tags
from .models import TagMembers
from .models import setup_db

import concurrent.futures

from typing import List, Any

import pandas as pd





class CranParser:
    def __init__(self,
        connection_string,
        package_list_url='https://cran.rstudio.com/src/contrib/PACKAGES', 
        download_path='./downloads',
        max_pool = 32):
        
        self.set_download_path(download_path)

        # create the engine and session for database
        print("Creating SQL engine and session objects")
        self.connection_string = connection_string
        self.engine = create_engine(connection_string)
        Session = sessionmaker(bind = self.engine)
        self.session = Session()

        self.set_cran_metadata(package_list_url)

        # create a worker pool for background tasks
        self.set_max_pool(max_pool)

        self.change_current = []
        self.change_archive = []

        # create comminication object for running R code
        print("Creating R communication object")
        self.communicator = RCom()
    
    def set_max_pool(self, max_pool):
        print("Setting max workers in pool to ", max_pool)
        self.MAX_POOL = max_pool

    def search_archive(self):
        packages = map(lambda x: x[0], self.meta_data)
        def inner(package):
            archive_versions = get_archive_name_versions(package)
            # print("Found archive for ", package)
            return archive_versions
        futures = []
        res = []
        with concurrent.futures.ThreadPoolExecutor(self.MAX_POOL) as executor:
            for package in packages:
                future = executor.submit(inner, package) 
                futures.append(future)
        # once they have all finished
            for f in tqdm(concurrent.futures.as_completed(futures), total = len(futures)):
                temp = f.result()
                res += temp
        self.archive = res

    def initial_db_fill(self):
        print("Setting up DB")
        setup_db(self.connection_string)
        print("Search archive")
        self.search_archive()
        self.get_current_packages()
        self.detect_meta_not_stored()
        self.detect_archive_not_stored()
        package_list = self.combine_change()
        self.download_and_parse_packages(package_list)
        for data in self.to_insert:
            self.soft_insert(data)
        self.session.commit()
    
    def update_db(self):
        print("Get current packages")
        self.get_current_packages()
        print("Detect changes")
        self.detect_meta_not_stored()
        package_list = self.combine_change()
        self.download_and_parse_packages(package_list)
        self.soft_update()
        self.session.commit()

    
    def combine_change(self):
        return list(map(lambda x: (x[0], x[1], "current"), self.change_current)) + list(map(lambda x: (x[0], x[1], "archived"), self.change_archive))



    
    def download_and_parse_packages(self, package_list):
        def inner(package, version, package_type):
            # print("Downloading ", package, " ", version, " ", package_type)
            try:
                if package_type == "current":
                    tar_file = download_tar_file(package, version, False, self.download_path)
                elif package_type == "archived":
                    tar_file = download_tar_file(package, version, True, self.download_path)
                if tar_file:
                    # print("Processing ", tar_file)
                    return package, version, package_type, process_tar(tar_file)
            except Exception as e:
                print(e)

        futures = []
        self.to_insert = []
        with concurrent.futures.ThreadPoolExecutor(self.MAX_POOL) as executor:
            print("Start download and processing")
            # submit those in current list
            for package, version, package_type in package_list:
                future = executor.submit(inner, package = package, version = version, package_type = package_type) 
                futures.append(future)
            # as they complete, read news and enter into database
            for future in tqdm(concurrent.futures.as_completed(futures), total = len(futures)):
                res = future.result()
                if res:
                    package, version, package_type, data = res
                    lib_loc = os.path.dirname(data['package_location'])
                    exports, types = self.read_exports(package, version, lib_loc)
                    categories, text = self.read_news(package, version, lib_loc)
                    data.update({
                        'exports': exports,
                        'types': types,
                        'categories': categories,
                        'text': text,
                        'package': package,
                        'version': version,
                        'package_type': package_type
                    })
                    self.to_insert += [data]
    
    def soft_update(self):
        package_keys = ['name','version']
        downloaded = [(d['name'], d['version']) for d in self.to_insert]
        new_packages_ix = self.find_new_packages(downloaded)
        print("Adding new packages")
        self.soft_insert([self.to_insert[i] for i in new_packages_ix])
        print("Updating updated packages")
        updated_packages, updated_packages_ix = self.find_updated_packages(downloaded)
        updated_ids = self.find_updated_ids(updated_packages)
        self.set_to_archive(updated_ids)
        print("Adding updated packages to DB")
        self.soft_insert([self.to_insert[i] for i in updated_packages_ix])
        print("Archiving removed packages")
        removed_packages = self.find_removed_package_ids()
        self.set_to_archive(removed_packages)

    
    def set_to_archive(self, ids):
        print("Archiving packages with ids ", ids)
        updater = update(Packages).where(Packages.id.in_(ids)).values(package_type = "archived")
        self.session.execute(updater)
    
    def find_updated_ids(self, updated_packages):
        names = [x for x,y in updated_packages]
        sub_packages = self.current_packages.query("package_type == 'current' & name == @names")
        ids = list(sub_packages['id'])
        return ids

    def find_new_packages(self, downloaded):
        existing = set(self.current_packages['name'])
        res =  [i for i, x in enumerate(downloaded) if x[0] not in existing]
        print("Found ", len(res), " new packages")
        return res
    
    def find_updated_packages(self, downloaded):
        existing =set(self.current_packages['name'])
        res_ix = [i for i, x in enumerate(downloaded) if x[0] in existing]
        res = [downloaded[i] for i in res_ix]
        print("Found ", len(res), " updated packages")
        return res, res_ix
    
    def find_removed_package_ids(self):
        sub_packages = self.current_packages.query("package_type == 'current'")
        res = list(set(sub_packages['name']) - set([x[0] for x in self.meta_data]))
        res = list(sub_packages.query('name == @res')['id'])
        print("Found ", len(res), " removed packages.")
        return res

        

    def soft_insert(self, data_vals):
        for data in data_vals:
            package_keys = ['name', 'title', 'version', 'date', 'description', 'maintainer', 'url', 'bugreport', 'package_type']
            if data['name'] == 'PCMBase':
                print("Will not try to add data for PCMBase")
                continue
            package_data = {k: data[k] for k in package_keys}
            package_info = Packages(**package_data)
            self.session.add(package_info)
            self.session.flush()
            self.session.refresh(package_info)
            id_num = package_info.id
            for k, v in data['imports'].items():
                import_info = Imports(package_id=id_num, name=k, version=v)
                self.session.add(import_info)

            for k, v in data['suggests'].items():
                suggest_info = Suggests(package_id=id_num, name=k, version=v)
                self.session.add(suggest_info)

            exports = data['exports']
            types = data['types']
            for i in range(len(exports)):
                export_info = Exports(package_id=id_num, name=exports[i], type=types[i])
                self.session.add(export_info)

            functions = data['functions']
            arguments = data['arguments']
            defaults = data['defaults']
            for i in range(len(functions)):
                for j in range(len(arguments[i])):
                    argument_info = Arguments(package_id=id_num, function=functions[i], name=arguments[i][j], default=defaults[i][j])
                    self.session.add(argument_info)

            categories = data['categories']
            text = data['text']
            for i in range(len(categories)):
                news_info = News(package_id=id_num, category=categories[i], text=text[i])
                self.session.add(news_info)


    def read_news(self, package, version, lib_loc):
        # print("Read news, ")
        # print(package)
        # print(version)
        # print(lib_loc)
        news_file = self.communicator.write_news(package, version, lib_loc)
        categories = []
        text_list = []
        if os.path.exists(news_file):
            with open(news_file, newline = '') as File:
                reader = csv.reader(File)
                for row in reader:
                    if row[0] == version:
                        if row[2] == 'NA':
                            categories.append('')
                        else:
                            categories.append(row[2])
                        text_list.append(row[3])
            os.remove(news_file)
        return(categories, text_list)


    def read_exports(self, package, version, lib_loc):
        exports_file = self.communicator.write_exports(package, version, lib_loc)
        exports = []
        types = []
        if os.path.exists(exports_file):
            with open(exports_file, newline = '') as File:
                reader = csv.reader(File)
                next(reader, None)  #Skip the headers
                for row in reader:
                    exports.append(row[0])
                    types.append(row[1])
            os.remove(exports_file)
        return(exports, types)

    
    def detect_meta_not_stored(self):
        cur = list(zip(self.current_packages['name'], self.current_packages['version']))
        self.change_current = list(filter(lambda x: not x in cur,self.meta_data))
    
    def detect_archive_not_stored(self):
        if not self.archive:
            raise Exception("You must search the archive before determining what is missing")
        cur = list(zip(self.current_packages['name'], self.current_packages['version']))
        self.change_archive = list(filter(lambda x: not x in cur,self.archive))

    def get_current_packages(self):
        pinfo = pd.read_sql_table('packages', self.engine)
        self.current_packages = pinfo
        return self.current_packages

    def set_download_path(self, download_path):
        # set somewhere for download
        print("Preparing for downloads in ", download_path)
        self.ensure_download_path(download_path)
        self.download_path = download_path

    
    def set_cran_metadata(self, url):
        print("Obtaining CRAN metadata from ", url)
        r = requests.get(url)
        output = r.text
        self.meta_data = parse_metadata(output)
        
    def ensure_download_path(self, download_path):
        """Ensure that the provided download path exists

        :params:
        download_path: A place to store downloaded tars
        """
        os.makedirs(download_path, exist_ok = True)


def parse_metadata(cran_metadata):
    """
    Create an enumerate object from cran metadata

    returns enumerate object, together with its length
    """
    #Split metadata into separate chunk for each package
    chunks = drop_duplicates(cran_metadata.split("\n\n"))
    return [get_package_and_version(chunk) for chunk in chunks]


def get_package_and_version(chunk):
    """Extracts the package and version from CRAN metadata chunk
    
    :params:
    chunk: A single string chunk of CRAN metadata

    """
    unparsed_fields = deb822_from_string(chunk)
    parsed_fields = parse_control_fields(unparsed_fields)
    package = parsed_fields['Package']
    version = parsed_fields['Version']
    return package, version


def drop_duplicates(l: List[Any])-> List[Any]:
    return list(set(l))


def get_archive_name_versions(package):
    """Scrapes package archive page to get previous version numbers
    within the last two years

    :param: package: string for the package name
    :return: list of archived versions within past two years
    """
    html_page = requests.get(f'https://cran.r-project.org/src/contrib/Archive/{package}/')
    soup = BeautifulSoup(html_page.text, 'html.parser')
    dates = [x.string.strip() for x in soup.select('body > table > tr > td:nth-child(3)') if len(x.string.strip()) > 0]
    version_list = []
    i = 0
    for link in BeautifulSoup(html_page.text, parse_only=SoupStrainer('a'), features="html.parser"):
        if link.has_attr('href'):
            if link['href'].startswith(package) and link['href'].endswith('.tar.gz'):
                date = dates[i]
                i += 1
                #Check if package older than 2 years
                date = parser.parse(date)
                two_years_ago = datetime.now() - timedelta(weeks=104)
                if two_years_ago > date:
                    continue
                version = link['href'].split('_')[1]
                version = version.rstrip('.tar.gz')
                version_list.append(version)
    return [(package, version) for version in version_list]


def download_tar_file(package, version, is_archive, target_path):
    #Download tar file
    path = (is_archive and f'https://cran.r-project.org/src/contrib/Archive/{package}/')or 'https://cran.r-project.org/src/contrib/'
    tar_file = f'{package}_{version}.tar.gz'
    src = f'{path}{tar_file}'
    os.path.exists(target_path) or os.mkdir(target_path)
    target = f'{target_path}/{tar_file}'
    try:
        urllib.request.urlretrieve(src, target)
    except urllib.error.HTTPError:
        try:
            path = f'https://cran.r-project.org/src/contrib/Archive/{package}/'
            src = f'{path}{tar_file}'
            urllib.request.urlretrieve(src, target)
        except urllib.error.HTTPError:
            raise ValueError(f'Could not download package archive for {package} v{version}')
    return(target)

def process_tar(tar_file):
    """does processing of the tar file, except readin the news
    """
    tar = tarfile.open(tar_file, "r:gz")
    tar_name = os.path.basename(tar_file).rstrip('.tar.gz$')
    ix = tar_name.index("_")
    pname = tar_name[:ix]
    tar_dir = os.path.dirname(tar_file)
    target_to_extract = f'{tar_dir}/{tar_name}'
    tar.extractall(target_to_extract)
    tar.close()
    package_location = f'{target_to_extract}/{pname}'
    
    data = read_description_file(package_location)
    title, description, url, bugreport, version, maintainer, date, imports, suggests = parse_description_file(data)
    functions, arguments, defaults = read_doc_files(package_location)
    res = {
        'data': data,
        'name': pname,
        'title': title,
        'description': description,
        'url': url,
        'bugreport': bugreport,
        'version': version,
        'maintainer': maintainer,
        'date': date,
        'imports': imports,
        'suggests': suggests,
        'functions': functions,
        'arguments': arguments,
        'defaults': defaults,
        'package_location': package_location
    }
    return res

def read_description_file(package):
    """Reads DESCRIPTION file

    :param: package: string for the package name
    :return: string for data read from DESCRIPTION file 
    """
    description_file = f"{package}/DESCRIPTION"
    try:
        with open(description_file, "r", encoding ='utf-8') as desc_file:
            data = desc_file.read()
    except UnicodeDecodeError:
        #Need to convert to UTF-8
        converted_file = convert_encoding(description_file)
        with open(converted_file, "r", encoding ='utf-8') as desc_file:
            data = desc_file.read()
    return data


def parse_description_file(data):
    """Parses DESCRIPTION file

    :param: data: string for DESCRIPTION file data
    :return: tuple of parsed description file metadata:
    title, description, url, bugreport, version, maintainer,
    date, import_dict, suggest_dict
    """
    unparsed_fields = deb822_from_string(data)
    parsed_fields = parse_control_fields(unparsed_fields)
    
    version = safe_parse('Version', parsed_fields)
    title = safe_parse('Title', parsed_fields)
    description = safe_parse('Description', parsed_fields)
    url = safe_parse('Url', parsed_fields)
    bugreport = safe_parse('Bugreports', parsed_fields)
    maintainer = safe_parse('Maintainer', parsed_fields)
    # Parse dates
    try:
        date = parsed_fields['Date/publication']
        # Parse datetimes
        try:
            date = parser.parse(date)
        except ValueError:
            date = parser.parse(date, dayfirst=True)
    except KeyError:
        try:
            #Some packages use 'Date'
            date = parsed_fields['Date']
            # Parse datetimes
            try:
                date = parser.parse(date)
            except ValueError:
                date = parser.parse(date, dayfirst=True)
        except KeyError:
            date = None
    # Parse imports
    try:
        imports = parsed_fields['Imports']
        #Imports does not get parsed properly,
        #so do this here
        imports = parse_depends(imports)
        import_dict = create_relationship_dict(imports)
    except KeyError:
       import_dict = {}
    # Parse suggests
    try:
        suggests = parsed_fields['Suggests']
        suggest_dict = create_relationship_dict(suggests)
    except KeyError:
        suggest_dict = {}
    return (title, description, url,
            bugreport, version, maintainer, date,
            import_dict, suggest_dict)


def create_relationship_dict(field):
    """Creates a relationship dict for imports and suggests

    :param: field: string for the field name 
    :return: relationship dict with name of package as key 
    and version number as value
    """
    relationship = field.relationships
    #Create dict of name, version pairs
    package_dict = {}
    for i in relationship:
        version = ''
        if hasattr(i, 'version'):
            version = i.version
        package_dict[i.name.strip("\n")] = version
    return package_dict


def safe_parse(key_name, parsed_fields):
    """Reads field values from DESCRIPTION file

    :param: key_name: string for the DESCRIPTION file field name
    :return: string for field value in DESCRIPTION file 
    """
    try:
        result = parsed_fields[key_name]
    except KeyError:
        result = ''
    return result



# is_archive = True
# package = "dplyr"
# version = "0.8.3"
# path = (is_archive and f'https://cran.r-project.org/src/contrib/Archive/{package}/')or 'https://cran.r-project.org/src/contrib/'
# tar_file = f'{package}_{version}.tar.gz'
# src = f'{path}{tar_file}'

# import urllib
# urllib.
