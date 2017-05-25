from django.db import models
from django.db import connection

from webmarks.drf_utils.managers import AggregateList


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


class MediaManager(models.Manager):
    pass


class TagManager(models.Manager):

    def with_counts(self, user_cre_id):

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT bookmarks_tag.id, bookmarks_tag.name,count(*)
                FROM bookmarks_tag
                left join  bookmarks_bookmark_tags
                        on bookmarks_tag.id = bookmarks_bookmark_tags.tag_id
                where user_cre_id  = %s
                group by bookmarks_tag.id,bookmarks_tag.name
                order by bookmarks_tag.name
                """, [user_cre_id])
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

    # def with_counts_test(self):

    #     return self.raw("""
    #             SELECT mynotes_tag.id, mynotes_tag.name, count(*) count , max()
    #             FROM mynotes_note_tags , mynotes_tag
    #             where mynotes_tag.id = mynotes_note_tags.tag_id
    #             group by mynotes_tag.id, mynotes_tag.name
    #             order by mynotes_tag.name
    #             """)
