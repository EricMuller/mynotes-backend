from django.db import models
from django.db import connection
# from itertools import izip
from webmarks_django_contrib.lists import AggregateList


class QueryMixin():

    def query_to_dicts(query_string, *query_args):
        """Run a simple query and produce a generator
        that returns the results as a bunch of dictionaries
        with keys for the column values selected.
        """
        cursor = connection.cursor()
        cursor.execute(query_string, query_args)
        col_names = [desc[0] for desc in cursor.description]
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            row_dict = dict(izip(col_names, row))
            yield row_dict
        return


class ScrapingManager(models.Manager):
    def create_scraping(self, name):
        scraping = self.create(name=name)
        # todo others fields
        return scraping


class TagManager(models.Manager):

    def with_counts(self, user_cre_id):
        meta = self.model._meta
        bookmark_tag = meta.app_label + '_' + meta.model_name
        bookmark_tags = meta.app_label + '_' + 'bookmark_tags'
        query = " SELECT {0}.id, {0}.name,count(*)  FROM {0}  left join  {1} \
         on {0}.id =    {1}.tag_id  \
                  where user_cre_id  = %s  group by {0}.id, {0}.name  order by\
                   {0}.name  ".format(bookmark_tag, bookmark_tags)

        with connection.cursor() as cursor:
            cursor.execute(query, [user_cre_id])
            result_list = []
            max_count = 0
            for row in cursor.fetchall():
                p = self.model(id=row[0], name=row[1])
                p.count = row[2]
                if row[2] > max_count:
                    max_count = row[2]

                result_list.append(p)

        result = AggregateList(result_list, self.model,
                               {"max_count": max_count})
        return result
