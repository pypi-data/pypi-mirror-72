import datetime
from sqlalchemy import create_engine, or_, and_, desc
from sqlalchemy.orm import sessionmaker
from .models import Packages
from .models import Imports
from .models import Suggests
from .models import Exports
from .models import Arguments
from .models import News
from .models import Tags
from .models import TagMembers


def make_querymaker(connect_string):
    """Instantiates QueryMaker class"""
    engine = create_engine(connect_string)
    Session = sessionmaker(bind=engine)
    query_maker = QueryMaker(Session())
    return query_maker


class NotFoundError(Exception):
    pass


class QueryMaker():
    def __init__(self, session):
        self.session = session


    def get_names(self):
        """Gets unique names of all packages in database

        return: list of package names
        """ 
        names = self.session.query(Packages.name).distinct()
        names = [element for tupl in names for element in tupl]
        return names

    
    def check_name_and_version(self, package_names, versions):
        """Checks that package names and corresponding versions are in database.
        Exception is raised if a package or a respective version is not.

        :params 
        package_names: list of package name strings
        versions: list of lists with package version number strings
        """
        query = (self.session.query(Packages.name, Packages.version)
                .filter(or_(and_(Packages.name == package_names[i], Packages.version.in_(versions[i])) for i in range(len(package_names)))))
        result = query.all()
        for p_id, package in enumerate(package_names):
            for version in versions[p_id]:
                db_entry = [i for i in result if i == (package, version)]
                if len(db_entry) == 0:
                    raise NotFoundError(f"{package} v{version}")


    def get_latest_versions(self, package_names):
        """Lists all versions of a given list of packages

        :param package_names: list of package name strings
        :return: a dictionary with list of versions for each package
        """
        query = (self.session.query(Packages.name, Packages.version)
                            .filter(Packages.name.in_(package_names))
                            .order_by(Packages.date.desc()))
        result = query.all()
        version_dict = {}
        for package in package_names:
            versions = [i[1] for i in result if i[0] == package]
            if len(versions) == 0:
                raise NotFoundError(package)
            version_dict.update({package: versions})
        return version_dict


    def query_imports(self, package_names, versions):
        """Get dictionary of package imports
            
        :params
        package_names: list of package name strings
        versions: list of lists with package version number strings
        
        :return: a dictionary of imports with their version numbers
        """
        self.check_name_and_version(package_names, versions)
        query = (self.session.query(Imports.name, Imports.version, Packages.name, Packages.version)
                .join(Packages, Packages.id == Imports.package_id)
                .filter(or_(and_(Packages.name == package_names[i], Packages.version.in_(versions[i])) for i in range(len(package_names)))))
        result = query.all()
        import_dict = {}
        for p_id, package in enumerate(package_names):
            package_dict = {}
            for version in versions[p_id]:
                imports = dict([i[:2] for i in result if i[2:] == (package, version)])
                package_dict.update({version: imports})
            import_dict.update({package: package_dict})
        return import_dict


    def query_suggests(self, package_names, versions):
        """Get dictionary of package suggests

        :params
        package_names: list of package name strings
        versions: list of lists with package version number strings

        :return: a dictionary of suggests with their version numbers
        """
        self.check_name_and_version(package_names, versions)
        query = (self.session.query(Suggests.name, Suggests.version, Packages.name, Packages.version)
                .join(Packages, Packages.id == Suggests.package_id)
                .filter(or_(and_(Packages.name == package_names[i], Packages.version.in_(versions[i])) for i in range(len(package_names)))))
        result = query.all()
        suggest_dict = {}
        for p_id, package in enumerate(package_names):
            package_dict = {}
            for version in versions[p_id]:
                suggests = dict([i[:2] for i in result if i[2:] == (package, version)])
                package_dict.update({version: suggests})
            suggest_dict.update({package: package_dict})
        return suggest_dict


    def query_exports(self, package_names, versions):
        """Get dictionary of package exports

        :params
        package_names: list of package name strings
        versions: list of lists with package version number strings

        :return: a dictionary of exports, including type (function, class, etc)
        """
        self.check_name_and_version(package_names, versions)
        query = (self.session.query(Exports.name, Exports.type, Packages.name, Packages.version)
                .join(Packages, Packages.id == Exports.package_id)
                .filter(or_(and_(Packages.name == package_names[i], Packages.version.in_(versions[i])) for i in range(len(package_names)))))
        result = query.all()
        export_dict = {}
        for p_id, package in enumerate(package_names):
            package_dict = {}
            for version in versions[p_id]:
                exports = dict([i[:2] for i in result if i[2:] == (package, version)])
                package_dict.update({version: exports})
            export_dict.update({package: package_dict})
        return export_dict
 

    def query_arguments(self, package_names, versions):
        """Get dictionary of package functions and their arguments

        :params
        package_names: list of package name strings
        versions: list of lists with package version number strings

        :return: a dictionary of functions and their arguments for each version
        """
        self.check_name_and_version(package_names, versions)
        query = (self.session.query(Packages.name, Packages.version, Arguments.function, Arguments.name, Arguments.default)
            .join(Arguments, Arguments.package_id == Packages.id)
            .filter(or_(and_(Packages.name == package_names[i], Packages.version.in_(versions[i])) for i in range(len(package_names)))))
        result = query.all()
        argument_dict = {}
        for p_id, package in enumerate(package_names):
            package_dict = {}
            for version in versions[p_id]:
                functions = set([row[2] for row in result if row[:2] == (package, version)])
                version_arguments = {}
                for function in functions:
                    arguments = dict([row[3:] for row in result if row[:3] == (package, version, function)])
                    version_arguments.update({function: arguments})
                package_dict.update({version: version_arguments})
            argument_dict.update({package: package_dict})
        return argument_dict


    def get_news_by_tag(self, since_date = None, tags = None):
        """Get list of news items filtered by date and tags

        :params
        since_date: datetime object with start-date for news search
        tags: list of tag names to filter the search

        :return: a list of dictionaries, one for each news category
        """
        since_date = since_date or datetime.datetime.utcnow() - datetime.timedelta(days = 30)
        package_filters = tags and [Tags.name.in_(tags)] or []
        package_filters.append(Packages.date >= since_date)
        pkgs = self.session.query(
            Packages.id, Packages.name, Packages.version, Packages.date
            ).join(TagMembers, Packages.id == TagMembers.package_id
            ).join(Tags, Tags.id == TagMembers.tag_id
            ).filter(and_(*package_filters)).subquery()
        return [{
                "name": res[0],
                "version": res[1],
                "date": res[2],
                "type": "updated package",
                "news_category": res[4],
                "news_text": res[3]
            } for res in self.session.query(pkgs.c.name, pkgs.c.version, pkgs.c.date, News.text, News.category).join(News, pkgs.c.id == News.package_id).order_by(desc(pkgs.c.date))]

    
    def get_news_by_package(self, since_date = None, packages = None):
        """Get list of news items filtered by date and packages

        :params
        since_date: datetime object with start-date for news search
        packages: list of names of CRAN packages to filter the search

        :return: a list of dictionaries, one for each news category
        """
        since_date = since_date or datetime.datetime.utcnow() - datetime.timedelta(days = 30)
        package_filters = packages and [Packages.name.in_(packages)] or []
        package_filters.append(Packages.date >= since_date)
        pkgs = self.session.query(
            Packages.id, Packages.name, Packages.version, Packages.date
            ).filter(and_(*package_filters)).subquery()
        return [{
            "name": res[0],
            "version": res[1],
            "date": res[2],
            "type": "updated package",
            "news_category": res[4],
            "news_text": res[3]
         } for res in self.session.query(pkgs.c.name, pkgs.c.version, pkgs.c.date, News.text, News.category).join(News, pkgs.c.id == News.package_id).order_by(desc(pkgs.c.date))]


    def get_news_by_version(self, package_names, versions):
        """Get list of news items filtered by package version

        :params
        package_names: list of names of CRAN packages
        versions: list of versions, one for each package

        :return: a list of news dictionaries, ordered by the input
        """
        package_filter = or_(and_(Packages.name == package_names[i], Packages.version == versions[i]) for i in range(len(package_names)))
        result = self.session.query(
            Packages.name, Packages.version, News.text, News.category
            ).filter(package_filter
            ).join(News, Packages.id == News.package_id).all()
        news_list = []
        for p_id, package in enumerate(package_names):
            #Get news for each version (empty list if no news)
            news = [{'category': i[3], 'text': i[2]} for i in result if i[0] == package and i[1] == versions[p_id]]
            news_dict = {
                    'name': package,
                    'version': versions[p_id],
                    'news': news
                }
            news_list.append(news_dict)
        return news_list


    def get_news(self, since_date = None, tag=None, package_names=[], versions=[]):
        filters = []
        if len(package_names) > 0:
            #Get news for these packages only (and versions if supplied)
            if len(versions) > 0:
                filters.append(or_(and_(Packages.name == package_names[i], Packages.version.in_(versions[i])) for i in range(len(package_names))))
            else:
                filters.append(Packages.name.in_(package_names))
        if len(versions) == 0:
            #Create datetime filter using specified period
            #If package version specified, don't use time filter
            news_start = since_date or datetime.datetime.utcnow() - datetime.timedelta(days = 30)
            filters.append(Packages.date > news_start)
            if tag:
                #Get list of tag member-packages
                tag_members = self.query_tag_members([tag])[tag]
                filters.append(Packages.name.in_(tag_members))
        #Execute db search using the defined filters
        package_results = self.session.query(Packages.id, Packages.name, Packages.version, Packages.date, Packages.title, Packages.description).filter(and_(*filters)).all()
        news_results = self.session.query(News.package_id, News.category, News.text).all()
        all_versions = self.session.query(Packages.name, Packages.version, Packages.date).all()
        #Get list of dates, starting most recent
        dates = list(set([i[3].date() for i in package_results]))
        dates.sort(reverse = True)
        new = {}
        updated = {}
        try:
            for date in dates:
                # get packages released on a specific date
                packages = [i for i in package_results if i[3].date() == date]
                new_packages = []
                package_news = []
                for package_data in packages:
                    version_dates = [i[2].date() for i in all_versions if i[0] == package_data[1]]
                    # are we just trying to find new packages here?
                    version_dates.sort()
                    if package_data[3].date() == version_dates[0] and len(package_names) == 0:
                        #State title / description if a new package
                        #If packages specified, output updates only
                        package_dict = {
                            "date": date,
                            "name": package_data[1],
                            "version": package_data[2],
                            "title": package_data[4],
                            "description": package_data[5],
                            "type": "new"
                            }
                        # package_dict.update({})
                        # package_dict.update({})
                        # package_dict.update({})
                        new_packages.append(package_dict)
                    else:
                        #Package update
                        news = [i[1:] for i in news_results if i[0] == package_data[0]]
                        #Build a single string using news categories and text
                        news_string = ""
                        for i in range(len(news)):
                            if news[i][0] == "":
                                extra = news[i][1] + " "
                            else:
                                extra = news[i][0] + ": " + news[i][1] + " "
                            news_string += extra
                        if len(versions) > 0:
                            #If versions specified, label news by version
                            version_dict = {f"{package_data[1]} {package_data[2]}": news_string}
                            updated.update(version_dict)
                        else:
                            version_dict = {
                                "name": package_data[1],
                                "version": package_data[2],
                                "type": "updated package",
                                "news": news_string
                            }
                            # version_dict.update({"new_version": })
                            # version_dict.update({"news": news_string})
                            package_news.append(version_dict)
                if len(new_packages) != 0:
                    new.update({date.strftime('%Y/%m/%d'): new_packages})
                if len(package_news) != 0 and len(versions) == 0:
                    #Do not label with date if specific versions queried
                    updated.update({date.strftime('%Y/%m/%d'): package_news})
        except Exception as e:
            print(f"date {date}, package_data {package_data}")
        return new, updated


    def get_tags(self):
        tags = self.session.query(Tags.name, Tags.topic).distinct()
        tags = [{"name": i[0], "topic": i[1]} for i in tags]
        return tags


    def query_tag_members(self, tags):
        """Lists all packages belonging to a list of tags

        :param tags: list of tags
        :return: a dictionary with list of member-packages for each tag
        """
        query = (self.session.query(Packages.name, Tags.name)
                .join(TagMembers, Packages.id == TagMembers.package_id)
                .join(Tags, Tags.id == TagMembers.tag_id)
                .filter(Tags.name.in_(tags)))
        result = query.all()
        member_dict = {}
        for tag in tags:
            members = [i[0] for i in result if i[1] == tag]
            if len(members) == 0:
                if len([i for i in result if i[1] == tag]) == 0:
                    #Tag is not in database
                    raise NotFoundError(tag)
            member_dict.update({tag: members})
        return member_dict


    def query_package_tags(self, package_names):
        """Lists all tags of a given list of packages

        :param package_names: list of package name strings
        :return: a dictionary with list of tags for each package
        """
        query = (self.session.query(Tags.name, Tags.topic, Packages.name)
                .join(TagMembers, Tags.id == TagMembers.tag_id)
                .join(Packages, Packages.id == TagMembers.package_id)
                .filter(Packages.name.in_(package_names)))
        result = query.all()
        tag_dict = {}
        for package in package_names:
            tags = [{"name": i[0], "topic": i[1]} for i in result if i[2] == package]
            if len(tags) == 0:
                if len([i for i in result if i[2] == package]) == 0:
                    #Package is not in database
                    raise NotFoundError(package)
            tag_dict.update({package: tags})
        return tag_dict


def get_diff(result_dict, package_names, version_pairs):
    """Get import or suggest diffs for specified pairs of versions
        
    :params
    result_dict: output from query_imports() or query_suggests()
    package_names: names of CRAN packages
    version_pairs: list of package version pairs

    :return: a list of dictionaries with added, removed and changed (version numbers) packages
    """
    diff_list = []
    for p_id, package in enumerate(package_names):
        # package_dict = {}
        pair = version_pairs[p_id]
        set1 = set(result_dict[package][pair[0]].items())
        set2 = set(result_dict[package][pair[1]].items())
        diff1 = set1 - set2
        diff2 = set2 - set1
        #Check for version changes
        changed = []
        added = []
        removed = []
        for i in diff1:
            was_changed = False
            for j in diff2:
                if i[0] == j[0]:
                    changed.append({'package': i[0], 'old': j[1], 'new': i[1]})
                    was_changed = True
                    break
            if not was_changed:
                added.append({'package': i[0], 'version': i[1]})
        for i in diff2:
            was_changed = False
            for j in diff1:
                if i[0] == j[0]:
                    was_changed = True
                    break
            if not was_changed:
                removed.append({'package': i[0], 'version': i[1]})
        # added = [list(elem) for elem in added]
        # removed = [list(elem) for elem in removed]
        pair_diff = {
            'name': package,
            'new': pair[0],
            'old': pair[1],
            'added': added,
            'removed': removed,
            'version changes': changed}
        # pair_key = f"{pair[0]}_{pair[1]}"
        # package_dict.update({pair_key: pair_diff})
        diff_list.append(pair_diff)
    # diff_dict.update({package: pair_diff})
    return diff_list


def get_export_diff(result_dict, package_names, version_pairs):
    """Get export diffs for specified pairs of versions
        
    :params
    result_dict: output from query_exports()
    package_names: names of CRAN packages
    version_pairs: list of package version pairs

    :return: a list of dictionaries with added and removed exports
    """
    diff_list = []
    for p_id, package in enumerate(package_names):
        # package_dict = {}
        pair = version_pairs[p_id]
        set1 = set(result_dict[package][pair[0]].items())
        set2 = set(result_dict[package][pair[1]].items())
        diff1 = set1 - set2
        diff2 = set2 - set1
        #Check which exports have been added / removed
        added = []
        removed = []
        for i in diff1:
            added.append({'name': i[0], 'type': i[1]})
        for i in diff2:
            removed.append({'name': i[0], 'type': i[1]})
        # added = [list(elem) for elem in added]
        # removed = [list(elem) for elem in removed]
        pair_diff = {
            'name': package,
            'new': pair[0],
            'old': pair[1],
            'added': added,
            'removed': removed
        }
        # pair_key = f"{pair[0]}_{pair[1]}"
        # package_dict.update({pair_key: pair_diff})
        diff_list.append(pair_diff)
    # diff_dict.update({package: pair_diff})
    return diff_list


def get_argument_diff(result_dict, package_names, version_pairs):
    """Get argument diffs for specified pairs of versions

    :params
    result_dict: output from query_arguments()
    package_names: names of CRAN packages
    version_pairs: list of package version pairs

    :return: a list of dictionaries with added and removed functions and argument changes for retained functions
    """
    diff_list = []
    for p_id, package in enumerate(package_names):
        # package_dict = {}
        pair = version_pairs[p_id]
        #Get functions of the two versions using dict keys
        new = result_dict[package][pair[0]].keys()
        old = result_dict[package][pair[1]].keys()
        #Check which functions have been added / removed
        added = new - old
        removed = old - new
        #Check argument difference for functions retained in latest version
        retained = new - added
        changed = []
        added_args = []
        removed_args = []
        for f in retained:
            set1 = set(result_dict[package][pair[0]][f].items())
            set2 = set(result_dict[package][pair[1]][f].items())
            diff1 = set1 - set2
            diff2 = set2 - set1
            #Check for added / removed arguments and changed default values
            for i in diff1:
                was_changed = False
                for j in diff2:
                    if i[0] == j[0]:
                        changed.append({'function': f, 'argument': i[0], 
                                        'old': j[1], 'new': i[1]})
                        was_changed = True
                        break
                if not was_changed:
                    added_args.append({'function': f, 'argument': i[0]})
            for i in diff2:
                was_changed = False
                for j in diff1:
                    if i[0] == j[0]:
                        was_changed = True
                        break
                if not was_changed:
                    removed_args.append({'function': f, 'argument': i[0]})
        pair_diff = {
            'name': package,
            'new': pair[0],
            'old': pair[1],
            'added functions': list(added),
            'removed functions': list(removed),
            'new arguments': added_args,
            'removed arguments': removed_args,
            'argument value changes': changed
        }
        # package_dict.update({pair_key: pair_diff})
        diff_list.append(pair_diff)
    # diff_dict.update({package: pair_diff})
    return diff_list
